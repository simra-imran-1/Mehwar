import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { resolve } from "node:path";
import { fileURLToPath } from "node:url";

// September 2026 historical record. These digests are intentionally fixed.
// Evolving product evidence belongs outside this route and its data file.
// Normalize only text line endings so Git's CRLF checkout setting is harmless.
const immutableFiles = {
  "content/submission-2026.json": "fe89dccd564d88505af8938876cacf60f558867f7a417bb793a08a2449c94086",
  "app/deftech-2026/page.tsx": "edccafeb9decba9e6211baf78f05f33b3346e5124f605df9cf984be84ae36bc7",
  "app/deftech-2026/snapshot.module.css": "75b0e835da912a88133004368ee608cc630a65a11c0e90a9e543d569a248fb1e",
  "public/c4-0000-success.png": "ed0ee4ee1e6a372e8a7ca26d36967b531c906513d3bf7e5ba0f3bb3527a856a2",
  "public/c4-0001-liveness-degradation.png": "bd4dad0e5804a1e001e43673d42048b5a1276cc88e0e13bea76ca8a2dbcc0160",
};

const siteRoot = fileURLToPath(new URL("../", import.meta.url));
const readJson = async (path) => JSON.parse(await readFile(path, "utf8"));

for (const [path, expected] of Object.entries(immutableFiles)) {
  const bytes = await readFile(resolve(siteRoot, path));
  const content = path.endsWith(".png") ? bytes : bytes.toString("utf8").replaceAll("\r\n", "\n");
  const actual = createHash("sha256").update(content).digest("hex");
  assert.equal(actual, expected, `Historical snapshot changed: ${path}. Preserve the submission record; put newer evidence on the homepage.`);
}

const snapshot = await readJson(resolve(siteRoot, "content/submission-2026.json"));
assert.equal(snapshot.provenance.freshHoldout, false);
assert.equal(snapshot.provenance.failureProtocol, "c4_c5_recurrence_v1");
assert.deepEqual(snapshot.scenarios.map((scenario) => scenario.id), ["C4-0001", "C4-0000"]);

// Optional audit against the authoritative frozen exports, without copying
// checkpoint filenames, local paths or other controller internals into the site.
const args = process.argv.slice(2);
if (args.length > 0) {
  assert.equal(args.length, 2, "Usage: node scripts/check-snapshot.mjs [--evidence-dir <frozen export directory>]");
  assert.equal(args[0], "--evidence-dir");
  const evidenceRoot = resolve(args[1]);
  const manifest = await readJson(resolve(evidenceRoot, "manifest.json"));
  const provenance = snapshot.provenance;
  assert.equal(provenance.frozenMvpSha, manifest.mehwar_git_commit);
  assert.equal(provenance.checkpointSha256, manifest.checkpoint_sha256);
  assert.equal(provenance.failureProtocol, manifest.failure_protocol);
  assert.equal(provenance.movementContract, manifest.movement_contract);
  assert.equal(provenance.scenarioClassification, manifest.scenario_classification);
  assert.equal(provenance.scenarioSelection, manifest.scenario_selection);
  assert.equal(provenance.freshHoldout, manifest.fresh_holdout);
  assert.equal(provenance.researchSourceCommit, manifest.research_source_commit);
  assert.equal(provenance.scenarioManifestGitBlob, manifest.scenario_manifest_git_blob);

  for (const scenario of snapshot.scenarios) {
    const report = await readJson(resolve(evidenceRoot, scenario.sourceReport));
    assert.equal(scenario.id, report.scenario_id);
    assert.equal(scenario.missionCompleted, report.success);
    assert.equal(scenario.steps, report.steps);
    assert.equal(scenario.invalidActions, report.diagnostics.invalid_actions);
    assert.equal(scenario.classification, report.failure_type);
    assert.equal(scenario.controllerPathCost, String(report.path_cost));
    assert.equal(scenario.referenceSteps, report.reference_result.steps);
    assert.equal(scenario.referencePathCost, String(report.reference_result.cost));
    assert.equal(provenance.dataClassification, report.provenance.data_classification);
    assert.equal(provenance.checkpointSha256, report.controller_metadata.checkpoint_sha256);
  }
  console.log("Authoritative frozen exports match the historical snapshot.");
}

console.log(`Historical snapshot integrity passed: ${Object.keys(immutableFiles).length} fixed files, including both original screenshot byte streams.`);
