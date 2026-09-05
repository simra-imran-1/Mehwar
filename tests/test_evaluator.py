import json

from mehwar import Controller, EvaluationResult
from mehwar.evaluator import ExecutionRecord, evaluate


class SyntheticEngineeringController(Controller[str, str]):
    def __init__(self) -> None:
        self.reset_calls: list[dict[str, object]] = []
        self.act_calls: list[tuple[str, list[str] | None]] = []

    def reset(self, **kwargs: object) -> None:
        self.reset_calls.append(kwargs)

    def act(
        self,
        observation: str,
        legal_actions: list[str] | None = None,
    ) -> str:
        self.act_calls.append((observation, legal_actions))
        return legal_actions[0] if legal_actions else "synthetic-action"

    def metadata(self) -> dict[str, str]:
        return {"kind": "synthetic-engineering-controller"}


def test_evaluate_orchestrates_one_synthetic_run() -> None:
    controller = SyntheticEngineeringController()
    runner_calls: list[Controller[str, str]] = []

    def synthetic_scenario_runner(
        runner_controller: Controller[str, str],
    ) -> ExecutionRecord:
        runner_calls.append(runner_controller)
        action = runner_controller.act("synthetic-observation", ["advance"])
        return ExecutionRecord(
            success=True,
            steps=2,
            path_cost=1.5,
            failure_type=None,
            trajectory=["synthetic-start", {"action": action}, "synthetic-goal"],
            diagnostics={"invalid_actions": 0},
        )

    result = evaluate(
        controller_id="explicit-controller-id",
        controller=controller,
        scenario_id="synthetic-scenario-001",
        scenario_family="synthetic-engineering-test",
        scenario_runner=synthetic_scenario_runner,
        reference_result={"status": "synthetic-reference-complete"},
        configuration={"purpose": "unit-test"},
        provenance={
            "data_classification": "synthetic-engineering-test",
            "research_evidence": False,
        },
        reset_kwargs={"seed": 7},
    )

    assert controller.reset_calls == [{"seed": 7}]
    assert runner_calls == [controller]
    assert controller.act_calls == [("synthetic-observation", ["advance"])]
    assert isinstance(result, EvaluationResult)
    assert result.controller == "explicit-controller-id"
    assert result.controller_metadata == {"kind": "synthetic-engineering-controller"}
    assert result.scenario_id == "synthetic-scenario-001"
    assert result.scenario_family == "synthetic-engineering-test"
    assert result.success is True
    assert result.steps == 2
    assert result.path_cost == 1.5
    assert result.failure_type is None
    assert result.trajectory == [
        "synthetic-start",
        {"action": "advance"},
        "synthetic-goal",
    ]
    assert result.diagnostics == {"invalid_actions": 0}
    assert result.reference_result == {"status": "synthetic-reference-complete"}
    assert result.configuration == {"purpose": "unit-test"}
    assert result.provenance == {
        "data_classification": "synthetic-engineering-test",
        "research_evidence": False,
    }
    assert json.loads(json.dumps(result.to_dict())) == result.to_dict()


def test_evaluate_keeps_unsupplied_optional_metadata_empty() -> None:
    controller = SyntheticEngineeringController()

    def synthetic_scenario_runner(
        runner_controller: Controller[str, str],
    ) -> ExecutionRecord:
        return ExecutionRecord(
            success=False,
            steps=0,
            path_cost=0.0,
            failure_type=None,
            trajectory=[],
            diagnostics={},
        )

    result = evaluate(
        controller_id="synthetic-controller",
        controller=controller,
        scenario_id="synthetic-empty-optionals",
        scenario_family="synthetic-engineering-test",
        scenario_runner=synthetic_scenario_runner,
    )

    assert controller.reset_calls == [{}]
    assert result.reference_result is None
    assert result.configuration == {}
    assert result.provenance == {}


def test_evaluate_passes_failure_type_through_without_classification() -> None:
    controller = SyntheticEngineeringController()

    def synthetic_scenario_runner(
        runner_controller: Controller[str, str],
    ) -> ExecutionRecord:
        return ExecutionRecord(
            success=False,
            steps=4,
            path_cost=4.0,
            failure_type="runner-defined-nonprogress",
            trajectory=["A", "B", "A", "B"],
            diagnostics={"source": "synthetic-runner"},
        )

    result = evaluate(
        controller_id="synthetic-controller",
        controller=controller,
        scenario_id="synthetic-pass-through",
        scenario_family="synthetic-engineering-test",
        scenario_runner=synthetic_scenario_runner,
    )

    assert result.failure_type == "runner-defined-nonprogress"
