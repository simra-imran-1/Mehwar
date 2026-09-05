# MEHWAR

MEHWAR is a research-backed functional prototype for characterizing navigation-controller capability boundaries and mission-liveness failures.

The integrated hero path is a verified frozen controller, selected C4 scenario execution, an `ExecutionRecord`, the common T4 evaluator, and the unchanged T1 `EvaluationResult`. The result feeds JSON/human reports and the Streamlit dashboard. The evaluator owns the single pre-run controller reset. The integration gate verifies this full path against both source lanes.

## Setup

Python 3.10 or newer:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev,ppo,dashboard]"
```

The optional groups are `dev`, `ppo` (NumPy/PyTorch), and `dashboard` (Streamlit). Normal core installation has no runtime dependencies. Contracts, common evaluator, failure classification, scenarios, A*, reporting, and dashboard data loading use only the standard library. For fixture/upload use without PyTorch, install `.[dev,dashboard]`; the full test suite requires all extras.

## Selected C4 demos and exact semantics

C4-0000 and C4-0001 are selected current MVP demos from the frozen C4 development-validation manifest, **not a fresh holdout**. Both are static 15x15 moderate `u_trap` cases.

- Runner and deterministic A* share 8-connected, destination-cell-only obstacle legality, corner cutting allowed, orthogonal cost 1, and diagonal cost sqrt(2). A* uses octile distance with deterministic tie breaking.
- Action IDs 0-7 are N, S, W, E, NW, NE, SW, SE in `(row, col)` coordinates.
- Episode budget: `max(10, ceil(optimal_steps * 2.0))`, giving 30 and 28.
- Frozen observations: float32 `local_map (8,11,11)`, `global_map (8,32,32)`, and `scalars (4,)`. No-fly, penalty, dynamic-change, and visitation-recency channels remain zero. Local out-of-bounds is occupied, never free. Global bin: `min(31, index * 32 // grid_size)`.
- Failure protocol: `c4_c5_recurrence_v1`, with precedence `success -> collision -> two_cell_loop -> longer_loop -> timeout_other`. Two-cell recurrence requires `len(trajectory) >= 4` and any `trajectory[i] == trajectory[i-2]`.
- `[A,B,A]` and `[A,B,C,A]` are `longer_loop`; `[A,B,A,B]` and `[A,B,A,C]` are `two_cell_loop`; `[A,B,C,D]` is `timeout_other`, absent success/collision.
- Illegal actions terminate with collision, without movement/cost, and remain separate diagnostics. Steps count completed legal moves; attempted actions also count illegal attempts. Recurrence never stops an episode early.

| Selected demo | Seed-33 outcome | Steps | Invalid actions | A* steps / cost |
|---|---|---|---|---|
| C4-0000 | success | 16 | 0 | 15 / 16.65685424949238 |
| C4-0001 | two_cell_loop | 28 | 0 | 14 / 16.071067811865476 |

These are selected local smoke outcomes, not general performance estimates. No historical paper percentages are presented as current MEHWAR measurements.

## External checkpoint and reproduction

The checkpoint is intentionally external, ignored, and untracked. The adapter never trains, downloads, or writes it. Place the separately supplied file under `artifacts/seed33`, or use another explicit path.

- Filename: `model_stage_301056_lifetime_452608.zip`
- SHA256: `c91d30711aa91957554dfa92b152d2a1d1e14a7b43fa01237722c54cb0acfaaf`
- Seed: 33; num_timesteps: 452608; checkpoint SB3 version: 2.9.0.
- Unique full policy parameter count: 428937, including critic, counting shared feature modules once.

`MaskablePPOCheckpointAdapter(checkpoint_path)` checks the hash, SB3 ZIP data/version/weights, alias agreement, and strict architecture. Direct CPU actor inference avoids SB3-Contrib and cloudpickle execution. Frozen deterministic argmax is restricted to supplied legal actions, with lowest-ID tie breaking. Checkpoint identity stays in `controller_metadata`.

```powershell
$env:MEHWAR_SEED33_CHECKPOINT = (Resolve-Path ".\artifacts\seed33\model_stage_301056_lifetime_452608.zip").Path
python -m pytest
python -m ruff check .
git diff --check
python -m mehwar.scenarios.c4_runner --checkpoint "$env:MEHWAR_SEED33_CHECKPOINT" --scenario C4-0000
python -m mehwar.scenarios.c4_runner --checkpoint "$env:MEHWAR_SEED33_CHECKPOINT" --scenario C4-0001 --json
python -m streamlit run app.py
```

Real-checkpoint tests skip only if the environment variable is unset/empty. A configured missing/corrupt checkpoint or missing inference dependencies fails. Tests verify both outcomes, the entire supplied C4-0001 trajectory, repeatability, and unchanged checkpoint hash/size/modification time.

## Dashboard and integration surface

The dashboard has three input paths: bundled synthetic engineering fixture, uploaded `EvaluationResult` JSON, and a locally executed selected C4 demo. The local path selects C4-0000 or C4-0001 and reads `MEHWAR_SEED33_CHECKPOINT`; missing/invalid configuration produces a visible error, never synthetic fallback. PPO imports occur only when a local run is requested. Results use the same rendering path for trajectory, reference, diagnostics, configuration, provenance, and limitations.

The bundled fixture remains **SYNTHETIC ENGINEERING FIXTURE - UI/INTEGRATION TEST ONLY**. Current selected C4 results are visibly labeled **CURRENT MEHWAR SELECTED DEMO RUN**. Status labels are accompanied by raw counts for one selected run; there is no opaque safety score or generalization from one success. Uploaded evidence classifications remain claims of the supplied payload.

```python
from mehwar.controllers.ppo import MaskablePPOCheckpointAdapter
from mehwar.dashboard.data import load_evaluation_result
from mehwar.reporting import render_human_report, result_to_json
from mehwar.scenarios.c4 import C4_0001
from mehwar.scenarios.c4_runner import run_c4

result = run_c4(MaskablePPOCheckpointAdapter(checkpoint_path), C4_0001)
print(render_human_report(result))
loaded = load_evaluation_result(result_to_json(result).encode("utf-8"))
```

Selected-demo provenance records the supplied research source identifiers: repository `muzzammilsajid1/uav-dynamic-routing`, commit `95b8ec3834e79464e18dd9cdcef3c0378ba343cc`, manifest `evaluation/manifests/rl_v3_phase_c4_validation.json`, blob `d687a62a72dc266eb9092fa36221cba7fe309153`, and classification `development_validation`. This gate uses the supplied identifiers without modifying the research repository. No timestamps, run IDs, or current MEHWAR SHA are fabricated. Custom scenarios retain unverified-source labels.

## Limitations

- Controlled 2-D grid-based mission-routing abstraction.
- Not physical flight validation.
- Not deployment approval.
- Not safety certification.
- Not evidence of general learned-controller or planner superiority.

Batch profiling, visualization polish, external feedback, application/submission, recorded demos, and red-team review are separate gates; this integration does not claim them complete.
