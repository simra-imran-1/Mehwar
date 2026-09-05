# MEHWAR LIVE STATE

**Last updated:** 2026-09-05 PKT
**Updated by:** Codex for Muzzammil Sajid's assurance-core lane
**Repository:** `simra-imran-1/Mehwar`
**Working branch:** `feat/assurance-core`

## 1. Current objective and branch boundary

Deliver the selected C4 structured-static assurance path against the frozen T1 contracts. Mandatory starting HEAD was verified as `4ff04898d34e6791f872ecf08eb36b47f47fe72f` after fetch and checkout. The current commit cannot embed its own SHA; `git rev-parse feat/assurance-core` is authoritative.

Only assurance-core was changed. `main` and `feat/product-dashboard` were not modified or merged. No frozen research repository was modified. `src/mehwar/contracts.py`, its package exports, the T1 contract tests, and the synthetic fixture remain unchanged.

## 2. Ticket status

| Ticket | Owner | Status / evidence | Remaining dependency |
|---|---|---|---|
| T0 Research reuse audit | Muzzammil | Previously reported substantially complete; external audit not reverified here | External governance evidence |
| T1 Scaffold/contracts | Simra | DONE; unchanged baseline and passing contract tests | None |
| T2a Checkpoint gate | Muzzammil | DONE; local seed-33 binary exists and SHA256/ZIP metadata verified | Binary remains external to Git |
| T2 PPO adapter | Muzzammil | DONE; direct frozen actor, strict weights, masking, unique count, real smoke tests | Optional ppo dependencies and external checkpoint |
| T3 C4 + A* | Muzzammil | DONE; both selected scenarios and exact reference outcomes tested | None |
| T4 Evaluator orchestration | Simra | Separate product lane; not implemented or verified here | Consume unchanged T1 result; selected C4 runner is available |
| T5 Failure intelligence | Muzzammil | DONE; exact c4_c5_recurrence_v1 and precedence tests | None |
| T6 Batch/evidence profiler | Simra | Separate product lane; not verified here | Evaluator integration |
| T7 Report/provenance | Muzzammil | DONE; lossless JSON, human evidence report, explicit limitations | Dashboard consumption |
| T8 Dashboard | Simra | Separate product lane; not implemented or verified here | Product branch integration |
| T9 Visualization polish | Simra | Not verified here | Dashboard |
| T10 Integration/repro | Both | PENDING; assurance-only real C4 runs verified | Integrate report/dashboard against EvaluationResult |
| T11 External feedback | Simra | UNVERIFIED here | External responses |
| T12 Application | Both | UNVERIFIED here | Outside assurance-core |
| T13 Demo/screenshots | Both | PENDING; CLI report available, no integrated recording/screenshots verified | Integrated application |
| T14 Red-team | Both | PENDING | Integrated candidate |
| T15 Submission | Both | PENDING | Prior gates |

## 3. Verified checkpoint gate

- Filename: `model_stage_301056_lifetime_452608.zip`
- SHA256: `c91d30711aa91957554dfa92b152d2a1d1e14a7b43fa01237722c54cb0acfaaf`
- Seed: 33; num_timesteps: 452608; checkpoint SB3 version: 2.9.0.
- Unique full policy parameter count: 428937. Shared feature-module aliases are not double/triple counted; critic parameters are included.
- Local artifact found under `artifacts/seed33/`; `MEHWAR_SEED33_CHECKPOINT` was set explicitly for verification because the inherited shell variable was empty.
- Binary is ignored, untracked, and unchanged. Adapter only reads it; no training path or SB3-Contrib runtime dependency.

## 4. Scientific decisions preserved

- C4-0000 and C4-0001 are selected current MVP demos from the frozen C4 development-validation manifest, not a fresh holdout.
- No historical paper metrics are claimed as current MEHWAR measurements.
- Runner/A* share static 8-connected destination-only legality, corner cutting allowed, cost 1 / sqrt(2).
- Budgets are `max(10, ceil(optimal_steps * 2.0))`: 30 and 28.
- Frozen global_local observation recency channel is zero; local out-of-bounds is occupied, never free.
- Protocol ID is `c4_c5_recurrence_v1`. Precedence is success, collision, two-cell loop, longer loop, timeout/other.
- The two-cell detector requires at least four trajectory positions. `[A,B,A]` is longer_loop; `[A,B,A,B]` and `[A,B,A,C]` are two_cell_loop.
- Invalid actions remain separate diagnostics; recurrence classification does not terminate episodes early.
- No Dijkstra, D* Lite, or old C2/C3/DDQN diagnostics were added.

## 5. Current verification

Environment: isolated `.venv`, Python 3.12.14, NumPy 2.5.2, PyTorch 2.14.0+cpu, pytest 8.4.2. Runtime versions are distinct from the checkpoint's SB3 version.

`python -m pytest` with `MEHWAR_SEED33_CHECKPOINT` set: **48 passed**, including all three real-checkpoint tests. `python -m ruff check .`: **All checks passed**. Standard-library-only imports were also verified with site packages disabled. The real tests fail on a configured bad path, invalid checkpoint, or missing optional inference dependency, and skip only if the checkpoint variable is unavailable.

| Current local measurement | Success | Steps | Protocol result | Invalid actions | A* steps / cost |
|---|---|---|---|---|---|
| C4-0000 | true | 16 | success | 0 | 15 / 16.65685424949238 |
| C4-0001 | false | 28 | two_cell_loop | 0 | 14 / 16.071067811865476 |

The full supplied C4-0001 trajectory matches exactly, including all repetitions through position 29. Repeated runs match. Checkpoint hash, size, and modification time are unchanged after the tests. Human and JSON reports expose current evidence; the T1 fixture stays labeled synthetic.

## 6. Limitations and blockers

Controlled 2-D grid-based mission-routing abstraction. Not physical flight validation. Not deployment approval. Not safety certification. Not evidence of general learned-controller or planner superiority.

No assurance implementation blocker remains. Reproduction requires the separately supplied checkpoint and optional `ppo` installation. General evaluator, batch/profile, dashboard, recording, external feedback, application, and submission state have not been verified on this branch.

## 7. Next integration dependency

Simra's product lane must consume `run_c4(controller, scenario) -> EvaluationResult`, preserve current-measurement versus synthetic evidence labels, and connect the result to the report/dashboard path with provenance and limitations visible. Integration must retain the unchanged Controller/EvaluationResult contracts and verify the real controller/scenario/report/dashboard flow. No product-dashboard branch was merged into assurance-core.
