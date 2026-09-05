from unittest.mock import Mock, call

import pytest

from mehwar import evaluator
from mehwar.contracts import Controller, EvaluationResult
from mehwar.dashboard.data import DashboardDataError
from mehwar.dashboard.local_demo import (
    SELECTED_DEMO_SCENARIO_IDS,
    run_selected_c4_batch,
)
from mehwar.scenarios.c4 import C4_0000, C4_0001


def result_for(scenario_id: str) -> EvaluationResult:
    return EvaluationResult(
        controller="test-controller",
        controller_metadata={},
        scenario_id=scenario_id,
        scenario_family="u_trap",
        success=scenario_id == "C4-0000",
        steps=1,
        path_cost=1.0,
        failure_type=("success" if scenario_id == "C4-0000" else "two_cell_loop"),
        trajectory=[],
        reference_result={"found": True},
        diagnostics={"invalid_actions": 0},
        configuration={},
        provenance={},
    )


class FirstLegalController(Controller):
    def __init__(self):
        self.reset_count = 0

    def reset(self, **kwargs):
        self.reset_count += 1

    def act(self, observation, legal_actions=None):
        return legal_actions[0]

    def metadata(self):
        return {"kind": "batch-path-test"}


def test_selected_batch_uses_run_c4_in_exact_order(monkeypatch):
    from mehwar.controllers import ppo
    from mehwar.scenarios import c4_runner

    controller = object()
    adapter = Mock(return_value=controller)
    run_c4 = Mock(side_effect=lambda _, scenario: result_for(scenario.scenario_id))
    monkeypatch.setenv("MEHWAR_SEED33_CHECKPOINT", "configured-checkpoint.zip")
    monkeypatch.setattr(ppo, "MaskablePPOCheckpointAdapter", adapter)
    monkeypatch.setattr(c4_runner, "run_c4", run_c4)

    results = run_selected_c4_batch()

    assert SELECTED_DEMO_SCENARIO_IDS == ("C4-0000", "C4-0001")
    adapter.assert_called_once_with("configured-checkpoint.zip")
    assert run_c4.call_args_list == [
        call(controller, C4_0000),
        call(controller, C4_0001),
    ]
    assert tuple(result.scenario_id for result in results) == SELECTED_DEMO_SCENARIO_IDS


def test_selected_batch_requires_configured_checkpoint(monkeypatch):
    monkeypatch.delenv("MEHWAR_SEED33_CHECKPOINT", raising=False)

    with pytest.raises(DashboardDataError, match="MEHWAR_SEED33_CHECKPOINT"):
        run_selected_c4_batch()


def test_selected_batch_reaches_common_evaluator_through_real_run_c4(monkeypatch):
    from mehwar.controllers import ppo

    controller = FirstLegalController()
    common_evaluate = Mock(wraps=evaluator.evaluate)
    monkeypatch.setenv("MEHWAR_SEED33_CHECKPOINT", "configured-checkpoint.zip")
    monkeypatch.setattr(
        ppo, "MaskablePPOCheckpointAdapter", Mock(return_value=controller)
    )
    monkeypatch.setattr(evaluator, "evaluate", common_evaluate)

    results = run_selected_c4_batch()

    assert tuple(result.scenario_id for result in results) == SELECTED_DEMO_SCENARIO_IDS
    assert common_evaluate.call_count == 2
    assert controller.reset_count == 2
