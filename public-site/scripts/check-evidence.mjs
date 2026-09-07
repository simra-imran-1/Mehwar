import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";

// Static evidence integrity checks only. This does not execute a controller,
// calculate new scientific results, or classify trajectories.
const exportUrl = new URL("../public/evidence/selected-runs.json", import.meta.url);
const bytes = await readFile(exportUrl);
const digest = (value) => createHash("sha256").update(value).digest("hex");
assert.equal(
  digest(bytes),
  "d16c0c39fdf0322b4ad06da3ab27c08aa07f10cc4de2989f955cee762719ea5e",
  "The immutable selected-run public evidence export changed. Review against the frozen source before updating this pin.",
);

const evidence = JSON.parse(bytes.toString("utf8"));
const frozenSha = "1586eebf9daa8a8e690bc6f62cc377ce540214ee";
const checkpointSha = "c91d30711aa91957554dfa92b152d2a1d1e14a7b43fa01237722c54cb0acfaaf";
assert.equal(evidence.schema_version, "mehwar-public-evidence-v1");
assert.equal(evidence.frozen_mvp_sha, frozenSha);
assert.equal(evidence.checkpoint_sha256, checkpointSha);
assert.equal(evidence.failure_protocol, "c4_c5_recurrence_v1");
assert.equal(evidence.fresh_holdout, false);
assert.equal(evidence.scenario_classification, "development_validation");
assert.equal(evidence.scenario_selection, "selected current MVP demo");
assert.equal(evidence.data_classification, "current-mehwar-selected-demo-run");
assert.equal(
  evidence.movement_contract,
  "8-connected destination-cell-only, corner cutting allowed, orthogonal cost 1, diagonal cost sqrt(2)",
);
assert.deepEqual(
  evidence.scenarios.map((scenario) => scenario.scenario_id),
  ["C4-0001", "C4-0000"],
);

const expected = {
  "C4-0001": {
    success: false,
    steps: 28,
    failure_type: "two_cell_loop",
    path_cost: 37.112698372208094,
    reference_steps: 14,
    reference_cost: 16.071067811865476,
    start: [8, 9],
    goal: [13, 1],
    budget: 28,
  },
  "C4-0000": {
    success: true,
    steps: 16,
    failure_type: "success",
    path_cost: 17.242640687119284,
    reference_steps: 15,
    reference_cost: 16.65685424949238,
    start: [7, 5],
    goal: [11, 14],
    budget: 30,
  },
};

for (const scenario of evidence.scenarios) {
  const approved = expected[scenario.scenario_id];
  for (const field of ["success", "steps", "failure_type", "path_cost"]) {
    assert.equal(scenario[field], approved[field], `${scenario.scenario_id}: ${field}`);
  }
  assert.equal(scenario.controller, "MaskablePPOCheckpointAdapter");
  assert.equal(scenario.controller_metadata.checkpoint_sha256, checkpointSha);
  assert.equal(scenario.controller_metadata.action_masking, true);
  assert.equal(scenario.controller_metadata.deterministic, true);
  assert.equal(scenario.diagnostics.invalid_actions, 0);
  assert.equal(scenario.diagnostics.collision, false);
  assert.equal(scenario.reference_result.planner, "A*");
  assert.equal(scenario.reference_result.found, true);
  assert.equal(scenario.reference_result.steps, approved.reference_steps);
  assert.equal(scenario.reference_result.cost, approved.reference_cost);
  assert.equal(scenario.trajectory.length, approved.steps + 1);
  assert.equal(scenario.reference_result.trajectory.length, approved.reference_steps + 1);
  assert.equal(scenario.configuration.grid_size, 15);
  assert.equal(scenario.configuration.blocked.length, 13);
  assert.deepEqual(scenario.configuration.start, approved.start);
  assert.deepEqual(scenario.configuration.goal, approved.goal);
  assert.equal(scenario.configuration.episode_budget, approved.budget);
  assert.equal(scenario.configuration.dynamics, false);
  assert.equal(scenario.configuration.failure_protocol, evidence.failure_protocol);
  assert.equal(scenario.provenance.fresh_holdout, false);
  assert.equal(scenario.provenance.scenario_classification, "development_validation");
  assert.equal(scenario.provenance.data_classification, evidence.data_classification);
  assert.equal("checkpoint_filename" in scenario.controller_metadata, false);
}

const recurrence = evidence.scenarios[0];
assert.equal(
  digest(JSON.stringify(recurrence.trajectory)),
  "ec7fea9558b5de358d71632065497c14170bf225e2ee9d94de42647ab9f81fc3",
  "C4-0001 trace must remain identical to the frozen regression oracle.",
);
assert.deepEqual(recurrence.trajectory.slice(15, 19), [[14, 1], [13, 0], [14, 1], [13, 0]]);
assert.deepEqual(
  evidence.source_lineage.exports.map((source) => source.sha256),
  [
    "8ebbad71923d4252bfff52c7f2be9ecc924311fcee0b7e2f1962e9bcb45a6dda",
    "77aa27d925a465b5dad06750c1e74702dae44aeb6e3838a1cf47482a2616d746",
    "7d7c95bcb0b122bbd8240a6dddbaa0e21874936f81ab48410a7ad63b33fc9e23",
  ],
);
assert.doesNotMatch(bytes.toString("utf8"), /[A-Z]:\\|\/Users\/|\/home\/|checkpoint_filename|\.zip|API_KEY|PRIVATE_KEY|CNIC/i);
console.log("PASS: frozen export checksum, approved facts, geometry counts, trace oracle, provenance and sanitized metadata.");
