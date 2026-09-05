"""Transparent summaries of already-supplied MEHWAR evaluation results."""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass

from mehwar.contracts import EvaluationResult

NO_FAILURE_OBSERVED = "NO FAILURE OBSERVED IN SELECTED DEMO SET"
LIVENESS_DEGRADATION_OBSERVED = "LIVENESS DEGRADATION OBSERVED"
FAILURE_BOUNDARY_OBSERVED = "FAILURE BOUNDARY OBSERVED"
INSUFFICIENT_EVIDENCE = "INSUFFICIENT EVIDENCE"

APPROVED_EVIDENCE_LABELS = frozenset(
    {
        NO_FAILURE_OBSERVED,
        LIVENESS_DEGRADATION_OBSERVED,
        FAILURE_BOUNDARY_OBSERVED,
        INSUFFICIENT_EVIDENCE,
    }
)
LIVENESS_FAILURE_TYPES = frozenset({"two_cell_loop", "longer_loop", "timeout_other"})


@dataclass(frozen=True)
class EvidenceProfile:
    """Raw counts for an explicitly selected development-validation set."""

    evidence_label: str
    scenarios_evaluated: int
    scenario_ids: tuple[str, ...]
    mission_completions: int
    mission_failures: int
    failure_type_counts: dict[str | None, int]
    invalid_actions_total: int | None
    invalid_actions_complete: bool
    reference_results_available: int
    reference_completions: int
    evidence_scope: str = "selected current MVP demo set"
    scenario_classification: str = "development_validation"
    fresh_holdout: bool = False


def build_evidence_profile(
    results: Sequence[EvaluationResult],
) -> EvidenceProfile:
    """Summarize supplied outcomes without reclassifying scientific failures."""

    supplied = tuple(results)
    scenarios_evaluated = len(supplied)
    mission_completions = sum(result.success for result in supplied)
    failure_type_counts = dict(Counter(result.failure_type for result in supplied))

    invalid_values = [result.diagnostics.get("invalid_actions") for result in supplied]
    invalid_actions_complete = bool(supplied) and all(
        not isinstance(value, bool) and isinstance(value, int) and value >= 0
        for value in invalid_values
    )
    invalid_actions_total = sum(invalid_values) if invalid_actions_complete else None

    reference_results = [
        result.reference_result
        for result in supplied
        if result.reference_result is not None
    ]
    reference_completions = sum(
        reference.get("found") is True for reference in reference_results
    )

    liveness_failures = sum(
        count
        for failure_type, count in failure_type_counts.items()
        if failure_type in LIVENESS_FAILURE_TYPES
    )
    if not supplied:
        evidence_label = INSUFFICIENT_EVIDENCE
    elif mission_completions == scenarios_evaluated:
        evidence_label = NO_FAILURE_OBSERVED
    elif mission_completions and liveness_failures:
        evidence_label = FAILURE_BOUNDARY_OBSERVED
    elif liveness_failures:
        evidence_label = LIVENESS_DEGRADATION_OBSERVED
    else:
        evidence_label = INSUFFICIENT_EVIDENCE

    return EvidenceProfile(
        evidence_label=evidence_label,
        scenarios_evaluated=scenarios_evaluated,
        scenario_ids=tuple(result.scenario_id for result in supplied),
        mission_completions=mission_completions,
        mission_failures=scenarios_evaluated - mission_completions,
        failure_type_counts=failure_type_counts,
        invalid_actions_total=invalid_actions_total,
        invalid_actions_complete=invalid_actions_complete,
        reference_results_available=len(reference_results),
        reference_completions=reference_completions,
    )
