"""Reproduce the two selected demos using the existing integrated execution path."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import subprocess
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from mehwar.contracts import EvaluationResult, JsonValue
from mehwar.controllers.ppo import CHECKPOINT_SHA256, MaskablePPOCheckpointAdapter
from mehwar.reporting import render_human_report, result_to_json
from mehwar.scenarios.c4 import C4_SCENARIOS
from mehwar.scenarios.c4_runner import run_c4

SELECTED_SCENARIO_IDS = ("C4-0000", "C4-0001")
_EXPECTED_OUTCOMES = {
    "C4-0000": (True, 16, "success"),
    "C4-0001": (False, 28, "two_cell_loop"),
}
# SHA256 of the existing regression oracle serialized as compact JSON arrays.
# This checks an expected trace; it does not implement movement or recurrence.
_C4_0001_TRACE_SHA256 = (
    "ec7fea9558b5de358d71632065497c14170bf225e2ee9d94de42647ab9f81fc3"
)
_PROVENANCE_KEYS = (
    "failure_protocol",
    "movement_contract",
    "research_source_repository",
    "research_source_commit",
    "scenario_manifest",
    "scenario_manifest_git_blob",
    "scenario_classification",
    "scenario_selection",
    "fresh_holdout",
)


def verify_expected_evidence(result: EvaluationResult) -> None:
    """Fail on drift from the supplied selected-demo evidence, without reclassifying."""
    expected = _EXPECTED_OUTCOMES[result.scenario_id]
    observed = (result.success, result.steps, result.failure_type)
    if observed != expected or result.diagnostics.get("invalid_actions") != 0:
        raise ValueError(f"{result.scenario_id}: selected-demo outcome mismatch")
    scenario = C4_SCENARIOS[result.scenario_id]
    reference = result.reference_result or {}
    cost = reference.get("cost")
    if (
        reference.get("planner") != "A*"
        or reference.get("found") is not True
        or reference.get("steps") != scenario.optimal_steps
        or not isinstance(cost, (int, float))
        or not math.isclose(cost, scenario.optimal_cost, rel_tol=0, abs_tol=1e-12)
    ):
        raise ValueError(f"{result.scenario_id}: A* reference mismatch")
    if result.controller_metadata.get("checkpoint_sha256") != CHECKPOINT_SHA256:
        raise ValueError("Result checkpoint SHA256 mismatch")
    if result.scenario_id == "C4-0001":
        trace = json.dumps(result.trajectory, separators=(",", ":")).encode("utf-8")
        if hashlib.sha256(trace).hexdigest() != _C4_0001_TRACE_SHA256:
            raise ValueError("C4-0001: complete trajectory regression mismatch")


def _repository_git_commit() -> str | None:
    """Record HEAD only for this source repository with a clean working tree."""
    root = Path(__file__).resolve().parents[2]
    if not (root / ".git").exists():
        return None
    try:

        def git(*args: str) -> str:
            return subprocess.run(
                ["git", "-C", str(root), *args],
                check=True,
                capture_output=True,
                text=True,
                timeout=5,
            ).stdout.strip()

        if Path(git("rev-parse", "--show-toplevel")).resolve() != root:
            return None
        if git("status", "--porcelain", "--untracked-files=normal"):
            return None
        commit = git("rev-parse", "HEAD")
        if len(commit) == 40 and all(char in "0123456789abcdef" for char in commit):
            return commit
    except (OSError, subprocess.SubprocessError):
        pass
    return None


def build_manifest(results: list[EvaluationResult]) -> dict[str, JsonValue]:
    """Copy known shared provenance from evaluated results, adding no run identity."""
    first = results[0]
    manifest: dict[str, JsonValue] = {
        key: first.provenance[key] for key in _PROVENANCE_KEYS
    }
    for result in results:
        if any(result.provenance[key] != manifest[key] for key in _PROVENANCE_KEYS):
            raise ValueError("Selected results have inconsistent provenance")
    manifest.update(
        {
            "selected_scenario_ids": [result.scenario_id for result in results],
            "checkpoint_sha256": first.controller_metadata["checkpoint_sha256"],
            "output_filenames": [
                f"{result.scenario_id}.{extension}"
                for result in results
                for extension in ("json", "txt")
            ]
            + ["manifest.json"],
        }
    )
    try:
        manifest["mehwar_package_version"] = version("mehwar")
    except PackageNotFoundError:
        pass
    commit = _repository_git_commit()
    if commit is not None:
        manifest["mehwar_git_commit"] = commit
    return manifest


def reproduce_selected_demo(
    scenario_ids: tuple[str, ...],
    *,
    checkpoint: str | Path | None = None,
    output_dir: str | Path | None = None,
) -> list[EvaluationResult]:
    """Run one or both selected demos, then optionally export verified results."""
    if scenario_ids not in (("C4-0000",), ("C4-0001",), SELECTED_SCENARIO_IDS):
        raise ValueError("Choose C4-0000, C4-0001, or --all (exactly these two demos)")
    configured = (
        checkpoint
        if checkpoint is not None
        else os.environ.get(
            "MEHWAR_SEED33_CHECKPOINT",
            "",
        )
    )
    if not str(configured).strip():
        raise ValueError("Set MEHWAR_SEED33_CHECKPOINT or supply --checkpoint")
    path = Path(configured)
    if not path.is_file():
        raise ValueError(f"Checkpoint file does not exist: {path}")
    # Optional tensor imports occur inside the existing adapter, after its hash gate.
    controller = MaskablePPOCheckpointAdapter(path)
    results = []
    for scenario_id in scenario_ids:
        result = run_c4(controller, C4_SCENARIOS[scenario_id])
        verify_expected_evidence(result)
        results.append(result)
    if output_dir is not None:
        manifest = build_manifest(results)
        output = Path(output_dir)
        files = {
            f"{result.scenario_id}.{extension}": render(result) + "\n"
            for result in results
            for extension, render in (
                ("json", result_to_json),
                ("txt", render_human_report),
            )
        }
        files["manifest.json"] = (
            json.dumps(
                manifest,
                indent=2,
                ensure_ascii=False,
                allow_nan=False,
            )
            + "\n"
        )
        if any((output / name).resolve() == path.resolve() for name in files):
            raise ValueError("Output files must not overwrite the checkpoint")
        # Verify all selected runs before writing any result; use portable UTF-8/LF.
        output.mkdir(parents=True, exist_ok=True)
        for name, content in files.items():
            (output / name).write_text(content, encoding="utf-8", newline="\n")
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--scenario", choices=SELECTED_SCENARIO_IDS)
    selection.add_argument(
        "--all", action="store_true", help="Run only C4-0000 and C4-0001"
    )
    parser.add_argument("--checkpoint", help="Override MEHWAR_SEED33_CHECKPOINT")
    parser.add_argument(
        "--output-dir", type=Path, help="Write result JSON/text and manifest"
    )
    args = parser.parse_args(argv)
    ids = SELECTED_SCENARIO_IDS if args.all else (args.scenario,)
    try:
        results = reproduce_selected_demo(
            ids,
            checkpoint=args.checkpoint,
            output_dir=args.output_dir,
        )
    except ImportError:
        parser.error(
            'Install the inference extra first: python -m pip install -e ".[ppo]"'
        )
    except (OSError, ValueError, RuntimeError) as exc:
        parser.error(str(exc))
    for result in results:
        print(
            f"PASS {result.scenario_id}: {result.failure_type}; "
            f"{result.steps} steps; 0 invalid actions; A* reference verified"
        )
        if args.output_dir is None:
            print(render_human_report(result))
    if args.output_dir is not None:
        print(f"Artifacts: {args.output_dir.resolve()}")
    print("Selected development-validation demos only; no general success rate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
