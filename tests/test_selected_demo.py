import hashlib
import json
import subprocess
import sys
from dataclasses import replace
from pathlib import Path
from unittest.mock import Mock

import pytest
from test_real_seed33 import EXPECTED_C4_0001

from mehwar import evaluator, selected_demo
from mehwar.controllers.ppo import CHECKPOINT_SHA256
from mehwar.dashboard.data import load_evaluation_result
from mehwar.evaluator import ExecutionRecord
from mehwar.reporting import DEFAULT_LIMITATIONS
from mehwar.scenarios import c4_runner


@pytest.fixture
def engineering_execution(monkeypatch, tmp_path):
    """Test exports with injected records, without extra checkpoint inference."""
    checkpoint = tmp_path / "engineering-placeholder.zip"
    checkpoint.write_bytes(b"unit test; adapter mocked, not real model evidence")
    controller = Mock()
    controller.metadata.return_value = {"checkpoint_sha256": CHECKPOINT_SHA256}
    adapter = Mock(return_value=controller)
    monkeypatch.setattr(selected_demo, "MaskablePPOCheckpointAdapter", adapter)
    monkeypatch.setenv("MEHWAR_SEED33_CHECKPOINT", str(checkpoint))
    monkeypatch.setattr(selected_demo, "_repository_git_commit", lambda: None)
    monkeypatch.setattr(selected_demo, "version", lambda name: "0.1.0")

    def execution(active_controller, scenario):
        success = scenario.scenario_id == "C4-0000"
        return ExecutionRecord(
            success=success,
            steps=16 if success else 28,
            path_cost=20.0,
            failure_type="success" if success else "two_cell_loop",
            trajectory=(
                [list(scenario.start)] * 17
                if success
                else [list(cell) for cell in EXPECTED_C4_0001]
            ),
            diagnostics={"invalid_actions": 0, "collision": False},
        )

    monkeypatch.setattr(c4_runner, "_execute_c4", execution)
    common = Mock(wraps=evaluator.evaluate)
    monkeypatch.setattr(evaluator, "evaluate", common)
    return checkpoint, adapter, controller, common


def test_all_exports_exactly_two_deterministic_results(engineering_execution, tmp_path):
    _, adapter, controller, common = engineering_execution
    directories = [tmp_path / "first", tmp_path / "second"]
    for directory in directories:
        assert selected_demo.main(["--all", "--output-dir", str(directory)]) == 0
        assert {path.name for path in directory.iterdir()} == {
            "C4-0000.json",
            "C4-0000.txt",
            "C4-0001.json",
            "C4-0001.txt",
            "manifest.json",
        }
        for scenario_id in selected_demo.SELECTED_SCENARIO_IDS:
            payload = directory / f"{scenario_id}.json"
            result = load_evaluation_result(payload)
            assert result.scenario_id == scenario_id
            assert json.loads(payload.read_text()) == result.to_dict()
            report = (directory / f"{scenario_id}.txt").read_text()
            assert all(limitation in report for limitation in DEFAULT_LIMITATIONS)
        manifest = json.loads((directory / "manifest.json").read_text())
        assert manifest == {
            "selected_scenario_ids": ["C4-0000", "C4-0001"],
            "checkpoint_sha256": CHECKPOINT_SHA256,
            "failure_protocol": "c4_c5_recurrence_v1",
            "movement_contract": (
                "8-connected destination-cell-only, corner cutting allowed, "
                "orthogonal cost 1, diagonal cost sqrt(2)"
            ),
            "research_source_repository": "muzzammilsajid1/uav-dynamic-routing",
            "research_source_commit": "95b8ec3834e79464e18dd9cdcef3c0378ba343cc",
            "scenario_manifest": "evaluation/manifests/rl_v3_phase_c4_validation.json",
            "scenario_manifest_git_blob": "d687a62a72dc266eb9092fa36221cba7fe309153",
            "scenario_classification": "development_validation",
            "scenario_selection": "selected current MVP demo",
            "fresh_holdout": False,
            "mehwar_package_version": "0.1.0",
            "output_filenames": [
                "C4-0000.json",
                "C4-0000.txt",
                "C4-0001.json",
                "C4-0001.txt",
                "manifest.json",
            ],
        }
    assert adapter.call_count == 2  # one model per invocation, not per scenario
    assert common.call_count == 4 and controller.reset.call_count == 4
    for path in directories[0].iterdir():
        assert path.read_bytes() == (directories[1] / path.name).read_bytes()
        assert b"%" not in path.read_bytes()  # no historical percentages


def test_single_scenario_and_explicit_checkpoint_override(
    engineering_execution,
    monkeypatch,
    tmp_path,
):
    checkpoint, adapter, _, _ = engineering_execution
    monkeypatch.setenv("MEHWAR_SEED33_CHECKPOINT", "incorrect-env-path")
    output = tmp_path / "single"
    assert (
        selected_demo.main(
            [
                "--scenario",
                "C4-0000",
                "--checkpoint",
                str(checkpoint),
                "--output-dir",
                str(output),
            ]
        )
        == 0
    )
    adapter.assert_called_once_with(checkpoint)
    assert {path.name for path in output.iterdir()} == {
        "C4-0000.json",
        "C4-0000.txt",
        "manifest.json",
    }


@pytest.mark.parametrize("configured", [None, "missing-file"])
def test_missing_checkpoint_is_a_clear_cli_error(monkeypatch, capsys, configured):
    if configured is None:
        monkeypatch.delenv("MEHWAR_SEED33_CHECKPOINT", raising=False)
    else:
        monkeypatch.setenv("MEHWAR_SEED33_CHECKPOINT", configured)
    with pytest.raises(SystemExit) as error:
        selected_demo.main(["--all"])
    assert error.value.code == 2
    message = capsys.readouterr().err
    assert (
        "MEHWAR_SEED33_CHECKPOINT" if configured is None else "does not exist"
    ) in message


def test_configured_wrong_checkpoint_fails_before_artifact_writes(
    monkeypatch,
    tmp_path,
    capsys,
):
    checkpoint = tmp_path / "incorrect.zip"
    checkpoint.write_bytes(b"incorrect model")
    monkeypatch.setenv("MEHWAR_SEED33_CHECKPOINT", str(checkpoint))
    output = tmp_path / "outputs"
    with pytest.raises(SystemExit) as error:
        selected_demo.main(["--all", "--output-dir", str(output)])
    assert error.value.code == 2 and "SHA256" in capsys.readouterr().err
    assert not output.exists()


def test_trace_digest_matches_the_existing_regression_oracle():
    trace = json.dumps(EXPECTED_C4_0001, separators=(",", ":")).encode()
    assert hashlib.sha256(trace).hexdigest() == selected_demo._C4_0001_TRACE_SHA256


@pytest.mark.parametrize("field", ["steps", "reference_result", "trajectory"])
def test_evidence_drift_is_rejected(engineering_execution, field):
    result = selected_demo.reproduce_selected_demo(("C4-0001",))[0]
    change = {"steps": 27, "reference_result": {"cost": 99}, "trajectory": [[8, 9]]}
    with pytest.raises(ValueError, match="mismatch"):
        selected_demo.verify_expected_evidence(
            replace(result, **{field: change[field]})
        )


def test_output_cannot_overwrite_checkpoint(engineering_execution, tmp_path):
    # Even a renamed checkpoint must not be overwritten by an output filename.
    checkpoint = tmp_path / "C4-0000.json"
    checkpoint.write_bytes(b"unit-test checkpoint placeholder")
    with pytest.raises(ValueError, match="overwrite the checkpoint"):
        selected_demo.reproduce_selected_demo(
            ("C4-0000",),
            checkpoint=checkpoint,
            output_dir=tmp_path,
        )
    assert checkpoint.read_bytes() == b"unit-test checkpoint placeholder"


def test_unresolvable_git_identity_is_omitted(monkeypatch):
    def unavailable(*args, **kwargs):
        raise OSError("git unavailable")

    monkeypatch.setattr(selected_demo.subprocess, "run", unavailable)
    assert selected_demo._repository_git_commit() is None


def test_cli_help_loads_without_optional_dependencies():
    root = Path(__file__).resolve().parents[1]
    script = (
        f"import sys; sys.path.insert(0, {str(root / 'src')!r}); "
        "from mehwar.selected_demo import main; main(['--help'])"
    )
    result = subprocess.run(
        [sys.executable, "-S", "-c", script],
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert result.returncode == 0 and "--all" in result.stdout


@pytest.mark.parametrize(
    "args", [[], ["--all", "--scenario", "C4-0000"], ["--scenario", "other"]]
)
def test_cli_rejects_ambiguous_or_unselected_scenarios(args):
    with pytest.raises(SystemExit) as error:
        selected_demo.main(args)
    assert error.value.code == 2
