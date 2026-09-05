import copy
from dataclasses import fields

import pytest

from mehwar.contracts import EvaluationResult
from mehwar.evidence import (
    APPROVED_EVIDENCE_LABELS,
    FAILURE_BOUNDARY_OBSERVED,
    INSUFFICIENT_EVIDENCE,
    LIVENESS_DEGRADATION_OBSERVED,
    NO_FAILURE_OBSERVED,
    build_evidence_profile,
)


def make_result(
    scenario_id: str = "C4-test",
    *,
    success: bool = False,
    failure_type: str | None = "timeout_other",
    invalid_actions: object = 0,
    reference_result: dict | None = None,
) -> EvaluationResult:
    diagnostics = {}
    if invalid_actions is not _MISSING:
        diagnostics["invalid_actions"] = invalid_actions
    return EvaluationResult(
        controller="test-controller",
        controller_metadata={"nested": {"identity": "preserve"}},
        scenario_id=scenario_id,
        scenario_family="test-family",
        success=success,
        steps=4,
        path_cost=4.0,
        failure_type=failure_type,
        trajectory=[[0, 0], [0, 1], [0, 0], [0, 1]],
        reference_result=reference_result,
        diagnostics=diagnostics,
        configuration={"nested": {"configuration": [1, 2]}},
        provenance={"fresh_holdout": False, "source": {"id": "preserve"}},
    )


_MISSING = object()


def test_empty_results_are_insufficient_and_have_no_diagnostic_evidence():
    profile = build_evidence_profile(())

    assert profile.evidence_label == INSUFFICIENT_EVIDENCE
    assert profile.scenarios_evaluated == 0
    assert profile.scenario_ids == ()
    assert profile.mission_completions == profile.mission_failures == 0
    assert profile.failure_type_counts == {}
    assert profile.invalid_actions_total is None
    assert profile.invalid_actions_complete is False
    assert profile.reference_results_available == profile.reference_completions == 0


def test_all_success_results_have_approved_no_failure_label():
    results = (
        make_result("C4-a", success=True, failure_type="success"),
        make_result("C4-b", success=True, failure_type="success"),
    )

    profile = build_evidence_profile(results)

    assert profile.evidence_label == NO_FAILURE_OBSERVED
    assert profile.mission_completions == 2
    assert profile.mission_failures == 0


@pytest.mark.parametrize(
    "failure_type", ["two_cell_loop", "longer_loop", "timeout_other"]
)
def test_liveness_failure_without_success_has_degradation_label(failure_type):
    profile = build_evidence_profile((make_result(failure_type=failure_type),))

    assert profile.evidence_label == LIVENESS_DEGRADATION_OBSERVED


def test_success_and_supplied_liveness_failure_have_boundary_label():
    profile = build_evidence_profile(
        (
            make_result("C4-0000", success=True, failure_type="success"),
            make_result("C4-0001", failure_type="two_cell_loop"),
        )
    )

    assert profile.evidence_label == FAILURE_BOUNDARY_OBSERVED
    assert profile.scenario_ids == ("C4-0000", "C4-0001")


def test_collision_only_is_not_reclassified_as_liveness_degradation():
    profile = build_evidence_profile((make_result(failure_type="collision"),))

    assert profile.evidence_label == INSUFFICIENT_EVIDENCE
    assert profile.failure_type_counts == {"collision": 1}


def test_failure_types_are_counted_exactly_as_supplied():
    results = (
        make_result("a", failure_type="two_cell_loop"),
        make_result("b", failure_type="two_cell_loop"),
        make_result("c", failure_type="unknown-supplied-value"),
        make_result("d", failure_type=None),
    )

    assert build_evidence_profile(results).failure_type_counts == {
        "two_cell_loop": 2,
        "unknown-supplied-value": 1,
        None: 1,
    }


def test_valid_invalid_action_counts_are_summed_only_when_complete():
    profile = build_evidence_profile(
        (
            make_result("a", invalid_actions=0),
            make_result("b", invalid_actions=3),
        )
    )

    assert profile.invalid_actions_complete is True
    assert profile.invalid_actions_total == 3


@pytest.mark.parametrize("invalid_actions", [_MISSING, True, False, -1])
def test_missing_bool_or_negative_invalid_actions_make_total_unknown(
    invalid_actions,
):
    profile = build_evidence_profile((make_result(invalid_actions=invalid_actions),))

    assert profile.invalid_actions_complete is False
    assert profile.invalid_actions_total is None


def test_reference_availability_and_found_values_are_not_assumed():
    results = (
        make_result("absent", reference_result=None),
        make_result("found", reference_result={"found": True}),
        make_result("not-found", reference_result={"found": False}),
        make_result("unknown", reference_result={"planner": "A*"}),
        make_result("non-bool", reference_result={"found": 1}),
    )

    profile = build_evidence_profile(results)

    assert profile.reference_results_available == 4
    assert profile.reference_completions == 1


def test_profiler_does_not_mutate_evaluation_results():
    result = make_result(reference_result={"found": True, "path": [[0, 0]]})
    before = copy.deepcopy(result.to_dict())

    build_evidence_profile((result,))

    assert result.to_dict() == before


def test_profile_exposes_no_percentage_confidence_or_safety_score():
    field_names = {field.name for field in fields(build_evidence_profile(()))}

    assert not any(
        token in field_name
        for field_name in field_names
        for token in ("percent", "rate", "confidence", "safety", "score")
    )


def test_unknown_failure_string_is_counted_but_does_not_create_label():
    profile = build_evidence_profile(
        (make_result(failure_type="caller-defined-unknown"),)
    )

    assert profile.failure_type_counts == {"caller-defined-unknown": 1}
    assert profile.evidence_label == INSUFFICIENT_EVIDENCE
    assert profile.evidence_label in APPROVED_EVIDENCE_LABELS
