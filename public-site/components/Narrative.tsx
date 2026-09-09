import { CopyHash } from "./CopyHash";
import { provenance } from "../content/evidence";
import {
  founders,
  roadmap,
  submissionVerification,
  workflow,
} from "../content/site";
import "./narrative.css";

function Label({
  number,
  children,
}: {
  number: string;
  children: React.ReactNode;
}) {
  return (
    <p className="n-label">
      <span>{number}</span>
      {children}
    </p>
  );
}

function Arrow({ diagonal = false }: { diagonal?: boolean }) {
  return (
    <svg aria-hidden="true" viewBox="0 0 24 24" width="24" height="24">
      <path
        d={diagonal ? "M6 18 18 6M6 6h12v12" : "M4 12h16m-7-7 7 7-7 7"}
        fill="none"
        stroke="currentColor"
        strokeWidth="1.5"
      />
    </svg>
  );
}

export function Narrative() {
  return (
    <>
      <section className="n-bridge" aria-labelledby="n-thesis">
        <div className="n-wrap">
          <Label number="01">The evaluation blind spot</Label>
          <h2 id="n-thesis">
            Legal action selection does not by itself guarantee{" "}
            <span>mission liveness.</span>
          </h2>
          <div className="n-bridge-foot">
            <p className="n-principle">
              The point is not that one algorithm wins. The point is that
              legality alone did not expose the failure.
            </p>
            <p>
              MEHWAR captures controller behavior as trajectory evidence,
              preserves diagnostics, records mission-liveness outcomes, and
              provides deterministic reference context.
            </p>
          </div>
        </div>
      </section>

      <section
        id="workflow"
        className="n-workflow"
        aria-labelledby="n-workflow-title"
      >
        <div className="n-wrap n-workflow-layout">
          <div className="n-workflow-intro">
            <Label number="02">Research → product</Label>
            <h2 id="n-workflow-title">
              A research question.
              <br />
              <span>A working evaluator.</span>
            </h2>
            <p className="n-research-question">
              Our UAV dynamic-routing research exposed a simple evaluation
              question: does obeying local movement constraints actually mean
              the controller is still progressing toward the mission?
            </p>
            <p>
              We built MEHWAR to turn that question into a reproducible
              evaluation workflow.
            </p>
            <div className="n-workflow-caption">
              <span className="n-status-dot" aria-hidden="true" />
              <p>
                Research-backed autonomy-assurance MVP
                <span>
                  Controlled 2-D grid-based mission-routing abstraction
                </span>
              </p>
            </div>
          </div>
          <div className="n-system">
            <div className="n-system-heading">
              <span>The current workflow</span>
              <span>Input → evidence</span>
            </div>
            <ol className="n-pipeline">
              {workflow.map(([title, description, artifact], index) => (
                <li key={title}>
                  <span className="n-stage-index" aria-hidden="true">
                    {String(index + 1).padStart(2, "0")}
                  </span>
                  <details name="mehwar-workflow" open={index === 0}>
                    <summary>
                      <h3>{title}</h3>
                      <span className="n-plus" aria-hidden="true">
                        +
                      </span>
                    </summary>
                    <div className="n-stage-body">
                      <p>{description}</p>
                      <span className="n-artifact">{artifact}</span>
                    </div>
                  </details>
                </li>
              ))}
            </ol>
            <p className="n-system-output">
              <Arrow />
              <span>
                Engineer-facing trajectory evidence, JSON, and human-readable
                reports.
              </span>
            </p>
          </div>
        </div>
      </section>

      <section
        id="boundaries"
        className="n-boundaries"
        aria-labelledby="n-boundaries-title"
      >
        <div className="n-wrap">
          <Label number="03">Interpretation boundaries</Label>
          <div className="n-boundary-intro">
            <h2 id="n-boundaries-title">
              Map the boundary.
              <br />
              <span>Keep the claim inside it.</span>
            </h2>
            <p>
              MEHWAR characterizes navigation-controller capability boundaries.
              What the evidence establishes matters as much as what it does not.
            </p>
          </div>
          <div className="n-boundary-map">
            <div className="n-observed">
              <div className="n-boundary-caption">
                <span className="n-region-mark" aria-hidden="true" />
                Selected controlled evidence
              </div>
              <h3>Observed</h3>
              <ul>
                <li>Action-legal behavior lost mission liveness in C4-0001.</li>
                <li>
                  Trajectories and separate diagnostics are preserved
                  reproducibly.
                </li>
                <li>
                  Recurrence is classified under explicit, versioned semantics.
                </li>
                <li>
                  Deterministic reference context supports interpretation.
                </li>
              </ul>
            </div>
            <div className="n-unestablished">
              <div className="n-boundary-caption">
                <span className="n-region-mark" aria-hidden="true" />
                Further validation required
              </div>
              <h3>Not established</h3>
              <ul>
                <li>Flight validation</li>
                <li>Deployment readiness</li>
                <li>Certification</li>
                <li>Generic UAV robustness</li>
                <li>HIL or OEM validation</li>
                <li>External autonomy-stack validation</li>
                <li>Generic PPO or planner superiority</li>
                <li>Collision-safety guarantees</li>
                <li>Product-market validation</li>
              </ul>
            </div>
          </div>
          <div className="n-boundary-foot">
            <span>Conceptual boundary · not a measured capability surface</span>
            <p>
              Two selected development-validation cases. Not a statistically
              representative benchmark or a fresh physically sealed holdout.
              MEHWAR is an evaluation workflow, not a planner or simulator
              replacement.
            </p>
          </div>
        </div>
      </section>

      <section
        id="provenance"
        className="n-provenance"
        aria-labelledby="n-provenance-title"
      >
        <div className="n-wrap n-provenance-layout">
          <div className="n-provenance-intro">
            <Label number="04">Reproducibility</Label>
            <h2 id="n-provenance-title">
              Evidence with
              <br />
              <span>an identity.</span>
            </h2>
            <p>
              A result is only useful if you can trace it back. These selected
              records remain tied to their frozen source, checkpoint, scenario
              contract, and failure protocol.
            </p>
            <a
              className="n-inline-link"
              href="/evidence/selected-runs.json"
              download
            >
              Download recorded evidence <Arrow diagonal />
            </a>
          </div>
          <div className="n-dossier">
            <div className="n-dossier-heading">
              <span>Evidence fingerprint</span>
              <span className="n-dossier-stamp">Frozen submission source</span>
            </div>
            <CopyHash
              label="Frozen MVP source SHA"
              value={provenance.frozen_mvp_sha}
            />
            <CopyHash
              label="Checkpoint SHA256"
              value={provenance.checkpoint_sha256}
            />
            <dl className="n-contract">
              <div>
                <dt>Failure protocol</dt>
                <dd>
                  <code>{provenance.failure_protocol}</code>
                </dd>
              </div>
              <div>
                <dt>Scenario classification</dt>
                <dd>
                  <code>{provenance.scenario_classification}</code>
                </dd>
              </div>
              <div>
                <dt>Fresh holdout</dt>
                <dd>
                  <code>{String(provenance.fresh_holdout)}</code>
                </dd>
              </div>
            </dl>
            <div className="n-verification">
              <h3>Implementation verification — not a safety score</h3>
              <p>Recorded submission verification</p>
              <ul>
                <li>
                  <strong>{submissionVerification.testsPassed}</strong> tests
                  passed
                </li>
                <li>
                  <strong>{submissionVerification.testsSkipped}</strong> skipped
                </li>
                <li>
                  Ruff <strong>{submissionVerification.ruff}</strong>
                </li>
                <li>
                  <code>git diff --check</code>{" "}
                  <strong>{submissionVerification.diffCheck}</strong>
                </li>
              </ul>
            </div>
            <a className="n-snapshot-link" href="/deftech-2026">
              <span>
                <strong>DEFTECH 2026</strong>
                <span>The immutable submission snapshot</span>
              </span>
              <Arrow diagonal />
            </a>
          </div>
        </div>
      </section>

      <section
        id="roadmap"
        className="n-roadmap"
        aria-labelledby="n-roadmap-title"
      >
        <div className="n-wrap">
          <Label number="05">The validation path</Label>
          <div className="n-roadmap-intro">
            <h2 id="n-roadmap-title">
              The next step is
              <br />
              <span>a harder question.</span>
            </h2>
            <div>
              <p>
                The submission captures the first validated MEHWAR build, not
                the ceiling of the product.
              </p>
              <p className="n-roadmap-caveat">
                Proposed validation sequence. Each stage is a question to
                resolve, not a capability already established.
              </p>
            </div>
          </div>
          <ol className="n-questions">
            {roadmap.map(([title, question], index) => (
              <li key={title}>
                <span className="n-question-number">
                  {String(index + 1).padStart(2, "0")}
                </span>
                <h3>{title}</h3>
                <p>{question}</p>
              </li>
            ))}
          </ol>
          <div className="n-deftech">
            <span className="n-small-label">Why DEFTECH / why now</span>
            <div>
              <h3>
                Our next bottleneck is external validation, not building the
                first prototype.
              </h3>
              <p>
                Technical-user feedback, UAV/OEM workflows, external-stack
                integration, and higher-fidelity environments can challenge the
                evidence. We seek NUST R&amp;D/lab access and prospective
                pilot/adoption pathways to shape that next validation.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section id="team" className="n-team" aria-labelledby="n-team-title">
        <div className="n-wrap">
          <Label number="06">The people behind the evidence</Label>
          <div className="n-team-intro">
            <h2 id="n-team-title">
              Research to assurance.
              <br />
              <span>Product to integration.</span>
            </h2>
            <p>
              MEHWAR combines research/assurance ownership with
              product/integration ownership. The project grew from UAV
              dynamic-routing research and has already been translated into a
              functioning, reproducible evaluation workflow.
            </p>
          </div>
          <div className="n-founders">
            {founders.map((founder) => (
              <article key={founder.name} className="n-founder">
                <span className="n-founder-institution">
                  {founder.shortInstitution}
                </span>
                <h3>{founder.name}</h3>
                <p className="n-founder-role">{founder.role}</p>
                <div className="n-founder-credentials">
                  <p>{founder.faculty}</p>
                  <p>{founder.institution}</p>
                  <p>{founder.location}</p>
                </div>
              </article>
            ))}
          </div>
          <div id="collaborate" className="n-collaborate">
            <div className="n-collaborate-heading">
              <span className="n-small-label">Technical collaboration</span>
              <h2>
                Challenge the workflow.
                <br />
                Shape what comes next.
              </h2>
              <p>
                We are actively seeking UAV/autonomy engineers, researchers,
                integrators and OEM teams as technical reviewers and prospective
                design partners to challenge the workflow and help define the
                most valuable integration paths.
              </p>
            </div>
            <div className="n-contacts">
              <p>Discuss Technical Validation</p>
              {founders.map((founder) => (
                <a
                  key={founder.email}
                  href={`mailto:${founder.email}?subject=MEHWAR%20%E2%80%94%20Technical%20Validation%20Discussion`}
                >
                  <span>
                    <strong>{founder.name}</strong>
                    <span>{founder.role.replace("Co-founder — ", "")}</span>
                    <span className="n-contact-email">{founder.email}</span>
                  </span>
                  <Arrow diagonal />
                </a>
              ))}
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
