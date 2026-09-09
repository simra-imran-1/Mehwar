export type RecurrencePresentationAnnotation = Readonly<{
  recurrenceStartStep: number;
  firstRevisitStep: number;
  recurrenceCells: readonly (readonly [number, number])[];
}>;

export const presentationAnnotations: Readonly<
  Record<string, RecurrencePresentationAnnotation | null | undefined>
>;

/** Clamp a presentation cursor to an inclusive recorded-step range. */
export function clampPlaybackStep(step: number, maximum: number): number;
