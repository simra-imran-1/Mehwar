"""Lossless contract JSON and human reports with explicit evidence limitations."""

import json

from mehwar.contracts import EvaluationResult

DEFAULT_LIMITATIONS = (
    "Controlled 2-D grid-based mission-routing abstraction.",
    "Not physical flight validation.",
    "Not deployment approval.",
    "Not safety certification.",
    "Not evidence of general learned-controller or planner superiority.",
)


def result_to_json(result: EvaluationResult) -> str:
    """Serialize the unchanged T1 contract; reject nonstandard NaN/Infinity."""
    return json.dumps(result.to_dict(), indent=2, ensure_ascii=False, allow_nan=False)


def render_human_report(result: EvaluationResult) -> str:
    """Display supplied provenance verbatim without filling unknown identities."""
    def formatted(value: object) -> str:
        return json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False)

    reference = (formatted(result.reference_result)
                 if result.reference_result is not None else "Not supplied")
    return "\n".join([
        "MEHWAR evaluation report",
        f"Controller: {result.controller}",
        f"Controller metadata: {formatted(result.controller_metadata)}",
        f"Scenario: {result.scenario_id} ({result.scenario_family})",
        f"Outcome: {'success' if result.success else 'failure'}",
        f"Failure type: {result.failure_type}",
        f"Steps: {result.steps}",
        f"Path cost: {result.path_cost}",
        f"A* reference: {reference}",
        f"Diagnostics: {formatted(result.diagnostics)}",
        f"Configuration: {formatted(result.configuration)}",
        f"Provenance: {formatted(result.provenance)}",
        "Limitations:",
        *[f"- {item}" for item in DEFAULT_LIMITATIONS],
    ])
