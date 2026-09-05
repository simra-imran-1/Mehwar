"""Framework-independent preparation of EvaluationResult dashboard data."""

from __future__ import annotations

import json
import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any

from mehwar.contracts import EvaluationResult, JsonValue

SYNTHETIC_FIXTURE_LABEL = (
    "SYNTHETIC ENGINEERING FIXTURE \u2014 UI/INTEGRATION TEST ONLY"
)
REFERENCE_UNAVAILABLE_MESSAGE = (
    "Deterministic reference result not available for this run."
)
CURRENT_DEMO_LABEL = "CURRENT MEHWAR SELECTED DEMO RUN"
SUPPLIED_CURRENT_DEMO_LABEL = "SUPPLIED CURRENT-DEMO EVIDENCE"

_RESULT_FIELD_NAMES = tuple(field.name for field in fields(EvaluationResult))
_MAPPING_FIELDS = (
    "controller_metadata",
    "diagnostics",
    "configuration",
    "provenance",
)
_SYNTHETIC_MARKERS = ("synthetic", "fixture", "sample", "non-research")


class DashboardDataError(ValueError):
    """Raised when dashboard input is not EvaluationResult-compatible JSON."""


@dataclass(frozen=True)
class RunSummary:
    """Fields shown in the dashboard's primary run summary."""

    controller: str
    scenario_id: str
    scenario_family: str
    mission_outcome: str
    steps: int
    path_cost: float
    failure_type: str | None


@dataclass(frozen=True)
class CoordinatePoint:
    """One conservatively recognized two-dimensional trajectory state."""

    step: int
    x: float
    y: float


def default_fixture_path() -> Path:
    """Return the repository's bundled dashboard fixture path."""

    return (
        Path(__file__).resolve().parents[3]
        / "fixtures"
        / ("sample_evaluation_result.json")
    )


def load_evaluation_result(source: Path | bytes | bytearray) -> EvaluationResult:
    """Load and minimally validate an EvaluationResult-compatible JSON payload."""

    try:
        if isinstance(source, Path):
            raw_payload = source.read_text(encoding="utf-8")
        else:
            raw_payload = bytes(source).decode("utf-8")
        payload = json.loads(raw_payload)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise DashboardDataError(
            f"Unable to read EvaluationResult JSON: {exc}"
        ) from exc

    if not isinstance(payload, dict):
        raise DashboardDataError("EvaluationResult JSON must be an object.")

    missing = sorted(set(_RESULT_FIELD_NAMES) - set(payload))
    extra = sorted(set(payload) - set(_RESULT_FIELD_NAMES))
    if missing:
        raise DashboardDataError(
            f"Missing EvaluationResult fields: {', '.join(missing)}"
        )
    if extra:
        raise DashboardDataError(
            f"Unexpected EvaluationResult fields: {', '.join(extra)}"
        )

    _validate_field_shapes(payload)
    return EvaluationResult(**payload)


def _validate_field_shapes(payload: dict[str, Any]) -> None:
    for field_name in ("controller", "scenario_id", "scenario_family"):
        if not isinstance(payload[field_name], str):
            raise DashboardDataError(f"{field_name} must be a string.")

    if not isinstance(payload["success"], bool):
        raise DashboardDataError("success must be a boolean.")
    if isinstance(payload["steps"], bool) or not isinstance(payload["steps"], int):
        raise DashboardDataError("steps must be an integer.")
    if isinstance(payload["path_cost"], bool) or not isinstance(
        payload["path_cost"], (int, float)
    ):
        raise DashboardDataError("path_cost must be numeric.")
    if not math.isfinite(float(payload["path_cost"])):
        raise DashboardDataError("path_cost must be finite.")
    if payload["failure_type"] is not None and not isinstance(
        payload["failure_type"], str
    ):
        raise DashboardDataError("failure_type must be a string or null.")
    if not isinstance(payload["trajectory"], list):
        raise DashboardDataError("trajectory must be a list.")
    if payload["reference_result"] is not None and not isinstance(
        payload["reference_result"], dict
    ):
        raise DashboardDataError("reference_result must be an object or null.")
    for field_name in _MAPPING_FIELDS:
        if not isinstance(payload[field_name], dict):
            raise DashboardDataError(f"{field_name} must be an object.")


def build_run_summary(result: EvaluationResult) -> RunSummary:
    """Extract display fields without deriving or changing failure semantics."""

    return RunSummary(
        controller=result.controller,
        scenario_id=result.scenario_id,
        scenario_family=result.scenario_family,
        mission_outcome=(
            "Mission completed" if result.success else "Mission not completed"
        ),
        steps=result.steps,
        path_cost=result.path_cost,
        failure_type=result.failure_type,
    )


def is_synthetic_or_non_research(provenance: Mapping[str, JsonValue]) -> bool:
    """Detect an explicit synthetic/non-research classification in provenance."""

    if provenance.get("research_evidence") is False:
        return True

    for key in ("data_classification", "evidence_classification", "source_type"):
        value = provenance.get(key)
        if isinstance(value, str):
            normalized = value.casefold()
            if any(marker in normalized for marker in _SYNTHETIC_MARKERS):
                return True
    return False


def is_current_selected_demo(provenance: Mapping[str, JsonValue]) -> bool:
    """Recognize the explicit current-demo label, never override synthetic markers."""
    return (
        not is_synthetic_or_non_research(provenance)
        and provenance.get("data_classification") == "current-mehwar-selected-demo-run"
        and provenance.get("scenario_selection") == "selected current MVP demo"
        and provenance.get("scenario_classification") == "development_validation"
        and provenance.get("fresh_holdout") is False
    )


def extract_coordinate_trajectory(
    trajectory: Sequence[JsonValue],
) -> tuple[CoordinatePoint, ...] | None:
    """Recognize only uniform, finite, direct two-dimensional coordinate states."""

    if len(trajectory) < 2:
        return None

    uses_mapping = isinstance(trajectory[0], Mapping)
    points: list[CoordinatePoint] = []
    for step, state in enumerate(trajectory):
        coordinates = _coordinates_from_state(state, uses_mapping=uses_mapping)
        if coordinates is None:
            return None
        x, y = coordinates
        points.append(CoordinatePoint(step=step, x=x, y=y))
    return tuple(points)


def _coordinates_from_state(
    state: JsonValue,
    *,
    uses_mapping: bool,
) -> tuple[float, float] | None:
    values: tuple[object, object]
    if uses_mapping:
        if not isinstance(state, Mapping) or "x" not in state or "y" not in state:
            return None
        values = (state["x"], state["y"])
    else:
        if (
            not isinstance(state, Sequence)
            or isinstance(state, (str, bytes, bytearray))
            or len(state) != 2
        ):
            return None
        values = (state[0], state[1])

    if any(isinstance(value, bool) for value in values):
        return None
    if not all(isinstance(value, (int, float)) for value in values):
        return None

    x, y = (float(value) for value in values)
    if not math.isfinite(x) or not math.isfinite(y):
        return None
    return x, y


def ordered_trajectory_rows(
    trajectory: Sequence[JsonValue],
) -> list[dict[str, int | str]]:
    """Return every generic trajectory event in its recorded order."""

    return [
        {
            "step": step,
            "recorded state / event": json.dumps(
                state,
                ensure_ascii=False,
                sort_keys=True,
            ),
        }
        for step, state in enumerate(trajectory)
    ]
