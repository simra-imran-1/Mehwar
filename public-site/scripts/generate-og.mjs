import { readFile, writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import sharp from "sharp";
import { presentationAnnotations } from "../content/playback.mjs";

// Projection of immutable evidence, with no synthesized or smoothed coordinates.
const evidence = JSON.parse(
  await readFile(
    new URL("../public/evidence/selected-runs.json", import.meta.url),
    "utf8",
  ),
);
const run = evidence.scenarios.find((entry) => entry.scenario_id === "C4-0001");
const size = 24,
  x = 746,
  y = 150;
const point = ([row, col]) => [x + (col + 0.5) * size, y + (row + 0.5) * size];
const path = (cells) => cells.map((cell) => point(cell).join(",")).join(" ");
const blocks = run.configuration.blocked
  .map(
    ([row, col]) =>
      `<rect x="${x + col * size + 2}" y="${y + row * size + 2}" width="20" height="20" fill="#59727d"/>`,
  )
  .join("");
const rings = presentationAnnotations[run.scenario_id].recurrenceCells
  .map((cell) => {
    const [cx, cy] = point(cell);
    return `<circle cx="${cx}" cy="${cy}" r="10" fill="#071b25" fill-opacity=".5" stroke="#efb366" stroke-width="2"/>`;
  })
  .join("");
const [sx, sy] = point(run.configuration.start),
  [gx, gy] = point(run.configuration.goal);
const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
<rect width="1200" height="630" fill="#071b25"/>
<g font-family="Arial, sans-serif" fill="#f2f1e9">
<path d="M58 80V54l17 19 17-19v26" fill="none" stroke="#f2f1e9" stroke-width="3"/><circle cx="58" cy="80" r="3"/><circle cx="92" cy="80" r="3"/>
<text x="110" y="79" font-size="30" font-weight="700" letter-spacing="4">MEHWAR</text>
<text x="58" y="153" font-size="13" letter-spacing="1.5" fill="#a4c8dc">AUTONOMY-ASSURANCE EVALUATION</text>
<text x="55" y="244" font-size="68" letter-spacing="-3">Every move legal.</text>
<text x="55" y="321" font-size="68" letter-spacing="-3" fill="#a4c8dc">Mission unfinished.</text>
<path d="M58 373H659" stroke="#35505c"/>
<text x="53" y="477" font-size="108" letter-spacing="-5">${run.diagnostics.invalid_actions}</text>
<text x="136" y="429" font-size="23">invalid actions</text>
<text x="136" y="462" font-size="17" fill="#efb366">Mission not completed.</text>
<text x="58" y="574" font-size="13" fill="#b0bec5">Selected controlled evidence · 2-D mission-routing abstraction</text>
<path d="M698 55V578" stroke="#35505c"/>
<text x="746" y="84" font-size="14" letter-spacing="1" fill="#b0bec5">${run.scenario_id} / RECORDED TRACE</text>
<defs><pattern id="grid" x="${x}" y="${y}" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#35505c" stroke-width=".8"/></pattern></defs>
<rect x="${x}" y="${y}" width="360" height="360" fill="url(#grid)" stroke="#35505c"/>
${blocks}<polyline points="${path(run.trajectory)}" fill="none" stroke="#a4c8dc" stroke-width="3"/>
<circle cx="${sx}" cy="${sy}" r="6" fill="#071b25" stroke="#a4c8dc" stroke-width="3"/>
<rect x="${gx - 5}" y="${gy - 5}" width="10" height="10" fill="#071b25" stroke="#f2f1e9" stroke-width="2"/>
${rings}<text x="746" y="558" font-size="13" letter-spacing="1" fill="#efb366">LEGAL TWO-CELL RECURRENCE</text>
<text x="746" y="582" font-size="12" fill="#b0bec5">${run.steps} recorded steps / ${run.failure_type}</text>
</g></svg>`;
await sharp(Buffer.from(svg))
  .png()
  .toFile(
    fileURLToPath(new URL("../public/opengraph-image.png", import.meta.url)),
  );
await writeFile(new URL("../public/opengraph-image.svg", import.meta.url), svg);
console.log(
  "Generated 1200×630 V3 social image from frozen C4-0001 coordinates.",
);
