import { SiteHeader } from "../components/SiteHeader";
import { Brand } from "../components/Brand";
import { TrajectoryVisual } from "../components/TrajectoryVisual";
import { EvidenceExplorer } from "../components/EvidenceExplorer";
import { CopyHash } from "../components/CopyHash";
import { degradation, provenance } from "../content/evidence";
import { siteConfig, workflow, roadmap } from "../content/site";

function SectionLabel({
  number,
  children,
}: {
  number: string;
  children: React.ReactNode;
}) {
  return (
    <p className="eyebrow section-label">
      <span>{number}</span>
      {children}
    </p>
  );
}
export default function Home() {
  return (
    <>
      <a className="skip-link" href="#main">
        Skip to content
      </a>
      <SiteHeader />
      <main id="main">
        <section className="hero wrap" aria-labelledby="thesis">
          <div className="build-line">
            <span>
              <i aria-hidden="true" />
              Latest Validated Build{" "}
              <span className="build-date">/ September 2026 evidence</span>
            </span>
            <a href="/deftech-2026">
              View DEFTECH 2026 submission snapshot{" "}
              <span aria-hidden="true">↗</span>
            </a>
          </div>
          <div className="hero-layout">
            <div className="hero-editorial">
              <p className="hero-category">
                Autonomy-assurance evaluation
                <br className="desktop-break" /> for navigation controllers
              </p>
              <h1 id="thesis">
                Legal action selection does not by itself guarantee{" "}
                <em>mission liveness.</em>
              </h1>
              <p className="hero-copy">
                For UAV autonomy teams, MEHWAR turns navigation-controller runs
                into reproducible evidence about capability boundaries,
                trajectories, and mission-liveness failures.
              </p>
              <div className="actions">
                <a className="button primary" href="#evidence">
                  Inspect Evidence <span aria-hidden="true">↘</span>
                </a>
                <a className="text-link" href="#workflow">
                  Explore the workflow <span aria-hidden="true">→</span>
                </a>
              </div>
            </div>
            <div className="hero-instrument">
              <TrajectoryVisual scenario={degradation} hero id="hero" />
              <div className="hero-observation">
                <p>
                  <span className="observation-line" aria-hidden="true" />
                  Mission not completed <code>{degradation.failure_type}</code>
                </p>
                <span className="mono">
                  {degradation.steps} steps <span aria-hidden="true">/</span>{" "}
                  {degradation.diagnostics.invalid_actions} invalid actions
                </span>
              </div>
            </div>
          </div>
          <div className="hero-foot">
            <span>Research-backed functional prototype</span>
            <p>
              Current scope <span aria-hidden="true">/</span> Controlled 2-D
              grid-based mission-routing abstraction
            </p>
            <a href="#evidence" aria-label="Continue to selected evidence">
              <span aria-hidden="true">↓</span>
            </a>
          </div>
        </section>

        <section id="evidence" className="section evidence-section">
          <div className="wrap">
            <div className="section-intro">
              <div>
                <SectionLabel number="01">Selected evidence</SectionLabel>
                <h2>
                  Legality is one signal.
                  <br />
                  <span className="muted">Progress is another.</span>
                </h2>
              </div>
              <p>
                Two selected development-validation scenarios. One evaluation
                workflow. Inspect what happened, and the evidence behind it.
              </p>
            </div>
            <EvidenceExplorer />
            <div className="evidence-conclusion">
              <p>
                The point is not that one algorithm wins. The point is that
                legality alone did not expose the failure.
              </p>
              <span>
                Selected controlled cases.
                <br />
                Not a statistically representative benchmark
                <br className="desktop-break" /> or a fresh physically sealed
                holdout.
              </span>
            </div>
            {siteConfig.demoVideo &&
              siteConfig.demoCaptions &&
              siteConfig.demoTranscript && (
                <div className="demo-video">
                  <h3>Narrated demonstration</h3>
                  <video
                    controls
                    preload="none"
                    poster="/c4-0001-liveness-degradation.png"
                  >
                    <source src={siteConfig.demoVideo} type="video/mp4" />
                    <track
                      kind="captions"
                      src={siteConfig.demoCaptions}
                      srcLang="en"
                      label="English"
                      default
                    />
                  </video>
                  <a className="text-link" href={siteConfig.demoTranscript}>
                    Read the demonstration transcript ↗
                  </a>
                </div>
              )}
          </div>
        </section>

        <section id="workflow" className="section wrap workflow-section">
          <div className="section-intro">
            <div>
              <SectionLabel number="02">The current workflow</SectionLabel>
              <h2>
                From controller behavior
                <br />
                to inspectable evidence.
              </h2>
            </div>
            <p>
              MEHWAR is a research-backed autonomy-assurance MVP for
              characterizing where autonomous navigation controllers lose
              mission progress and how those failures appear in trajectory
              evidence.
            </p>
          </div>
          <ol className="workflow">
            {workflow.map(([title, text, fragment], index) => (
              <li key={title}>
                <details open={index === 0}>
                  <summary>
                    <span className="stage-node">
                      {String(index + 1).padStart(2, "0")}
                    </span>
                    <h3>{title}</h3>
                    <span className="stage-open" aria-hidden="true">
                      +
                    </span>
                  </summary>
                  <div>
                    <p>{text}</p>
                    <span className="stage-fragment">{fragment}</span>
                  </div>
                </details>
              </li>
            ))}
          </ol>
          <div className="research-note">
            <p className="eyebrow">RESEARCH → PRODUCT</p>
            <p>
              Our UAV dynamic-routing research exposed a simple evaluation
              question: does obeying local movement constraints actually mean
              the controller is still progressing toward the mission?
            </p>
            <p>
              We built MEHWAR to turn that question into a reproducible
              evaluation workflow.
            </p>
          </div>
        </section>

        <section id="boundaries" className="section boundary-section">
          <div className="wrap">
            <SectionLabel number="03">Interpretation boundaries</SectionLabel>
            <div className="boundary-heading">
              <h2>
                The boundary is
                <br />
                part of the evidence.
              </h2>
              <p>
                Every observation belongs to a tested scenario, controller,
                evaluation contract and environment. Knowing what remains
                unestablished is part of the product.
              </p>
            </div>
            <div className="boundary-columns">
              <div>
                <p className="boundary-overline">
                  <span aria-hidden="true">●</span> Evidence observed
                </p>
                <h3>
                  What the current
                  <br />
                  evidence demonstrates
                </h3>
                <ul>
                  {[
                    "Selected controller behavior can remain action-legal while losing mission liveness.",
                    "Trajectories and diagnostics can be preserved reproducibly.",
                    "Recurrence can be classified under explicit versioned semantics.",
                    "Deterministic task-reference context can be provided under the shared movement contract.",
                  ].map((text) => (
                    <li key={text}>{text}</li>
                  ))}
                </ul>
              </div>
              <div>
                <p className="boundary-overline">
                  <span aria-hidden="true">○</span> Evidence not established
                </p>
                <h3>
                  What the current
                  <br />
                  evidence does not demonstrate
                </h3>
                <ul className="limits">
                  {[
                    "Flight validation",
                    "Deployment readiness",
                    "Safety certification",
                    "Generic UAV robustness",
                    "Generic PPO superiority",
                    "Generic planner superiority",
                    "Collision-safety guarantee",
                    "External OEM validation",
                    "HIL validation",
                    "Product-market validation",
                  ].map((text) => (
                    <li key={text}>{text}</li>
                  ))}
                </ul>
              </div>
            </div>
            <p className="boundary-foot">
              Mission-liveness classification is a versioned diagnostic, not a
              certification or safety score. No current customer validation,
              pilot or external autonomy-stack validation is claimed.
            </p>
          </div>
        </section>

        <section id="provenance" className="section wrap provenance-section">
          <div>
            <SectionLabel number="04">Evidence provenance</SectionLabel>
            <h2>
              An observation
              <br />
              with a source.
            </h2>
            <p>
              Reproducible submission state.
              <br />
              The website evolves; the September evidence stays identifiable.
            </p>
            <a className="text-link" href="/deftech-2026">
              View DEFTECH 2026 submission snapshot{" "}
              <span aria-hidden="true">↗</span>
            </a>
            {siteConfig.evidenceArchiveUrl && (
              <a className="text-link" href={siteConfig.evidenceArchiveUrl}>
                View DEFTECH 2026 Evidence Snapshot{" "}
                <span aria-hidden="true">↗</span>
              </a>
            )}
          </div>
          <div className="provenance-record">
            <div className="provenance-row">
              <span>Frozen MEHWAR branch</span>
              <code>feat/integration-demo</code>
            </div>
            <CopyHash
              label="Frozen MVP source SHA"
              value={provenance.frozen_mvp_sha}
            />
            <CopyHash
              label="Checkpoint SHA256"
              value={provenance.checkpoint_sha256}
            />
            <div className="provenance-row">
              <span>Failure protocol</span>
              <code>{provenance.failure_protocol}</code>
            </div>
            <div className="provenance-row">
              <span>Scenario provenance</span>
              <code>{provenance.scenario_classification}</code>
            </div>
            <div className="verification">
              <p className="eyebrow">RECORDED SUBMISSION VERIFICATION</p>
              <p>
                137 tests passed <span>·</span> 0 skipped <span>·</span> Ruff
                PASS <span>·</span> diff check PASS
              </p>
              <span>Implementation verification — not a safety score</span>
            </div>
            <a className="text-link" href="/evidence/selected-runs.json">
              Inspect machine-readable provenance{" "}
              <span aria-hidden="true">↗</span>
            </a>
          </div>
        </section>

        <section id="roadmap" className="section roadmap-section">
          <div className="wrap roadmap-layout">
            <div className="roadmap-heading">
              <SectionLabel number="05">Next validation steps</SectionLabel>
              <h2>
                Expand the evidence.
                <br />
                <span className="muted">Reduce the uncertainty.</span>
              </h2>
              <p>
                The submission captures the first validated MEHWAR build, not
                the ceiling of the product.
              </p>
              <span className="planned-label">
                PLANNED / NOT CURRENT CAPABILITIES
              </span>
              <p className="small">
                Directions depend on access, integration findings and
                feasibility. No dates or validation outcomes are promised.
              </p>
            </div>
            <ol className="roadmap">
              {roadmap.map(([title, question], index) => (
                <li key={title}>
                  <span className="mono">
                    {String(index + 1).padStart(2, "0")}
                  </span>
                  <div>
                    <h3>{title}</h3>
                    <p>{question}</p>
                  </div>
                </li>
              ))}
            </ol>
          </div>
        </section>

        <section className="section wrap why-section">
          <SectionLabel number="06">Why DEFTECH</SectionLabel>
          <div className="why-layout">
            <h2>
              Our next bottleneck is external validation, not building the first
              prototype.
            </h2>
            <div>
              <p>
                The current environment is deliberately controlled and
                reproducible. The next question is whether the evidence remains
                useful in external autonomy stacks and higher-fidelity
                environments.
              </p>
              <p>
                DEFTECH can help connect the workflow to UAV/OEM technical
                stakeholders, external evaluation practice, the NUST R&amp;D/lab
                ecosystem, and adoption or pilot design.
              </p>
            </div>
          </div>
        </section>

        <section id="team" className="section wrap team-section">
          <div className="section-intro">
            <div>
              <SectionLabel number="07">The team</SectionLabel>
              <h2>
                Research & assurance.
                <br />
                Product & integration.
              </h2>
            </div>
            <p>
              MEHWAR combines research/assurance ownership with
              product/integration ownership. The project grew from UAV
              dynamic-routing research and has already been translated into a
              functioning, reproducible evaluation workflow.
            </p>
          </div>
          <div className="team">
            <article>
              <span className="team-number mono">01 / GIKI</span>
              <h3>Muzzammil Sajid</h3>
              <p>Co-founder — Research &amp; Assurance</p>
            </article>
            <article>
              <span className="team-number mono">02 / NUST · SEECS</span>
              <h3>Simra Imran</h3>
              <p>Co-founder — Product &amp; Integration</p>
            </article>
          </div>
        </section>

        <section id="collaborate" className="contact-section">
          <div className="wrap">
            <SectionLabel number="08">Technical collaboration</SectionLabel>
            <div className="contact-layout">
              <h2>
                Challenge the workflow.
                <br />
                Shape the next validation.
              </h2>
              <div>
                <p>
                  We are actively seeking UAV/autonomy engineers, researchers,
                  integrators and OEM teams as technical reviewers and
                  prospective design partners to challenge the workflow and help
                  define the most valuable integration paths.
                </p>
                {siteConfig.publicEmail ? (
                  <a
                    className="button primary"
                    href={`mailto:${siteConfig.publicEmail}?subject=MEHWAR%20%E2%80%94%20Technical%20Validation%20Discussion`}
                  >
                    Discuss Technical Validation{" "}
                    <span aria-hidden="true">↗</span>
                  </a>
                ) : (
                  <div className="contact-pending">
                    <h3>Discuss Technical Validation</h3>
                    <p>A public contact channel is not yet listed.</p>
                    <a className="text-link" href="/deftech-2026">
                      Explore the submission evidence{" "}
                      <span aria-hidden="true">↗</span>
                    </a>
                  </div>
                )}
              </div>
            </div>
          </div>
        </section>
      </main>
      <footer className="footer wrap">
        <div>
          <a href="#main" aria-label="MEHWAR home">
            <Brand />
          </a>
          <p>
            Map the boundary.
            <br />
            Build the evidence.
          </p>
        </div>
        <div className="footer-links">
          <a href="#evidence">Inspect Evidence ↗</a>
          <a href="/deftech-2026">DEFTECH 2026 submission snapshot ↗</a>
          <span>Controlled 2-D evidence · September 2026</span>
        </div>
      </footer>
    </>
  );
}
