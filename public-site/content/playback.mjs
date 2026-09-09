/**
 * Fixed annotations for presenting the accepted, recorded trajectories.
 * These are editorial pointers verified against the frozen export, never
 * recurrence detection, a failure classifier, or an evaluation result.
 * Step 0 is the recorded initial position; each later index is a completed move.
 */

/** @typedef {readonly [number, number]} Cell */
/**
 * @typedef {Readonly<{
 *   recurrenceStartStep: number,
 *   firstRevisitStep: number,
 *   recurrenceCells: readonly Cell[]
 * }>} RecurrencePresentationAnnotation
 */

/** @type {Readonly<Record<string, RecurrencePresentationAnnotation | null | undefined>>} */
export const presentationAnnotations = Object.freeze({
  "C4-0001": Object.freeze({
    recurrenceStartStep: 15,
    firstRevisitStep: 17,
    recurrenceCells: Object.freeze([
      Object.freeze([14, 1]),
      Object.freeze([13, 0]),
    ]),
  }),
  "C4-0000": null,
});

/**
 * Bound a presentation cursor to the recorded positions. This changes neither
 * the trace nor its supplied final outcome, diagnostics, steps, or path cost.
 * Fractional slider values select the preceding recorded position.
 * @param {number} step Requested presentation cursor.
 * @param {number} maximum Final recorded step, inclusive.
 * @returns {number} A recorded-position index from zero through maximum.
 * @throws {RangeError} If maximum is not a nonnegative integer.
 */
export function clampPlaybackStep(step, maximum) {
  if (!Number.isInteger(maximum) || maximum < 0) {
    throw new RangeError("Playback maximum must be a nonnegative integer.");
  }
  if (Number.isNaN(step)) return 0;
  return Math.min(maximum, Math.max(0, Math.trunc(step)));
}
