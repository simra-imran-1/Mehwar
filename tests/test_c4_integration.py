from dataclasses import replace
from unittest.mock import Mock

from mehwar import Controller, evaluator
from mehwar.dashboard.data import (
    default_fixture_path,
    is_current_selected_demo,
    is_synthetic_or_non_research,
    load_evaluation_result,
)
from mehwar.evaluator import ExecutionRecord
from mehwar.reporting import result_to_json
from mehwar.scenarios import c4_runner
from mehwar.scenarios.c4 import C4_0001


class CountingController(Controller):
    def __init__(self):
        self.reset_calls = 0
        self.actions = 0

    def reset(self, **kwargs):
        self.reset_calls += 1
        self.actions = 0

    def act(self, observation, legal_actions=None):
        assert self.reset_calls == 1
        self.actions += 1
        return 1 if self.actions % 2 else 0

    def metadata(self):
        return {"controller_family": "integration test controller"}


def test_c4_uses_common_evaluator_and_raw_execution_record(monkeypatch):
    controller = CountingController()
    common_evaluate = Mock(wraps=evaluator.evaluate)
    raw_runner = Mock(wraps=c4_runner._execute_c4)
    monkeypatch.setattr(evaluator, "evaluate", common_evaluate)
    monkeypatch.setattr(c4_runner, "_execute_c4", raw_runner)
    result = c4_runner.run_c4(controller, C4_0001)
    assert common_evaluate.call_count == 1
    assert raw_runner.call_count == 1
    assert common_evaluate.call_args.kwargs["controller"] is controller
    assert controller.reset_calls == 1 and controller.actions == 28
    assert result.failure_type == "two_cell_loop"
    assert result.reference_result["planner"] == "A*"
    assert result.reference_result["steps"] == 14
    assert load_evaluation_result(result_to_json(result).encode()) == result


def test_raw_execution_does_not_reset_controller():
    controller = CountingController()
    # The raw function is internal; caller must satisfy its pre-reset contract.
    controller.reset()
    record = c4_runner._execute_c4(controller, C4_0001)
    assert isinstance(record, ExecutionRecord)
    assert controller.reset_calls == 1 and record.steps == 28
    assert record.diagnostics["invalid_actions"] == 0


def test_evaluator_return_is_the_public_result(monkeypatch):
    sentinel = object()
    common_evaluate = Mock(return_value=sentinel)
    monkeypatch.setattr(evaluator, "evaluate", common_evaluate)
    assert c4_runner.run_c4(CountingController(), C4_0001) is sentinel
    common_evaluate.assert_called_once()


def test_selected_provenance_and_synthetic_distinction():
    result = c4_runner.run_c4(CountingController(), C4_0001)
    provenance = result.provenance
    assert is_current_selected_demo(provenance)
    assert not is_synthetic_or_non_research(provenance)
    assert provenance["research_source_repository"] == (
        "muzzammilsajid1/uav-dynamic-routing"
    )
    assert provenance["research_source_commit"] == (
        "95b8ec3834e79464e18dd9cdcef3c0378ba343cc"
    )
    assert provenance["scenario_manifest"] == (
        "evaluation/manifests/rl_v3_phase_c4_validation.json"
    )
    assert provenance["scenario_manifest_git_blob"] == (
        "d687a62a72dc266eb9092fa36221cba7fe309153"
    )
    assert provenance["scenario_classification"] == "development_validation"
    assert provenance["failure_protocol"] == "c4_c5_recurrence_v1"
    assert provenance["movement_contract"] == (
        "8-connected destination-cell-only, corner cutting allowed, "
        "orthogonal cost 1, diagonal cost sqrt(2)"
    )
    assert not {"timestamp", "run_id", "mehwar_commit"} & provenance.keys()
    fixture = load_evaluation_result(default_fixture_path())
    assert is_synthetic_or_non_research(fixture.provenance)
    assert not is_current_selected_demo(fixture.provenance)
    assert not is_current_selected_demo({**provenance, "research_evidence": False})


def test_custom_scenario_does_not_inherit_research_identity():
    custom = replace(C4_0001, scenario_id="custom-test")
    result = c4_runner.run_c4(CountingController(), custom)
    assert not is_current_selected_demo(result.provenance)
    assert "research_source_commit" not in result.provenance
    assert "scenario_manifest_git_blob" not in result.provenance
