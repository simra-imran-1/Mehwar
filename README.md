# MEHWAR

MEHWAR is a research-backed functional prototype for characterizing navigation-controller capability boundaries and mission-liveness failures.

The integrated hero path is a verified frozen controller, selected C4 scenario execution, an `ExecutionRecord`, the common T4 evaluator, and the unchanged T1 `EvaluationResult`. The result feeds JSON/human reports and the Streamlit dashboard. The evaluator owns the single pre-run controller reset. The integration gate verifies this full path against both source lanes.

## Reproduce the selected MEHWAR demo

Python 3.10 or newer:

```powershell
git clone --branch feat/integration-demo https://github.com/simra-imran-1/Mehwar.git
cd Mehwar
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev,ppo,dashboard]"
$env:MEHWAR_SEED33_CHECKPOINT = (Resolve-Path ".\artifacts\seed33\model_stage_301056_lifetime_452608.zip").Path
.\scripts\verify_selected_demo.ps1 -OutputDir outputs/selected_demo
python -m streamlit run app.py
```

Supply the checkpoint separately before resolving its path; any explicit external path is valid. The helper verifies its SHA256 **before tests**, shows the checkout SHA, runs pytest/Ruff, and executes both selected demos. It stops on failure and finishes with PASS only after checking the expected evidence and unchanged checkpoint. Add `-InstallDependencies` to have the helper run the install command itself.

After setup, the one-command reproduction entry point is:

```powershell
python scripts/run_selected_demo.py --all --output-dir outputs/selected_demo
```

Use `--scenario C4-0000` or `--scenario C4-0001` instead of `--all` for one case. `--checkpoint PATH` overrides the environment variable. The command verifies the checkpoint through the existing adapter, uses integrated `run_c4`, and asserts outcomes, A* references, and the complete C4-0001 regression trajectory. These are **current MEHWAR measurements on selected development-validation demos**, not a fresh holdout, within a controlled 2-D abstraction.

`--all` writes exactly two result pairs (`C4-0000.json/.txt`, `C4-0001.json/.txt`) and `manifest.json` in a fresh output directory. JSON retains the unchanged EvaluationResult schema and can be uploaded to the dashboard; text uses the existing human report with limitations. Without `--output-dir`, reports print to the terminal. Repeated commands overwrite their named outputs; `outputs/` is disposable and ignored by Git.

The manifest copies known source/checkpoint/protocol identifiers and lists output filenames. It adds the package version when resolvable, and `mehwar_git_commit` only when Git identifies this source checkout and its working tree is clean. Otherwise the commit is omitted. No timestamps, run IDs, or environment identities are generated. Repeated exports in the same checkout/runtime have identical content; a different verified Git SHA is an explicit provenance change.

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

Real-checkpoint tests skip only if the environment variable is unset/empty. A configured missing/corrupt checkpoint or missing inference dependencies fails. Tests verify both outcomes, the entire supplied C4-0001 trajectory, repeatability, and unchanged checkpoint hash/size/modification time.

## Dashboard and integration surface

The dashboard has three input paths: bundled synthetic engineering fixture, uploaded `EvaluationResult` JSON, and a locally executed selected C4 demo. The local path selects C4-0000 or C4-0001 and reads `MEHWAR_SEED33_CHECKPOINT`; missing/invalid configuration produces a visible error, never synthetic fallback. PPO imports occur only when a local run is requested. Results use the same rendering path for trajectory, reference, diagnostics, configuration, provenance, and limitations.

The bundled fixture remains **SYNTHETIC ENGINEERING FIXTURE - UI/INTEGRATION TEST ONLY**. Current selected C4 results are visibly labeled **CURRENT MEHWAR SELECTED DEMO RUN**. Status labels are accompanied by raw counts for one selected run; there is no opaque safety score or generalization from one success. Uploaded evidence classifications remain claims of the supplied payload.

Selected-demo provenance records the supplied research source identifiers: repository `muzzammilsajid1/uav-dynamic-routing`, commit `95b8ec3834e79464e18dd9cdcef3c0378ba343cc`, manifest `evaluation/manifests/rl_v3_phase_c4_validation.json`, blob `d687a62a72dc266eb9092fa36221cba7fe309153`, and classification `development_validation`. This gate uses the supplied identifiers without modifying the research repository. No timestamps, run IDs, or current MEHWAR SHA are fabricated. Custom scenarios retain unverified-source labels.

## Limitations

- Controlled 2-D grid-based mission-routing abstraction.
- Not physical flight validation.
- Not deployment approval.
- Not safety certification.
- Not evidence of general learned-controller or planner superiority.

Batch profiling, visualization polish, external feedback, application/submission, recorded demos, and red-team review are separate gates; this integration does not claim them complete.
