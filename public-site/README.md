# MEHWAR public website V3

MEHWAR’s public evidence experience uses Next.js, React and TypeScript to publish a static website. The evolving homepage is the **Latest Validated Build** presentation; `/deftech-2026` preserves the September 2026 submission record. The permanent Vercel project is **`mehwar-deftech`**, at [mehwar-deftech.vercel.app](https://mehwar-deftech.vercel.app/).

V3 starts from accepted V2 branch `codex/mehwar-web-v2`, commit `81bf5d15d696759f7d98e0cd4dba3ef7cb7769ea`, on successor branch `codex/mehwar-web-v3`. All implementation changes belong inside `public-site/`. The frozen scientific MVP remains `feat/integration-demo` at `1586eebf9daa8a8e690bc6f62cc377ce540214ee`. Do not change `main`, scientific source, evaluator, controller/checkpoint, scenarios, research repositories or frozen tests for website work.

V2 was successfully deployed to the existing production URL, including the historical route. [HANDOFF.md](HANDOFF.md) records V3’s own verification and deployment state; a source branch does not establish a deployment.

## Develop and verify

Use Node.js 20.9 or newer and the committed lockfile. From `public-site/`:

```powershell
npm ci
npm run lint
npm run typecheck
npm run build
npm run check:static
git diff --check
```

`npm run build` first runs the three presentation-integrity scripts in `npm test`, then generates `out/`. These protect selected evidence, historical files and playback indexing; they do not execute scientific evaluation. Run `npm run check:static` after every release build to check the generated output.

For development, use `npm run dev`. `npm run preview` serves the exact static export on local port 4175. A separate port can be passed for concurrent work:

```powershell
node scripts/preview.mjs 4181
```

The preview supports clean routes and gzip for text assets. Adding `?nojs=1` applies a local-only script-blocking content security policy. This is QA tooling, not a production backend.

## Design and architecture

Three directions were explored: **Trajectory Theatre**, **Technical Editorial**, and **Assurance Instrument**. V3 combines a dark opening built around the real C4-0001 recording, an inspectable evidence instrument, and a warm editorial explanation. Actual trajectory geometry leads the visual identity. The conceptual boundary section explicitly separates observed evidence from capabilities not established.

Space Grotesk provides homepage display typography, Manrope carries reading text and IBM Plex Mono carries technical notation. Framework-optimized font files are served from the site. Deep navy, warm paper, steel-blue paths, amber recurrence and restrained teal completion form the semantic palette. Labels, shapes and line styles reinforce color. No stock imagery, invented telemetry or fabricated scientific geometry is needed.

| Source | Responsibility |
| --- | --- |
| `app/page.tsx` | Composes V3 and scopes its display font |
| `app/globals.css` | Shared reset, base typography, focus and reduced-motion defaults |
| `app/v3.css` | Scoped V3 header, hero, instrument, controls and responsive styles |
| `components/EvidenceExperience.tsx` | Scenario selection, static fallback, final evidence, technical disclosure and native image dialog |
| `components/RecordedInstrument.tsx` | Isolated playback/reference state, visibility-aware arrival replay, reduced-motion handling and transport |
| `components/RecordedTrajectory.tsx` and `recorded-trajectory.css` | Exact SVG projection and presentation annotations |
| `content/playback.mjs` | Immutable annotation landmarks and bounded integer cursor; no classifier |
| `components/Narrative.tsx` and `narrative.css` | Thesis, research/workflow, boundaries, provenance, roadmap, team and collaboration |
| `components/SiteHeader.tsx` | Navigation and native mobile disclosure with Escape focus restoration |
| `components/CopyHash.tsx` | Clipboard enhancement and independent full-hash disclosure |
| `content/evidence.ts` | Typed presentation model for the immutable public export |
| `content/site.ts` | Approved founder contacts, workflow, roadmap and historical implementation verification |
| `content/submission-2026.json` and `app/deftech-2026/` | Independent historical submission data, route and stylesheet |
| `public/evidence/` | Downloadable allowlisted evidence and source lineage |
| `scripts/generate-og.mjs` | Trajectory-derived OpenGraph artwork generation |

The default final C4-0001 trace and facts are rendered into static HTML. After hydration, arrival playback begins once the instrument is at least 75% visible and motion is permitted, then settles at the final recorded position. Hiding the document or leaving the viewport pauses playback; re-entry does not restart it. Frequent step updates remain isolated from editorial and final-evidence content. Scenario selection loads the chosen run’s final state. Play/pause/replay, step controls and a scrubber change the displayed position; recorded final-run outcome and diagnostics remain unchanged.

Coordinates are `[row, col]`, projected as `x = col`, `y = row`, with rows increasing downward. Step zero is the initial position: C4-0001 has 29 positions for 28 moves; C4-0000 has 17 positions for 16 moves. Each frame shows an exact prefix with straight recorded segments. Timing is illustrative, not recorded wall-clock time. There is no smoothing, invented coordinate, speed measurement or outcome recomputation.

The fixed C4-0001 recurrence cells `(14, 1)` and `(13, 0)` occur at steps 15 and 16; the first revisit is step 17. Its annotation appears at that revisit. This is checked presentation metadata, not a second recurrence classifier. The optional complete A* path is static task-feasibility context, not simultaneous playback.

Reduced-motion preference selects a meaningful final state. Without JavaScript, the default trace and facts remain readable, disclosures/contact links work, and a secondary C4-0000 summary links to both historical records. This fallback is visible in static HTML and hidden only after enhancement, so it also survives blocked or failed scripts. Playback and scenario switching require JavaScript and remain disabled until enhanced. Full-resolution screenshot links work independently of the dialog.

## Evidence and historical integrity

The authoritative records are existing frozen outputs:

- `outputs/final-submission-selected-demo/C4-0000.json`
- `outputs/final-submission-selected-demo/C4-0001.json`
- `outputs/final-submission-selected-demo/manifest.json`

Geometry was checked against `src/mehwar/scenarios/c4.py`; the C4-0001 trajectory was checked against `tests/test_real_seed33.py` and the oracle hash in `src/mehwar/selected_demo.py`. `src/mehwar/dashboard/visualization.py` establishes the coordinate convention. No trajectory was reconstructed from screenshots. [The evidence lineage record](public/evidence/README.md) contains source/screenshot digests and the exact movement contract.

| Record | Mission / outcome | Controller steps / invalid actions | Exact controller cost | A* steps / exact cost |
| --- | --- | --- | --- | --- |
| C4-0001 | Not completed / `two_cell_loop` | 28 / 0 | `37.112698372208094` | 14 / `16.071067811865476` |
| C4-0000 | Completed / `success` | 16 / 0 | `17.242640687119284` | 15 / `16.65685424949238` |

`public/evidence/selected-runs.json` has SHA256 `d16c0c39fdf0322b4ad06da3ab27c08aa07f10cc4de2989f955cee762719ea5e`. The site’s `.gitattributes` preserves its exact bytes. Do not reformat it or alter the expected checksum to conceal a change.

`check-evidence.mjs` checks the export checksum, selected facts, geometry, provenance and sanitization. `check-playback.mjs` checks immutable annotations, exact index landmarks and cursor bounds. `check-snapshot.mjs` pins five historical files: submission data, route source, route stylesheet and both original screenshot byte streams; only historical source text line endings are normalized. New scientific evidence requires a separately identified record, not an in-place rewrite of submission truth.

With original ignored outputs available, an additional read-only comparison can be run:

```powershell
node scripts/check-snapshot.mjs --evidence-dir <frozen-export-directory>
```

The original PNGs remain unedited final T13 artifacts at 1920 × 1065. “137 tests passed, 0 skipped, Ruff PASS, git diff --check PASS” is recorded submission implementation verification. It was not rerun as science for V3 and is not a safety score.

Both selected records remain `development_validation`, with `fresh_holdout: false`, in a controlled 2-D grid-based mission-routing abstraction. The browser consumes `c4_c5_recurrence_v1` outcomes and keeps invalid actions separate. A* remains the **deterministic A* reliability reference under the shared grid contract**. No success percentage, controller ranking, generic superiority, physical validation, certification, deployment readiness, external validation or safety guarantee follows from two selected cases.

## Contacts and optional configuration

`content/site.ts` contains the approved equal co-founder roles, full institutional credentials and explicit public recipients:

- Muzzammil Sajid — Research & Assurance: `muzzammilsajid1@gmail.com`.
- Simra Imran — Product & Integration: `simraimran158@gmail.com`.

These are authorized contacts, not missing configuration. V3 uses recipient-specific `mailto:` links and does not send messages itself. Legacy empty `siteConfig.publicEmail` is not the V3 contact source.

Keep `canonicalUrl` set to `https://mehwar-deftech.vercel.app`. Optional archive/demo fields remain empty; the site is complete without those media. Do not assume entering a URL adds a rendered integration: implement and verify its UI before exposure. A future video requires captions and transcript together. Do not invent credentials, contact details, relationships or visible placeholders.

## Deployment and release QA

Publish only validated `out/` and `vercel.json` to existing project **`mehwar-deftech`**. Never deploy the Python root, scientific binaries or local QA artifacts. Do not create a substitute project or hostname. Inspect existing project settings before generic source deployment; a Git push alone does not establish publication.

`node scripts/deployment-payload.mjs` prints a JSON payload containing base64-encoded export files and the clean-URL routing configuration. It does not authenticate or deploy. The authenticated Vercel API/CLI can publish it after resolving the existing project and owning team. Keep credentials out of source, payload metadata and delivered output. Record the final source SHA and returned deployment ID in [HANDOFF.md](HANDOFF.md).

Before release, inspect widths 1920, 1440, 1366, 1280, 1024, 820, 768, 430, 412, 390, 375 and 360; 1728 is optional. Exercise both scenarios, playback endpoints, pause/replay, scrubber, first recurrence, reference overlay, disclosure, original-image dialog/Escape, copy fallback, mobile menu, keyboard, reduced motion and no-JavaScript behavior. Check overflow, narrative rhythm, roadmap, team/contact and the historical route.

After publishing, verify the permanent homepage and `/deftech-2026` return HTTP 200 without authentication and serve distinct intended content. Recheck live interactions, console, PNG/JSON artifacts, metadata, OpenGraph, favicon and desktop/mobile layout. Representative mobile Lighthouse targets are performance 90+ and accessibility, best practices and SEO 95+. Distinguish lab results from field Core Web Vitals; do not claim field INP without data.

The architecture has no accounts, database, uploads, inference, simulator, fake API or telemetry feed. Scan source and built output for secrets, private paths, checkpoint locations and unrelated personal data while allowing approved founder contacts and deliberate public provenance. Build success alone does not establish production accessibility.
