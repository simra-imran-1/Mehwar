# MEHWAR public-site handoff

Status: DEPLOYED

Production: https://mehwar-deftech.vercel.app

Vercel project: `mehwar-deftech`

Deployment ID: `dpl_DLnbqzckc19quFk9SUUU1HGb2RiY`

## Isolation and implementation

- Website branch: `feat/public-site`, created directly from the frozen source in a separate worktree.
- Frozen MEHWAR source: `1586eebf9daa8a8e690bc6f62cc377ce540214ee`.
- Frozen submission branch: `feat/integration-demo`; unchanged.
- All added files are inside `public-site/`. No scientific source, dashboard, reports, evaluator, scenarios, checkpoint, or frozen tests were changed.
- Next.js 16.3.4, React 19.2.8, TypeScript; static export. No backend, auth, database, analytics, trackers, controller execution, or remote font requests.
- `package-lock.json` records installed versions. All source components render statically; the evidence disclosure uses native HTML.

## Validation

- Dependency installation: PASS.
- `npm run lint`: PASS.
- `npm run typecheck`: PASS.
- `npm run build`: PASS; prerendered `/` and static not-found output.
- `git diff --check`: PASS.
- Local browser checks: 1920×1080, 1440×900, 768×1024, 390×844.
- All four local widths: HTTP 200, no horizontal overflow, valid section anchors, both evidence images loaded with alt text, correct title and frozen SHA, no browser console/page errors, no external requests.
- Live production browser checks also passed at all four widths in fresh unauthenticated browser contexts, including both CTA targets, both evidence images, exact SHA, no overflow, no console/page errors, and no external requests.
- Keyboard focus styles and skip link are implemented; native links, buttons and disclosure are keyboard accessible. No meaning depends on color alone.
- Exact metrics were cross-checked against the final selected-demo JSON records tied to the frozen SHA.
- Claim review: selected controlled cases only; no representative success rates, safety scores, flight validation, readiness, certification, general algorithm superiority, OEM validation or invented relationships. Roadmap and evidence are separately labeled. A* uses the exact required reference wording.
- Sensitive-data review: source and rendered page contain no private contact details, machine paths, localhost references or checkpoint paths. Public images were visually reviewed.

## Assets

Both PNGs are unedited copies of the final T13 micro-polish captures, 1920×1065. Their content matches the frozen dashboard, and no private information is visible.

| Public asset | SHA256 |
| --- | --- |
| `c4-0000-success.png` | `ed0ee4ee1e6a372e8a7ca26d36967b531c906513d3bf7e5ba0f3bb3527a856a2` |
| `c4-0001-liveness-degradation.png` | `bd4dad0e5804a1e001e43673d42048b5a1276cc88e0e13bea76ca8a2dbcc0160` |

No narrated demo video was found or included. Set `demoVideo` in `content/site.ts` after adding the approved final asset.

## Deployment and remaining configuration

The authenticated Vercel connector accepted the 25 production-export files, totaling 1,034,198 bytes. No Python repository files, checkpoint, source maps, local QA artifacts, or secrets were uploaded. This is a direct static deployment, not a Git-integrated deployment.

The production alias responds without authentication. The initial generated deployment alias redirects to Vercel login and must not be used for the application. The connector's subsequent deployment-status lookup returned 404, so direct production HTTP and browser checks are the independent verification of the live result.

- Drive snapshot CTA: works as an on-page link to the immutable snapshot; approved Drive URL remains optional in configuration.
- Contact CTA: disabled with an explicit pending-contact label. **Manual completion:** put a team-approved public `mailto:` address in `content/site.ts` and redeploy.
- Video: optional, absent, configurable with one asset-path change.
- Future builds: use the separate latest-build configuration and retain `submissionSnapshot` unchanged.
- Future CLI deployments: run `vercel login` first because the old CLI credential is invalid. See README for exact deployment commands and optional Git integration setup.

## Files added

`app/page.tsx`, `app/layout.tsx`, `app/globals.css`, `content/site.ts`, `public/c4-0000-success.png`, `public/c4-0001-liveness-degradation.png`, `public/icon.svg`, `package.json`, `package-lock.json`, `tsconfig.json`, `next-env.d.ts`, `next.config.ts`, `eslint.config.mjs`, `.gitignore`, `README.md`, and `HANDOFF.md`.
