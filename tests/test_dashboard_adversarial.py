import json
from unittest.mock import Mock

import pytest

from mehwar import EvaluationResult
from mehwar.dashboard.data import (
    SYNTHETIC_FIXTURE_LABEL,
    DashboardDataError,
    default_fixture_path,
    extract_coordinate_trajectory,
    is_current_selected_demo,
    is_synthetic_or_non_research,
    load_evaluation_result,
)
from mehwar.reporting import DEFAULT_LIMITATIONS
from mehwar.scenarios.c4 import C4_0001

APP_PATH = default_fixture_path().parent.parent / "app.py"
CURRENT_PROVENANCE = {
    "data_classification": "current-mehwar-selected-demo-run",
    "scenario_selection": "selected current MVP demo",
    "fresh_holdout": False,
}


@pytest.fixture
def payload():
    return json.loads(default_fixture_path().read_text(encoding="utf-8"))


@pytest.fixture
def dashboard_modules():
    pytest.importorskip("streamlit")
    from streamlit.testing.v1 import AppTest

    from mehwar.dashboard import app as dashboard_app

    return dashboard_app, AppTest


@pytest.mark.parametrize(
    ("raw", "message"),
    [
        (b'{"controller":', "Unable to read EvaluationResult JSON"),
        (b"\xff", "Unable to read EvaluationResult JSON"),
        (b"[]", "must be an object"),
        (b"null", "must be an object"),
        (b'"result"', "must be an object"),
    ],
)
def test_loader_rejects_malformed_input(raw, message):
    with pytest.raises(DashboardDataError, match=message):
        load_evaluation_result(raw)


@pytest.mark.parametrize(
    "field",
    [
        "controller", "controller_metadata", "scenario_id", "scenario_family",
        "success", "steps", "path_cost", "failure_type", "trajectory",
        "reference_result", "diagnostics", "configuration",
    ],
)
def test_loader_requires_every_contract_field(payload, field):
    # Missing provenance is already covered by the inherited loader tests.
    del payload[field]
    with pytest.raises(
        DashboardDataError, match=f"Missing EvaluationResult fields: {field}",
    ):
        load_evaluation_result(json.dumps(payload).encode())


def test_loader_rejects_schema_additions_without_silently_dropping_them(payload):
    payload.update(z_future_field=1, a_unexpected_field={"unverified": True})
    with pytest.raises(
        DashboardDataError,
        match="Unexpected EvaluationResult fields: a_unexpected_field, z_future_field",
    ):
        load_evaluation_result(json.dumps(payload).encode())


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("controller", None, "controller must be a string"),
        ("scenario_id", 7, "scenario_id must be a string"),
        ("scenario_family", [], "scenario_family must be a string"),
        ("success", 1, "success must be a boolean"),
        ("steps", True, "steps must be an integer"),
        ("steps", 1.5, "steps must be an integer"),
        ("path_cost", False, "path_cost must be numeric"),
        ("path_cost", "1.0", "path_cost must be numeric"),
        ("failure_type", 0, "failure_type must be a string or null"),
        ("trajectory", {}, "trajectory must be a list"),
        ("reference_result", [], "reference_result must be an object or null"),
        ("controller_metadata", [], "controller_metadata must be an object"),
        ("diagnostics", None, "diagnostics must be an object"),
        ("configuration", "grid", "configuration must be an object"),
        ("provenance", [], "provenance must be an object"),
    ],
)
def test_loader_rejects_wrong_contract_field_shapes(payload, field, value, message):
    payload[field] = value
    with pytest.raises(DashboardDataError, match=message):
        load_evaluation_result(json.dumps(payload).encode())


@pytest.mark.parametrize("token", ["NaN", "Infinity", "-Infinity", "1e400"])
@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("path_cost", "NONFINITE_TOKEN"),
        ("diagnostics", {"nested": [{"value": "NONFINITE_TOKEN"}]}),
        ("trajectory", [{"x": 0, "y": "NONFINITE_TOKEN"}]),
        ("reference_result", {"cost": "NONFINITE_TOKEN"}),
    ],
)
def test_loader_rejects_nonfinite_numbers_at_any_depth(payload, field, value, token):
    payload[field] = value
    encoded = json.dumps(payload).replace('"NONFINITE_TOKEN"', token).encode()
    with pytest.raises(DashboardDataError):
        load_evaluation_result(encoded)


@pytest.mark.parametrize(
    "trajectory",
    [
        [],
        [[0, 1], [2]],
        [[0, 1], [2, 3, 4]],
        [[0, 1], "23"],
        [[0, 1], None],
        [[0, 1], [2, "3"]],
        [[0, 1], [2, False]],
        [[0, 1], {"x": 2, "y": 3}],
        [{"x": 0, "y": 1}, {"x": 2}],
        [{"x": 0, "y": 1}, {"y": 3}],
        [{"x": 0, "y": 1}, {"x": None, "y": 3}],
    ],
)
def test_coordinate_recognition_rejects_malformed_or_mixed_states(trajectory):
    assert extract_coordinate_trajectory(trajectory) is None


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf")])
@pytest.mark.parametrize("axis", [0, 1])
def test_coordinate_recognition_rejects_nonfinite_values_in_each_representation(
    value, axis,
):
    point = [2, 3]
    point[axis] = value
    assert extract_coordinate_trajectory([[0, 1], point]) is None
    assert extract_coordinate_trajectory(
        [{"x": 0, "y": 1}, {"x": point[0], "y": point[1]}],
    ) is None


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("data_classification", "SYNTHETIC-engineering"),
        ("evidence_classification", "Fixture"),
        ("source_type", "NON-RESEARCH sample"),
        ("research_evidence", False),
    ],
)
def test_synthetic_markers_override_current_demo_classification(field, value):
    provenance = {**CURRENT_PROVENANCE, field: value}
    assert is_synthetic_or_non_research(provenance)
    assert not is_current_selected_demo(provenance)


@pytest.mark.parametrize("field", list(CURRENT_PROVENANCE))
def test_current_demo_requires_every_explicit_classification_marker(field):
    provenance = CURRENT_PROVENANCE.copy()
    del provenance[field]
    assert not is_current_selected_demo(provenance)


@pytest.mark.parametrize("holdout", [True, 0, "false", None])
def test_current_demo_requires_explicit_false_holdout(holdout):
    provenance = {**CURRENT_PROVENANCE, "fresh_holdout": holdout}
    assert not is_current_selected_demo(provenance)


def test_failed_real_rerun_discards_prior_result_without_synthetic_fallback(
    monkeypatch, payload, dashboard_modules,
):
    dashboard_app, app_test = dashboard_modules
    monkeypatch.setenv("MEHWAR_SEED33_CHECKPOINT", "test-checkpoint.zip")
    payload.update(provenance=CURRENT_PROVENANCE.copy(), scenario_id="C4-0000")
    run_demo = Mock(side_effect=[
        EvaluationResult(**payload), DashboardDataError("injected execution failure"),
    ])
    monkeypatch.setattr(dashboard_app, "run_local_c4_demo", run_demo)
    app = app_test.from_file(str(APP_PATH), default_timeout=30).run()
    app.radio[0].set_value(dashboard_app.LOCAL_INPUT).run()
    app.button[0].click().run()
    assert not app.exception and app.metric
    assert "local_c4_result" in app.session_state

    app.button[0].click().run()

    assert run_demo.call_count == 2
    assert not app.exception and not app.metric
    assert "local_c4_result" not in app.session_state
    assert any("injected execution failure" in item.value for item in app.error)
    assert not any(SYNTHETIC_FIXTURE_LABEL in item.value for item in app.warning)
    app.run()
    assert run_demo.call_count == 2 and not app.metric


def test_ordinary_uploaded_result_always_renders_limitations(
    monkeypatch, payload, dashboard_modules,
):
    dashboard_app, app_test = dashboard_modules
    payload["provenance"] = {"research_evidence": True, "source": "caller supplied"}
    upload = Mock(name="upload")
    upload.name = "ordinary-result.json"
    upload.getvalue.return_value = json.dumps(payload).encode()
    monkeypatch.setattr(
        dashboard_app.st.sidebar, "file_uploader", Mock(return_value=upload),
    )
    app = app_test.from_file(str(APP_PATH), default_timeout=30).run()
    app.radio[0].set_value(dashboard_app.UPLOAD_INPUT).run()
    assert not app.exception and app.metric
    assert not any(SYNTHETIC_FIXTURE_LABEL in item.value for item in app.warning)
    for limitation in DEFAULT_LIMITATIONS:
        assert any(limitation in item.value for item in app.warning)


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="T9 integration dependency (Simra): C4 row/col is rendered as x/y",
)
def test_c4_trajectory_plot_uses_columns_horizontally_and_rows_vertically(
    monkeypatch, payload, dashboard_modules,
):
    dashboard_app, _ = dashboard_modules
    # C4 cells are explicitly (row, col); only record the presentation regression.
    # Simra owns the feature fix, including the grid's vertical-axis convention.
    row, col = C4_0001.start
    payload.update(
        scenario_id=C4_0001.scenario_id,
        trajectory=[[row, col], [row + 1, col]],
        configuration={"grid_size": C4_0001.grid_size},
        provenance=CURRENT_PROVENANCE.copy(),
    )
    streamlit = Mock()
    monkeypatch.setattr(dashboard_app, "st", streamlit)

    dashboard_app._render_trajectory(EvaluationResult(**payload))

    plot_rows = streamlit.vega_lite_chart.call_args.args[0]
    assert [(point["x"], point["y"]) for point in plot_rows] == [
        (float(col), float(row)), (float(col), float(row + 1)),
    ]
