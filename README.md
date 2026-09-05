# MEHWAR

MEHWAR is a controller-agnostic evaluation layer for characterizing navigation-controller capability boundaries and mission-liveness failures. The assurance-core lane implements a selected C4 structured-static path through the unchanged T1 `Controller` and `EvaluationResult` contracts: frozen MaskablePPO inference, observation construction, episode execution, recurrence classification, deterministic A*, and JSON/human reporting.

## Scope and scientific semantics

`C4-0000` and `C4-0001` are **selected current MVP demo scenarios from the frozen C4 development-validation manifest**. They are not a fresh holdout, and two selected outcomes do not estimate general performance. No historical paper metrics are presented as current MEHWAR measurements.

- Both cases are 15x15, `u_trap`, moderate difficulty, with no dynamics.
- The runner and A* share 8-connected, destination-cell-only obstacle legality. Corner cutting is allowed. Orthogonal moves cost 1 and diagonals cost sqrt(2).
- Frozen action IDs 0-7 are N, S, W, E, NW, NE, SW, SE in `(row, col)` coordinates.
- The C4 episode budget is `max(10, ceil(optimal_steps * 2.0))`: 30 for C4-0000 and 28 for C4-0001.
- A* uses octile distance and deterministic tie breaking. Its reference results are 15 steps / 16.65685424949238 for C4-0000 and 14 steps / 16.071067811865476 for C4-0001.
- Observations are float32 `local_map (8,11,11)`, `global_map (8,32,32)`, and `scalars (4,)`. Frozen global_local C4 leaves no-fly, penalty, dynamic-change, and visitation-recency channels zero. Local out-of-bounds cells are obstacles, never free. Global indices use `min(31, index * 32 // grid_size)`.
- `c4_c5_recurrence_v1` has exact precedence `success -> collision -> two_cell_loop -> longer_loop -> timeout_other`. Two-cell recurrence requires **at least four trajectory positions** and any `trajectory[i] == trajectory[i-2]`. Thus `[A,B,A]` is `longer_loop`; `[A,B,A,B]` and `[A,B,A,C]` are `two_cell_loop`; `[A,B,C,A]` is `longer_loop`.
- Invalid actions are separate diagnostics. An illegal action causes collision and termination without movement. `steps` counts completed legal moves; `attempted_actions` also counts an illegal attempt. Recurrence is classified after termination and does not stop a run early.

## Lightweight installation

Python 3.10 or newer:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest
python -m ruff check .
```

Contracts, failure classification, A*, scenarios, and reporting use only the standard library. Observation construction requires NumPy; actor inference additionally requires PyTorch. Tests for those optional components skip if their dependency is absent. Real-checkpoint tests skip **only** when `MEHWAR_SEED33_CHECKPOINT` is unset or empty; a configured bad path, incorrect checkpoint, or missing inference dependency fails them.

## Verified seed-33 smoke

The checkpoint is intentionally external and untracked. `artifacts/` and model binaries are ignored. Obtain the verified checkpoint separately; this repository never downloads, trains, or writes it.

Expected filename: `model_stage_301056_lifetime_452608.zip`

Expected SHA256: `c91d30711aa91957554dfa92b152d2a1d1e14a7b43fa01237722c54cb0acfaaf`

```powershell
python -m pip install -e ".[dev,ppo]"
$env:MEHWAR_SEED33_CHECKPOINT = (Resolve-Path ".\artifacts\seed33\model_stage_301056_lifetime_452608.zip").Path
python -m pytest -m real_checkpoint -v
python -m pytest
python -m ruff check .
python -m mehwar.scenarios.c4_runner --checkpoint "$env:MEHWAR_SEED33_CHECKPOINT" --scenario C4-0000
python -m mehwar.scenarios.c4_runner --checkpoint "$env:MEHWAR_SEED33_CHECKPOINT" --scenario C4-0001 --json
```

The example assumes the separately supplied binary is placed under `artifacts/seed33`; the environment variable may instead point to any explicit external path.

`MaskablePPOCheckpointAdapter(checkpoint_path)` verifies SHA256 before inspecting the ZIP's `data`, `policy.pth`, and `_stable_baselines3_version`. It verifies seed **33**, **452608** timesteps, and checkpoint SB3 **2.9.0**. The unique full policy module count is **428937**, including the critic, with shared feature extractors counted once. Duplicated `state_dict` aliases are checked for agreement and are not added to that count.

The adapter performs direct CPU actor inference with frozen weights and strict architecture loading; SB3-Contrib is not required. It never deserializes the cloudpickled objects in SB3 JSON metadata. Selection is deterministic argmax over supplied legal action IDs, with lowest-ID tie breaking. A nonempty legal-action set is required. The feed-forward controller resets between runs and retains no episode history.

Real checkpoint verification on this branch reproduces:

| Selected demo | Success | Steps | Failure protocol output | Invalid actions |
|---|---|---|---|---|
| C4-0000 | true | 16 | success | 0 |
| C4-0001 | false | 28 | two_cell_loop | 0 |

The real tests also assert the entire supplied 29-position C4-0001 trajectory, repeat both runs, and check that checkpoint size, modification time, and SHA256 remain unchanged.

## Integration surface

```python
from mehwar.controllers.ppo import MaskablePPOCheckpointAdapter
from mehwar.reporting import render_human_report, result_to_json
from mehwar.scenarios.c4 import C4_0001
from mehwar.scenarios.c4_runner import run_c4

controller = MaskablePPOCheckpointAdapter(checkpoint_path)
result = run_c4(controller, C4_0001)  # unchanged T1 EvaluationResult
print(render_human_report(result))
payload = result_to_json(result)  # JSON string, no added contract fields
```

The human report exposes controller metadata, scenario, outcome, failure type, steps, cost, A* reference, diagnostics, provenance, configuration, and limitations. Provenance records current runner execution and selected-demo origin; unknown checkpoint identity is never fabricated for other controllers. Custom caller-supplied scenarios are labeled as unverified sources. `fixtures/sample_evaluation_result.json` remains a synthetic engineering fixture.

This branch does not implement Simra's general evaluator, batch profiler, dashboard, or their integration. Those components can consume the existing `EvaluationResult` without a contract change.

## Limitations

- Controlled 2-D grid-based mission-routing abstraction.
- Not physical flight validation.
- Not deployment approval.
- Not safety certification.
- Not evidence of general learned-controller or planner superiority.
