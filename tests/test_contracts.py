import json
from pathlib import Path

import mehwar
from mehwar import Controller, EvaluationResult

REQUIRED_RESULT_FIELDS = {
    "controller",
    "controller_metadata",
    "scenario_id",
    "scenario_family",
    "success",
    "steps",
    "path_cost",
    "failure_type",
    "trajectory",
    "reference_result",
    "diagnostics",
    "configuration",
    "provenance",
}


class SampleController(Controller[str, str]):
    def reset(self, **kwargs: object) -> None:
        self.reset_options = kwargs

    def act(
        self,
        observation: str,
        legal_actions: list[str] | None = None,
    ) -> str:
        if legal_actions:
            return legal_actions[0]
        return f"sample-action-for-{observation}"

    def metadata(self) -> dict[str, str]:
        return {"kind": "synthetic-test-controller"}


def test_package_imports() -> None:
    assert mehwar.Controller is Controller
    assert mehwar.EvaluationResult is EvaluationResult


def test_minimal_controller_uses_contract() -> None:
    controller = SampleController()

    controller.reset(seed=7)

    assert controller.reset_options == {"seed": 7}
    assert controller.act("observation", ["legal-action"]) == "legal-action"
    assert controller.metadata() == {"kind": "synthetic-test-controller"}


def test_evaluation_result_instantiates_and_serializes() -> None:
    result = EvaluationResult(
        controller="synthetic-test-controller",
        controller_metadata={"kind": "engineering-test"},
        scenario_id="synthetic-test-scenario",
        scenario_family="engineering-test",
        success=True,
        steps=1,
        path_cost=1.0,
        failure_type=None,
        trajectory=[{"state_id": "start"}, {"state_id": "goal"}],
        reference_result=None,
        diagnostics={"invalid_actions": 0},
        configuration={"purpose": "unit-test"},
        provenance={"checkpoint_identity": None, "research_evidence": False},
    )

    payload = result.to_dict()

    assert json.loads(json.dumps(payload)) == payload
    assert set(payload) == REQUIRED_RESULT_FIELDS


def test_sample_fixture_is_json_serializable_and_complete() -> None:
    fixture_path = (
        Path(__file__).resolve().parents[1]
        / "fixtures"
        / "sample_evaluation_result.json"
    )
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))

    assert json.loads(json.dumps(fixture)) == fixture
    assert set(fixture) == REQUIRED_RESULT_FIELDS
    assert fixture["provenance"]["data_classification"] == (
        "synthetic-engineering-sample"
    )
    assert fixture["provenance"]["research_evidence"] is False
