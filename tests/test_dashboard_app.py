import json
from pathlib import Path

from streamlit.testing.v1 import AppTest

from mehwar.dashboard.data import (
    REFERENCE_UNAVAILABLE_MESSAGE,
    SYNTHETIC_FIXTURE_LABEL,
)

APP_PATH = Path(__file__).resolve().parents[1] / "app.py"


def test_default_fixture_renders_required_evidence_sections() -> None:
    dashboard = AppTest.from_file(str(APP_PATH)).run(timeout=30)

    assert not dashboard.exception
    assert dashboard.title[0].value == "MEHWAR"
    assert any(
        SYNTHETIC_FIXTURE_LABEL in warning.value for warning in dashboard.warning
    )

    metrics = {metric.label: metric.value for metric in dashboard.metric}
    assert metrics["Scenario"] == "synthetic-sample-scenario-001"
    assert metrics["Mission outcome"] == "Mission completed"
    assert metrics["Steps"] == "1"
    assert metrics["Failure type"] == "Not supplied"

    subheaders = {subheader.value for subheader in dashboard.subheader}
    assert {
        "Trajectory evidence",
        "Deterministic reference result",
        "Diagnostics",
        "Configuration",
        "Provenance",
        "Evidence limitations",
    } <= subheaders
    assert any(info.value == REFERENCE_UNAVAILABLE_MESSAGE for info in dashboard.info)
    assert any(
        "Fixture data does not constitute research or product-performance evidence."
        in warning.value
        for warning in dashboard.warning
    )

    assert any(
        "Legal action selection does not by itself guarantee mission liveness."
        in item.value for item in dashboard.markdown
    )
    expanders = {item.label: item for item in dashboard.expander}
    assert {
        "Controller metadata", "Diagnostics",
        "Deterministic reference — full supplied record", "Configuration",
        "Provenance", "Evidence limitations — read before interpreting",
    } <= expanders.keys()
    assert all(not item.proto.expanded for item in expanders.values())
    metadata_text = "\n".join(
        item.value for item in expanders["Controller metadata"].markdown
    )
    assert "Controller: synthetic-sample-controller" in metadata_text
    assert "Scenario family: engineering-sample" in metadata_text
    assert "Trajectory records: 2" in metadata_text
    text = [item.value for item in dashboard.markdown]
    assert "Controller path cost" in text and "1.0" in text
    assert "Invalid actions" in text
    assert "A* reference steps" not in text
    assert "A* reference cost" not in text
    assert any(
        "dashboard does not create hashes" in item.value
        for item in expanders["Provenance"].caption
    )
    # Every supplied mapping remains inspectable after the presentation move.
    payload = json.loads(
        (APP_PATH.parent / "fixtures/sample_evaluation_result.json").read_text()
    )
    for section, field in (
        ("Controller metadata", "controller_metadata"),
        ("Diagnostics", "diagnostics"), ("Configuration", "configuration"),
        ("Provenance", "provenance"),
    ):
        assert json.loads(expanders[section].json[0].value) == payload[field]
