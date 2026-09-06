from dataclasses import replace
from math import sqrt

import pytest

from mehwar.contracts import Controller
from mehwar.scenarios.c4 import C4_0000, C4_0001
from mehwar.scenarios.c4_runner import build_observation, run_c4

np = pytest.importorskip("numpy", reason="Observation tests require the ppo extra")


class ScriptedController(Controller):
    def __init__(self, actions):
        self.actions = actions
        self.reset_count = 0
        self.observations = []

    def reset(self, **kwargs):
        self.reset_count += 1
        self.index = 0
        self.observations = []

    def act(self, observation, legal_actions=None):
        self.observations.append(observation)
        action = self.actions[self.index % len(self.actions)]
        self.index += 1
        return action

    def metadata(self):
        return {"controller_family": "synthetic scripted test"}


def test_observation_channels_bins_and_scalars():
    observation = build_observation(C4_0001, (8, 9))
    local, global_map, scalars = (
        observation[name] for name in ("local_map", "global_map", "scalars")
    )
    assert local.shape == (8, 11, 11)
    assert global_map.shape == (8, 32, 32)
    assert scalars.shape == (4,)
    for array in observation.values():
        assert array.dtype == np.float32
    for maps in (local, global_map):
        assert not maps[[1, 2, 5, 7]].any()
    assert local[3, 5, 5] == 1 and local[3].sum() == 1
    assert local[4].sum() == 0  # goal outside local view
    assert local[0, 1, 4] == 1  # obstacle (4, 8)
    assert local[6, 1, 4] == 0
    assert global_map[3, 17, 19] == 1  # floor(8*32/15), floor(9*32/15)
    assert global_map[4, 27, 2] == 1
    assert global_map[0].sum() == 13
    assert global_map[6].sum() == 225 - 13
    assert global_map[0, 8, 17] == 1
    np.testing.assert_allclose(scalars, [5/14, -8/14, .15, -1])
    assert build_observation(C4_0001, (8, 9), 6)["scalars"][3] == 6


def test_local_bounds_goal_and_global_last_cell():
    observation = build_observation(C4_0001, (14, 0))
    local = observation["local_map"]
    assert (local[0, 6:, :] == 1).all()
    assert (local[0, :, :5] == 1).all()
    assert not local[6, 6:, :].any()
    assert not local[6, :, :5].any()
    assert local[4, 4, 6] == 1
    assert observation["global_map"][3, 29, 0] == 1


@pytest.mark.parametrize("action", [-1, 8, 0.0, True, None, 2])
def test_invalid_action_is_collision_separate_diagnostic(action):
    # West (2) is blocked from C4-0001's start.
    controller = ScriptedController([action])
    result = run_c4(controller, C4_0001)
    assert not result.success and result.failure_type == "collision"
    assert result.steps == 0 and result.path_cost == 0
    assert result.trajectory == [[8, 9]]
    assert result.diagnostics == {
        "invalid_actions": 1, "collision": True,
        "attempted_actions": 1, "truncated": False,
    }


def test_appending_illegal_action_cannot_change_evaluator_legality():
    class AppendController(ScriptedController):
        def act(self, observation, legal_actions=None):
            assert isinstance(legal_actions, list)
            assert 2 not in legal_actions
            legal_actions.append(2)
            return 2

    result = run_c4(AppendController([]), C4_0001)
    assert result.success is False
    assert result.failure_type == "collision"
    assert result.steps == 0 and result.path_cost == 0
    assert result.trajectory == [[8, 9]]
    assert result.diagnostics["invalid_actions"] == 1
    assert result.diagnostics["collision"] is True


def test_removing_legal_action_cannot_change_evaluator_legality():
    class RemoveController(ScriptedController):
        def act(self, observation, legal_actions=None):
            assert isinstance(legal_actions, list)
            assert 3 in legal_actions
            legal_actions.remove(3)
            return 3

    scenario = replace(C4_0000, blocked=frozenset(), start=(0, 0),
                       goal=(0, 1), optimal_steps=1, optimal_cost=1.0)
    result = run_c4(RemoveController([]), scenario)
    assert result.success is True
    assert result.failure_type == "success"
    assert result.steps == 1 and result.path_cost == 1.0
    assert result.trajectory == [[0, 0], [0, 1]]
    assert result.diagnostics["invalid_actions"] == 0
    assert result.diagnostics["collision"] is False


def test_runner_resets_and_succeeds_on_final_budget_step():
    scenario = replace(C4_0000, blocked=frozenset(), start=(0, 0),
                       goal=(10, 10), optimal_steps=1)
    controller = ScriptedController([7])
    first = run_c4(controller, scenario)
    second = run_c4(controller, scenario)
    assert first == second
    assert controller.reset_count == 2
    assert first.success and first.failure_type == "success" and first.steps == 10
    assert first.path_cost == pytest.approx(10 * sqrt(2))
    assert first.diagnostics["truncated"] is False
    assert controller.observations[0]["scalars"][3] == -1
    assert controller.observations[1]["scalars"][3] == 7


def test_recurrence_does_not_terminate_episode_early():
    result = run_c4(ScriptedController([1, 0]), C4_0001)
    assert result.steps == 28 and len(result.trajectory) == 29
    assert result.failure_type == "two_cell_loop"
    assert result.diagnostics["invalid_actions"] == 0
    assert result.diagnostics["truncated"] is True


def test_start_at_goal_never_calls_act():
    controller = ScriptedController([])
    result = run_c4(controller, replace(C4_0000, goal=C4_0000.start))
    assert result.success and result.steps == 0 and result.path_cost == 0
    assert controller.reset_count == 1
    assert not controller.observations
