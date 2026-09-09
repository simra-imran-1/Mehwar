"use client";

import { memo, useEffect, useRef, useState } from "react";
import Image from "next/image";
import {
  scenarios,
  provenance,
  type EvidenceScenario,
} from "../content/evidence";
import { referenceLabel } from "../content/site";
import { RecordedInstrument } from "./RecordedInstrument";
import { CopyHash } from "./CopyHash";

const TechnicalRecord = memo(function TechnicalRecord({
  scenario,
}: {
  scenario: EvidenceScenario;
}) {
  return (
    <>
      <dl className="technical-grid">
        <div>
          <dt>Scenario ID</dt>
          <dd>{scenario.scenario_id}</dd>
        </div>
        <div>
          <dt>Recorded classification</dt>
          <dd>{scenario.failure_type}</dd>
        </div>
        <div>
          <dt>Controller path cost · exact</dt>
          <dd>{scenario.path_cost}</dd>
        </div>
        <div>
          <dt>A* reference path cost · exact</dt>
          <dd>{scenario.reference_result.cost}</dd>
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
          <dd>{scenario.configuration.failure_protocol}</dd>
        </div>
        <div>
          <dt>Fresh holdout</dt>
          <dd>{String(scenario.provenance.fresh_holdout)}</dd>
        </div>
        <div>
          <dt>Scenario provenance</dt>
          <dd>{scenario.provenance.scenario_classification}</dd>
        </div>
        <div>
          <dt>Evidence classification</dt>
          <dd>{scenario.provenance.data_classification}</dd>
        </div>
        <div>
          <dt>Movement contract</dt>
          <dd>{scenario.configuration.movement_contract}</dd>
        </div>
        <div>
          <dt>Step definition / episode budget</dt>
          <dd>
            {scenario.configuration.step_definition} /{" "}
            {scenario.configuration.episode_budget}
          </dd>
        </div>
      </dl>
      <p className="contract-note">
        Controlled 2-D grid-based mission-routing abstraction. Eight-connected
        movement; destination-cell-only validity; corner cutting allowed.
        Orthogonal cost 1, diagonal cost √2. Invalid actions remain separate
        diagnostics. Classifications are read from frozen evidence; this website
        does not run an evaluator.
      </p>
      <div className="technical-hashes">
        <CopyHash
          label="Frozen MVP source SHA"
          value={provenance.frozen_mvp_sha}
        />
        <CopyHash
          label="Checkpoint SHA256"
          value={provenance.checkpoint_sha256}
        />
      </div>
      <details className="coordinates">
        <summary>
          Read all recorded coordinates <span aria-hidden="true">+</span>
        </summary>
        <p>
          Coordinates are (row, column), including the initial position and
          every repeated state.
        </p>
        <p className="coordinate-list">
          {scenario.trajectory
            .map((cell) => `(${cell.join(", ")})`)
            .join(" → ")}
        </p>
      </details>
    </>
  );
});

export function EvidenceExperience() {
  const [selection, setSelection] = useState({ index: 0, hasChosen: false });
  const selected = selection.index;
  const scenario = scenarios[selected];
  const [enhanced, setEnhanced] = useState(false);
  const viewer = useRef<HTMLDialogElement>(null);

  // Core evidence is already present in the server render. Enhancement enables
  // controls and hides the static fallback once, independently of playback.
  useEffect(() => {
    const frame = requestAnimationFrame(() => setEnhanced(true));
    return () => cancelAnimationFrame(frame);
  }, []);

  const choose = (index: number) => {
    setSelection({ index, hasChosen: true });
  };

  return (
    <section
      id="evidence"
      className={`evidence-stage ${scenario.success ? "case-complete" : "case-recurrence"}`}
      aria-labelledby="hero-heading"
    >
      <div className="stage-top v-wrap">
        <p className="v-eyebrow">
          Autonomy-assurance evaluation for navigation controllers
        </p>
        <a href="/deftech-2026">
          DEFTECH 2026 snapshot <span aria-hidden="true">↗</span>
        </a>
      </div>
      <div className="stage-layout v-wrap">
        <div className="stage-editorial">
          <p className="case-caption">
            <span className="case-marker" aria-hidden="true" />{" "}
            {scenario.scenario_id} <span>/ Selected controlled evidence</span>
          </p>
          <h1 id="hero-heading">
            {scenario.success ? (
              <>
                A completed mission.<em>The same scrutiny.</em>
              </>
            ) : (
              <>
                Every move legal.<em>Mission unfinished.</em>
              </>
            )}
          </h1>
          <p className="stage-definition">
            MEHWAR helps UAV autonomy teams find where navigation controllers
            stop making mission progress—and turn that behavior into
            reproducible evidence.
          </p>
          <div className="stage-actions">
            <a className="v-button" href="#recorded-run">
              Inspect the recorded run <span aria-hidden="true">↘</span>
            </a>
            <a className="v-text-link" href="#collaborate">
              Discuss Technical Validation <span aria-hidden="true">↗</span>
            </a>
          </div>
          <div className="legality-observation">
            <strong>{scenario.diagnostics.invalid_actions}</strong>
            <p>
              <span>invalid actions</span>
              <small>
                Recorded final-run total.
                <br />
                {scenario.success
                  ? "Mission completed in this selected run."
                  : "Mission still failed through legal recurrence."}
              </small>
            </p>
          </div>
          <p className="stage-scope">
            Latest Validated Build · September 2026 evidence
            <br />
            Research-backed functional prototype
            <br />
            <span>Controlled 2-D grid-based mission-routing abstraction</span>
          </p>
        </div>
        <RecordedInstrument
          key={scenario.scenario_id}
          scenario={scenario}
          enhanced={enhanced}
          autoPlayOnArrival={!selection.hasChosen}
        />
      </div>
      <div className="run-record v-wrap">
        <div className="record-toolbar">
          <fieldset className="scenario-selector">
            <legend>Select recorded evidence</legend>
            {scenarios.map((entry, index) => (
              <label
                className={index === selected ? "selected" : ""}
                key={entry.scenario_id}
              >
                <input
                  type="radio"
                  name="selected-scenario"
                  value={entry.scenario_id}
                  checked={index === selected}
                  onChange={() => choose(index)}
                  disabled={!enhanced}
                />
                <span>{entry.scenario_id}</span>
                <small>
                  {entry.success
                    ? "Mission completion"
                    : "Liveness degradation"}
                </small>
              </label>
            ))}
          </fieldset>
          <span className="v-mono final-record-label">
            RECORDED FINAL-RUN EVIDENCE
            <br />
            <span>Independent of playback position</span>
          </span>
        </div>
        <div className="final-outcome">
          <p className="evidence-label">{scenario.evidenceLabel}</p>
          <dl>
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
              <dd>{scenario.success ? "Completed" : "Not completed"}</dd>
            </div>
            <div>
              <dt>Recorded classification</dt>
              <dd>
                <code>{scenario.failure_type}</code>
              </dd>
            </div>
          </dl>
        </div>
        <div className="record-interpretation">
          <p>{scenario.interpretation}</p>
          <div>
            <span className="v-eyebrow">Task-feasibility context</span>
            <p>{referenceLabel}</p>
            <span className="v-mono">
              {scenario.reference_result.steps} steps /{" "}
              {scenario.reference_result.cost.toFixed(3)} path cost
            </span>
          </div>
        </div>
        <details className="technical-record">
          <summary>
            <span>
              Inspect the evidence fingerprint
              <small>Exact values, contract & provenance</small>
            </span>
            <span aria-hidden="true">+</span>
          </summary>
          <TechnicalRecord scenario={scenario} />
          <div className="artifact-actions">
            <button
              className="v-button"
              onClick={() => viewer.current?.showModal()}
              disabled={!enhanced}
            >
              Open original evaluator evidence <span aria-hidden="true">↗</span>
            </button>
            <a href={scenario.screenshot} target="_blank" rel="noreferrer">
              Original screenshot in a new tab ↗
            </a>
            <a href="/evidence/selected-runs.json" download>
              Download frozen JSON ↓
            </a>
          </div>
        </details>
        <p className="record-limit">
          Two selected development-validation scenarios. Not a statistically
          representative benchmark or a fresh physically sealed holdout.
        </p>
        <div className="static-evidence-fallback" hidden={enhanced}>
          <div className="no-js-evidence">
            <p>
              Interactive playback requires JavaScript. The complete{" "}
              {scenarios[0].scenario_id} trace and final evidence are shown
              above.
            </p>
            <h2>{scenarios[1].scenario_id} · secondary selected record</h2>
            <p>
              {scenarios[1].evidenceLabel}. Mission completed;{" "}
              {scenarios[1].failure_type}; {scenarios[1].steps} controller
              steps; {scenarios[1].diagnostics.invalid_actions} invalid actions.
              Controller path cost {scenarios[1].path_cost}. Deterministic A*
              reference: {scenarios[1].reference_result.steps} steps, path cost{" "}
              {scenarios[1].reference_result.cost}.
            </p>
            <a href="/deftech-2026">
              Inspect both original records in the historical snapshot ↗
            </a>
          </div>
        </div>
      </div>
      <dialog
        ref={viewer}
        className="evidence-viewer"
        aria-labelledby="viewer-title"
      >
        <div className="viewer-heading">
          <div>
            <span className="v-eyebrow">Original evaluator artifact</span>
            <h2 id="viewer-title">{scenario.scenario_id}</h2>
          </div>
          <form method="dialog">
            <button aria-label="Close original evidence viewer">
              Close <span aria-hidden="true">×</span>
            </button>
          </form>
        </div>
        {/* Original immutable evidence, deliberately untransformed. */}
        <Image
          unoptimized
          loading="lazy"
          src={scenario.screenshot}
          width="1920"
          height="1065"
          alt={`Original evaluator screenshot for ${scenario.scenario_id}, showing the recorded trajectory, diagnostics, and interpretation boundaries.`}
        />
        <div className="viewer-footer">
          <span>Unedited final T13 evaluator screenshot</span>
          <a href={scenario.screenshot} target="_blank" rel="noreferrer">
            Open full resolution in a new tab ↗
          </a>
        </div>
      </dialog>
    </section>
  );
}
