import type { EvidenceScenario } from "../content/evidence";
// SVG projection only. All grid cells and path vertices come from the frozen export.
const size = 28;
const origin = 64;
const point = (cell: readonly number[]) => [
  origin + cell[1] * size + size / 2,
  origin + cell[0] * size + size / 2,
];
const points = (cells: readonly (readonly number[])[]) =>
  cells.map((cell) => point(cell).join(",")).join(" ");
export function TrajectoryVisual({
  scenario,
  hero = false,
  id,
}: {
  scenario: EvidenceScenario;
  hero?: boolean;
  id: string;
}) {
  const config = scenario.configuration;
  const start = point(config.start);
  const goal = point(config.goal);
  const recurrence =
    scenario.recurrenceStartIndex === undefined
      ? []
      : scenario.trajectory.slice(
          scenario.recurrenceStartIndex,
          scenario.recurrenceStartIndex + 2,
        );
  return (
    <figure className={`trajectory ${hero ? "hero-trajectory" : ""}`}>
      <div className="plot-heading">
        <span className="mono">
          {scenario.scenario_id}{" "}
          <span className="muted">
            / {scenario.scenario_family.replaceAll("_", " ")}
          </span>
        </span>
        <span className="plot-kind">RECORDED TRACE</span>
      </div>
      <svg
        className="trajectory-svg"
        viewBox="0 0 548 552"
        role="img"
        aria-labelledby={`${id}-title ${id}-description`}
      >
        <title id={`${id}-title`}>
          {`${scenario.scenario_id} recorded controller trajectory and deterministic A* reference`}
        </title>
        <desc id={`${id}-description`}>
          {`Exact ${config.grid_size} by ${config.grid_size} controlled grid. Coordinates are row, column. Start ${config.start.join(", ")}; goal ${config.goal.join(", ")}. The controller records ${scenario.steps} legal moves and ${scenario.success ? "reaches" : "does not reach"} the goal. The A* reference reaches the goal in ${scenario.reference_result.steps} steps. Shaded cells are blocked. Solid blue is the controller; dashed grey is reference context.${recurrence.length ? " Amber rings mark legal recurrence between (14,1) and (13,0)." : ""}`}
        </desc>
        <defs>
          <pattern
            id={`${id}-grid`}
            width={size}
            height={size}
            patternUnits="userSpaceOnUse"
            x={origin}
            y={origin}
          >
            <path
              d={`M ${size} 0 L 0 0 0 ${size}`}
              fill="none"
              stroke="var(--grid-line)"
              strokeWidth="0.8"
            />
          </pattern>
        </defs>
        <rect
          x={origin}
          y={origin}
          width={size * config.grid_size}
          height={size * config.grid_size}
          fill={`url(#${id}-grid)`}
          stroke="var(--grid-line)"
          strokeWidth=".8"
        />
        {[0, 5, 10, 14].map((n) => (
          <g key={n} className="axis-label">
            <text
              x={origin + n * size + 14}
              y={origin - 15}
              textAnchor="middle"
            >
              {String(n).padStart(2, "0")}
            </text>
            <text x={origin - 18} y={origin + n * size + 18} textAnchor="end">
              {String(n).padStart(2, "0")}
            </text>
          </g>
        ))}
        <text x="484" y="27" textAnchor="end" className="axis-label">
          COLUMN →
        </text>
        {config.blocked.map((cell) => (
          <rect
            key={cell.join()}
            x={origin + cell[1] * size + 2}
            y={origin + cell[0] * size + 2}
            width={size - 4}
            height={size - 4}
            rx="1"
            fill="var(--obstacle)"
          />
        ))}
        <polyline
          className="reference-path"
          points={points(scenario.reference_result.trajectory)}
          fill="none"
          stroke="var(--reference)"
          strokeWidth="2.8"
          strokeDasharray="3 6"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <polyline
          className={hero ? "controller-path trace-once" : "controller-path"}
          pathLength="1"
          points={points(scenario.trajectory)}
          fill="none"
          stroke="var(--trace)"
          strokeWidth="3.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        {scenario.trajectory
          .slice(1, scenario.recurrenceStartIndex)
          .map((cell, i) => {
            const p = point(cell);
            return (
              <circle key={i} cx={p[0]} cy={p[1]} r="2.7" fill="var(--trace)" />
            );
          })}
        <circle
          cx={start[0]}
          cy={start[1]}
          r="7"
          fill="var(--paper)"
          stroke="var(--trace)"
          strokeWidth="3"
        />
        <text x={start[0] + 13} y={start[1] - 12} className="map-label">
          START
        </text>
        <rect
          x={goal[0] - 7}
          y={goal[1] - 7}
          width="14"
          height="14"
          fill="var(--paper)"
          stroke="var(--ink)"
          strokeWidth="2"
        />
        <path
          d={`M ${goal[0] + 13} ${goal[1] - 10} L ${goal[0] + 29} ${goal[1] - 26} H ${goal[0] + 78}`}
          fill="none"
          stroke="var(--reference)"
        />
        <text x={goal[0] + 32} y={goal[1] - 31} className="map-label">
          GOAL
        </text>
        {recurrence.length > 0 && (
          <g
            className={hero ? "recurrence-mark pulse-once" : "recurrence-mark"}
          >
            <polyline
              points={points(recurrence)}
              fill="none"
              stroke="var(--amber)"
              strokeWidth="5"
            />
            {recurrence.map((cell) => {
              const p = point(cell);
              return (
                <g key={cell.join()}>
                  <circle
                    cx={p[0]}
                    cy={p[1]}
                    r="12"
                    fill="var(--amber-wash)"
                    fillOpacity=".55"
                    stroke="var(--amber)"
                    strokeWidth="1.5"
                  />
                  <circle cx={p[0]} cy={p[1]} r="4" fill="var(--amber)" />
                </g>
              );
            })}
            <path
              d="M 78 416 V 281 H 119"
              fill="none"
              stroke="var(--amber)"
              strokeWidth="1"
            />
            <text x="87" y="257" className="recurrence-label">
              LEGAL RECURRENCE
            </text>
            <text x="87" y="275" className="recurrence-coordinate">
              (14,1) ↔ (13,0)
            </text>
          </g>
        )}
        <text x="64" y="520" className="axis-label">
          15 × 15 / CONTROLLED 2-D GRID
        </text>
        <text x="484" y="520" textAnchor="end" className="axis-label">
          ROW ↓
        </text>
      </svg>
      <figcaption className="plot-legend">
        <span>
          <i className="legend-line" />
          Controller
        </span>
        <span>
          <i className="legend-line reference" />
          A* reference
        </span>
        {!scenario.success && (
          <span>
            <i className="legend-ring" />
            Recurrence
          </span>
        )}
        <span>
          <i className="legend-block" />
          Blocked
        </span>
      </figcaption>
    </figure>
  );
}
