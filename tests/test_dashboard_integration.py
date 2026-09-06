import json
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest
from streamlit.testing.v1 import AppTest

from mehwar import evaluator
from mehwar.dashboard import app as dashboard_app
from mehwar.dashboard.data import (
    CURRENT_DEMO_LABEL,
    SYNTHETIC_FIXTURE_LABEL,
    DashboardDataError,
    is_current_selected_demo,
    is_synthetic_or_non_research,
    load_evaluation_result,
)
from mehwar.dashboard.local_demo import run_local_c4_demo
from mehwar.reporting import DEFAULT_LIMITATIONS, result_to_json

APP_PATH = Path(__file__).resolve().parents[1] / "app.py"


def test_missing_checkpoint_has_error_and_no_fixture_fallback(monkeypatch):
    monkeypatch.delenv("MEHWAR_SEED33_CHECKPOINT", raising=False)
    app = AppTest.from_file(str(APP_PATH)).run()
    app.radio[0].set_value(dashboard_app.LOCAL_INPUT).run()
    assert not app.exception
    assert any("MEHWAR_SEED33_CHECKPOINT" in error.value for error in app.error)
    assert not app.metric
    assert not any(SYNTHETIC_FIXTURE_LABEL in item.value for item in app.warning)
    with pytest.raises(DashboardDataError, match="MEHWAR_SEED33_CHECKPOINT"):
        run_local_c4_demo("C4-0000")


def test_bad_checkpoint_run_has_error_and_no_fixture_fallback(monkeypatch, tmp_path):
    path = tmp_path / "incorrect.zip"
    path.write_bytes(b"not the verified model")
    monkeypatch.setenv("MEHWAR_SEED33_CHECKPOINT", str(path))
    app = AppTest.from_file(str(APP_PATH)).run()
    app.radio[0].set_value(dashboard_app.LOCAL_INPUT).run()
    app.button[0].click().run()
    assert not app.exception and not app.metric
    assert any("SHA256" in error.value for error in app.error)
    assert not any(SYNTHETIC_FIXTURE_LABEL in item.value for item in app.warning)


def test_upload_mode_waits_for_file_without_fixture_fallback():
    app = AppTest.from_file(str(APP_PATH)).run()
    app.radio[0].set_value(dashboard_app.UPLOAD_INPUT).run()
    assert not app.exception and not app.metric
    assert any("Upload an EvaluationResult" in info.value for info in app.info)


def test_upload_payload_uses_existing_renderer(monkeypatch):
    # AppTest does not expose a file-uploader setter; supply its normal byte API.
    upload = Mock()
    upload.name = "uploaded-result.json"
    upload.getvalue.return_value = (
        APP_PATH.parent / "fixtures/sample_evaluation_result.json"
    ).read_bytes()
    monkeypatch.setattr(
        dashboard_app.st.sidebar, "file_uploader", Mock(return_value=upload),
    )
    app = AppTest.from_file(str(APP_PATH)).run()
    app.radio[0].set_value(dashboard_app.UPLOAD_INPUT).run()
    assert not app.exception
    assert any(SYNTHETIC_FIXTURE_LABEL in item.value for item in app.warning)
    assert any("uploaded-result.json" in item.value for item in app.caption)


def test_fixture_loads_without_torch():
    script = """
import sys
sys.modules['torch'] = None
from streamlit.testing.v1 import AppTest
app = AppTest.from_file('app.py').run(timeout=30)
assert not app.exception
assert any('SYNTHETIC ENGINEERING FIXTURE' in item.value for item in app.warning)
assert 'mehwar.controllers.ppo' not in sys.modules
assert 'mehwar.controllers._frozen_policy' not in sys.modules
"""
    process = subprocess.run(
        [sys.executable, "-c", script], cwd=APP_PATH.parent,
        capture_output=True, text=True, timeout=60,
    )
    assert process.returncode == 0, process.stdout + process.stderr


@pytest.mark.real_checkpoint
@pytest.mark.parametrize(
    ("scenario", "success", "steps", "status", "counts"),
    [
        ("C4-0000", True, 16, "NO FAILURE OBSERVED IN SELECTED DEMO RUN",
         "1 selected run | 1 success | 0 observed failures"),
        ("C4-0001", False, 28, "LIVENESS DEGRADATION OBSERVED",
         "1 selected run | 0 successes | 1 observed failures | 1 two_cell_loop | "
         "0 collisions | 0 invalid actions"),
    ],
)
def test_real_local_dashboard_uses_evaluator_and_shared_renderer(
    monkeypatch, scenario, success, steps, status, counts,
):
    if not os.environ.get("MEHWAR_SEED33_CHECKPOINT"):
        pytest.skip("MEHWAR_SEED33_CHECKPOINT is unavailable")
    from mehwar.controllers.ppo import MaskablePPOCheckpointAdapter

    common_evaluate = Mock(wraps=evaluator.evaluate)
    reset_count = 0
    original_reset = MaskablePPOCheckpointAdapter.reset

    def count_reset(self, **kwargs):
        nonlocal reset_count
        reset_count += 1
        original_reset(self, **kwargs)

    monkeypatch.setattr(evaluator, "evaluate", common_evaluate)
    monkeypatch.setattr(MaskablePPOCheckpointAdapter, "reset", count_reset)
    app = AppTest.from_file(str(APP_PATH)).run(timeout=30)
    app.radio[0].set_value(dashboard_app.LOCAL_INPUT).run()
    app.selectbox[0].set_value(scenario).run()
    assert common_evaluate.call_count == 0
    app.button[0].click().run(timeout=30)
    assert not app.exception and not app.error
    assert common_evaluate.call_count == 1 and reset_count == 1
    result = app.session_state["local_c4_result"][2]
    assert result.success is success and result.steps == steps
    assert result.diagnostics["invalid_actions"] == 0
    assert result.reference_result["planner"] == "A*"
    assert is_current_selected_demo(result.provenance)
    assert not is_synthetic_or_non_research(result.provenance)
    assert load_evaluation_result(result_to_json(result).encode()) == result
    assert any(CURRENT_DEMO_LABEL in item.value for item in app.info)
    assert not any(SYNTHETIC_FIXTURE_LABEL in item.value for item in app.warning)
    assert any(status in item.value for item in app.markdown)
    assert any(counts in item.value for item in app.markdown)
    metrics = {item.label: item.value for item in app.metric}
    assert metrics["Steps"] == str(steps) and metrics["Scenario"] == scenario
    assert app.title[0].value == "MEHWAR"
    assert metrics["Mission outcome"] == (
        "Mission completed" if success else "Mission not completed"
    )
    assert metrics["Failure type"] == result.failure_type
    assert "Controller" not in metrics
    text = [item.value for item in app.markdown]
    assert (
        "**Legal action selection does not by itself guarantee mission liveness.**"
        in text
    )
    assert "Invalid actions" in text and "0" in text
    assert "Controller path cost" in text and str(result.path_cost) in text
    assert "A* reference steps" in text
    assert str(result.reference_result["steps"]) in text
    assert "A* reference cost" in text
    assert str(result.reference_result["cost"]) in text
    assert any(
        item.value ==
        "deterministic A* reliability reference under the shared grid contract"
        for item in app.caption
    )
    banner = next(item.value for item in app.info if CURRENT_DEMO_LABEL in item.value)
    assert "Selected development-validation scenario; not a fresh holdout." in banner
    assert "single run does not establish general controller performance" in banner
    expanders = {item.label: item for item in app.expander}
    assert all(not item.proto.expanded for item in expanders.values())
    assert "Evidence limitations — read before interpreting" in expanders
    assert any(result.controller in item.value
               for item in expanders["Controller metadata"].markdown)
    for section, mapping in (
        ("Controller metadata", result.controller_metadata),
        ("Diagnostics", result.diagnostics),
        ("Deterministic reference — full supplied record", result.reference_result),
        ("Configuration", result.configuration), ("Provenance", result.provenance),
    ):
        assert json.loads(expanders[section].json[0].value) == mapping
    # The chart precedes engineering details; sizing is the only spec change.
    from mehwar.dashboard.visualization import build_c4_visualization, c4_chart_spec

    chart = app.get("vega_lite_chart")[0]
    expected_spec = c4_chart_spec(build_c4_visualization(result))
    actual_spec = json.loads(chart.proto.spec)
    assert actual_spec["layer"] == expected_spec["layer"]
    assert actual_spec["encoding"] == expected_spec["encoding"]
    elements = list(app.main)
    assert elements.index(chart) < elements.index(expanders["Controller metadata"])
    assert str(os.environ["MEHWAR_SEED33_CHECKPOINT"]) not in str(app.main)
    for limitation in DEFAULT_LIMITATIONS:
        assert any(limitation in item.value for item in app.warning)
    if scenario == "C4-0001":
        assert result.failure_type == "two_cell_loop"
        # Reuse the frozen branch's literal trajectory oracle without changing it.
        from test_real_seed33 import EXPECTED_C4_0001

        assert result.trajectory == [list(cell) for cell in EXPECTED_C4_0001]
    # Ordinary Streamlit reruns must not execute the model or reset it again.
    app.run()
    assert common_evaluate.call_count == 1 and reset_count == 1
    other = "C4-0001" if scenario == "C4-0000" else "C4-0000"
    app.selectbox[0].set_value(other).run()
    assert not app.metric  # do not display the previous scenario's result
