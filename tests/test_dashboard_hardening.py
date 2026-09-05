from dataclasses import replace
from pathlib import Path
from unittest.mock import Mock

from streamlit.testing.v1 import AppTest

from mehwar.contracts import EvaluationResult
from mehwar.dashboard import app as dashboard_app
from mehwar.dashboard.data import (
    CURRENT_DEMO_LABEL,
    SUPPLIED_CURRENT_DEMO_LABEL,
    is_current_selected_demo,
)
from mehwar.dashboard.local_demo import run_local_c4_demo
from mehwar.reporting import result_to_json

APP_PATH = Path(__file__).resolve().parents[1] / "app.py"


def current_demo_result(*, success: bool = True) -> EvaluationResult:
    return EvaluationResult(
        controller="hardening-test-controller",
        controller_metadata={},
        scenario_id="C4-0000",
        scenario_family="u_trap",
        success=success,
        steps=1,
        path_cost=1.0,
        failure_type="success" if success else "collision",
        trajectory=[[7, 5], [8, 5]],
        reference_result={"found": True, "trajectory": [[7, 5], [8, 5]]},
        diagnostics={"invalid_actions": 0},
        configuration={
            "grid_size": 15,
            "blocked": [[3, 3]],
            "start": [7, 5],
            "goal": [11, 14],
        },
        provenance={
            "data_classification": "current-mehwar-selected-demo-run",
            "scenario_selection": "selected current MVP demo",
            "scenario_classification": "development_validation",
            "fresh_holdout": False,
        },
    )


def test_current_demo_recognition_requires_development_validation():
    provenance = current_demo_result().provenance

    assert is_current_selected_demo(provenance)
    assert not is_current_selected_demo(
        {**provenance, "scenario_classification": "final_test"}
    )
    assert not is_current_selected_demo(
        {
            key: value
            for key, value in provenance.items()
            if key != "scenario_classification"
        }
    )


def test_local_run_uses_current_banner_and_single_run_wording(monkeypatch):
    runner = Mock(return_value=current_demo_result())
    monkeypatch.setenv("MEHWAR_SEED33_CHECKPOINT", "configured-checkpoint.zip")
    monkeypatch.setattr(dashboard_app, "run_local_c4_demo", runner)

    app = AppTest.from_file(str(APP_PATH)).run()
    app.radio[0].set_value(dashboard_app.LOCAL_INPUT).run()
    app.button[0].click().run()

    assert not app.exception and not app.error
    assert any(CURRENT_DEMO_LABEL in item.value for item in app.info)
    assert not any(SUPPLIED_CURRENT_DEMO_LABEL in item.value for item in app.info)
    assert any(
        item.value.strip("*") == "NO FAILURE OBSERVED IN SELECTED DEMO RUN"
        for item in app.markdown
    )
    assert not any(
        item.value.strip("*") == "NO FAILURE OBSERVED IN SELECTED DEMO SET"
        for item in app.markdown
    )


def test_single_non_liveness_failure_uses_run_not_set_wording(monkeypatch):
    runner = Mock(return_value=current_demo_result(success=False))
    monkeypatch.setenv("MEHWAR_SEED33_CHECKPOINT", "configured-checkpoint.zip")
    monkeypatch.setattr(dashboard_app, "run_local_c4_demo", runner)

    app = AppTest.from_file(str(APP_PATH)).run()
    app.radio[0].set_value(dashboard_app.LOCAL_INPUT).run()
    app.button[0].click().run()

    assert any(
        item.value.strip("*") == "FAILURE OBSERVED IN SELECTED DEMO RUN"
        for item in app.markdown
    )


def test_uploaded_current_demo_is_supplied_not_locally_verified(monkeypatch):
    upload = Mock()
    upload.name = "supplied-current-demo.json"
    upload.getvalue.return_value = result_to_json(current_demo_result()).encode()
    monkeypatch.setattr(
        dashboard_app.st.sidebar, "file_uploader", Mock(return_value=upload)
    )

    app = AppTest.from_file(str(APP_PATH)).run()
    app.radio[0].set_value(dashboard_app.UPLOAD_INPUT).run()

    assert not app.exception and not app.error
    assert any(SUPPLIED_CURRENT_DEMO_LABEL in item.value for item in app.info)
    assert not any(CURRENT_DEMO_LABEL in item.value for item in app.info)
    assert any(
        "did not independently execute or verify" in item.value for item in app.info
    )


def test_uploaded_filename_cannot_spoof_local_execution_banner(monkeypatch):
    upload = Mock()
    upload.name = "Local verified seed-33 / spoofed-name.json"
    upload.getvalue.return_value = result_to_json(current_demo_result()).encode()
    monkeypatch.setattr(
        dashboard_app.st.sidebar, "file_uploader", Mock(return_value=upload)
    )

    app = AppTest.from_file(str(APP_PATH)).run()
    app.radio[0].set_value(dashboard_app.UPLOAD_INPUT).run()

    assert any(SUPPLIED_CURRENT_DEMO_LABEL in item.value for item in app.info)
    assert not any(CURRENT_DEMO_LABEL in item.value for item in app.info)


def test_final_test_upload_is_not_rendered_as_known_current_demo(monkeypatch):
    result = replace(
        current_demo_result(),
        provenance={
            **current_demo_result().provenance,
            "scenario_classification": "final_test",
        },
    )
    upload = Mock()
    upload.name = "final-test.json"
    upload.getvalue.return_value = result_to_json(result).encode()
    monkeypatch.setattr(
        dashboard_app.st.sidebar, "file_uploader", Mock(return_value=upload)
    )

    app = AppTest.from_file(str(APP_PATH)).run()
    app.radio[0].set_value(dashboard_app.UPLOAD_INPUT).run()

    assert not any(SUPPLIED_CURRENT_DEMO_LABEL in item.value for item in app.info)
    assert not any(CURRENT_DEMO_LABEL in item.value for item in app.info)
    assert any(
        "classification is taken from the supplied payload" in item.value
        for item in app.info
    )


def test_local_checkpoint_error_does_not_expose_absolute_path(monkeypatch):
    from mehwar.controllers import ppo

    private_path = r"C:\Users\Private Person\secret-checkpoint.zip"
    monkeypatch.setenv("MEHWAR_SEED33_CHECKPOINT", private_path)
    monkeypatch.setattr(
        ppo,
        "MaskablePPOCheckpointAdapter",
        Mock(side_effect=OSError(f"cannot read {private_path}")),
    )

    try:
        run_local_c4_demo("C4-0000")
    except ValueError as error:
        message = str(error)
    else:
        raise AssertionError("Expected the local execution error")

    assert private_path not in message
    assert "Private Person" not in message
    assert "local filesystem paths are not displayed" in message


def test_safe_checkpoint_validation_detail_is_retained_without_path(monkeypatch):
    from mehwar.controllers import ppo

    private_path = r"C:\Users\Private Person\secret-checkpoint.zip"
    monkeypatch.setenv("MEHWAR_SEED33_CHECKPOINT", private_path)
    monkeypatch.setattr(
        ppo,
        "MaskablePPOCheckpointAdapter",
        Mock(
            side_effect=ValueError(
                f"Checkpoint SHA256 does not match frozen seed-33 model: {private_path}"
            )
        ),
    )

    try:
        run_local_c4_demo("C4-0000")
    except ValueError as error:
        message = str(error)
    else:
        raise AssertionError("Expected the local execution error")

    assert message.endswith("Checkpoint SHA256 does not match frozen seed-33 model")
    assert private_path not in message
