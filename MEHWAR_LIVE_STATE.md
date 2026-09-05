# MEHWAR LIVE STATE — FIRST INTEGRATION GATE

**Last updated:** 2026-09-05 PKT

**Repository:** `simra-imran-1/Mehwar`

**Working branch:** `feat/integration-demo`

## Verified source branches

The remote refs were fetched and verified exactly before creating the integration branch:

| Source | Immutable SHA |
|---|---|
| Frozen main / T1 baseline | `4ff04898d34e6791f872ecf08eb36b47f47fe72f` |
| Product/dashboard — `feat/product-dashboard` | `3edaf9da3094d8c1b52408dcd950e78e10665c37` |
| Assurance — `feat/assurance-core` | `b6dd92ead9dca470c4159885897c6fe69464ef3c` |

Integration was created from the frozen main baseline, then both feature branches were merged with `--no-ff`: product merge `293828b`, assurance merge `16887d3`. README was the only textual merge conflict. Both narratives were combined, and Streamlit was moved from a mandatory dependency to the `dashboard` extra alongside `dev` and `ppo`.

Only integration-demo is modified. Main and both source branches remain unchanged; no frozen research repository was modified. The current integration SHA is determined by Git, not embedded as a guessed self-reference.

## Ticket status

| Ticket | Status | Evidence / next dependency |
|---|---|---|
| T1 Scaffold/contracts | DONE | Frozen Controller/EvaluationResult source and original tests unchanged; source hash regression test passes |
| T2a Checkpoint gate | DONE | Verified external seed-33 binary, SHA256, ZIP metadata, and 428937 unique policy parameters |
| T2 PPO adapter | DONE | Frozen direct actor inference, legal-action masking, no training/write path; construction does not call the run-reset hook |
| T3 Selected C4 + A* | DONE | Both selected scenarios and exact deterministic references preserved |
| T4 Common evaluator | DONE | Hero path calls common evaluate(), receiving ExecutionRecord from raw C4 execution; exactly one reset per run |
| T5 Failure intelligence | DONE | Exact c4_c5_recurrence_v1 guard, precedence, and diagnostics preserved |
| T6 Batch/evidence profiler | NOT DONE | Single-run raw count display is not a batch profiler |
| T7 Report/provenance | DONE | Existing JSON/human reports retained, supplied research identifiers added, dashboard loader round-trip verified |
| T8 Fixture/dashboard | DONE | Fixture, uploaded JSON, and local selected-C4 execution use the same renderer; Streamlit AppTest verifies both real cases |
| T9 Visualization polish | NOT DONE | Existing trajectory presentation retained; no independent polish gate completed |
| T10 Integration/repro | IN PROGRESS — first integration gate PASS | Combined tests/lint and real dashboard execution pass; broader integration/reproduction review remains |
| T11 External feedback | NOT VERIFIED | No external response state established by this gate |
| T12 Application | NOT VERIFIED | Outside this gate |
| T13 Demo/screenshots | NOT DONE | Automated dashboard runs verified; no recording or screenshot deliverable produced |
| T14 Red-team | NOT DONE | Requires independent integrated-candidate review |
| T15 Submission | NOT DONE | Depends on subsequent gates |

## Integrated execution and dashboard flow

`MaskablePPOCheckpointAdapter -> raw C4 execution -> ExecutionRecord -> common T4 evaluate() -> EvaluationResult -> report/dashboard`

`run_c4(controller, scenario)` delegates to `mehwar.evaluator.evaluate()`. The evaluator resets the controller once; `_execute_c4()` does not reset it. Integration tests spy on the real evaluator call, verify raw record type and reset count, and assert the public wrapper returns the evaluator's result.

The dashboard preserves bundled synthetic fixture and uploaded JSON inputs and adds local selection of C4-0000/C4-0001. Local execution reads `MEHWAR_SEED33_CHECKPOINT`, imports PPO lazily on the explicit run button, and routes through integrated run_c4. Missing or invalid checkpoint configuration shows an error without synthetic fallback. Ordinary Streamlit reruns reuse the displayed result; switching scenario does not display the previous scenario's result.

Real selected runs display `CURRENT MEHWAR SELECTED DEMO RUN`, a descriptive status, and adjacent raw single-run counts. C4-0000 displays `NO FAILURE OBSERVED IN SELECTED DEMO SET`; C4-0001 displays `LIVENESS DEGRADATION OBSERVED`. Synthetic fixture warnings remain visible for synthetic data. There is no opaque safety score.

## Verification evidence

- `python -m pip install -e ".[dev,ppo,dashboard]"`: succeeded in the repository `.venv`.
- `python -m pytest` with checkpoint configured: **76 passed, zero skipped**. Includes all inherited product and assurance tests unchanged, plus 15 integration tests; five real-checkpoint cases executed.
- `python -m ruff check .`: **All checks passed**.
- `git diff --check`: passed.
- Streamlit AppTest selected and executed both real scenarios, checked shared rendering, evidence status/counts, and all five limitations. The real dashboard path called the common evaluator once and reset once, including controller construction.
- Current result JSON round-trips through `load_evaluation_result()`; current and synthetic evidence labels remain distinct.
- Fixture AppTest works with PyTorch import blocked. Pure integration/data modules import with site packages disabled; neither torch nor Streamlit is mandatory for the core.
- Frozen T1 source, package exports, synthetic fixture, and every inherited test were checked unchanged against their respective source commits.
- Checkpoint remains ignored/untracked. Hash is unchanged; the real-checkpoint suite also checks size and modification time.

Runtime: Python 3.12.14, NumPy 2.5.2, PyTorch 2.14.0+cpu, Streamlit 1.63.0, pytest 8.4.2. Runtime versions are distinct from the checkpoint's SB3 2.9.0 metadata.

| Current integrated selected run | Success | Steps | Failure protocol output | Invalid actions | A* steps / cost |
|---|---|---|---|---|---|
| C4-0000 | true | 16 | success | 0 | 15 / 16.65685424949238 |
| C4-0001 | false | 28 | two_cell_loop | 0 | 14 / 16.071067811865476 |

The entire supplied 29-position C4-0001 trajectory is identical, including its repeated final cells. These are current selected-demo runs, not a fresh holdout or a general performance estimate.

## Checkpoint and scientific provenance

Checkpoint: `model_stage_301056_lifetime_452608.zip`, SHA256 `c91d30711aa91957554dfa92b152d2a1d1e14a7b43fa01237722c54cb0acfaaf`, seed 33, num_timesteps 452608, 428937 unique full-policy parameters including critic. Duplicated feature-extractor aliases are not added repeatedly to the parameter count. The inherited shell variable was empty; verification commands explicitly set it to the existing ignored local `artifacts/seed33` file.

Selected C4 provenance includes the supplied research repository `muzzammilsajid1/uav-dynamic-routing`, source commit `95b8ec3834e79464e18dd9cdcef3c0378ba343cc`, manifest `evaluation/manifests/rl_v3_phase_c4_validation.json`, and manifest blob `d687a62a72dc266eb9092fa36221cba7fe309153`. Scenario classification is `development_validation`, selection is `selected current MVP demo`, and fresh_holdout is false. This gate did not modify the source repository or invent additional identifiers. Current MEHWAR commit, run IDs, and timestamps are not fabricated at runtime. Controller checkpoint identity remains in controller_metadata.

Movement remains static 8-connected destination-cell-only legality, corner cutting allowed, costs 1 / sqrt(2). Budgets remain 30 and 28. Frozen observation channels and the recurrence detector remain unchanged: success precedes collision, two-cell recurrence requires at least four positions, and invalid actions remain separate diagnostics. No historical paper percentages are presented as current measurements.

## Limitations / next dependency

Controlled 2-D grid-based mission-routing abstraction. Not physical flight validation. Not deployment approval. Not safety certification. Not evidence of general learned-controller or planner superiority.

No blocker remains for this first integration gate. Reproduction requires the external verified checkpoint and the optional PPO/dashboard dependencies. The next dependency is review of the integrated candidate and broader reproduction, then separately verified batch profiling, visualization polish, demo recording, and red-team work before any submission claim.
