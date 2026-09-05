"""Framework-independent contracts shared across MEHWAR components."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from typing import Generic, TypeAlias, TypeVar

JsonScalar: TypeAlias = str | int | float | bool | None
JsonValue: TypeAlias = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]

ObservationT = TypeVar("ObservationT")
ActionT = TypeVar("ActionT")


class Controller(ABC, Generic[ObservationT, ActionT]):
    """Minimal interface implemented by controllers evaluated by MEHWAR."""

    @abstractmethod
    def reset(self, **kwargs: object) -> None:
        """Reset controller state before an evaluation run."""

    @abstractmethod
    def act(
        self,
        observation: ObservationT,
        legal_actions: Sequence[ActionT] | None = None,
    ) -> ActionT:
        """Select an action for an observation and optional legal-action set."""

    @abstractmethod
    def metadata(self) -> Mapping[str, JsonValue]:
        """Return JSON-compatible controller identity and configuration metadata."""


@dataclass(frozen=True)
class EvaluationResult:
    """JSON-oriented output shared by future evaluator and presentation layers."""

    controller: str
    controller_metadata: dict[str, JsonValue]
    scenario_id: str
    scenario_family: str
    success: bool
    steps: int
    path_cost: float
    failure_type: str | None
    trajectory: list[JsonValue]
    reference_result: dict[str, JsonValue] | None
    diagnostics: dict[str, JsonValue]
    configuration: dict[str, JsonValue]
    provenance: dict[str, JsonValue]

    def to_dict(self) -> dict[str, JsonValue]:
        """Return a standard-library JSON-serializable representation."""

        return asdict(self)
