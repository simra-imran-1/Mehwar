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
    assert metrics["Controller"] == "synthetic-sample-controller"
    assert metrics["Scenario"] == "synthetic-sample-scenario-001"
    assert metrics["Scenario family"] == "engineering-sample"
    assert metrics["Mission outcome"] == "Mission completed"
    assert metrics["Steps"] == "1"
    assert metrics["Path cost"] == "1"
    assert metrics["Failure type"] == "Not supplied"

    subheaders = {subheader.value for subheader in dashboard.subheader}
    assert {
        "Run summary",
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
