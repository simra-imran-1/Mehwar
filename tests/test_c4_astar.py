from dataclasses import replace
from math import sqrt

import pytest

from mehwar.references.astar import astar
from mehwar.scenarios.c4 import (
    C4_0000,
    C4_0001,
    destination,
    legal_actions,
    movement_cost,
)


@pytest.mark.parametrize(
    ("scenario", "steps", "cost", "budget"),
    [(C4_0000, 15, 16.65685424949238, 30),
     (C4_0001, 14, 16.071067811865476, 28)],
)
def test_selected_references(scenario, steps, cost, budget):
    result = astar(scenario)
    assert result.found
    assert result.steps == steps
    assert result.cost == pytest.approx(cost, abs=1e-12)
    assert result.trajectory[0] == scenario.start
    assert result.trajectory[-1] == scenario.goal
    assert result == astar(scenario)
    assert scenario.episode_budget == budget
    path_cost = 0.0
    for source, target in zip(result.trajectory, result.trajectory[1:]):
        action = next(a for a in legal_actions(scenario, source)
                      if destination(source, a) == target)
        path_cost += movement_cost(action)
    assert path_cost == result.cost


def test_destination_only_corner_cutting():
    scenario = replace(C4_0000, grid_size=2, start=(0, 0), goal=(1, 1),
                       blocked=frozenset({(0, 1), (1, 0)}))
    assert legal_actions(scenario, (0, 0)) == [7]
    result = astar(scenario)
    assert result.found and result.steps == 1
    assert result.cost == sqrt(2)


def test_unreachable_and_start_at_goal():
    closed = replace(C4_0000, grid_size=3, start=(0, 0), goal=(2, 2),
                     blocked=frozenset({(0, 1), (1, 0), (1, 1)}))
    assert not astar(closed).found
    assert astar(closed).cost is None
    same = replace(C4_0000, goal=C4_0000.start)
    result = astar(same)
    assert result.found and result.steps == 0 and result.cost == 0
