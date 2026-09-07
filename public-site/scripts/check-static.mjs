import assert from "node:assert/strict";
import { readFile, readdir, stat } from "node:fs/promises";
import { extname, relative, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

// Run after `npm run build`. This checks the delivered presentation only;
// it never executes the scientific controller, evaluator or scenario code.
const root = resolve(fileURLToPath(new URL("../out/", import.meta.url)));
const siteRoot = fileURLToPath(new URL("../", import.meta.url));
const origin = "https://mehwar-deftech.vercel.app";
// Avoid dumping file bodies (or a discovered credential) into a failed check.
const assertMatch = (value, pattern, message) => assert(pattern.test(value), message || `Required pattern missing: ${pattern}`);
const assertNoMatch = (value, pattern, message) => assert(!pattern.test(value), message || `Forbidden pattern found: ${pattern}`);
const files = [];
async function walk(directory) {
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const path = resolve(directory, entry.name);
    if (entry.isDirectory()) await walk(path);
    else files.push(path);
  }
}
await walk(root);
assert(files.length > 0, "Build the static export before running this check.");
const textExtensions = new Set([".html", ".txt", ".json", ".js", ".css", ".svg", ".xml", ".md"]);
const contents = new Map();
for (const file of files) {
  if (textExtensions.has(extname(file))) contents.set(file, await readFile(file, "utf8"));
  assert(!/\.(?:map|env|zip|pt|pth|ckpt|pkl|pickle)$/i.test(file), `Unexpected public artifact: ${relative(root, file)}`);
}

const decode = (value) => value.replace(/&(?:amp|quot|apos|lt|gt|#39|#x27|#x2F|nbsp);/gi, (entity) => ({
  "&amp;": "&", "&quot;": '"', "&apos;": "'", "&#39;": "'", "&#x27;": "'",
  "&#x2f;": "/", "&lt;": "<", "&gt;": ">", "&nbsp;": " ",
})[entity.toLowerCase()]);
const renderedText = (html) => decode(html
  .replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, "")
  .replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, "")
  .replace(/<!--[\s\S]*?-->/g, "")
  .replace(/<[^>]+>/g, " ")
  .replace(/\s+/g, " ")).trim();
const ids = (html) => [...html.matchAll(/\bid="([^"]+)"/g)].map((match) => decode(match[1]));
const pageUrl = (file) => {
  const path = relative(root, file).split(sep).join("/");
  return new URL(path === "index.html" ? "/" : `/${path.replace(/\.html$/, "")}`, origin);
};
let checkedLinks = 0;
async function checkLocalLink(value, baseUrl, source) {
  value = decode(value);
  assert(value.trim(), `Empty URL in ${source}`);
  if (/^(?:data:|mailto:|tel:)/i.test(value)) return;
  const url = new URL(value, baseUrl);
  assert(!/^javascript:/i.test(url.protocol), `Script URL in ${source}`);
  if (url.origin !== origin) return;
  const pathname = decodeURIComponent(url.pathname);
  const candidate = resolve(root, `.${pathname}`);
  assert(candidate === root || candidate.startsWith(root + sep), `URL escapes export: ${value}`);
  const options = pathname === "/" ? [resolve(root, "index.html")] : [candidate, `${candidate}.html`, resolve(candidate, "index.html")];
  let target;
  for (const option of options) {
    try { if ((await stat(option)).isFile()) { target = option; break; } } catch { /* Try the next static-export route form. */ }
  }
  assert(target, `Unresolved local URL ${value} in ${source}`);
  if (url.hash && extname(target) === ".html") {
    const targetHtml = contents.get(target);
    assert(ids(targetHtml).includes(decodeURIComponent(url.hash.slice(1))), `Missing fragment ${value} in ${source}`);
  }
  checkedLinks++;
}

for (const [file, content] of contents) {
  const name = relative(root, file);
  if (extname(file) === ".html") {
    const identifiers = ids(content);
    assert.equal(identifiers.length, new Set(identifiers).size, `Duplicate HTML/SVG ID in ${name}`);
    for (const match of content.matchAll(/\b(?:href|src|poster)="([^"]*)"/g)) {
      await checkLocalLink(match[1], pageUrl(file), name);
    }
    for (const match of content.matchAll(/\bsrcset="([^"]*)"/g)) {
      for (const item of decode(match[1]).split(",")) {
        await checkLocalLink(item.trim().split(/\s+/)[0], pageUrl(file), name);
      }
    }
    for (const match of content.matchAll(/\b(?:aria-controls|aria-labelledby|aria-describedby)="([^"]+)"/g)) {
      for (const id of match[1].split(/\s+/)) assert(identifiers.includes(id), `Unresolved accessible reference ${id} in ${name}`);
    }
  }
  if (extname(file) === ".css") {
    const cssUrl = new URL(`/${name.split(sep).join("/")}`, origin);
    for (const match of content.matchAll(/url\(\s*["']?([^\s"')]+)["']?\s*\)/g)) {
      await checkLocalLink(match[1], cssUrl, name);
    }
  }
}

const home = contents.get(resolve(root, "index.html"));
const snapshot = contents.get(resolve(root, "deftech-2026.html"));
assert(home && snapshot, "Homepage and immutable snapshot must both be exported.");
const commonFacts = [
  "Legal action selection does not by itself guarantee mission liveness.",
  "C4-0001", "C4-0000", "LIVENESS DEGRADATION OBSERVED",
  "NO FAILURE OBSERVED IN SELECTED DEMO RUN", "two_cell_loop",
  "37.112698372208094", "16.071067811865476", "17.242640687119284", "16.65685424949238",
  "c4_c5_recurrence_v1", "1586eebf9daa8a8e690bc6f62cc377ce540214ee",
  "c91d30711aa91957554dfa92b152d2a1d1e14a7b43fa01237722c54cb0acfaaf",
  "deterministic A* reliability reference under the shared grid contract",
  "The point is not that one algorithm wins. The point is that legality alone did not expose the failure.",
  "137 tests passed", "0 skipped", "Ruff PASS", "Muzzammil Sajid", "Simra Imran",
  "Co-founder — Research & Assurance", "Co-founder — Product & Integration",
];
for (const [label, html] of [["homepage", home], ["snapshot", snapshot]]) {
  const text = renderedText(html);
  for (const fact of commonFacts) assert(text.includes(fact), `Missing statically readable ${label} fact: ${fact}`);
  assertMatch(text, /development.validation/i, `${label}: selected-evidence caveat missing`);
  assertMatch(text, /not a statistically representative benchmark/i, `${label}: benchmark limitation missing`);
  assertMatch(text, /2-D grid-based mission.routing/i, `${label}: environment boundary missing`);
  assertMatch(text, /Fresh holdout\s*false/i, `${label}: fresh-holdout flag missing`);
  for (const boundary of ["flight validation", "deployment readiness", "safety certification", "OEM", "HIL"]) {
    assert(text.toLowerCase().includes(boundary.toLowerCase()), `${label}: missing boundary ${boundary}`);
  }
  assert.equal((html.match(/<h1\b/g) || []).length, 1, `${label}: expected one h1`);
  assertMatch(html, /<html[^>]*\blang="en"/);
  assertMatch(html, /<main\b/);
  assertMatch(html, /name="description"/);
  assertMatch(html, /property="og:image"/);
  const imageUrl = html.match(/property="og:image" content="([^"]+)"/)[1];
  await checkLocalLink(imageUrl, origin, `${label} OpenGraph image`);
  assertMatch(html, /name="twitter:card" content="summary_large_image"/);
  assertMatch(html, /name="theme-color"/);
}
assertMatch(home, /<title>MEHWAR — Autonomy-Assurance Evaluation for Navigation Controllers<\/title>/);
assertMatch(home, /property="og:image"[^>]+opengraph-image\.png/);
assertMatch(home, /rel="canonical" href="https:\/\/mehwar-deftech\.vercel\.app\/?"/);
assertMatch(snapshot, /rel="canonical" href="https:\/\/mehwar-deftech\.vercel\.app\/deftech-2026"/);
assertMatch(renderedText(home), /Latest Validated Build/);
assertMatch(renderedText(snapshot), /September 2026/);
assertMatch(renderedText(snapshot), /historical record preserves/i);
assertMatch(home, /type="radio"[^>]*name="evidence-scenario"[^>]*checked=""[^>]*value="C4-0001"/);
assert.equal((home.match(/<details\b/g) || []).length >= 4, true, "Exact evidence must remain accessible through native disclosure without JS.");

// Current optional configuration: absent values must produce a complete page,
// without a fabricated address, empty links, placeholder player or archive URL.
const config = await readFile(resolve(siteRoot, "content/site.ts"), "utf8");
if (/publicEmail:\s*""/.test(config)) {
  assertNoMatch(home, /href="mailto:/i);
  assertMatch(renderedText(home), /A public contact channel is not yet listed\./);
  assertMatch(renderedText(home), /Discuss Technical Validation/);
}
if (/evidenceArchiveUrl:\s*""/.test(config)) {
  assertMatch(home, /href="\/deftech-2026"/);
  assertNoMatch(home, /href="https?:\/\/(?:drive|docs)\.google\.com/i);
}
if (/demoVideo:\s*""/.test(config)) {
  assertNoMatch(home, /<video\b|<iframe\b/i);
  assertNoMatch(renderedText(home), /video (?:coming soon|placeholder)/i);
}

// Known secret and machine-path signatures, including their escaped build forms.
// Public SHA values and repository-relative source identifiers are permitted.
const denied = [
  ["Windows user path", /[A-Z]:[\\/]+(?:Users|Windows|Program Files)[\\/]/i],
  ["Unix home path", /\/(?:Users|home)\/[A-Za-z0-9._ -]+\//],
  ["private key", /-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/],
  ["GitHub credential", /\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b/],
  ["service credential", /\b(?:sk_live_[A-Za-z0-9]{20,}|sk-proj-[A-Za-z0-9_-]{30,}|AKIA[A-Z0-9]{16})\b/],
  ["credential assignment", /(?:API_KEY|VERCEL_TOKEN|GITHUB_TOKEN|PRIVATE_KEY)\s*[=:]\s*["'][^"'\s]{8,}["']/i],
  ["checkpoint filename", /\b[^\s"'<>\\/]*(?:checkpoint|maskableppo|ppo_seed)[^\s"'<>\\/]*\.(?:zip|pt|pth|ckpt|pkl)\b/i],
  ["national identity number", /\b\d{5}-\d{7}-\d\b/],
  ["private phone number", /(?:\+92[ -]?3\d{2}[ -]?\d{7}|\b03\d{2}[- ]\d{7}\b)/],
];
for (const [file, content] of contents) {
  for (const [label, pattern] of denied) assertNoMatch(content, pattern, `${label} in ${relative(root, file)}`);
}
const exportJson = contents.get(resolve(root, "evidence/selected-runs.json"));
assertNoMatch(exportJson, /checkpoint_filename|checkpoint_path|local_path|\bemail\b|\bphone\b/i);
assert.equal(exportJson, await readFile(resolve(siteRoot, "public/evidence/selected-runs.json"), "utf8"), "Published evidence must be byte-identical to the checked source export.");
console.log(`PASS: ${files.length} exported files; ${checkedLinks} local links/assets/fragments; unique IDs and accessible references; static facts, metadata and boundaries on both routes; missing optional config; privacy signatures and immutable published evidence.`);
