# MEHWAR LIVE STATE

**Last updated:** 2026-09-05 PKT
**Updated by:** Codex for the T1 baseline
**Repository:** `simra-imran-1/Mehwar`

## 1. Current objective

Freeze the T1 shared Controller and EvaluationResult contracts before assurance-core and product-dashboard feature work begins.

## 2. Repository state

- `main`: T1 baseline commit containing this file; resolve the exact immutable SHA with `git rev-parse main` - demo-ready contract baseline.
- `feat/assurance-core`: same T1 baseline commit as `main` - ready for Muzzammil's assurance lane; no feature-specific commits.
- `feat/product-dashboard`: same T1 baseline commit as `main` - ready for Simra's product lane; no feature-specific commits.
- `feat/integration-demo`: N/A - not created.

The three active branch names are required to resolve to one exact commit at the T1 integration gate. The commit cannot embed its own SHA; Git refs are the authoritative SHA record.

## 3. Ticket status

| Ticket | Owner | Status | SHA / evidence | Blocker |
|---|---|---|---|---|
| T0 Research reuse audit | Muzzammil | Reported substantially complete in project governance; delta not verified in T1 | External frozen-research evidence | Outside T1 |
| T1 Scaffold/contracts | Simra | DONE | T1 baseline commit; `python -m pytest` | None |
| T2a Checkpoint gate | Muzzammil | TODO | None | Verified checkpoint availability unknown |
| T2 PPO adapter | Muzzammil | TODO | None | Depends on T2a |
| T3 C4 + A* | Muzzammil | TODO | None | Not started |
| T4 Evaluator orchestration | Simra | TODO | None | Starts after T1 |
| T5 Failure intelligence | Muzzammil | TODO | None | Exact detector intentionally not implemented in T1 |
| T6 Batch/evidence profiler | Simra | TODO | None | Depends on evaluator output |
| T7 Report/provenance | Muzzammil | TODO | None | Not started |
| T8 Dashboard | Simra | TODO | None | Not started |
| T9 Visualization polish | Simra | TODO | None | Not started |
| T10 Integration/repro | Both | TODO | None | Depends on feature lanes |
| T11 External feedback | Simra | IN PARALLEL / UNVERIFIED | None | No response state verified in T1 |
| T12 Application | Simra + Muzzammil | TODO / UNVERIFIED | None | Outside T1 |
| T13 Demo/screenshots | Both | TODO | None | No application/demo exists |
| T14 Red-team | Both | TODO | None | Depends on integrated candidate |
| T15 Submission | Both | TODO | None | Depends on prior gates |

## 4. Frozen decisions

- Product thesis: characterize navigation-controller capability boundaries and mission-liveness failures; do not crown a controller winner or imply assurance not supported by evidence.
- Hero demo family: C4 structured-static.
- Deterministic reference: A*.
- Research-derived C4/C5 failure protocol: `c4_c5_recurrence_v1`.
- Exact recurrence detector implementation belongs to T5, not T1.
- Failure precedence: `success -> collision -> two_cell_loop -> longer_loop -> timeout_other`.
- Two-cell recurrence has the authoritative `len(trajectory) >= 4` guard. Assuming neither success nor collision, `[A, B, A]` is `longer_loop`, while `[A, B, A, B]` is `two_cell_loop`.
- Invalid actions remain separate diagnostics.
- Evidence labels must expose the underlying raw counts; no opaque safety score.

## 5. Current blockers

1. No verified PPO checkpoint identity or availability was established in T1.
2. No scenario, evaluator, detector, A* reference, report, or dashboard exists yet.

## 6. Latest verification

- Install command: `python -m pip install -e ".[dev]"` in an isolated `.venv`.
- Tests: T1 contract tests pass with `python -m pytest`.
- Real PPO checkpoint status: unknown and unverified.
- End-to-end run status: not implemented or verified.
- Dashboard status: not implemented.
- Report status: not implemented.

## 7. Application / outreach / demo

- DEFTECH fields captured: unverified in T1.
- Application draft status: unverified in T1.
- Foxtrot response: unverified in T1.
- Swift response: unverified in T1.
- Demo recording status: not started.
- Screenshots status: not started.
- Current application/demo status: no application or executable demo is present in this repository.

## 8. Next actions

### Muzzammil

1. Begin T2a on `feat/assurance-core` and record the verified checkpoint result without inventing provenance.
2. Continue only the assurance-lane tickets after their dependencies pass.

### Simra

1. Begin T4 on `feat/product-dashboard` against the frozen T1 contracts.
2. Keep synthetic fixture output clearly separated from current measurements and research evidence.

## 9. Next integration gate

One real controller/scenario evaluation must produce the shared EvaluationResult contract and feed the report/dashboard path, with relevant tests passing, provenance and limitations visible, and no unsupported scientific or deployment claims.
