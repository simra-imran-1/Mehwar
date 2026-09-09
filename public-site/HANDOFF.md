# MEHWAR WEB V3 handoff

Release review: 9 September 2026. The public frontend is deployed; this document distinguishes website QA from frozen scientific evidence.

## STATUS

**MEHWAR WEB V3 — EXCEPTIONAL FRONTEND PASS**

The existing production URL serves V3. Scientific integrity, historical preservation, functional QA and public access pass. Mobile Lighthouse performance is 88, two points below the aspirational 90 target; this measured limitation is retained below.

## SOURCE

- Starting branch: `codex/mehwar-web-v2`.
- Accepted starting SHA: `81bf5d15d696759f7d98e0cd4dba3ef7cb7769ea`.
- Final branch: `codex/mehwar-web-v3`, pushed to origin.
- Deployed implementation SHA: `68f30ab9be542a29e6237138c8935e9a14dd60fa`.
- This subsequent handoff-only commit records deployment and QA; it does not change the deployed export. `git rev-parse HEAD` identifies the final documentation revision.
- Latest fetched `origin/feat/public-site`: `49ab7591129e4e9b9bc0ba3b39c6e02c7850b03c`.
- Frozen MVP: `feat/integration-demo`, `1586eebf9daa8a8e690bc6f62cc377ce540214ee`; original checkout remains clean.
- `main` remains `4ff04898d34e6791f872ecf08eb36b47f47fe72f`.
- Every committed change is within `public-site/`. No scientific source, evaluator, controller/checkpoint, scenario, research repository or frozen test was modified or executed for V3.

## DESIGN DIRECTION

**Trajectory Theatre → Assurance Instrument → Technical Editorial.** Three directions were explored: a recorded-trajectory opening, a typography-led editorial page, and a dense engineering instrument. The selected direction lets the C4-0001 observation lead, provides exact inspection, then explains the research, product and evidence boundaries.

Grid topology, recorded segments, recurrence and provenance supply the identity. Space Grotesk supplies display type, Manrope reading text and IBM Plex Mono technical notation. Deep navy and warm paper establish section rhythm; blue identifies the controller trace, amber recurrence and teal selected completion. Labels, shapes and line styles reinforce color.

A finite replay begins only when the instrument is mostly visible. It reveals recorded positions with illustrative timing, never synthesized coordinates. The useful final trace remains visible before playback and under reduced motion.

## WHAT CHANGED

- **Hero and trajectory:** a dark opening built around “Every move legal. Mission unfinished.” and the real controlled trace, with a separated final-run zero-invalid-action observation.
- **Evidence explorer:** one instrument, integer scrubber, previous/next, pause/replay, first-recurrence inspection, two scenario radios and an optional complete deterministic reference layer.
- **Evidence depth:** exact costs, diagnostics, contract, protocol, coordinates and hashes in native disclosures; an original-image dialog, independent full-resolution links and frozen JSON download.
- **Workflow:** research origin and seven connected native disclosures explain the controller-to-evidence workflow.
- **Boundaries and provenance:** observed/not-established composition, inspectable source identity, copy fallback and explicitly recorded submission implementation verification.
- **Roadmap:** seven validation questions, with external integration and higher-fidelity work presented as future investigation.
- **Team/contact:** equal co-founder treatment, approved full institutional credentials and recipient-specific public email actions.
- **Snapshot:** independent historical route/data/style and original screenshots retain their fixed digests. Current founder-contact expansion does not enter the snapshot.
- **Responsive:** phone hierarchy brings the plot forward, tablet controls remain usable, the header is opaque, anchor offsets avoid duplication, and legend/status space stays stable.
- **Metadata/footer:** V3 trajectory-derived OpenGraph art, canonical URL, favicon, robots/sitemap, page-specific theme color and permanent historical navigation.
- **Cleanup:** obsolete V2 explorer/trajectory components removed; the historical route used neither.

## ADVANCED FRONTEND TECHNIQUES USED

- Exact data-driven SVG projection and integer-index trajectory-prefix playback.
- Isolated high-frequency state in a keyed instrument; memoized fixed technical evidence.
- IntersectionObserver-triggered finite arrival replay, document/viewport pause and reduced-motion handling.
- Reference layering and fixed recurrence landmarks without scientific recomputation.
- Native range/radio controls, progressive enhancement, disclosures and modal focus behavior.
- Static fallback visible until enhancement succeeds, including blocked/failed-script cases.
- Scoped responsive CSS, fluid typography, semantic color transitions, self-hosted optimized fonts and static export.

No Canvas/WebGL, motion library, live simulation, product backend or fabricated telemetry is claimed.

## AUTHORITATIVE DATA SOURCES

| Evidence | Exact source |
| --- | --- |
| Selected recorded results and trajectories | `outputs/final-submission-selected-demo/C4-0000.json` and `C4-0001.json` in the frozen MVP checkout |
| Frozen source/checkpoint/protocol lineage | `outputs/final-submission-selected-demo/manifest.json` |
| Grid, obstacles, start and goal | `src/mehwar/scenarios/c4.py` at the frozen MVP SHA |
| C4-0001 trajectory oracle and digest | `tests/test_real_seed33.py` and `src/mehwar/selected_demo.py` at the frozen MVP SHA |
| Row/column display convention | `src/mehwar/dashboard/visualization.py` at the frozen MVP SHA |
| Original screenshots | `outputs/t13-micro-screenshots/C4-0000-hero.png` and `C4-0001-hero.png` in the separate `codex-workers/t13-ui-polish` checkout, also at the frozen MVP SHA; both hashes rechecked against public PNGs |
| Browser evidence input | `public/evidence/selected-runs.json`; lineage and source digests in `public/evidence/README.md` |

Public JSON SHA256: `d16c0c39fdf0322b4ad06da3ab27c08aa07f10cc4de2989f955cee762719ea5e`. Its exact bytes remain unchanged; `.gitattributes` prevents line-ending conversion. Coordinates and facts were not reconstructed from screenshots.

| Record | Mission / classification | Controller steps / invalid actions | Exact controller cost | A* steps / exact cost |
| --- | --- | --- | --- | --- |
| C4-0001 | Not completed / `two_cell_loop` | 28 / 0 | `37.112698372208094` | 14 / `16.071067811865476` |
| C4-0000 | Completed / `success` | 16 / 0 | `17.242640687119284` | 15 / `16.65685424949238` |

## SCIENTIFIC AUDIT

**PASS.** The independent source/evidence review and release guards confirm:

- “Legal action selection does not by itself guarantee mission liveness.”
- “The point is not that one algorithm wins. The point is that legality alone did not expose the failure.”
- A* remains the **deterministic A* reliability reference under the shared grid contract**; no rankings or generic superiority claims.
- Both cases retain their exact results, costs, classifications and zero-invalid-action diagnostics. C4-0000 retains `NO FAILURE OBSERVED IN SELECTED DEMO RUN`.
- Both remain selected `development_validation`, `fresh_holdout: false`, in a controlled 2-D grid-based mission-routing abstraction. No representative success rate follows from two cases.
- `c4_c5_recurrence_v1` outcomes are consumed from frozen records. Playback does not classify prefixes, evaluate legality, calculate path costs or regenerate results.
- Coordinates remain `[row, col]`, with rows increasing downward; step zero is the initial position. C4-0001 recurrence annotation appears at its fixed first revisit, step 17.
- Final-run outcomes and diagnostics stay fixed independently of the presentation cursor. Invalid actions remain separate diagnostics.
- 137 passed / 0 skipped / Ruff PASS / diff-check PASS is recorded submission verification, not fresh V3 science, a safety score or certification.
- No physical/flight validation, deployment readiness, certification, collision-safety guarantee, external-stack/HIL/OEM validation, invented customers/partners, generic robustness or product-market validation is asserted.
- MEHWAR remains assurance/evaluation, not a new navigation algorithm, planner/simulator replacement or planner-versus-PPO benchmark.

## DESIGN QA

**PASS** across widths 1920, 1728, 1440, 1366, 1280, 1024, 820, 768, 430, 412, 390, 375 and 360. Document/visible-element overflow checks and desktop/mobile visual inspection found no clipping or crowding blocker. Browser-emulated widths are not physical-device certification.

Both selected cases, step endpoints, exact recurrence timing, reference overlay, technical disclosures, screenshot dialog, keyboard controls, visible focus and clipboard-denial fallback were exercised. Reduced-motion initial load and preference changes retain correct final states. True scripting-disabled Chrome and CSP script blocking both preserve readable evidence and contacts. Dialog pointer activation, close focus, Escape and trigger focus restoration were verified.

Self-review covered the hero screenshot, evidence insight, engineer-facing depth, scientific claims, narrative rhythm, equal founders and footer. This was agent/browser review, not an external customer or jury study. Production visual review confirmed the same custom evidence-led composition; no additional production-only design defect required another deployment.

Local evidence: `qa/v3-design-review.md`, `qa/browser-audit-summary.md`, desktop/mobile screenshots and raw interaction results. QA artifacts are ignored and excluded from deployment.

## TECHNICAL QA

| Check | Result |
| --- | --- |
| Locked dependency installation | `npm ci` PASS; no lockfile/dependency expansion |
| Full lint / TypeScript | PASS; zero lint errors or warnings |
| Evidence, snapshot and playback guards | PASS |
| Read-only comparison with original frozen exports | PASS |
| Production build / static export | PASS; Next.js 16.3.4, Node.js 20.20.2 |
| Exported-site check | PASS: 59 files, 116 local links/assets/fragments, IDs/ARIA, exact facts, fallback, contacts, metadata, privacy and immutable artifacts |
| Working/staged diff checks | PASS |
| Normal browser runtime errors | None observed |
| Mobile Lighthouse | **88 performance / 100 accessibility / 100 best practices / 100 SEO** |
| Lab metrics | LCP 2.9 s; CLS 0; TBT 330 ms; FCP 1.1 s; speed index 2.3 s |
| Initial transfer in audit | 244,169 bytes total; 149,924 bytes scripts; 0 image-transfer bytes (SVG is inline; original PNGs load on inspection) |
| Field Core Web Vitals / INP | Not established; no field data claimed |

The final isolated local mobile audit was measured at `2026-09-09T06:54:26.235Z`. Isolating playback and avoiding offscreen work improved performance from 77 and TBT 640 ms to 88 and TBT 330 ms. Remaining framework startup cost keeps the score below the aspirational 90 target; no visual or scientific content was removed to chase a score. Full reports: `qa/lighthouse-mobile.json` and `qa/lighthouse-summary.json`.

## SECURITY

**PASS.** Source and exported-output scans found no secrets, private home/checkpoint paths, binary checkpoint assets, unrelated personal data or preview URLs in delivered output. The two founder emails are expressly approved public contacts; source and checkpoint hashes are deliberate provenance.

Only the validated export plus `vercel.json` was uploaded: 60 packaged files, 1,587,735 bytes. No local QA, auth material, Python source, scientific outputs outside the allowlist, dependencies or masterprompt was packaged. The application has no accounts, database, uploads, inference, runtime evaluator, fake API or telemetry feed.

## PRODUCTION

- Homepage: [https://mehwar-deftech.vercel.app/](https://mehwar-deftech.vercel.app/).
- Historical snapshot: [https://mehwar-deftech.vercel.app/deftech-2026](https://mehwar-deftech.vercel.app/deftech-2026).
- Existing Vercel project: `mehwar-deftech`, ID `prj_CxbE3TAkDg3W4WT2pa1Aoa1UEnxA`.
- Owning team: `team_ZwATULjpU8bNF0Ex3vcgSNyd`.
- Deployment: `dpl_4mhF8jKJCHnUourY1TGJ4Wuyi9uJ`.
- State: **READY**, permanent alias assigned; deployed implementation SHA `68f30ab9be542a29e6237138c8935e9a14dd60fa`.
- Both permanent routes return unauthenticated HTTP 200 and their distinct intended content.
- All 59 exported files passed live verification: 58 exact byte matches; one JavaScript file has only Vercel's standard opt-in toolbar suffix, with the complete exported code preserved as its exact prefix. No evidence file differs.
- Live canonical metadata, OpenGraph, favicon, CSS/fonts/scripts, frozen JSON, historical HTML and original PNGs were included in verification.
- Live pointer review confirmed first recurrence at 17, the full 15-position reference layer, C4-0000 at 16, its original image dialog, Escape and 390 px layout without overflow.
- Independent live browser verification is recorded in `qa/production-browser-summary.md`; byte and route results are in `qa/production-verification.json`.

No replacement project or public URL was created.

## MANUAL ITEMS

None required for public use. Optional archive/video, custom domain, analytics or social links are not release requirements. Approved founder contacts are implemented. Future performance work may reduce the remaining framework startup cost; the measured 88 score is disclosed rather than represented as 90+.

## FINAL SELF-RATING

| Dimension | Score / 10 |
| --- | --- |
| Visual impact | 9 |
| Memorability | 9 |
| Evidence clarity | 9.5 |
| Technical credibility | 9.5 |
| Responsive quality | 9 |
| Accessibility | 9 |
| Performance | 8.5 |

Performance is below 9 because the representative mobile audit remains 88 with LCP 2.9 s and TBT 330 ms. Accessibility reflects automated and keyboard/motion/fallback checks, not exhaustive assistive-device certification.

## FINAL RECOMMENDATION

**PUBLICLY READY**