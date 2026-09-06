import json
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import Mock

import pytest
from streamlit.testing.v1 import AppTest

from mehwar.dashboard import app as dashboard_app
from mehwar.dashboard.data import (
    REFERENCE_UNAVAILABLE_MESSAGE,
    SYNTHETIC_FIXTURE_LABEL,
)

APP_PATH = Path(__file__).resolve().parents[1] / "app.py"


class PresentationParser(HTMLParser):
    """Read visible text and semantic term/value pairs from rendered UI markup."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text = []
        self.fields = {}
        self.active = None
        self.term = ""
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in ("dt", "dd"):
            self.active, self.parts = tag, []

    def handle_data(self, data):
        self.text.append(data)
        if self.active:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag == self.active:
            if tag == "dt":
                self.term = "".join(self.parts)
            else:
                self.fields[self.term] = "".join(self.parts)
            self.active = None


def presentation(app):
    parser = PresentationParser()
    for item in app.markdown:
        parser.feed(item.value)
    return parser


def assert_no_run_content(app):
    assert not app.get("vega_lite_chart")
    assert not presentation(app).fields
    assert not any('class="mw-outcome"' in item.value for item in app.markdown)


def test_default_fixture_renders_required_evidence_sections() -> None:
    dashboard = AppTest.from_file(str(APP_PATH)).run(timeout=30)

    assert not dashboard.exception
    assert dashboard.title[0].value == "MEHWAR"
    assert any(
        SYNTHETIC_FIXTURE_LABEL in warning.value for warning in dashboard.warning
    )

    rendered = presentation(dashboard)
    assert "Scenario synthetic-sample-scenario-001" in rendered.text
    assert "Mission completed" in rendered.text
    assert rendered.fields["Steps"] == "1"
    assert rendered.fields["Failure type"] == "Not supplied"

    subheaders = {subheader.value for subheader in dashboard.subheader}
    assert {
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
    assert rendered.fields["Controller path cost"] == "1.000"
    assert rendered.fields["Invalid actions"] == "0"
    assert "Trajectory evidence" in rendered.text
    assert "A* reference steps" not in rendered.fields
    assert "A* reference cost" not in rendered.fields
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


def test_uploaded_presentation_escapes_supplied_text(monkeypatch):
    payload = json.loads(
        (APP_PATH.parent / "fixtures/sample_evaluation_result.json").read_text()
    )
    supplied = '<img src=x onerror="alert(1)"> & evidence'
    for field in ("controller", "scenario_id", "scenario_family", "failure_type"):
        payload[field] = supplied
    payload["diagnostics"]["invalid_actions"] = supplied
    payload["reference_result"] = {"planner": "A*", "steps": supplied, "cost": supplied}
    upload = Mock(name="upload")
    upload.name = "supplied-text.json"
    upload.getvalue.return_value = json.dumps(payload).encode()
    monkeypatch.setattr(
        dashboard_app.st.sidebar, "file_uploader", Mock(return_value=upload)
    )
    app = AppTest.from_file(str(APP_PATH)).run()
    app.radio[0].set_value(dashboard_app.UPLOAD_INPUT).run()
    assert not app.exception
    rendered = presentation(app)
    assert f"Scenario {supplied}" in rendered.text
    for label in (
        "Controller", "Failure type", "Invalid actions",
        "A* reference steps", "A* reference cost",
    ):
        assert rendered.fields[label] == supplied
    markup = "\n".join(
        item.value for item in app.markdown if item.proto.allow_html
    )
    assert '<img src=x' not in markup
    assert '&lt;img src=x' in markup


def test_missing_supplied_context_values_are_not_invented(monkeypatch):
    payload = json.loads(
        (APP_PATH.parent / "fixtures/sample_evaluation_result.json").read_text()
    )
    payload["reference_result"] = {"planner": "A*"}
    payload["diagnostics"] = {}
    upload = Mock(name="upload")
    upload.name = "incomplete-context.json"
    upload.getvalue.return_value = json.dumps(payload).encode()
    monkeypatch.setattr(
        dashboard_app.st.sidebar, "file_uploader", Mock(return_value=upload)
    )
    app = AppTest.from_file(str(APP_PATH)).run()
    app.radio[0].set_value(dashboard_app.UPLOAD_INPUT).run()
    assert not app.exception
    fields = presentation(app).fields
    for label in ("Invalid actions", "A* reference steps", "A* reference cost"):
        assert fields[label] == "Not supplied"
    reference = next(
        item for item in app.expander
        if item.label == "Deterministic reference — full supplied record"
    )
    assert json.loads(reference.json[0].value) == {"planner": "A*"}


@pytest.mark.parametrize(
    ("success", "failure", "invalid", "visible"),
    [(False, "two_cell_loop", 0, True),
     (True, "two_cell_loop", 0, False),
     (False, "two_cell_loop", 1, False),
     (False, "two_cell_loop", None, False),
     (False, "timeout_other", 0, False)],
)
def test_recurrence_insight_uses_only_supplied_run_fields(
    monkeypatch, success, failure, invalid, visible,
):
    from dataclasses import replace

    from mehwar.dashboard.data import load_evaluation_result

    result = load_evaluation_result(
        APP_PATH.parent / "fixtures/sample_evaluation_result.json"
    )
    result = replace(
        result, success=success, failure_type=failure,
        diagnostics={} if invalid is None else {"invalid_actions": invalid},
    )
    monkeypatch.setattr(
        dashboard_app, "_load_selected_result",
        lambda: (result, "supplied run", None, False),
    )
    app = AppTest.from_file(str(APP_PATH)).run()
    assert not app.exception
    assert any(
        item.value
        == "0 invalid actions · mission still failed through legal recurrence"
        for item in app.caption
    ) is visible
