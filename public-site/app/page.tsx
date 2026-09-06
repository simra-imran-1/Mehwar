import Image from "next/image";
import {
  referenceLabel,
  siteConfig,
  submissionSnapshot as snapshot,
} from "../content/site";

const workflow = [
  ["Controller", "Verified MaskablePPO controller adapter"],
  ["Scenario runner", "Selected structured C4 scenarios"],
  ["Trajectory recorder", "Trajectory and diagnostic capture"],
  [
    "Failure intelligence",
    "Versioned mission-liveness and failure semantics; invalid actions recorded separately",
  ],
  ["Deterministic reference", referenceLabel],
  ["Evidence profile", "Provenance and explicit limitations"],
  [
    "Dashboard + report",
    "Engineer-facing trajectories, JSON and human-readable reporting",
  ],
];
const roadmap = [
  "Technical-user discovery with UAV/autonomy engineers",
  "External controller / autonomy-stack integration",
  "Broader structured scenario coverage",
  "Higher-fidelity simulation / SIL evaluation",
  "Cross-fidelity evidence study",
  "Controlled lab / HIL-style validation where feasible",
  "Pilot / design-partner specification",
];

function SectionHeading({
  number,
  label,
  title,
}: {
  number: string;
  label: string;
  title: string;
}) {
  return (
    <div className="section-heading">
      <p className="eyebrow">
        <span>{number}</span> {label}
      </p>
      <h2>{title}</h2>
    </div>
  );
}

function EvidenceImage({
  scenario,
  success = false,
}: {
  scenario: string;
  success?: boolean;
}) {
  const path = success
    ? "/c4-0000-success.png"
    : "/c4-0001-liveness-degradation.png";
  return (
    <figure className="evidence-image">
      <a
        href={path}
        target="_blank"
        rel="noreferrer"
        aria-label={`Open full-size ${scenario} dashboard evidence`}
      >
        <Image
          src={path}
          width={1920}
          height={1065}
          sizes="(max-width: 800px) 100vw, 1200px"
          alt={`Frozen MEHWAR dashboard for ${scenario}: ${success ? "mission completed in 16 steps with zero invalid actions" : "mission not completed; two-cell recurrence in 28 steps with zero invalid actions"}. Trajectory and deterministic reference are shown.`}
        />
      </a>
      <figcaption>
        Frozen dashboard · {scenario} · Selected controlled scenario{" "}
        <span>Open full-size ↗</span>
      </figcaption>
    </figure>
  );
}

export default function Home() {
  return (
    <>
      <a className="skip-link" href="#main">
        Skip to content
      </a>
      <header className="site-header">
        <a className="wordmark" href="#" aria-label="MEHWAR home">
          <span className="brand-mark" aria-hidden="true">
            M
          </span>
          MEHWAR
        </a>
        <nav aria-label="Main navigation">
          <a href="#workflow">Workflow</a>
          <a href="#evidence">Evidence</a>
          <a href="#boundaries">Limitations</a>
          <a href="#team">Team</a>
        </nav>
        <a className="nav-cta" href="#collaborate">
          Technical collaboration <span aria-hidden="true">↗</span>
        </a>
      </header>
      <main id="main">
        <section className="hero wrap">
          <div className="snapshot-line">
            <span className="status-dot" />
            {snapshot.title} · {snapshot.date}
          </div>
          <div className="hero-layout">
            <div>
              <p className="eyebrow descriptor">
                Autonomy-assurance evaluation for navigation controllers
              </p>
              <h1>
                Legal action selection does not by itself guarantee{" "}
                <em>mission liveness.</em>
              </h1>
              <p className="hero-copy">
                MEHWAR is a research-backed MVP for characterizing where
                autonomous navigation controllers lose mission progress and how
                those failures appear in trajectory evidence.
              </p>
              <div className="actions">
                <a className="button primary" href="#evidence">
                  View Current Evidence <span aria-hidden="true">↘</span>
                </a>
                <a
                  className="button"
                  href={siteConfig.snapshotUrl || "#snapshot"}
                >
                  Submission Snapshot
                </a>
              </div>
            </div>
            <aside className="hero-note">
              <p className="eyebrow">The evaluation question</p>
              <p className="question">
                Is the controller still moving <span>toward the mission?</span>
              </p>
              <div className="signal-row">
                <span>Action legality</span>
                <strong>0 invalid actions</strong>
              </div>
              <div className="signal-row amber">
                <span>Mission outcome</span>
                <strong>Not completed</strong>
              </div>
              <p className="small">
                Selected case C4-0001. Controlled 2-D grid-based mission-routing
                abstraction.
              </p>
              <a className="text-link" href="#evidence">
                Inspect the evidence <span aria-hidden="true">↓</span>
              </a>
            </aside>
          </div>
          <div className="hero-bottom">
            <span>Research-backed functional prototype</span>
            <span>
              Mission-liveness diagnostics and reproducible trajectory evidence
            </span>
          </div>
        </section>

        <section className="research section wrap">
          <SectionHeading
            number="01"
            label="Research → product"
            title="A research finding. An evaluation workflow."
          />
          <div className="section-copy">
            <p>
              Our UAV dynamic-routing research exposed a simple evaluation
              question: does obeying local movement constraints actually mean
              the controller is still progressing toward the mission?
            </p>
            <p className="emphasis">
              We built MEHWAR to turn that question into a reproducible
              evaluation workflow.
            </p>
          </div>
        </section>

        <section id="workflow" className="section wash">
          <div className="wrap">
            <SectionHeading
              number="02"
              label="What MEHWAR does today"
              title="Follow the behavior. Preserve the evidence."
            />
            <p className="intro">
              Navigation-controller capability-boundary evaluation, from a
              selected scenario to an inspectable evidence record.
            </p>
            <ol className="workflow">
              {workflow.map(([title, text], index) => (
                <li key={title}>
                  <span className="step-number">
                    {String(index + 1).padStart(2, "0")}
                  </span>
                  <h3>{title}</h3>
                  <p>{text}</p>
                </li>
              ))}
            </ol>
          </div>
        </section>

        <section id="evidence" className="section wrap">
          <SectionHeading
            number="03"
            label="Current evidence"
            title="Zero illegal actions. Still failed to make mission progress."
          />
          <p className="intro">
            This observation belongs to selected demo case{" "}
            <strong>C4-0001</strong>. Two selected development-validation
            scenarios illustrate the workflow; they are not a statistically
            representative benchmark or a fresh physical holdout.
          </p>
          <article className="case primary-case">
            <div className="case-top">
              <div>
                <p className="eyebrow">
                  C4-0001 · Selected controlled scenario
                </p>
                <h3>Mission not completed</h3>
              </div>
              <span className="badge amber-badge">
                Liveness degradation observed
              </span>
            </div>
            <div className="metrics">
              <div>
                <strong>28</strong>
                <span>Controller steps</span>
              </div>
              <div>
                <strong>0</strong>
                <span>Invalid actions</span>
              </div>
              <div>
                <strong className="mono failure">two_cell_loop</strong>
                <span>Failure classification</span>
              </div>
            </div>
            <EvidenceImage scenario="C4-0001" />
            <div className="case-reading">
              <p>
                In this selected controlled scenario, zero invalid actions were
                recorded, yet the controller entered a legal two-cell recurrence
                and did not complete the mission.
              </p>
              <p className="emphasis">
                The point is not that one algorithm wins. The point is that
                legality alone did not expose the failure.
              </p>
            </div>
            <div className="costs">
              <p>
                <span>Controller path cost</span>
                <code>37.112698372208094</code>
              </p>
              <p>
                <span>{referenceLabel}</span>
                <strong>
                  14 steps <span aria-hidden="true">·</span>{" "}
                  <code>16.071067811865476</code> path cost
                </strong>
              </p>
            </div>
          </article>
          <article className="case secondary-case">
            <div className="case-top">
              <div>
                <p className="eyebrow">
                  C4-0000 · Selected controlled scenario
                </p>
                <h3>Mission completed</h3>
              </div>
              <span className="badge">Completion recorded</span>
            </div>
            <p>
              The same evaluation workflow also records successful mission
              completion.
            </p>
            <div className="metrics">
              <div>
                <strong>16</strong>
                <span>Controller steps</span>
              </div>
              <div>
                <strong>0</strong>
                <span>Invalid actions</span>
              </div>
              <div>
                <strong className="mono compact">17.242640687119284</strong>
                <span>Controller path cost</span>
              </div>
            </div>
            <details>
              <summary>
                Inspect C4-0000 dashboard evidence{" "}
                <span aria-hidden="true">+</span>
              </summary>
              <EvidenceImage scenario="C4-0000" success />
            </details>
            <div className="costs">
              <p>
                <span>{referenceLabel}</span>
                <strong>
                  15 steps · <code>16.65685424949238</code> path cost
                </strong>
              </p>
            </div>
          </article>
          {siteConfig.demoVideo && (
            <section className="demo">
              <h3>Narrated demonstration</h3>
              <video controls preload="metadata" src={siteConfig.demoVideo}>
                Your browser does not support embedded video.
              </video>
            </section>
          )}
        </section>

        <section id="boundaries" className="section boundaries">
          <div className="wrap">
            <SectionHeading
              number="04"
              label="Interpretation boundaries"
              title="Evidence with explicit limits."
            />
            <div className="boundary-grid">
              <div>
                <h3>What this demonstrates</h3>
                <ul>
                  {[
                    "Selected controller behavior can remain action-legal while losing mission liveness",
                    "Trajectories and diagnostics can be preserved reproducibly",
                    "Recurrence can be classified under explicit versioned semantics",
                    "Deterministic reference context can help interpret the graph task",
                  ].map((t) => (
                    <li key={t}>{t}</li>
                  ))}
                </ul>
              </div>
              <div>
                <h3>What this does not demonstrate</h3>
                <ul className="limits">
                  {[
                    "Flight validation",
                    "Deployment readiness",
                    "Safety certification",
                    "Generic UAV robustness",
                    "PPO superiority",
                    "Planner superiority",
                    "Collision-safety guarantee",
                    "External OEM validation",
                  ].map((t) => (
                    <li key={t}>{t}</li>
                  ))}
                </ul>
              </div>
            </div>
            <p className="boundary-foot">
              A research-backed autonomy-assurance MVP in a controlled 2-D
              abstraction. No current customer validation, pilot, or external
              autonomy-stack validation is claimed.
            </p>
          </div>
        </section>

        <section id="snapshot" className="section wrap snapshot">
          <SectionHeading
            number="05"
            label="Immutable evidence snapshot"
            title="Current validated submission build"
          />
          <div className="snapshot-card">
            <div className="snapshot-title">
              <h3>{snapshot.title}</h3>
              <span>{snapshot.date}</span>
            </div>
            <dl>
              <div>
                <dt>Frozen branch</dt>
                <dd>
                  <code>{snapshot.branch}</code>
                </dd>
              </div>
              <div>
                <dt>MEHWAR source SHA</dt>
                <dd>
                  <code>{snapshot.sha}</code>
                </dd>
              </div>
              <div>
                <dt>Checkpoint SHA256</dt>
                <dd>
                  <code>{snapshot.checkpointSha256}</code>
                </dd>
              </div>
            </dl>
            <div className="verification">
              {snapshot.verification.map((v) => (
                <span key={v}>{v}</span>
              ))}
            </div>
            <p className="small">
              Implementation verification recorded for the frozen submission
              build. These are not safety scores or safety checks.
            </p>
          </div>
          <p className="small snapshot-caption">
            This page represents the DEFTECH submission snapshot. Future
            validated builds will be identified separately from this historical
            record.
          </p>
        </section>

        <section id="roadmap" className="section wash">
          <div className="wrap roadmap-layout">
            <div>
              <SectionHeading
                number="06"
                label="Roadmap · Next phase"
                title="From controlled evidence to external validation."
              />
              <p className="intro">
                The submission captures the first validated MEHWAR build, not
                the ceiling of the product.
              </p>
              <p className="small">
                Planned directions, dependent on access, integration findings
                and feasibility. No completion dates or validation outcomes are
                promised.
              </p>
            </div>
            <ol className="roadmap">
              {roadmap.map((r, i) => (
                <li key={r}>
                  <span>{String(i + 1).padStart(2, "0")}</span>
                  {r}
                </li>
              ))}
            </ol>
          </div>
        </section>

        <section className="section wrap research">
          <SectionHeading
            number="07"
            label="Why DEFTECH"
            title="Our next bottleneck is external validation, not building the first prototype."
          />
          <div className="section-copy">
            <p>
              DEFTECH can help us work with UAV/OEM technical stakeholders,
              understand real evaluation workflows, connect MEHWAR to stronger
              autonomy environments, and progress toward higher-fidelity and
              controlled lab validation.
            </p>
            <div className="tags">
              <span>OEM access</span>
              <span>NUST R&D/lab ecosystem</span>
              <span>Technical mentorship</span>
              <span>Adoption/pilot pathway</span>
            </div>
          </div>
        </section>

        <section id="collaborate" className="wrap collaboration">
          <p className="eyebrow">08 · Technical collaboration</p>
          <h2>Help define the next validation step.</h2>
          <p>
            We are actively seeking UAV/autonomy engineers, researchers,
            integrators, and OEM teams as technical reviewers and prospective
            design partners to challenge the workflow and help define the most
            valuable integration paths.
          </p>
          {siteConfig.contactMailto ? (
            <a className="button primary" href={siteConfig.contactMailto}>
              Discuss Technical Validation ↗
            </a>
          ) : (
            <div>
              <button className="button contact-pending" disabled>
                Discuss Technical Validation
              </button>
              <p className="small contact-note">
                Public contact channel will be added here.
              </p>
            </div>
          )}
        </section>

        <section id="team" className="section wrap">
          <SectionHeading
            number="09"
            label="Team"
            title="Research and integration, together."
          />
          <div className="team-grid">
            <div>
              <h3>Muzzammil Sajid</h3>
              <p>Co-founder — Research & Assurance</p>
              <span>GIKI</span>
            </div>
            <div>
              <h3>Simra Imran</h3>
              <p>Co-founder — Product & Integration</p>
              <span>NUST / SEECS</span>
            </div>
            <p>
              MEHWAR combines research/assurance ownership with
              product/integration ownership. The project grew from UAV
              dynamic-routing research and has already been translated into a
              functioning, reproducible evaluation workflow.
            </p>
          </div>
        </section>
      </main>
      <footer className="wrap">
        <div>
          <a className="wordmark" href="#">
            MEHWAR
          </a>
          <p>
            Evidence is tied to the tested scenario, controller/configuration,
            evaluation semantics, and environment.
          </p>
        </div>
        <div>
          <p>
            {snapshot.title}
            <br />
            {snapshot.date}
          </p>
          <code>Frozen source · {snapshot.sha.slice(0, 7)}</code>
        </div>
      </footer>
    </>
  );
}
