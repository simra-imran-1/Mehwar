import type { EvidenceScenario } from "../content/evidence";
import {
  clampPlaybackStep,
  presentationAnnotations,
} from "../content/playback.mjs";
import "./recorded-trajectory.css";

// Projection only. Coordinates and final scientific facts come from the frozen
// export; playback reveals an exact prefix and never evaluates that prefix.
const cellSize = 28;
const origin = 64;
const project = (cell: readonly number[]) => [
  origin + cell[1] * cellSize + cellSize / 2,
  origin + cell[0] * cellSize + cellSize / 2,
];
const polylinePoints = (cells: readonly (readonly number[])[]) =>
  cells.map((cell) => project(cell).join(",")).join(" ");

export function RecordedTrajectory({
  scenario,
  step,
  showReference = false,
  id,
  transitionKey,
}: {
  scenario: EvidenceScenario;
  step: number;
  showReference?: boolean;
  id: string;
  transitionKey?: number;
}) {
  const visibleStep = clampPlaybackStep(step, scenario.steps);
  const visibleTrace = scenario.trajectory.slice(0, visibleStep + 1);
  const currentCell = scenario.trajectory[visibleStep];
  const current = project(currentCell);
  const config = scenario.configuration;
  const start = project(config.start);
  const goal = project(config.goal);
  const goalOnRight = goal[0] > origin + cellSize * 10;
  const goalDirection = goalOnRight ? -1 : 1;
  const annotation = presentationAnnotations[scenario.scenario_id];
  const recurrenceVisible =
    !!annotation && visibleStep >= annotation.firstRevisitStep;
  const recurrenceCells = recurrenceVisible ? annotation.recurrenceCells : [];

  return (
    <figure className="recorded-field">
      <svg
        className="recorded-field-svg"
        viewBox="0 0 548 552"
        role="img"
        aria-labelledby={`${id}-title ${id}-description`}
      >
        <title id={`${id}-title`}>
          {`${scenario.scenario_id} recorded trajectory, displayed step ${visibleStep} of ${scenario.steps}`}
        </title>
        <desc id={`${id}-description`}>
          {`Exact ${config.grid_size} by ${config.grid_size} controlled 2-D grid. Coordinates are row, column; rows increase downward. Start (${config.start.join(", ")}); goal (${config.goal.join(", ")}). The displayed recorded position after ${visibleStep} completed moves is (${currentCell.join(", ")}). Shaded cells are blocked. The solid path reveals the controller's recorded positions through this step. Recorded final outcome: ${scenario.failure_type}; mission ${scenario.success ? "completed" : "not completed"} after ${scenario.steps} steps, with ${scenario.diagnostics.invalid_actions} invalid actions. These final-run facts are not recalculated during playback.${recurrenceVisible ? " Amber rings identify the recorded recurrence cells (14, 1) and (13, 0); the first revisit is recorded at step 17." : ""}${showReference ? ` The dashed path is the complete deterministic A* reference, ${scenario.reference_result.steps} steps, shown as static context rather than simultaneous playback.` : " The deterministic A* reference layer is hidden."}`}
        </desc>

        <defs>
          <pattern
            id={`${id}-grid`}
            width={cellSize}
            height={cellSize}
            patternUnits="userSpaceOnUse"
            x={origin}
            y={origin}
          >
            <path
              d={`M ${cellSize} 0 L 0 0 0 ${cellSize}`}
              fill="none"
              className="recorded-grid-line"
            />
          </pattern>
        </defs>
        <rect
          x={origin}
          y={origin}
          width={cellSize * config.grid_size}
          height={cellSize * config.grid_size}
          fill={`url(#${id}-grid)`}
          className="recorded-grid-boundary"
        />
        {[0, 5, 10, 14].map((index) => (
          <g key={index} className="recorded-axis">
            <text
              x={origin + index * cellSize + cellSize / 2}
              y={origin - 15}
              textAnchor="middle"
            >
              {String(index).padStart(2, "0")}
            </text>
            <text
              x={origin - 18}
              y={origin + index * cellSize + 18}
              textAnchor="end"
            >
              {String(index).padStart(2, "0")}
            </text>
          </g>
        ))}
        <text x="484" y="27" textAnchor="end" className="recorded-axis">
          COLUMN →
        </text>
        <text x="64" y="520" className="recorded-axis">
          15 × 15 / CONTROLLED 2-D GRID
        </text>
        <text x="484" y="520" textAnchor="end" className="recorded-axis">
          ROW ↓
        </text>

        <g
          key={transitionKey ?? scenario.scenario_id}
          className="recorded-scenario"
        >
          {config.blocked.map((cell) => (
            <rect
              key={cell.join()}
              x={origin + cell[1] * cellSize + 2}
              y={origin + cell[0] * cellSize + 2}
              width={cellSize - 4}
              height={cellSize - 4}
              rx="1"
              className="recorded-obstacle"
            />
          ))}
          {showReference && (
            <polyline
              points={polylinePoints(scenario.reference_result.trajectory)}
              className="recorded-reference"
              fill="none"
            />
          )}
          <polyline
            points={polylinePoints(visibleTrace)}
            className="recorded-controller"
            fill="none"
          />
          {visibleTrace.slice(1, -1).map((cell, index) => {
            const [x, y] = project(cell);
            return (
              <circle
                key={index}
                cx={x}
                cy={y}
                r="2.6"
                className="recorded-waypoint"
              />
            );
          })}

          <circle
            cx={start[0]}
            cy={start[1]}
            r="7"
            className="recorded-start"
          />
          <text x={start[0] + 13} y={start[1] - 12} className="recorded-label">
            START
          </text>
          <rect
            x={goal[0] - 7}
            y={goal[1] - 7}
            width="14"
            height="14"
            className="recorded-goal"
          />
          <path
            d={`M ${goal[0] + goalDirection * 13} ${goal[1] - 10} L ${goal[0] + goalDirection * 29} ${goal[1] - 26} H ${goal[0] + goalDirection * 78}`}
            className="recorded-callout"
            fill="none"
          />
          <text
            x={goal[0] + goalDirection * 32}
            y={goal[1] - 31}
            textAnchor={goalOnRight ? "end" : "start"}
            className="recorded-label"
          >
            GOAL
          </text>

          {recurrenceVisible && (
            <g className="recorded-recurrence">
              <polyline
                points={polylinePoints(recurrenceCells)}
                fill="none"
                className="recorded-recurrence-line"
              />
              {recurrenceCells.map((cell) => {
                const [x, y] = project(cell);
                return (
                  <circle
                    key={cell.join()}
                    cx={x}
                    cy={y}
                    r="12"
                    className="recorded-recurrence-ring"
                  />
                );
              })}
              <path
                d="M 78 424 V 289 H 121"
                fill="none"
                className="recorded-recurrence-callout"
              />
              <text x="87" y="257" className="recorded-recurrence-label">
                LEGAL RECURRENCE
              </text>
              <text x="87" y="277" className="recorded-recurrence-coordinate">
                (14,1) ↔ (13,0)
              </text>
            </g>
          )}

          <g
            className={`recorded-current${recurrenceVisible ? " is-recurrent" : ""}`}
          >
            <circle
              cx={current[0]}
              cy={current[1]}
              r="8"
              className="recorded-current-ring"
            />
            <circle
              cx={current[0]}
              cy={current[1]}
              r="3.6"
              className="recorded-current-point"
            />
          </g>
        </g>
      </svg>
      <figcaption className="recorded-legend">
        <span>
          <i className="recorded-legend-line" aria-hidden="true" />
          Recorded controller
        </span>
        {showReference && (
          <span>
            <i
              className="recorded-legend-line is-reference"
              aria-hidden="true"
            />
            A* reference
          </span>
        )}
        <span>
          <i className="recorded-legend-block" aria-hidden="true" />
          Blocked cell
        </span>
        {recurrenceVisible && (
          <span>
            <i className="recorded-legend-ring" aria-hidden="true" />
            Recurrence
          </span>
        )}
      </figcaption>
    </figure>
  );
}
