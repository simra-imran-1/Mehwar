import hashlib
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def test_t1_contract_source_remains_frozen():
    source = (REPO / "src/mehwar/contracts.py").read_text(encoding="utf-8")
    assert hashlib.sha256(source.encode()).hexdigest() == (
        "68d4c5d4aba93541bbda725cd0498f5712cd0648f16aecbdf626ef2201383149"
    )


def test_checkpoint_is_ignored_and_no_model_is_tracked():
    checkpoint = "artifacts/seed33/model_stage_301056_lifetime_452608.zip"
    ignored = subprocess.run(
        ["git", "check-ignore", checkpoint], cwd=REPO,
        capture_output=True, text=True, check=True,
    )
    assert ignored.stdout.strip() == checkpoint
    tracked = subprocess.run(
        ["git", "ls-files", "--", "*.zip", "*.pth", "*.pt"], cwd=REPO,
        capture_output=True, text=True, check=True,
    )
    assert not tracked.stdout.strip()


def test_lightweight_integration_imports_without_site_packages():
    source = str(REPO / "src")
    script = f"""
import sys
sys.path.insert(0, {source!r})
import mehwar.contracts
import mehwar.evaluator
import mehwar.failure
import mehwar.references.astar
import mehwar.scenarios.c4_runner
import mehwar.reporting
import mehwar.dashboard.data
import mehwar.dashboard.local_demo
assert not {{'numpy', 'torch', 'streamlit'}} & sys.modules.keys()
"""
    result = subprocess.run(
        [sys.executable, "-S", "-c", script], cwd=REPO,
        capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr
