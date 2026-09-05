"""Selected demos from the frozen C4 development-validation manifest.

These structured-static cases are not a fresh holdout. Coordinates are (row, col).
"""

from dataclasses import dataclass
from math import ceil, sqrt

Position = tuple[int, int]

# Frozen discrete policy action IDs: N, S, W, E, NW, NE, SW, SE.
ACTION_DELTAS: tuple[Position, ...] = (
    (-1, 0), (1, 0), (0, -1), (0, 1),
    (-1, -1), (-1, 1), (1, -1), (1, 1),
)
MOVEMENT_CONTRACT = "8-connected_destination-only_corner-cutting_static_v1"


@dataclass(frozen=True)
class C4Scenario:
    scenario_id: str
    grid_size: int
    family: str
    difficulty: str
    blocked: frozenset[Position]
    start: Position
    goal: Position
    optimal_cost: float
    optimal_steps: int

    @property
    def episode_budget(self) -> int:
        return max(10, ceil(self.optimal_steps * 2.0))

    def is_free(self, position: Position) -> bool:
        return (
            all(0 <= index < self.grid_size for index in position)
            and position not in self.blocked
        )


def destination(position: Position, action: int) -> Position:
    dr, dc = ACTION_DELTAS[action]
    return position[0] + dr, position[1] + dc


def movement_cost(action: int) -> float:
    dr, dc = ACTION_DELTAS[action]
    return sqrt(2) if dr and dc else 1.0


def legal_actions(scenario: C4Scenario, position: Position) -> list[int]:
    """Only the destination cell matters; adjacent corner obstacles are allowed."""
    return [
        action for action in range(8)
        if scenario.is_free(destination(position, action))
    ]


C4_0000 = C4Scenario(
    scenario_id="C4-0000", grid_size=15, family="u_trap", difficulty="moderate",
    blocked=frozenset({
        (3, 3), (3, 4), (3, 5), (3, 6),
        (4, 6), (5, 6), (6, 6), (7, 6), (8, 6),
        (9, 3), (9, 4), (9, 5), (9, 6),
    }),
    start=(7, 5), goal=(11, 14),
    optimal_cost=16.65685424949238, optimal_steps=15,
)
C4_0001 = C4Scenario(
    scenario_id="C4-0001", grid_size=15, family="u_trap", difficulty="moderate",
    blocked=frozenset({
        (4, 8), (4, 9), (4, 10), (4, 11),
        (5, 8), (6, 8), (7, 8), (8, 8), (9, 8),
        (10, 8), (10, 9), (10, 10), (10, 11),
    }),
    start=(8, 9), goal=(13, 1),
    optimal_cost=16.071067811865476, optimal_steps=14,
)
C4_SCENARIOS = {case.scenario_id: case for case in (C4_0000, C4_0001)}
