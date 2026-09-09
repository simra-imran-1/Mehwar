import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import {
  clampPlaybackStep,
  presentationAnnotations,
} from "../content/playback.mjs";

// Website presentation checks only: no controller, scenario runner, movement
// legality check, path-cost calculation, or recurrence classifier is executed.
const evidence = JSON.parse(
  await readFile(
    new URL("../public/evidence/selected-runs.json", import.meta.url),
    "utf8",
  ),
);
const unchangedEvidence = JSON.stringify(evidence);
const byId = Object.fromEntries(
  evidence.scenarios.map((scenario) => [scenario.scenario_id, scenario]),
);

assert.deepEqual(Object.keys(presentationAnnotations), ["C4-0001", "C4-0000"]);
assert.equal(presentationAnnotations["C4-0000"], null);
const recurrence = presentationAnnotations["C4-0001"];
assert.deepEqual(recurrence, {
  recurrenceStartStep: 15,
  firstRevisitStep: 17,
  recurrenceCells: [
    [14, 1],
    [13, 0],
  ],
});
const failureTrace = byId["C4-0001"].trajectory;
assert.deepEqual(
  failureTrace.slice(
    recurrence.recurrenceStartStep,
    recurrence.recurrenceStartStep + 2,
  ),
  recurrence.recurrenceCells,
  "The fixed recurrence cells must remain exact recorded positions.",
);
assert.deepEqual(failureTrace[recurrence.firstRevisitStep], [14, 1]);
assert.deepEqual(failureTrace[recurrence.firstRevisitStep - 1], [13, 0]);
assert.deepEqual(failureTrace[recurrence.firstRevisitStep + 1], [13, 0]);
assert.ok(Object.isFrozen(presentationAnnotations));
assert.ok(Object.isFrozen(recurrence));
assert.ok(Object.isFrozen(recurrence.recurrenceCells));
for (const cell of recurrence.recurrenceCells) assert.ok(Object.isFrozen(cell));
assert.throws(() => {
  recurrence.firstRevisitStep = 18;
}, TypeError);
assert.throws(() => {
  recurrence.recurrenceCells[0][0] = 13;
}, TypeError);

const accepted = {
  "C4-0001": {
    steps: 28,
    positions: 29,
    initial: [8, 9],
    final: [13, 0],
    outcome: "two_cell_loop",
  },
  "C4-0000": {
    steps: 16,
    positions: 17,
    initial: [7, 5],
    final: [11, 14],
    outcome: "success",
  },
};
for (const [id, expected] of Object.entries(accepted)) {
  const scenario = byId[id];
  assert.equal(scenario.steps, expected.steps);
  assert.equal(scenario.trajectory.length, expected.positions);
  assert.equal(scenario.failure_type, expected.outcome);
  assert.deepEqual(scenario.trajectory[0], expected.initial);
  assert.deepEqual(scenario.trajectory[expected.steps], expected.final);

  for (let step = 0; step <= expected.steps; step += 1) {
    assert.equal(
      clampPlaybackStep(step, scenario.steps),
      step,
      `${id}: preserve recorded step ${step}`,
    );
  }
  for (const [input, output] of [
    [-1, 0],
    [-Infinity, 0],
    [0, 0],
    [0.99, 0],
    [1.99, 1],
    [expected.steps - 0.01, expected.steps - 1],
    [expected.steps, expected.steps],
    [expected.steps + 1, expected.steps],
    [Infinity, expected.steps],
    [NaN, 0],
  ]) {
    assert.equal(
      clampPlaybackStep(input, scenario.steps),
      output,
      `${id}: clamp ${input}`,
    );
  }
}

assert.equal(
  clampPlaybackStep(28, byId["C4-0000"].steps),
  16,
  "Switching to the shorter run cannot retain an out-of-range cursor.",
);
assert.equal(
  clampPlaybackStep(3, 0),
  0,
  "A single-position trace has only step zero.",
);
for (const invalidMaximum of [-1, 1.5, NaN, Infinity]) {
  assert.throws(() => clampPlaybackStep(0, invalidMaximum), RangeError);
}
assert.equal(
  JSON.stringify(evidence),
  unchangedEvidence,
  "Presentation checks must not mutate recorded evidence.",
);
console.log(
  "PASS: frozen playback annotations, exact index landmarks, immutable cells, both recorded-step ranges, and cursor bounds. No scientific evaluation performed.",
);
