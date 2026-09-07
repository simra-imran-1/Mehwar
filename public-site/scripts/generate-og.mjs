import { readFile, writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import sharp from "sharp";

// The social card renders frozen coordinates; it does not synthesize a trace.
const evidence = JSON.parse(
  await readFile(
    new URL("../public/evidence/selected-runs.json", import.meta.url),
    "utf8",
  ),
);
const run = evidence.scenarios.find((entry) => entry.scenario_id === "C4-0001");
const step = 24,
  x = 736,
  y = 138;
const point = ([row, col]) => [
  x + col * step + step / 2,
  y + row * step + step / 2,
];
const path = (cells) => cells.map((cell) => point(cell).join(",")).join(" ");
const blocks = run.configuration.blocked
  .map(
    ([row, col]) =>
      `<rect x="${x + col * step + 2}" y="${y + row * step + 2}" width="20" height="20" fill="#7f919b"/>`,
  )
  .join("");
const rings = run.trajectory
  .slice(15, 17)
  .map((cell) => {
    const [cx, cy] = point(cell);
    return `<circle cx="${cx}" cy="${cy}" r="10" fill="#f2e7d5" stroke="#946022" stroke-width="2"/>`;
  })
  .join("");
const [sx, sy] = point(run.configuration.start),
  [gx, gy] = point(run.configuration.goal);
const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
<rect width="1200" height="630" fill="#f8f8f4"/>
<g font-family="Arial, sans-serif" fill="#172d3c">
<path d="M58 80V54l17 19 17-19v26" fill="none" stroke="#172d3c" stroke-width="3"/><circle cx="58" cy="80" r="3"/><circle cx="92" cy="80" r="3"/>
<text x="110" y="79" font-size="30" font-weight="700" letter-spacing="4">MEHWAR</text>
<text x="58" y="150" font-size="15" fill="#426b87">AUTONOMY-ASSURANCE EVALUATION</text>
<text x="55" y="239" font-size="61" letter-spacing="-2">Legal action selection</text>
<text x="55" y="310" font-size="61" letter-spacing="-2">does not guarantee</text>
<text x="55" y="382" font-size="61" fill="#426b87" letter-spacing="-2">mission liveness.</text>
<path d="M58 433H644" stroke="#d6dcdd"/>
<text x="58" y="480" font-size="22">0 invalid actions.</text><text x="58" y="516" font-size="22" fill="#946022">Mission not completed.</text>
<text x="58" y="581" font-size="13" fill="#52636d">C4-0001 · Selected controlled evidence · 2-D mission-routing abstraction</text>
<path d="M693 56V565" stroke="#d6dcdd"/>
<text x="736" y="85" font-size="14" fill="#52636d" font-family="Arial, sans-serif">C4-0001 / RECORDED TRACE</text>
<defs><pattern id="grid" x="${x}" y="${y}" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#dce2e2"/></pattern></defs>
<rect x="${x}" y="${y}" width="360" height="360" fill="url(#grid)" stroke="#dce2e2"/>
${blocks}<polyline points="${path(run.reference_result.trajectory)}" fill="none" stroke="#71828c" stroke-width="2" stroke-dasharray="3 5"/>
<polyline points="${path(run.trajectory)}" fill="none" stroke="#426b87" stroke-width="3" stroke-linejoin="round"/>
<circle cx="${sx}" cy="${sy}" r="6" fill="#f8f8f4" stroke="#426b87" stroke-width="3"/>
<rect x="${gx - 5}" y="${gy - 5}" width="10" height="10" fill="#f8f8f4" stroke="#172d3c" stroke-width="2"/>
${rings}<text x="750" y="548" font-size="13" fill="#946022" font-family="Arial, sans-serif">LEGAL TWO-CELL RECURRENCE</text>
</g></svg>`;
await sharp(Buffer.from(svg))
  .png()
  .toFile(
    fileURLToPath(new URL("../public/opengraph-image.png", import.meta.url)),
  );
await writeFile(new URL("../public/opengraph-image.svg", import.meta.url), svg);
console.log("Generated 1200×630 social image from frozen C4-0001 coordinates.");
