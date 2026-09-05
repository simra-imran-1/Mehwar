from pathlib import Path
from unittest.mock import Mock

from streamlit.testing.v1 import AppTest

from mehwar.contracts import EvaluationResult
from mehwar.dashboard import app as dashboard_app

APP_PATH = Path(__file__).resolve().parents[1] / "app.py"


def batch_result(
    scenario_id: str, success: bool, failure_type: str
) -> EvaluationResult:
    return EvaluationResult(
        controller="batch-test-controller",
        controller_metadata={"identity": scenario_id},
        scenario_id=scenario_id,
        scenario_family="u_trap",
        success=success,
        steps=1,
        path_cost=1.0,
        failure_type=failure_type,
        trajectory=[[0, 0], [0, 1]],
        reference_result={"planner": "A*", "found": True},
        diagnostics={"invalid_actions": 0},
        configuration={"scenario": scenario_id},
        provenance={
            "data_classification": "current-mehwar-selected-demo-run",
            "scenario_selection": "selected current MVP demo",
            "scenario_classification": "development_validation",
            "fresh_holdout": False,
        },
    )


def test_selected_batch_profile_requires_click_and_preserves_individual_results(
    monkeypatch,
):
    results = (
        batch_result("C4-0000", True, "success"),
        batch_result("C4-0001", False, "two_cell_loop"),
    )
    batch_runner = Mock(return_value=results)
    monkeypatch.setenv("MEHWAR_SEED33_CHECKPOINT", "configured-checkpoint.zip")
    monkeypatch.setattr(dashboard_app, "run_selected_c4_batch", batch_runner)

    app = AppTest.from_file(str(APP_PATH)).run()
    app.radio[0].set_value(dashboard_app.LOCAL_INPUT).run()
    assert batch_runner.call_count == 0
    app.button[1].click().run()

    assert not app.exception and not app.error
    assert batch_runner.call_count == 1
    assert any("FAILURE BOUNDARY OBSERVED" in item.value for item in app.markdown)
    metrics = {item.label: item.value for item in app.metric}
    assert metrics["Scenarios evaluated"] == "2"
    assert metrics["Mission completions"] == "1"
    assert metrics["Mission failures"] == "1"
    assert metrics["Reference completions"] == "2"
    all_text = "\n".join(
        item.value
        for element_type in (app.markdown, app.caption)
        for item in element_type
    )
    assert "C4-0000, C4-0001" in all_text
    assert "two_cell_loop=1" in all_text
    assert "longer_loop=0" in all_text
    assert "timeout_other=0" in all_text
    assert "collision=0" in all_text
    assert "Invalid actions: 0" in all_text
    assert "not a fresh holdout or general performance estimate" in all_text
    assert not any(
        item.value.strip("*# ") == "FAILURE OBSERVED IN SELECTED DEMO SET"
        for item in app.markdown
    )
    assert "%" not in all_text
    assert "safety score" not in all_text.casefold()
    assert {item.label for item in app.expander} >= {
        "Individual EvaluationResult — C4-0000",
        "Individual EvaluationResult — C4-0001",
    }

    app.run()
    assert batch_runner.call_count == 1
    app.selectbox[0].set_value("C4-0001").run()
    assert batch_runner.call_count == 1
    assert any(metric.value == "C4-0001" for metric in app.metric)
