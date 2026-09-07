# MEHWAR public website V2

MEHWAR’s public evidence presentation, built with Next.js, React and TypeScript as a static export. The homepage is the **Latest Validated Build** presentation; `/deftech-2026` preserves the September 2026 submission record. The permanent production project is `mehwar-deftech`, at [mehwar-deftech.vercel.app](https://mehwar-deftech.vercel.app/).

Website work is isolated to `public-site/` on `codex/mehwar-web-v2`, based on the latest fetched `feat/public-site` commit, `49ab7591129e4e9b9bc0ba3b39c6e02c7850b03c`. The frozen MVP is `feat/integration-demo` at `1586eebf9daa8a8e690bc6f62cc377ce540214ee`. Website verification does not execute or change the scientific evaluator, controller, scenarios, checkpoint or frozen tests.

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

`npm run build` first runs the two evidence-integrity checks in `npm test`, then produces `out/`. The post-build static check resolves local links, assets and fragments, validates accessible references and required statically readable claims, checks both routes and optional configuration, and searches delivered text for sensitive-data signatures. These are website presentation checks, not new scientific results.

For a development server, run `npm run dev`. To inspect the exact production export:

```powershell
npm run preview
```

The local preview serves `out/` at `http://127.0.0.1:4175`, with clean route resolution and gzip for text assets. `/?nojs=1` blocks scripts through a local-only content security policy for degradation checks. The preview server is QA tooling, not a deployment backend.

## Design and architecture

The chosen direction combines an editorial hero with an engineering evidence instrument. Warm paper, deep navy, steel-blue controller paths and restrained amber recurrence markers give the actual C4-0001 evidence priority. Manrope carries headings and reading text; IBM Plex Mono is reserved for technical identifiers. Next’s optimized font build serves the font assets from the site itself.

The audit identified submission-history preservation as a prerequisite, followed by the screenshot-led hero, repetitive boxed sections and shallow evidence inspection as the highest-value redesign opportunities. Three directions were considered: a pure evidence instrument, an editorial assurance story, and their hybrid. The hybrid best supports both a quick technical reading and detailed inspection. Extra feature count, generic drone imagery, artificial telemetry, heavy 3-D and continuous animation were excluded.

Key source responsibilities:

| Source | Responsibility |
| --- | --- |
| `app/page.tsx` | Homepage narrative, workflow, boundaries, provenance, roadmap, team and collaboration |
| `app/globals.css` | Typography, layout, native scenario selection, responsive behavior and reduced-motion rules |
| `components/TrajectoryVisual.tsx` | SVG rendering of supplied grid geometry and trajectories; no evaluator logic |
| `components/EvidenceExplorer.tsx` | Native radio selector, both static scenario records, exact-value disclosures and original-image links |
| `components/SiteHeader.tsx` | Sticky navigation and compact native mobile disclosure; Escape returns focus to its summary |
| `components/CopyHash.tsx` | Copy feedback and a native full-hash disclosure as the manual fallback |
| `content/evidence.ts` | Typed presentation model for the allowlisted evidence export |
| `content/site.ts` | Approved optional links/media and current workflow/roadmap copy |
| `content/submission-2026.json` and `app/deftech-2026/` | Independent historical submission data and route |
| `public/evidence/` | Downloadable frozen evidence export and source lineage |
| `scripts/generate-og.mjs` | Generates the OpenGraph artwork from the supplied C4-0001 trajectory |

Most content is server-rendered into static HTML. Only the navigation enhancements and clipboard affordance need client code. The scenario selector and technical disclosures use native HTML/CSS; both scenario records remain in the static document. There is no database, account system, evaluator endpoint, model execution, analytics or tracking script.

## Evidence provenance and immutability

The authoritative records are the existing `outputs/final-submission-selected-demo/C4-0000.json`, `C4-0001.json` and `manifest.json` in the frozen MEHWAR source checkout. The manifest identifies the frozen MVP SHA above. Grid definitions were checked against `src/mehwar/scenarios/c4.py`; the C4-0001 trace was also checked against `tests/test_real_seed33.py` and the oracle hash in `src/mehwar/selected_demo.py`.

`public/evidence/selected-runs.json` copies allowed fields from those records, including complete controller and deterministic A* trajectories. Coordinates are `[row, col]`, rendered as `x = col`, `y = row`, with rows increasing downward. Geometry was not reconstructed from screenshots. See [the evidence lineage record](public/evidence/README.md) for source digests, screenshot digests and the exact movement contract.

`node scripts/check-evidence.mjs` pins the export checksum and verifies selected-case facts, geometry, provenance and sanitization. `node scripts/check-snapshot.mjs` pins five historical files: submission data, route source, route stylesheet and both original screenshot byte streams. Text hashes normalize CRLF only. Do not update the expected hashes merely to make a changed historical record pass. Later scientific evidence needs a separately identified record on the evolving homepage; it must not silently replace submission-era truth.

When the original ignored outputs are available, an additional read-only comparison can be run with their directory:

```powershell
node scripts/check-snapshot.mjs --evidence-dir <frozen-export-directory>
```

The public screenshots remain unedited final T13 artifacts at 1920 × 1065. Full-resolution links open them separately for inspection. The recorded submission statement, “137 tests passed, 0 skipped, Ruff PASS, git diff --check PASS,” is implementation verification from the submission record. It was not rerun for the website and is not a safety score.

The website consumes supplied classifications under `c4_c5_recurrence_v1`. It does not infer outcomes from the picture, reimplement recurrence classification or generate new scientific metrics. Invalid actions remain separate from mission outcome. A* is a deterministic reliability reference under the shared grid contract, never a leaderboard opponent.

## Optional configuration

Set only approved values in `content/site.ts`:

| Key | Current behavior when empty |
| --- | --- |
| `publicEmail` | No invented address or mail link. The collaboration section states that a public contact channel is not yet listed. |
| `evidenceArchiveUrl` | The historical snapshot remains available internally at `/deftech-2026`; no broken Drive link is shown. |
| `demoVideo`, `demoCaptions`, `demoTranscript` | The optional video section renders only when all three exist. No placeholder player appears. |

`publicEmail` expects an email address, not a `mailto:` prefix; the page builds the mail link and discussion subject. Provide an approved video asset, captions and transcript together. Keep `canonicalUrl` set to `https://mehwar-deftech.vercel.app`. Do not add private personal information, unapproved social accounts, customers or relationships.

## Deployment and production verification

Use the existing Vercel project **`mehwar-deftech`**. Never create a replacement project or public hostname as a fallback. Deploy only the validated website export or configure the existing project’s root to `public-site`; do not deploy the Python repository root. The V2 deployment state, final website commit and production checks are recorded in [HANDOFF.md](HANDOFF.md).

With a Vercel CLI already authenticated to the account that owns the project, verify ownership and link to the existing project before deploying:

```powershell
vercel whoami
vercel link --project mehwar-deftech
vercel --prod
```

An authenticated connector can alternatively publish the validated `out/` files to the same existing project. `node scripts/deployment-payload.mjs` prints the connector payload with base64-encoded export files and `vercel.json`; it does not deploy. The payload targets production under the existing `mehwar-deftech` name. `vercel.json` enables clean URLs for `/deftech-2026`. Do not infer that pushing this branch deploys the website: Git integration must be explicitly verified. If the existing project cannot be accessed, retain the build and report the access issue instead of creating a substitute.

After publishing, verify the permanent homepage and `/deftech-2026` without authentication, including evidence selection, disclosures, original images, downloadable JSON, navigation and mobile layouts. Check 1920 × 1080, 1440 × 900, 1280 × 800, 1024, 768, 430, 390 and 360 widths. Confirm the canonical/OG metadata, absence of browser errors, unchanged selected-case facts and preserved interpretation boundaries. Local build success and access to an authenticated preview do not establish public production accessibility.
