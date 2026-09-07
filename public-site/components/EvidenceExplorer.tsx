import {
  scenarios,
  provenance,
  type EvidenceScenario,
} from "../content/evidence";
import { referenceLabel } from "../content/site";
import { TrajectoryVisual } from "./TrajectoryVisual";
import { CopyHash } from "./CopyHash";

function EvidenceRecord({
  scenario,
  index,
}: {
  scenario: EvidenceScenario;
  index: number;
}) {
  return (
    <section
      id={`evidence-panel-${index}`}
      className={`evidence-panel ${scenario.success ? "completion-record" : "degradation-record"}`}
      aria-labelledby={`scenario-${index}-label`}
    >
      <div className="record-top">
        <p className="evidence-label">{scenario.evidenceLabel}</p>
        <span className="record-context">
          Selected development-validation run
        </span>
      </div>
      <div className="record-layout">
        <div className="record-reading">
          <p className="eyebrow">{scenario.scenario_id} / OBSERVATION</p>
          <h3>
            {scenario.success ? (
              <>
                The mission
                <br />
                completed.
              </>
            ) : (
              <>
                0 invalid actions.
                <br />
                <span>Mission still failed.</span>
              </>
            )}
          </h3>
          <p>{scenario.interpretation}</p>
          <dl className="record-metrics">
            <div>
              <dt>Controller steps</dt>
              <dd>{scenario.steps}</dd>
            </div>
            <div>
              <dt>Invalid actions</dt>
              <dd>{scenario.diagnostics.invalid_actions}</dd>
            </div>
            <div>
              <dt>Mission outcome</dt>
              <dd className="text-value">
                {scenario.success ? "Completed" : "Not completed"}
              </dd>
            </div>
            <div>
              <dt>Recorded classification</dt>
              <dd className="text-value">
                <code>{scenario.failure_type}</code>
              </dd>
            </div>
          </dl>
          <p className="controller-cost">
            Controller path cost <code>{scenario.path_cost.toFixed(3)}</code>
            <span>Exact precision below</span>
          </p>
          <div className="reference-reading">
            <span className="eyebrow">TASK-FEASIBILITY CONTEXT</span>
            <p>{referenceLabel}</p>
            <span className="mono">
              {scenario.reference_result.steps} steps ·{" "}
              {scenario.reference_result.cost.toFixed(3)} path cost
            </span>
          </div>
        </div>
        <div className="record-visual">
          <TrajectoryVisual scenario={scenario} id={`explorer-${index}`} />
          <p className="plot-note">
            Original recorded coordinates · solid controller trace · dashed
            reference context
          </p>
        </div>
      </div>
      <details className="technical-details">
        <summary>
          <span>
            Inspect technical evidence{" "}
            <span className="detail-hint">
              Exact values, contracts & provenance
            </span>
          </span>
          <span className="disclosure-symbol" aria-hidden="true">
            +
          </span>
        </summary>
        <div className="technical-body">
          <dl className="technical-grid">
            <div>
              <dt>Scenario ID</dt>
              <dd>
                <code>{scenario.scenario_id}</code>
              </dd>
            </div>
            <div>
              <dt>Outcome / classification</dt>
              <dd>
                <code>{scenario.failure_type}</code>
              </dd>
            </div>
            <div>
              <dt>Controller path cost · exact</dt>
              <dd>
                <code>{scenario.path_cost}</code>
              </dd>
            </div>
            <div>
              <dt>A* reference path cost · exact</dt>
              <dd>
                <code>{scenario.reference_result.cost}</code>
              </dd>
            </div>
            <div>
              <dt>Controller / reference steps</dt>
              <dd>
                {scenario.steps} / {scenario.reference_result.steps}
              </dd>
            </div>
            <div>
              <dt>Invalid actions · separate diagnostic</dt>
              <dd>{scenario.diagnostics.invalid_actions}</dd>
            </div>
            <div>
              <dt>Failure protocol</dt>
              <dd>
                <code>{scenario.configuration.failure_protocol}</code>
              </dd>
            </div>
            <div>
              <dt>Fresh holdout</dt>
              <dd>
                <code>false</code>
              </dd>
            </div>
            <div>
              <dt>Environment abstraction</dt>
              <dd>
                Controlled 2-D grid-based mission routing; static obstacles
              </dd>
            </div>
            <div>
              <dt>Evidence classification</dt>
              <dd>
                <code>{scenario.provenance.data_classification}</code>
              </dd>
            </div>
            <div>
              <dt>Movement contract</dt>
              <dd>
                <code>{scenario.configuration.movement_contract}</code>
              </dd>
            </div>
            <div>
              <dt>Step definition</dt>
              <dd>
                {scenario.configuration.step_definition}; episode budget{" "}
                {scenario.configuration.episode_budget}
              </dd>
            </div>
          </dl>
          <p>
            Eight-connected movement. Destination-cell-only validity; corner
            cutting allowed. Orthogonal cost 1; diagonal cost √2. Invalid
            actions remain separate from mission-liveness classification.
          </p>
          <CopyHash
            label="Frozen MVP source SHA"
            value={provenance.frozen_mvp_sha}
          />
          <CopyHash
            label="Checkpoint SHA256"
            value={provenance.checkpoint_sha256}
          />
          <p className="small">
            Selected development-validation evidence. No fresh physically sealed
            holdout, statistically representative benchmark, flight validation
            or safety certification. Classification is read from the frozen
            export; the website does not run an evaluator.
          </p>
          <details className="coordinate-details">
            <summary>
              Read the controller trajectory as coordinates{" "}
              <span aria-hidden="true">+</span>
            </summary>
            <p>
              Coordinates are (row, column), in recorded order, including
              repeated states.
            </p>
            <p className="coordinate-trace mono">
              {scenario.trajectory
                .map((cell) => `(${cell.join(", ")})`)
                .join(" → ")}
            </p>
          </details>
        </div>
      </details>
      <div className="record-links">
        <a href={scenario.screenshot} target="_blank" rel="noreferrer">
          View original evaluator screenshot <span aria-hidden="true">↗</span>
          <span className="sr-only">
            {" "}
            — {scenario.scenario_id}, opens a new tab
          </span>
        </a>
        <a href="/evidence/selected-runs.json" download>
          Download recorded evidence <span aria-hidden="true">↓</span>
        </a>
      </div>
    </section>
  );
}
export function EvidenceExplorer() {
  return (
    <fieldset className="explorer">
      <legend className="sr-only">Select a recorded evidence scenario</legend>
      <div className="scenario-selector">
        {scenarios.map((scenario, index) => (
          <label
            key={scenario.scenario_id}
            className="scenario-option"
            id={`scenario-${index}-label`}
          >
            <input
              type="radio"
              name="evidence-scenario"
              value={scenario.scenario_id}
              id={`scenario-${index}`}
              defaultChecked={index === 0}
              aria-controls={`evidence-panel-${index}`}
            />
            <span>
              <strong className="mono">{scenario.scenario_id}</strong>
              <span>
                {scenario.success
                  ? "Mission completion"
                  : "Liveness degradation"}
              </span>
            </span>
            <span className="selection-mark" aria-hidden="true">
              ↗
            </span>
          </label>
        ))}
      </div>
      {scenarios.map((scenario, index) => (
        <EvidenceRecord
          key={scenario.scenario_id}
          scenario={scenario}
          index={index}
        />
      ))}
    </fieldset>
  );
}
