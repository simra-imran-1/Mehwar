"""Deterministic A* using exactly the C4 runner's movement contract."""

from dataclasses import dataclass
from heapq import heappop, heappush
from itertools import count
from math import sqrt

from mehwar.scenarios.c4 import (
    C4Scenario,
    Position,
    destination,
    legal_actions,
    movement_cost,
)


@dataclass(frozen=True)
class AStarResult:
    found: bool
    steps: int
    cost: float | None
    trajectory: tuple[Position, ...]


def _heuristic(position: Position, goal: Position) -> float:
    dr, dc = abs(position[0] - goal[0]), abs(position[1] - goal[1])
    return max(dr, dc) + (sqrt(2) - 1) * min(dr, dc)


def astar(scenario: C4Scenario) -> AStarResult:
    """Use octile distance and stable insertion-order tie breaking."""
    if not scenario.is_free(scenario.start) or not scenario.is_free(scenario.goal):
        return AStarResult(False, 0, None, ())
    sequence = count()
    frontier = [(_heuristic(scenario.start, scenario.goal),
                 next(sequence), 0.0, scenario.start)]
    costs = {scenario.start: 0.0}
    parent: dict[Position, Position] = {}
    while frontier:
        _, _, cost, position = heappop(frontier)
        if cost > costs[position]:
            continue
        if position == scenario.goal:
            path = [position]
            while position in parent:
                position = parent[position]
                path.append(position)
            return AStarResult(True, len(path) - 1, cost, tuple(reversed(path)))
        for action in legal_actions(scenario, position):
            target = destination(position, action)
            candidate = cost + movement_cost(action)
            if candidate < costs.get(target, float("inf")):
                costs[target] = candidate
                parent[target] = position
                heappush(frontier, (
                    candidate + _heuristic(target, scenario.goal),
                    next(sequence), candidate, target,
                ))
    return AStarResult(False, 0, None, ())
