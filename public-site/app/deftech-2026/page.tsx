import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import snapshot from "../../content/submission-2026.json";
import styles from "./snapshot.module.css";

export const metadata: Metadata = {
  title: { absolute: "MEHWAR — DEFTECH 2026 Submission Snapshot" },
  description:
    "Historical September 2026 record of MEHWAR’s selected controller evidence, frozen source provenance and explicit capability boundaries.",
  alternates: { canonical: "https://mehwar-deftech.vercel.app/deftech-2026" },
  openGraph: {
    title: "MEHWAR — DEFTECH 2026 Submission Snapshot",
    description: "Frozen September 2026 evidence. Selected C4 scenarios, reproducible provenance and explicit interpretation boundaries.",
    url: "https://mehwar-deftech.vercel.app/deftech-2026",
    type: "website",
    images: [{ url: "/c4-0001-liveness-degradation.png", width: 1920, height: 1065, alt: "Original C4-0001 evaluator evidence" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "MEHWAR — DEFTECH 2026 Submission Snapshot",
    description: "Frozen September 2026 evidence and interpretation boundaries.",
    images: ["/c4-0001-liveness-degradation.png"],
  },
};

export default function SubmissionSnapshot() {
  const provenance = snapshot.provenance;

  return (
    <div className={styles.snapshot}>
      <a className={styles.skipLink} href="#snapshot-main">Skip to historical record</a>
      <header className={styles.header}>
        <Link className={styles.wordmark} href="/" aria-label="MEHWAR homepage">MEHWAR</Link>
        <Link className={styles.returnLink} href="/">Latest validated build <span aria-hidden="true">↗</span></Link>
      </header>

      <main id="snapshot-main" className={styles.main}>
        <section className={styles.hero} aria-labelledby="snapshot-title">
          <p className={styles.eyebrow}>Historical record · {snapshot.date}</p>
          <h1 id="snapshot-title">DEFTECH 2026<br /><span>Submission snapshot.</span></h1>
          <p className={styles.notice}>{snapshot.historicalNotice}</p>
          <nav className={styles.contents} aria-label="Historical record contents">
            <a href="#submission-evidence">Selected evidence <span aria-hidden="true">↓</span></a>
            <a href="#submission-scope">Scope &amp; limitations <span aria-hidden="true">↓</span></a>
            <a href="#submission-provenance">Provenance <span aria-hidden="true">↓</span></a>
            <a href="#submission-team">Team <span aria-hidden="true">↓</span></a>
          </nav>
        </section>

        <section className={styles.thesis} aria-labelledby="submission-thesis">
          <p className={styles.eyebrow}>{snapshot.category}</p>
          <h2 id="submission-thesis">{snapshot.thesis}</h2>
          <p>{snapshot.definition}</p>
          <p className={styles.environment}>{snapshot.environment}</p>
        </section>

        <section id="submission-evidence" className={styles.section} aria-labelledby="evidence-title">
          <div className={styles.sectionHeading}>
            <p className={styles.eyebrow}>01 / Selected evidence</p>
            <h2 id="evidence-title">The submission’s evidence record.</h2>
            <p>{snapshot.selectionCaveat}</p>
          </div>
          {snapshot.scenarios.map((scenario) => (
            <article className={styles.scenario} key={scenario.id} aria-labelledby={`record-${scenario.id}`}>
              <div className={styles.scenarioHeading}>
                <div>
                  <p className={styles.eyebrow}>{scenario.id} · Selected controlled scenario</p>
                  <h3 id={`record-${scenario.id}`}>{scenario.outcome}</h3>
                </div>
                <p className={scenario.missionCompleted ? styles.completionLabel : styles.degradationLabel}>{scenario.evidenceLabel}</p>
              </div>
              <p className={styles.interpretation}>{scenario.interpretation}</p>
              <dl className={styles.measurements}>
                <div><dt>Controller steps</dt><dd>{scenario.steps}</dd></div>
                <div><dt>Invalid actions</dt><dd>{scenario.invalidActions}</dd></div>
                <div><dt>Recorded classification</dt><dd><code>{scenario.classification}</code></dd></div>
                <div><dt>Controller path cost</dt><dd><code>{scenario.controllerPathCost}</code></dd></div>
              </dl>
              <div className={styles.reference}>
                <p>{snapshot.referenceLabel}</p>
                <p><strong>{scenario.referenceSteps} steps</strong><span aria-hidden="true"> · </span><code>{scenario.referencePathCost}</code> path cost</p>
              </div>
              <figure className={styles.figure}>
                <a href={scenario.screenshot} target="_blank" rel="noreferrer" aria-label={`View original evaluator screenshot for ${scenario.id} (opens in a new tab)`}>
                  <Image src={scenario.screenshot} width={1920} height={1065} sizes="(max-width: 768px) 100vw, 1120px" alt={scenario.screenshotAlt} unoptimized />
                </a>
                <figcaption>
                  <span>Original submission-era evaluator screenshot · {scenario.id}</span>
                  <a href={scenario.screenshot} target="_blank" rel="noreferrer">View original evaluator screenshot <span aria-hidden="true">↗</span><span className={styles.srOnly}> (opens in a new tab)</span></a>
                </figcaption>
              </figure>
              <p className={styles.sourceNote}>Frozen evidence record: <code>{scenario.sourceReport}</code></p>
            </article>
          ))}
          <p className={styles.conclusion}>{snapshot.referenceInterpretation}</p>
        </section>

        <section id="submission-scope" className={styles.section} aria-labelledby="scope-title">
          <div className={styles.sectionHeading}>
            <p className={styles.eyebrow}>02 / Submission-era scope</p>
            <h2 id="scope-title">A functioning workflow. A bounded claim.</h2>
            <p>{snapshot.environment}. The submission used a verified MaskablePPO adapter in selected structured C4 scenarios.</p>
          </div>
          <ol className={styles.workflow}>
            {snapshot.workflow.map((step, index) => (
              <li key={step.stage}>
                <span className={styles.stepNumber}>{String(index + 1).padStart(2, "0")}</span>
                <div><h3>{step.stage}</h3><p>{step.description}</p></div>
              </li>
            ))}
          </ol>
          <div className={styles.boundaries}>
            <div><h3>What the evidence demonstrates</h3><ul>{snapshot.demonstrates.map((item) => <li key={item}>{item}</li>)}</ul></div>
            <div><h3>What the evidence does not establish</h3><ul>{snapshot.notEstablished.map((item) => <li key={item}>{item}</li>)}</ul></div>
          </div>
          <p className={styles.boundaryNote}>Mission-liveness classification is a versioned diagnostic, not a certification or safety score. Invalid actions remain a separate diagnostic.</p>
        </section>

        <section id="submission-provenance" className={styles.section} aria-labelledby="provenance-title">
          <div className={styles.sectionHeading}>
            <p className={styles.eyebrow}>03 / Frozen provenance</p>
            <h2 id="provenance-title">Reproducible submission state.</h2>
          </div>
          <dl className={styles.provenance}>
            <div><dt>Submission date</dt><dd>{snapshot.date}</dd></div>
            <div><dt>Frozen MVP branch</dt><dd><code>{provenance.frozenBranch}</code></dd></div>
            <div><dt>Frozen MVP source SHA</dt><dd><code>{provenance.frozenMvpSha}</code></dd></div>
            <div><dt>Checkpoint SHA256</dt><dd><code>{provenance.checkpointSha256}</code></dd></div>
            <div><dt>Failure protocol</dt><dd><code>{provenance.failureProtocol}</code></dd></div>
            <div><dt>Scenario provenance</dt><dd><code>{provenance.scenarioClassification}</code> · {provenance.scenarioSelection}</dd></div>
            <div><dt>Evidence classification</dt><dd><code>{provenance.dataClassification}</code></dd></div>
            <div><dt>Fresh holdout</dt><dd><code>{String(provenance.freshHoldout)}</code></dd></div>
            <div><dt>Movement contract</dt><dd>{provenance.movementContract}</dd></div>
          </dl>
          <div className={styles.verification}>
            <p className={styles.eyebrow}>Implementation verification — not a safety score</p>
            <ul>{provenance.verification.map((item) => <li key={item}>{item}</li>)}</ul>
            <p>{provenance.verificationInterpretation}</p>
          </div>
          <details className={styles.sourceDetails}>
            <summary>Inspect historical source identities <span aria-hidden="true">+</span></summary>
            <dl className={styles.provenance}>
              <div><dt>Submission website source SHA</dt><dd><code>{provenance.websiteSourceSha}</code></dd></div>
              <div><dt>Selected evidence export</dt><dd><code>{provenance.evidenceDirectory}/{provenance.manifestFile}</code></dd></div>
              <div><dt>Research source commit</dt><dd><code>{provenance.researchSourceCommit}</code></dd></div>
              <div><dt>Scenario manifest Git blob</dt><dd><code>{provenance.scenarioManifestGitBlob}</code></dd></div>
            </dl>
          </details>
        </section>

        <section id="submission-team" className={styles.section} aria-labelledby="team-title">
          <div className={styles.sectionHeading}>
            <p className={styles.eyebrow}>04 / Submission team</p>
            <h2 id="team-title">Research and integration, together.</h2>
          </div>
          <div className={styles.team}>
            {snapshot.team.map((person) => <article key={person.name}><h3>{person.name}</h3><p>{person.role}</p><p className={styles.affiliation}>{person.affiliation}</p></article>)}
          </div>
          <p className={styles.teamStory}>{snapshot.teamStory}</p>
        </section>
      </main>

      <footer className={styles.footer}>
        <div><strong>{snapshot.title}</strong><p>{snapshot.evidenceBoundary}</p></div>
        <Link href="/">Return to the latest validated build <span aria-hidden="true">↗</span></Link>
      </footer>
    </div>
  );
}
