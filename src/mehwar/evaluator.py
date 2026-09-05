"""Framework-independent orchestration for one controller evaluation run."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import TypeVar

from mehwar.contracts import Controller, EvaluationResult, JsonValue

ObservationT = TypeVar("ObservationT")
ActionT = TypeVar("ActionT")


@dataclass(frozen=True)
class ExecutionRecord:
    """Raw scenario-runner output needed to build an evaluation result."""

    success: bool
    steps: int
    path_cost: float
    failure_type: str | None
    trajectory: list[JsonValue]
    diagnostics: dict[str, JsonValue]


def evaluate(
    *,
    controller_id: str,
    controller: Controller[ObservationT, ActionT],
    scenario_id: str,
    scenario_family: str,
    scenario_runner: Callable[[Controller[ObservationT, ActionT]], ExecutionRecord],
    reference_result: Mapping[str, JsonValue] | None = None,
    configuration: Mapping[str, JsonValue] | None = None,
    provenance: Mapping[str, JsonValue] | None = None,
    reset_kwargs: Mapping[str, object] | None = None,
) -> EvaluationResult:
    """Reset a controller, run one scenario, and return its structured result."""

    controller.reset(**(dict(reset_kwargs) if reset_kwargs is not None else {}))
    execution = scenario_runner(controller)
    controller_metadata = controller.metadata()

    return EvaluationResult(
        controller=controller_id,
        controller_metadata=dict(controller_metadata),
        scenario_id=scenario_id,
        scenario_family=scenario_family,
        success=execution.success,
        steps=execution.steps,
        path_cost=execution.path_cost,
        failure_type=execution.failure_type,
        trajectory=list(execution.trajectory),
        reference_result=(
            dict(reference_result) if reference_result is not None else None
        ),
        diagnostics=dict(execution.diagnostics),
        configuration=(dict(configuration) if configuration is not None else {}),
        provenance=dict(provenance) if provenance is not None else {},
    )
