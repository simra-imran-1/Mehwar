# MEHWAR public evidence site

Isolated static Next.js / TypeScript front door for the DEFTECH 2026 submission. No database, authentication, controller execution, analytics, or trackers. All website files are confined to `public-site/` on `feat/public-site`, branched from `1586eebf9daa8a8e690bc6f62cc377ce540214ee`.

## Local verification

Use Node.js 20.9 or newer. From this directory:

```powershell
npm ci
npm run lint
npm run typecheck
npm run build
```

`out/` contains the static production site. `npm run dev` starts the development preview. Website verification does not rerun or alter the frozen MVP's scientific tests.

## Deploy to Vercel

Production: https://mehwar-deftech.vercel.app — Vercel project `mehwar-deftech`.

The authenticated Vercel connector deployed the locally validated `out/` files directly to production. The local CLI's `vercel whoami` returned an invalid-token error; CLI login is needed only for future CLI updates. This deployment does not configure Git integration, so pushing this branch alone will not republish the site. Use the short production URL above for the application; generated deployment aliases can require authentication.

After authenticating, run from this directory:

```powershell
vercel login
vercel whoami
vercel link --yes --project mehwar-deftech
vercel --prod
```

If the project name is unavailable in your account, use `mehwar-autonomy`. Select the intended team when prompted. Do not deploy from the Python repository root.

Alternatively, import `simra-imran-1/Mehwar` in Vercel, choose `feat/public-site` as the production branch, set Root Directory to `public-site`, Framework Preset to Next.js, Install Command to `npm ci`, Build Command to `npm run build`, and Output Directory to `out`. Do not change the repository default branch or the frozen submission branch. Use a normal `vercel.app` domain; no domain purchase is needed.

After deployment, open the production alias in a signed-out browser and confirm it is publicly accessible. Check the evidence images, both CTAs, 1920×1080 and 1440×900 desktop, 768px tablet, and 390px phone layouts. Confirm the frozen SHA and limitations appear unchanged. Preview authentication is not evidence of public production accessibility.

## Approved links and future updates

Edit `content/site.ts`:

- `snapshotUrl`: empty until an approved public Drive snapshot URL exists. The current CTA safely targets the on-page snapshot.
- `contactMailto`: empty mailto configuration placeholder. Set only to an approved public `mailto:` address. The current CTA is disabled and explicitly says the public contact channel is pending.
- `demoVideo`: empty. Add the final narrated video to `public/` and set its `/filename.mp4` path to enable the native video section. No fake video is shown.
- `submissionSnapshot`: historical record. Keep immutable. A future latest-build record should use the separate `latestValidatedBuild` configuration and a separately labeled section, without rewriting the September snapshot.

## Evidence assets and scientific scope

The two public PNGs are byte-for-byte copies of the final T13 `t13-micro-screenshots` captures from the T13 worktree, whose HEAD is the frozen source SHA. Each is 1920×1065. They show the dashboard only, with no terminals, private paths, phone numbers, or checkpoint files. No image editing or scientific rerendering was used.

- `public/c4-0001-liveness-degradation.png`: C4-0001, 28 steps, 0 invalid actions, `two_cell_loop`.
- `public/c4-0000-success.png`: C4-0000, 16 steps, 0 invalid actions, success.

Full-precision path costs come from the user-approved brief and match the final selected-demo JSON records at the frozen SHA. The dashboard images round their displayed costs. Screenshot links open the original full-resolution images for zooming on smaller screens; adjacent HTML retains accessible, readable metrics.

The 137 passed / 0 skipped / Ruff PASS / diff-check PASS values are recorded submission implementation-verification facts supplied in the brief, not a new run of the frozen test suite and not safety scores. This page makes no claims of flight validation, deployment readiness, safety certification, generic superiority, customer validation, pilots, or external-stack validation.
