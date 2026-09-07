import exported from "../public/evidence/selected-runs.json";
type Cell = readonly number[];
export type RecordedScenario = {
  scenario_id: string;
  scenario_family: string;
  controller: string;
  success: boolean;
  steps: number;
  path_cost: number;
  failure_type: string;
  trajectory: readonly Cell[];
  reference_result: {
    planner: string;
    found: boolean;
    steps: number;
    cost: number;
    trajectory: readonly Cell[];
    movement_contract: string;
  };
  diagnostics: {
    invalid_actions: number;
    collision: boolean;
    attempted_actions: number;
    truncated: boolean;
  };
  configuration: {
    grid_size: number;
    start: Cell;
    goal: Cell;
    blocked: readonly Cell[];
    episode_budget: number;
    movement_contract: string;
    failure_protocol: string;
    step_definition: string;
    dynamics: boolean;
  };
  provenance: {
    fresh_holdout: boolean;
    scenario_classification: string;
    data_classification: string;
    scenario_source: string;
    scenario_selection: string;
  };
};
export type EvidenceScenario = RecordedScenario & {
  evidenceLabel: string;
  interpretation: string;
  screenshot: string;
  // Presentation annotation verified against the frozen trace; never a classifier.
  recurrenceStartIndex?: number;
};
export const provenance = exported;
const records: readonly RecordedScenario[] = exported.scenarios;
function record(id: string): RecordedScenario {
  const found = records.find((entry) => entry.scenario_id === id);
  if (!found) throw new Error(`Missing frozen evidence record: ${id}`);
  return found;
}
export const degradation: EvidenceScenario = {
  ...record("C4-0001"),
  evidenceLabel: "LIVENESS DEGRADATION OBSERVED",
  interpretation:
    "In this selected controlled scenario, the controller remained action-legal but entered a legal two-cell recurrence and failed to complete the mission.",
  screenshot: "/c4-0001-liveness-degradation.png",
  recurrenceStartIndex: 15,
};
export const completion: EvidenceScenario = {
  ...record("C4-0000"),
  evidenceLabel: "NO FAILURE OBSERVED IN SELECTED DEMO RUN",
  interpretation:
    "The same evaluation workflow records successful mission completion. This selected run does not establish controller safety, robustness or general reliability.",
  screenshot: "/c4-0000-success.png",
};
export const scenarios = [degradation, completion] as const;
