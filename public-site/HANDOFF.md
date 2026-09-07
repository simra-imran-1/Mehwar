# MEHWAR WEB V2 handoff

## STATUS

`PASS WITH MANUAL ITEMS`

The V2 implementation and local quality gates are complete. Publishing is blocked by Vercel project permissions: the authenticated connector rejected the production deployment with HTTP 403. V2 has not been deployed; the existing live homepage is unchanged.

## SOURCE STATE

- Website branch: `codex/mehwar-web-v2`.
- Starting point: latest fetched `origin/feat/public-site`, `49ab7591129e4e9b9bc0ba3b39c6e02c7850b03c`.
- Final website SHA: **pending final commit**.
- Frozen MVP branch: `feat/integration-demo`.
- Frozen MVP SHA: `1586eebf9daa8a8e690bc6f62cc377ce540214ee`.
- Scope: all website changes are inside `public-site/` in a separate worktree. The original frozen checkout and `main` remain unchanged. No scientific source, evaluator, controller, checkpoint, scenario, research repository or frozen test was modified.

## PRODUCTION

- Permanent homepage: [https://mehwar-deftech.vercel.app/](https://mehwar-deftech.vercel.app/).
- Historical route: [https://mehwar-deftech.vercel.app/deftech-2026](https://mehwar-deftech.vercel.app/deftech-2026).
- Existing Vercel project: `mehwar-deftech`.
- V2 public accessibility: **not deployed**. The existing live alias continues to serve V1. `/deftech-2026` is built and locally verified but has not been published. No successful V2 deployment ID was returned.
- The old V1 deployment was inspected before redesign. The connector was given the existing project name and team identity, target `production`, and 56 files totaling 1,638,923 bytes. It returned HTTP 403: “You don't have permission to create a Production Deployment for this project.” The local CLI has no authenticated credentials. An authorized project member must deploy the prepared export to the same project after authentication. No replacement project or hostname was created.

## DESIGN DIRECTION

An editorial hero leads into an engineering evidence instrument. Actual C4-0001 geometry, paths and recurrence cells drive the visual identity, supported by Manrope, restrained technical mono, a warm paper canvas, deep navy text and amber recurrence emphasis. Pure instrument, pure editorial and hybrid directions were considered; the hybrid best balances a fast understanding of the liveness blind spot with precise evidence inspection. The audit prioritized preserving submission history, replacing screenshot-led storytelling, improving hierarchy and reducing repetitive boxed sections. Additional decorative effects and feature expansion were intentionally omitted.

## MAJOR CHANGES

- **Hero:** the exact legality/liveness thesis, immediate selected-case context and native trajectory evidence; the mobile layout puts the key failure observation before the diagram.
- **Evidence explorer:** default C4-0001 and selectable C4-0000, native keyboard-operable radios, separate invalid-action diagnostics, rounded reading values and full-precision technical disclosures.
- **Trajectory:** original grid, blocked cells, start/goal and complete controller/A* paths. The recurrence region is explicitly annotated; color is reinforced by labels, line styles and shapes. A one-pass trace settles after a short recurrence pulse; reduced-motion CSS supplies the static state.
- **Workflow:** seven connected stages from verified controller adapter to dashboard/report, with a vertical mobile composition.
- **Boundaries:** observed evidence and unestablished capabilities are prominent. The selected development-validation and controlled 2-D abstraction caveats remain explicit.
- **Provenance:** full-hash disclosures, copy feedback, downloadable sanitized JSON, exact source lineage and original full-resolution screenshots.
- **Historical snapshot:** `/deftech-2026` has separate submission data and route content, preserving September 2026 evidence, scope, limitations, team and screenshots. Integrity checks pin five historical files.
- **Roadmap:** seven validation questions from technical-user discovery through a prospective pilot specification; future work is not presented as existing capability.
- **Team/contact:** equal co-founder roles and approved affiliations; graceful absent-email behavior with a working internal snapshot link.
- **Responsive/accessibility:** sticky compact navigation, Escape-to-close mobile menu with focus restoration, semantic landmarks, visible focus, textual trajectory equivalents and native disclosures. Core evidence selection remains usable without JavaScript.
- **Metadata/performance:** static export, self-hosted optimized fonts, custom trajectory-derived 1200 × 630 OpenGraph artwork, favicon, canonical URL, Twitter card, robots and sitemap. No new runtime library, backend, tracker or analytics integration.

## AUTHORITATIVE EVIDENCE USED

| Evidence | Exact source |
| --- | --- |
| C4-0000 result and both trajectories | `outputs/final-submission-selected-demo/C4-0000.json` in the frozen source checkout |
| C4-0001 result and both trajectories | `outputs/final-submission-selected-demo/C4-0001.json` in the frozen source checkout |
| Source/checkpoint/protocol provenance | `outputs/final-submission-selected-demo/manifest.json` |
| Scenario geometry | `src/mehwar/scenarios/c4.py` at the frozen MVP SHA |
| Independent C4-0001 trajectory oracle | `tests/test_real_seed33.py` and the pinned trace hash in `src/mehwar/selected_demo.py` at the frozen MVP SHA |
| Coordinate convention | `src/mehwar/dashboard/visualization.py` at the frozen MVP SHA |
| Original evaluator screenshots | Final T13 `outputs/t13-micro-screenshots/C4-0000-hero.png` and `C4-0001-hero.png`, retained as `public/c4-0000-success.png` and `public/c4-0001-liveness-degradation.png` |
| Submission verification statement | Approved submission specification and existing public-site provenance record; not a new scientific test run |

The ignored original evaluation outputs were read directly. No trajectory was reconstructed from a screenshot. The public allowlisted export is `public/evidence/selected-runs.json`, SHA256 `d16c0c39fdf0322b4ad06da3ab27c08aa07f10cc4de2989f955cee762719ea5e`. Source digests, screenshot digests and detailed lineage are in [public/evidence/README.md](public/evidence/README.md).

| Selected record | Mission / classification | Controller steps / invalid actions | Exact controller cost | A* steps / exact cost |
| --- | --- | --- | --- | --- |
| C4-0001 | Not completed / `two_cell_loop` | 28 / 0 | `37.112698372208094` | 14 / `16.071067811865476` |
| C4-0000 | Completed / `success` | 16 / 0 | `17.242640687119284` | 15 / `16.65685424949238` |

## TESTS / CHECKS

- Dependency installation: PASS using `npm ci` and the existing lockfile.
- `npm run lint`: PASS.
- `npm run typecheck`: PASS.
- `npm run build`: PASS; includes both integrity tests and static export of `/`, `/deftech-2026`, robots and sitemap.
- `git diff --check`: PASS.
- `npm test`: PASS for the allowlisted evidence checksum/facts and five fixed historical files. Optional snapshot comparison against the authoritative frozen exports also passed.
- `npm run check:static`: PASS for all 55 exported files and 113 local links/assets/fragments, unique IDs, accessible references, static claim text and metadata on both routes, missing optional configuration, privacy signatures and byte-identical delivered evidence.
- Homepage layout checks: 1920 × 1080, 1440 × 900, 1280 × 800, 1024, 768, 430, 390 and 360 widths; no document horizontal overflow. Hero screenshots were visually inspected at 1920, 1440, 390 and 360.
- Snapshot: all eight widths checked without horizontal overflow; anchors correct, console clean, both original screenshots loaded and their links opened.
- Interaction: scenario selection and native arrow-key switching update the correct record; mobile menu Escape closes and returns focus; exact technical values expand; copy feedback appears. Full-hash text is independently available through native disclosure.
- Degradation: scripts blocked by the preview’s `?nojs=1` policy; native scenario controls were exercised and correctly switched panels. Core text and the full-hash fallback remain present.
- Accessibility: local Lighthouse 100; keyboard/disclosure checks and contrast review completed. Blocked-cell contrast and the success SVG description were corrected during red-team review. Reduced-motion rules are implemented and source-reviewed. No claim of a complete assistive-technology certification is made.
- Performance: compressed local static-export Lighthouse mobile score **93 performance / 100 accessibility / 100 best practices / 100 SEO**. FCP 1.3 s, LCP 2.8 s, CLS 0, TBT 180 ms. This local lab result is below the aspirational performance target of 95; it is not production field data. Production V2 measurement is unavailable because the deployment was rejected.
- Scientific red-team: selected record values, geometry, provenance, neutral reference framing and limitations cross-checked. A React SVG-title hydration issue found in browser QA was corrected; the fresh static build has no reported console errors.

## SCIENTIFIC CLAIM AUDIT

- A* remains the **deterministic A* reliability reference under the shared grid contract**. It supplies reference context; there is no winner, controller ranking or generic superiority claim.
- No flight validation, deployment readiness, safety certification, collision-safety guarantee, OEM validation, external-stack/HIL validation or invented partner/customer claim is made.
- Invalid actions remain a separate diagnostic from mission outcome. C4-0000 is labeled only `NO FAILURE OBSERVED IN SELECTED DEMO RUN`.
- Evidence remains selected `development_validation`, `fresh_holdout: false`, in a controlled 2-D grid-based mission-routing abstraction. It is not a representative benchmark or physically sealed holdout study.
- `c4_c5_recurrence_v1` classifications are consumed from frozen records. The browser does not classify trajectories, run controllers or generate new scientific results.
- The 137 passed / 0 skipped / Ruff PASS / diff-check PASS statement is explicitly recorded submission implementation verification, not a reliability rate or safety score.

## PRIVACY / SECURITY

Website source content and local build artifacts were reviewed for machine paths, credential signatures, private personal data and checkpoint filenames. The public export omits checkpoint filename, binary and local runtime location. Only the checkpoint hash is published as provenance. Original screenshots were retained and visually reviewed. The rejected deployment package contained only `out/` and the static routing configuration; it excludes Python source, local QA artifacts and scientific binaries. No tracking service or external contact address was added.

## CONFIG STILL NEEDED

- Approved public email: `siteConfig.publicEmail` is empty.
- Optional approved evidence archive URL: `siteConfig.evidenceArchiveUrl` is empty; the internal historical route already works.
- Optional approved narrated demo: `demoVideo`, `demoCaptions` and `demoTranscript` are empty; the section is omitted until all three are supplied.

## REMAINING LIMITATIONS

The product evidence is limited to two selected development-validation cases under the frozen grid contract. External-stack utility, higher-fidelity relevance, controlled lab/HIL work and prospective pilot design remain validation questions. Website checks do not expand those scientific boundaries.

Production publishing is blocked by the authenticated account's project permissions; unauthenticated V2 verification can only follow a successful deployment. The public contact channel is absent by design until approved. Local Lighthouse performance is 93, with no production Core Web Vitals field data. Browser QA and automated accessibility checks do not replace a full screen-reader and assistive-device audit.

## FINAL RECOMMENDATION

`PUBLICLY READY` — the validated local export is ready for an authorized project member to publish to the existing `mehwar-deftech` project. This recommendation concerns the prepared website, not the current live deployment. Run the production checks in README after permission is restored and publishing succeeds.
