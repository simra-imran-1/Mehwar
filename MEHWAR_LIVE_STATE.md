# MEHWAR LIVE STATE — FINAL T6/T9 INTEGRATION GATE

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
| T6 Batch/evidence profiler | DONE | Selected-demo batch profiler integrated; current EvaluationResult objects drive raw counts and approved descriptive evidence labels; no generalized success rate, safety score, or capability score |
| T7 Report/provenance | DONE | Existing JSON/human reports retained, supplied research identifiers added, dashboard loader round-trip verified |
| T8 Fixture/dashboard | DONE | Fixture, uploaded JSON, and local selected-C4 execution use the same renderer; Streamlit AppTest verifies both real cases |
| T9 Visualization polish | DONE | Selected C4 visualization integrated with scientific (row,col), x=col/y=row, obstacles/start/goal, learned-controller path, supplied deterministic A* path, and repeated-cell markers for supplied two_cell_loop evidence |
| T10 Integration/repro | DONE | Final T6/T9 integration gate passed with verified seed-33 checkpoint: 128 passed, zero skipped; Ruff PASS; git diff --check PASS; selected-demo helper PASS; independent reproduction PASS; manual dashboard review PASS |
| T11 External feedback | NOT VERIFIED | No external response state established by this gate |
| T12 Application | NOT VERIFIED | Outside this gate |
| T13 Demo/screenshots | IN PROGRESS | Integrated C4-0000 and C4-0001 dashboard screenshots captured and manually reviewed; final 45–60 s recording still pending |
| T14 Red-team | NOT DONE | Requires independent integrated-candidate review |
| T15 Submission | NOT DONE | Depends on subsequent gates |

## Integrated execution and dashboard flow

`MaskablePPOCheckpointAdapter -> raw C4 execution -> ExecutionRecord -> common T4 evaluate() -> EvaluationResult -> report/dashboard`

`run_c4(controller, scenario)` delegates to `mehwar.evaluator.evaluate()`. The evaluator resets the controller once; `_execute_c4()` does not reset it. Integration tests spy on the real evaluator call, verify raw record type and reset count, and assert the public wrapper returns the evaluator's result.

The dashboard preserves bundled synthetic fixture and uploaded JSON inputs and adds local selection of C4-0000/C4-0001. Local execution reads `MEHWAR_SEED33_CHECKPOINT`, imports PPO lazily on the explicit run button, and routes through integrated run_c4. Missing or invalid checkpoint configuration shows an error without synthetic fallback. Ordinary Streamlit reruns reuse the displayed result; switching scenario does not display the previous scenario's result.

Real locally executed selected runs display `CURRENT MEHWAR SELECTED DEMO RUN`, explicitly state that the scenario is development-validation rather than a fresh holdout, and show adjacent raw evidence counts. C4-0000 displays `NO FAILURE OBSERVED IN SELECTED DEMO RUN`; C4-0001 displays `LIVENESS DEGRADATION OBSERVED`. The integrated T6 profiler can evaluate the selected two-scenario set using raw counts and approved descriptive labels without presenting a generalized success rate or safety/capability score. Uploaded evidence is distinguished from locally executed evidence, and contradictory current-demo provenance is rejected.

## Verification evidence

- `python -m pip install -e ".[dev,ppo,dashboard]"`: succeeded in the repository `.venv`.
- `python -m pytest` with checkpoint configured: **128 passed, zero skipped**. The inherited test suite remains covered alongside the T10 reproduction tests and the integrated T6/T9/dashboard-hardening tests; real-checkpoint cases executed successfully.
- `python -m ruff check .`: **All checks passed**.
- `git diff --check`: passed.
- Streamlit AppTest selected and executed both real scenarios, checked shared rendering, evidence status/counts, and all five limitations. The real dashboard path called the common evaluator once and reset once, including controller construction.
- Current result JSON round-trips through `load_evaluation_result()`; current and synthetic evidence labels remain distinct.
- Fixture AppTest works with PyTorch import blocked. Pure integration/data modules import with site packages disabled; neither torch nor Streamlit is mandatory for the core.
- Frozen T1 source, package exports, synthetic fixture, and every inherited test were checked unchanged against their respective source commits.
- Checkpoint remains ignored/untracked. Hash is unchanged; the real-checkpoint suite also checks size and modification time.
- Final T6/T9 integrated verification ran on Python 3.13.6 with the verified external seed-33 checkpoint. The complete suite passed: **128 passed, zero skipped**.
- `scripts/verify_selected_demo.ps1 -OutputDir outputs/selected_demo` completed with PASS after using an explicit writable pytest basetemp because the default Windows user pytest temporary/cache directory was inaccessible.
- The pytest basetemp workaround changed no MEHWAR source, scientific semantics, checkpoint contents, or filesystem ACLs.
- Independent `python scripts/run_selected_demo.py --all --output-dir outputs/selected_demo_final` passed for both selected development-validation scenarios.
- Manual integrated dashboard review confirmed the T9 coordinate convention `x = col`, `y = row`, obstacles/start/goal, learned trajectory, supplied deterministic A* trajectory, and C4-0001 recurrence markers.

Runtime: Python 3.13.6, NumPy 2.3.4, PyTorch 2.10.0+cpu, Streamlit 1.63.0, pytest 8.4.2. Runtime versions are distinct from the checkpoint's SB3 2.9.0 metadata.

## Assurance-side reproducibility gate

Mandatory starting HEAD was verified as `972c431756c2cb6d438c6d32faa36b75f00191c1` after fetch and checkout. Changes are confined to reproduction tooling, its tests, output ignore rules, README, and this record. Controller/EvaluationResult contracts, integrated runner/evaluator, recurrence semantics, hero scenarios, PPO identity, A* movement contract, and approved dashboard labels were not changed. T6 and T9 remain outside this task.

- `python scripts/run_selected_demo.py --scenario C4-0000` and `--scenario C4-0001` select one case; `--all` selects exactly those two. The checkpoint defaults to `MEHWAR_SEED33_CHECKPOINT`, with an explicit `--checkpoint` override.
- The entry point uses the existing adapter and integrated run_c4 path, including ExecutionRecord/common evaluator, A*, recurrence classification, and EvaluationResult. It checks the supplied expected outcomes and reference costs/steps without implementing scientific rules again. A compact-JSON trajectory digest checks the entire C4-0001 trace; a test binds that digest to the unchanged regression oracle.
- `scripts/verify_selected_demo.ps1` checks repository identity, displays current HEAD, verifies the external checkpoint hash before tests, documents or installs the extras, runs pytest/Ruff/whitespace checks, executes both selected demos, checks the final checkpoint hash, and prints PASS only on success.
- Extras installation succeeded. An initial helper invocation stopped on existing Windows pytest temporary/cache directory permissions. The final integrated helper run passed using an explicit writable workspace pytest basetemp with the cache provider disabled. No ACL changes, MEHWAR source changes, scientific-semantic changes, or model modifications were needed.
- The real helper run with `-OutputDir outputs/selected_demo` passed. The independent reproduction command wrote a second copy under `outputs/selected_demo_repeat`; all five exported files were byte-identical between runs in the same source/runtime state.
- Each output set contains exactly `C4-0000.json`, `C4-0000.txt`, `C4-0001.json`, `C4-0001.txt`, and `manifest.json`. JSON round-trips through the existing dashboard loader. Human reports contain all five scientific limitations. Both hero outcomes, A* references, and the complete C4-0001 trajectory match the existing evidence.
- The manifest copies known source/protocol/movement/checkpoint metadata and explicitly identifies development_validation, selected current MVP demo, and fresh_holdout false. It lists output filenames and includes the resolvable package version. No timestamp, run ID, or environment identity is invented. The Git commit is included only when the source repository can be identified and its working tree is clean; it is omitted while edits are uncommitted.
- `outputs/` is disposable and ignored. Neither generated reports nor the checkpoint are committed. There is no generalized benchmark mode, aggregate success rate, historical percentage, T6 profiler, or T9 visualization change.

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

No blocker remains for T10. T6 and T9 are integrated and the final checkpoint-backed integration/reproduction gate passed. Remaining pre-submission work is T12 application completion, T13 final 45–60 s demo recording/screenshots, T14 independent jury/technical red-team, any critical-only fixes, and T15 submission. The current prototype remains a controlled 2-D grid-based mission-routing abstraction: not physical flight validation, deployment approval, safety certification, or evidence of general learned-controller/planner superiority.
