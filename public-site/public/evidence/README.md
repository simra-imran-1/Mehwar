# Selected MEHWAR evidence — immutable public export

`selected-runs.json` is a presentation-only, allowlisted export of existing evidence. No controller, evaluator, recurrence classifier, scenario generator or scientific test was executed to produce this file. The complete controller and deterministic A* reference trajectories are copied from the original JSON records, not reconstructed from screenshots.

## Frozen source and lineage

- MEHWAR source branch: `feat/integration-demo`.
- Frozen MEHWAR source commit: `1586eebf9daa8a8e690bc6f62cc377ce540214ee`.
- Original records: `outputs/final-submission-selected-demo/C4-0000.json`, `outputs/final-submission-selected-demo/C4-0001.json`, and `outputs/final-submission-selected-demo/manifest.json` in the MEHWAR source checkout. These are existing ignored evaluation outputs. The manifest identifies the exact frozen commit above.
- Grid, obstacle, start and goal definitions: `src/mehwar/scenarios/c4.py` at the frozen commit.
- Full C4-0001 controller trajectory oracle: `tests/test_real_seed33.py` at the frozen commit. Its compact-JSON SHA256 is `ec7fea9558b5de358d71632065497c14170bf225e2ee9d94de42647ab9f81fc3`, also pinned by `src/mehwar/selected_demo.py`.
- Coordinate convention: positions are `[row, col]`; display `x = col`, `y = row`, with rows increasing downward, as in frozen `src/mehwar/dashboard/visualization.py`.
- Research source: `muzzammilsajid1/uav-dynamic-routing`, commit `95b8ec3834e79464e18dd9cdcef3c0378ba343cc`.
- Research scenario manifest: `evaluation/manifests/rl_v3_phase_c4_validation.json`, Git blob `d687a62a72dc266eb9092fa36221cba7fe309153`.
- Scenario classification: `development_validation`; selected current MVP demo; `fresh_holdout: false`.

| Source record | SHA256 |
| --- | --- |
| `C4-0000.json` | `8ebbad71923d4252bfff52c7f2be9ecc924311fcee0b7e2f1962e9bcb45a6dda` |
| `C4-0001.json` | `77aa27d925a465b5dad06750c1e74702dae44aeb6e3838a1cf47482a2616d746` |
| `manifest.json` | `7d7c95bcb0b122bbd8240a6dddbaa0e21874936f81ab48410a7ad63b33fc9e23` |
| Public `selected-runs.json` | `d16c0c39fdf0322b4ad06da3ab27c08aa07f10cc4de2989f955cee762719ea5e` |

## What was preserved and omitted

Preserved: supplied outcomes, steps, path costs, failure labels, complete trajectories, deterministic reference results, separate invalid-action diagnostics, scenario configuration, source provenance, checkpoint hash, deterministic/action-masking metadata and seed.

Omitted: checkpoint filename, machine/runtime implementation metadata and any private local source location. No checkpoint binary is published. Source locations above are repository-relative evidence identifiers.

The two supplied evidence labels used by the website are `LIVENESS DEGRADATION OBSERVED` for C4-0001 and `NO FAILURE OBSERVED IN SELECTED DEMO RUN` for C4-0000. These labels are approved interpretations of individual selected runs. They do not establish a generalized success rate, safety score or algorithm ranking.

The public site displays supplied `failure_type` values under `c4_c5_recurrence_v1`; it must not calculate new classifications. The movement contract is static 8-connected destination-cell-only legality, with corner cutting allowed, orthogonal cost 1 and diagonal cost sqrt(2). Deterministic A* is reliability reference context under that shared grid contract.

## Original evaluator screenshots

The existing public images are unedited final T13 micro-polish screenshots at 1920 × 1065. Their SHA256s match the original `outputs/t13-micro-screenshots/C4-0000-hero.png` and `C4-0001-hero.png` artifacts in the T13 checkout at the same frozen source commit.

| Public asset | SHA256 |
| --- | --- |
| `c4-0000-success.png` | `ed0ee4ee1e6a372e8a7ca26d36967b531c906513d3bf7e5ba0f3bb3527a856a2` |
| `c4-0001-liveness-degradation.png` | `bd4dad0e5804a1e001e43673d42048b5a1276cc88e0e13bea76ca8a2dbcc0160` |

## Scope and verification

The evidence is a controlled 2-D grid-based mission-routing abstraction. It is not physical flight validation, deployment approval, safety certification or evidence of general learned-controller/planner superiority. External autonomy-stack and higher-fidelity relevance remain validation questions.

The recorded submission verification statement — 137 tests passed, 0 skipped, Ruff PASS and diff check PASS — comes from the approved submission specification and existing public-site provenance record. It was not rerun for this website work and is implementation verification, not a safety score. The older `MEHWAR_LIVE_STATE.md` contains earlier 128/130-test gate chronology and does not supersede that submission record.

Run `node scripts/check-evidence.mjs` from `public-site/` to check the immutable export checksum, approved selected-case facts, geometry counts, source digests and sanitization. These checks do not evaluate scientific behavior. A future scientific build needs a separate evidence record; do not rewrite this submission export in place.
