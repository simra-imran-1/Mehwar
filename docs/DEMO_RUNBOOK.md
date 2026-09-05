# MEHWAR jury demo operator card

**Prerequisites:** PowerShell, Git, Python >=3.10; a clean reviewed checkout of
`simra-imran-1/Mehwar` containing the selected-demo base `3f19a2710b78144857a0dbeb60a65a0910a53ee1`;
an activated virtual environment with `.[dev,ppo,dashboard]`; the separately supplied
seed-33 ZIP. Its SHA256 must be
`c91d30711aa91957554dfa92b152d2a1d1e14a7b43fa01237722c54cb0acfaaf`.

**Launch from this worktree (same PowerShell terminal):**

```powershell
Set-Location 'C:\Users\Fast Computer\MEHWAR_WORK\codex-workers\demo-operator'
.\.venv\Scripts\Activate.ps1
$env:MEHWAR_SEED33_CHECKPOINT = (Resolve-Path 'C:\Users\Fast Computer\MEHWAR_WORK\Mehwar\artifacts\seed33\model_stage_301056_lifetime_452608.zip').Path
.\scripts\start_demo.ps1
```

For another machine, substitute its checkout and supplied checkpoint paths. First
setup only: `python -m venv .venv`, activate it, then add `-InstallDependencies` to
the launch command (requires network/cache). Normal launch never installs anything.
To pin a reviewed candidate, add `-ExpectedSha <full-reviewed-commit-SHA>`.
Preflight displays checkout identity, checks imports/output/checkpoint, and calls
the existing exact selected-demo verifier. Expect **PASS**, then Streamlit's URL;
open **http://127.0.0.1:8501**. Keep the terminal open. Ctrl+C stops it.

**Exact clicks and evidence (rehearse before presenting):**

1. Sidebar **Input source** -> **Run selected verified C4 demo locally**.
   The initial page is a labeled synthetic fixture; select local input before presenting.
2. **Selected C4 scenario** -> **C4-0000** -> **Run verified C4 demo**.
   Confirm **CURRENT MEHWAR SELECTED DEMO RUN**, scenario C4-0000,
   **success / 16 steps / 0 invalid actions**. Point at Run summary and Trajectory evidence.
3. **Selected C4 scenario** -> **C4-0001** -> **Run verified C4 demo** again.
   Confirm scenario C4-0001, **two_cell_loop / 28 steps / 0 invalid actions** and
   **LIVENESS DEGRADATION OBSERVED**. Point at the repeated cells in the ordered
   trajectory table and Diagnostics; the plot alone can hide revisits.
4. Scroll to **Deterministic reference result**, **Provenance**, and **Evidence limitations**.
   A* reference steps/cost: C4-0000 **15 / 16.65685424949238**;
   C4-0001 **14 / 16.071067811865476**.

**45-60 second narration:** 0-10s: “These are two selected development-validation
cases using the verified frozen seed-33 controller.” 10-25s, C4-0000: “This run
reaches the goal in 16 steps with zero invalid actions.” 25-40s, C4-0001: “This run
takes 28 legal steps but exhibits a two-cell loop, also with zero invalid actions.
Legal action selection does not by itself guarantee mission liveness.” 40-60s:
“A* is a deterministic A* reliability reference under the shared grid contract.
These selected cases characterize a capability boundary, not general performance
or planner superiority.” Point to provenance and limitations as you finish.

**Recovery:**

- Missing checkpoint variable: set it with the command above using the supplied ZIP,
  then restart the launcher in that same terminal. A missing file or wrong hash must
  be corrected; never substitute another model or a synthetic fixture.
- Streamlit fails: read the terminal error. For missing imports/wrong editable
  checkout, activate this worktree's venv and explicitly rerun with
  `-InstallDependencies`. For an occupied port, stop your previous demo or use
  `.\scripts\start_demo.ps1 -Port 8502`, then open the printed URL. Do not kill an
  unrelated server. If the browser alone fails to open, paste the printed URL.
- Live inference unavailable: use **already generated** JSON from a previous PASS
  folder printed under `outputs/demo_operator/<folder>/`. Start the upload UI with
  `python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501`.
  Sidebar **Input source** -> **Uploaded EvaluationResult JSON** -> **Browse files**
  -> `C4-0000.json`; replace it with `C4-0001.json` second. Say these are saved
  verified runs, not fresh execution; inspect their scenario, checkpoint metadata,
  and provenance. Upload each result JSON, **not** `manifest.json`. The launcher
  never switches to this fallback automatically. If Streamlit remains unavailable,
  show the corresponding saved `.txt` reports and disclose the UI failure.

**Exact claim boundaries:** Controlled 2-D grid-based mission-routing abstraction.
Not physical flight validation. Not deployment approval. Not safety certification.
Not evidence of general learned-controller or planner superiority. Selected current
MVP development-validation demos, not a fresh holdout or a general success rate;
no historical percentages as current measurements. The reference shares static
8-connected destination-cell-only legality, corner cutting allowed, and costs
1 / sqrt(2). No flight, deployment, or safety claim follows from this demo.
