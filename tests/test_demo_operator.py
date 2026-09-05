"""Exercise the PowerShell entry points' early failures without model inference."""

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
POWERSHELL = shutil.which("pwsh") or shutil.which("powershell")
pytestmark = pytest.mark.skipif(POWERSHELL is None, reason="PowerShell unavailable")


@pytest.mark.parametrize("script", ["demo_preflight.ps1", "start_demo.ps1"])
@pytest.mark.parametrize(
    ("failure", "message"),
    [
        ("missing_variable", "Set $env:MEHWAR_SEED33_CHECKPOINT"),
        ("missing_file", "does not name an existing file"),
        ("wrong_hash", "Checkpoint SHA256 mismatch"),
        ("wrong_sha", "HEAD mismatch"),
        ("wrong_directory", "Run from this checkout's root"),
    ],
)
def test_invalid_setup_never_installs_or_launches(tmp_path, script, failure, message):
    environment = os.environ.copy()
    environment.pop("MEHWAR_SEED33_CHECKPOINT", None)
    arguments = []
    cwd = ROOT
    if failure == "missing_file":
        environment["MEHWAR_SEED33_CHECKPOINT"] = str(tmp_path / "missing.zip")
    elif failure == "wrong_hash":
        checkpoint = tmp_path / "wrong.zip"
        checkpoint.write_bytes(b"invalid test checkpoint, never scientific evidence")
        environment["MEHWAR_SEED33_CHECKPOINT"] = str(checkpoint)
    elif failure == "wrong_sha":
        arguments = ["-ExpectedSha", "0" * 40]
    elif failure == "wrong_directory":
        cwd = tmp_path
    completed = subprocess.run(
        [
            POWERSHELL,
            "-NoProfile",
            "-NonInteractive",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(ROOT / "scripts" / script),
            # Deliberately invalid: reaching Python would mask the expected error.
            "-Python",
            str(tmp_path / "must-not-run-python.exe"),
            "-InstallDependencies",
            *arguments,
        ],
        cwd=cwd,
        env=environment,
        capture_output=True,
        text=True,
        timeout=30,
    )
    output = completed.stdout + completed.stderr
    assert completed.returncode != 0, output
    assert "DEMO PREFLIGHT FAILED" in output and message in output
    assert "PASS:" not in output and "Starting dashboard" not in output


def test_failed_preflight_prevents_streamlit_even_with_caught_error(tmp_path):
    """An enclosing operator shell must receive a terminating launcher failure."""
    environment = os.environ.copy()
    environment.pop("MEHWAR_SEED33_CHECKPOINT", None)
    # Paths are arguments, not interpolated PowerShell source.
    wrapper = tmp_path / "invoke.ps1"
    wrapper.write_text(
        "param($Script, $Python)\n"
        "try { & $Script -Python $Python; exit 0 }\n"
        "catch { Write-Output $_.Exception.Message; exit 19 }\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [
            POWERSHELL,
            "-NoProfile",
            "-NonInteractive",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(wrapper),
            str(ROOT / "scripts/start_demo.ps1"),
            sys.executable,
        ],
        cwd=ROOT,
        env=environment,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 19, result.stdout + result.stderr
    assert "DEMO START FAILED" in result.stdout
    assert "Starting dashboard" not in result.stdout
