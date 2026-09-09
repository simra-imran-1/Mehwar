import { Space_Grotesk } from "next/font/google";
import type { Viewport } from "next";
import { SiteHeader } from "../components/SiteHeader";
import { Brand } from "../components/Brand";
import { EvidenceExperience } from "../components/EvidenceExperience";
import { Narrative } from "../components/Narrative";
import "./v3.css";

const display = Space_Grotesk({
  subsets: ["latin"],
  variable: "--font-display",
  display: "swap",
});
export const viewport: Viewport = { themeColor: "#071b25" };
export default function Home() {
  return (
    <div className={`v3 ${display.variable}`}>
      <a className="skip-link" href="#main">
        Skip to content
      </a>
      <SiteHeader />
      <main id="main">
        <EvidenceExperience />
        <Narrative />
      </main>
      <footer className="site-footer v-wrap">
        <div>
          <Brand />
          <p>
            Evidence is tied to the tested scenario, controller/configuration,
            evaluation semantics, and environment.
          </p>
        </div>
        <nav aria-label="Footer navigation">
          <a href="/deftech-2026">
            DEFTECH 2026 snapshot <span aria-hidden="true">↗</span>
          </a>
          <a href="#main">
            Back to the evidence <span aria-hidden="true">↑</span>
          </a>
        </nav>
      </footer>
    </div>
  );
}
