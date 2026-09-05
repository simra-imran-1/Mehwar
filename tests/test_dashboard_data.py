import json
from pathlib import Path

import pytest

from mehwar import EvaluationResult
from mehwar.dashboard.data import (
    REFERENCE_UNAVAILABLE_MESSAGE,
    build_run_summary,
    default_fixture_path,
    extract_coordinate_trajectory,
    is_synthetic_or_non_research,
    load_evaluation_result,
    ordered_trajectory_rows,
)


def make_result(**overrides: object) -> EvaluationResult:
    values: dict[str, object] = {
        "controller": "synthetic-test-controller",
        "controller_metadata": {},
        "scenario_id": "synthetic-test-scenario",
        "scenario_family": "engineering-test",
        "success": False,
        "steps": 4,
        "path_cost": 4.0,
        "failure_type": "runner-supplied-nonprogress",
        "trajectory": ["A", "B", "A", "B"],
        "reference_result": None,
        "diagnostics": {},
        "configuration": {},
        "provenance": {},
    }
    values.update(overrides)
    return EvaluationResult(**values)  # type: ignore[arg-type]


def test_fixture_json_loads_successfully() -> None:
    result = load_evaluation_result(default_fixture_path())

    assert isinstance(result, EvaluationResult)
    assert result.controller == "synthetic-sample-controller"


def test_required_display_fields_are_extracted_correctly() -> None:
    result = load_evaluation_result(default_fixture_path())

    summary = build_run_summary(result)

    assert summary.controller == "synthetic-sample-controller"
    assert summary.scenario_id == "synthetic-sample-scenario-001"
    assert summary.scenario_family == "engineering-sample"
    assert summary.mission_outcome == "Mission completed"
    assert summary.steps == 1
    assert summary.path_cost == 1.0
    assert summary.failure_type is None


def test_synthetic_classification_is_detected_from_provenance() -> None:
    result = load_evaluation_result(default_fixture_path())

    assert is_synthetic_or_non_research(result.provenance) is True
    assert is_synthetic_or_non_research({"research_evidence": True}) is False
    assert is_synthetic_or_non_research({}) is False


def test_absent_reference_is_unavailable_not_fabricated() -> None:
    result = make_result(reference_result=None)

    assert result.reference_result is None
    assert REFERENCE_UNAVAILABLE_MESSAGE == (
        "Deterministic reference result not available for this run."
    )


def test_absent_provenance_remains_absent() -> None:
    result = make_result(provenance={})

    assert result.provenance == {}
    assert is_synthetic_or_non_research(result.provenance) is False


def test_generic_non_coordinate_trajectory_uses_ordered_representation() -> None:
    trajectory = [
        {"state_id": "start"},
        {"event": "advance"},
        "goal",
    ]

    assert extract_coordinate_trajectory(trajectory) is None
    assert ordered_trajectory_rows(trajectory) == [
        {"step": 0, "recorded state / event": '{"state_id": "start"}'},
        {"step": 1, "recorded state / event": '{"event": "advance"}'},
        {"step": 2, "recorded state / event": '"goal"'},
    ]


def test_coordinate_recognition_is_conservative() -> None:
    points = extract_coordinate_trajectory(
        [{"x": 0, "y": 1, "label": "start"}, {"x": 2, "y": 3}]
    )

    assert points is not None
    assert [(point.step, point.x, point.y) for point in points] == [
        (0, 0.0, 1.0),
        (1, 2.0, 3.0),
    ]
    assert extract_coordinate_trajectory([[0, 1], [2, 3]]) is not None
    assert extract_coordinate_trajectory([{"x": 0, "y": 1}, [2, 3]]) is None
    assert (
        extract_coordinate_trajectory([{"x": True, "y": 1}, {"x": 2, "y": 3}]) is None
    )
    assert extract_coordinate_trajectory([{"x": 0, "y": 1}]) is None


def test_run_summary_passes_through_failure_type_without_classification() -> None:
    result = make_result(
        success=False,
        failure_type="runner-supplied-custom-value",
        trajectory=["A", "B", "A", "B"],
    )

    summary = build_run_summary(result)

    assert summary.mission_outcome == "Mission not completed"
    assert summary.failure_type == "runner-supplied-custom-value"


def test_loader_rejects_missing_contract_fields(tmp_path: Path) -> None:
    payload = json.loads(default_fixture_path().read_text(encoding="utf-8"))
    del payload["provenance"]
    fixture_path = tmp_path / "missing-field.json"
    fixture_path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="Missing EvaluationResult fields: provenance"):
        load_evaluation_result(fixture_path)
