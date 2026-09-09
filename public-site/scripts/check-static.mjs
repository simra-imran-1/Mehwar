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
const assertMatch = (value, pattern, message) =>
  assert(
    pattern.test(value),
    message || `Required pattern missing: ${pattern}`,
  );
const assertNoMatch = (value, pattern, message) =>
  assert(
    !pattern.test(value),
    message || `Forbidden pattern found: ${pattern}`,
  );
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
const textExtensions = new Set([
  ".html",
  ".txt",
  ".json",
  ".js",
  ".css",
  ".svg",
  ".xml",
  ".md",
]);
const contents = new Map();
for (const file of files) {
  if (textExtensions.has(extname(file)))
    contents.set(file, await readFile(file, "utf8"));
  assert(
    !/\.(?:map|env|zip|pt|pth|ckpt|pkl|pickle)$/i.test(file),
    `Unexpected public artifact: ${relative(root, file)}`,
  );
}

const decode = (value) =>
  value.replace(
    /&(?:amp|quot|apos|lt|gt|#39|#x27|#x2F|nbsp);/gi,
    (entity) =>
      ({
        "&amp;": "&",
        "&quot;": '"',
        "&apos;": "'",
        "&#39;": "'",
        "&#x27;": "'",
        "&#x2f;": "/",
        "&lt;": "<",
        "&gt;": ">",
        "&nbsp;": " ",
      })[entity.toLowerCase()],
  );
const renderedText = (html) =>
  decode(
    html
      .replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, "")
      .replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, "")
      .replace(/<!--[\s\S]*?-->/g, "")
      .replace(/<[^>]+>/g, " ")
      .replace(/\s+/g, " "),
  ).trim();
const ids = (html) =>
  [...html.matchAll(/\bid="([^"]+)"/g)].map((match) => decode(match[1]));
// Attribute order is a serializer detail, not an accessibility contract.
const attributes = (tag) =>
  Object.fromEntries(
    [...tag.matchAll(/\s([\w:-]+)(?:="([^"]*)")?/g)].map((match) => [
      match[1].toLowerCase(),
      decode(match[2] ?? ""),
    ]),
  );
const elements = (html, name) =>
  [...html.matchAll(new RegExp(`<${name}\\b[^>]*>`, "gi"))].map((match) => ({
    tag: match[0],
    attrs: attributes(match[0]),
  }));
const hasAttribute = (attrs, name) => Object.hasOwn(attrs, name);
const pageUrl = (file) => {
  const path = relative(root, file).split(sep).join("/");
  return new URL(
    path === "index.html" ? "/" : `/${path.replace(/\.html$/, "")}`,
    origin,
  );
};
let checkedLinks = 0;
async function checkLocalLink(value, baseUrl, source) {
  value = decode(value);
  assert(value.trim(), `Empty URL in ${source}`);
  if (/^(?:data:|mailto:|tel:)/i.test(value)) return;
  const url = new URL(value, baseUrl);
  assert(!/^javascript:/i.test(url.protocol), `Script URL in ${source}`);
  assert(
    !/^(?:localhost|127\.0\.0\.1|0\.0\.0\.0|\[::1\])$/i.test(url.hostname),
    `Local preview URL in ${source}`,
  );
  if (url.origin !== origin) return;
  const pathname = decodeURIComponent(url.pathname);
  const candidate = resolve(root, `.${pathname}`);
  assert(
    candidate === root || candidate.startsWith(root + sep),
    `URL escapes export: ${value}`,
  );
  const options =
    pathname === "/"
      ? [resolve(root, "index.html")]
      : [candidate, `${candidate}.html`, resolve(candidate, "index.html")];
  let target;
  for (const option of options) {
    try {
      if ((await stat(option)).isFile()) {
        target = option;
        break;
      }
    } catch {
      /* Try the next static-export route form. */
    }
  }
  assert(target, `Unresolved local URL ${value} in ${source}`);
  if (url.hash && extname(target) === ".html") {
    const targetHtml = contents.get(target);
    assert(
      ids(targetHtml).includes(decodeURIComponent(url.hash.slice(1))),
      `Missing fragment ${value} in ${source}`,
    );
  }
  checkedLinks++;
}

for (const [file, content] of contents) {
  const name = relative(root, file);
  if (extname(file) === ".html") {
    const identifiers = ids(content);
    assert.equal(
      identifiers.length,
      new Set(identifiers).size,
      `Duplicate HTML/SVG ID in ${name}`,
    );
    for (const match of content.matchAll(/\b(?:href|src|poster)="([^"]*)"/g)) {
      await checkLocalLink(match[1], pageUrl(file), name);
    }
    for (const match of content.matchAll(/\bsrcset="([^"]*)"/g)) {
      for (const item of decode(match[1]).split(",")) {
        await checkLocalLink(item.trim().split(/\s+/)[0], pageUrl(file), name);
      }
    }
    for (const match of content.matchAll(
      /\b(?:aria-controls|aria-labelledby|aria-describedby)="([^"]+)"/g,
    )) {
      for (const id of match[1].split(/\s+/))
        assert(
          identifiers.includes(id),
          `Unresolved accessible reference ${id} in ${name}`,
        );
    }
  }
  if (extname(file) === ".css") {
    const cssUrl = new URL(`/${name.split(sep).join("/")}`, origin);
    for (const match of content.matchAll(
      /url\(\s*["']?([^\s"')]+)["']?\s*\)/g,
    )) {
      await checkLocalLink(match[1], cssUrl, name);
    }
  }
}

const home = contents.get(resolve(root, "index.html"));
const snapshot = contents.get(resolve(root, "deftech-2026.html"));
assert(
  home && snapshot,
  "Homepage and immutable snapshot must both be exported.",
);
const commonFacts = [
  "Legal action selection does not by itself guarantee mission liveness.",
  "C4-0001",
  "C4-0000",
  "LIVENESS DEGRADATION OBSERVED",
  "NO FAILURE OBSERVED IN SELECTED DEMO RUN",
  "two_cell_loop",
  "37.112698372208094",
  "16.071067811865476",
  "17.242640687119284",
  "16.65685424949238",
  "c4_c5_recurrence_v1",
  "1586eebf9daa8a8e690bc6f62cc377ce540214ee",
  "c91d30711aa91957554dfa92b152d2a1d1e14a7b43fa01237722c54cb0acfaaf",
  "deterministic A* reliability reference under the shared grid contract",
  "The point is not that one algorithm wins. The point is that legality alone did not expose the failure.",
  "137 tests passed",
  "0 skipped",
  "Ruff PASS",
  "Muzzammil Sajid",
  "Simra Imran",
  "Co-founder — Research & Assurance",
  "Co-founder — Product & Integration",
];
for (const [label, html] of [
  ["homepage", home],
  ["snapshot", snapshot],
]) {
  const text = renderedText(html);
  for (const fact of commonFacts)
    assert(
      text.includes(fact),
      `Missing statically readable ${label} fact: ${fact}`,
    );
  assertMatch(
    text,
    /development.validation/i,
    `${label}: selected-evidence caveat missing`,
  );
  assertMatch(
    text,
    /not a statistically representative benchmark/i,
    `${label}: benchmark limitation missing`,
  );
  assertMatch(
    text,
    /2-D grid-based mission.routing/i,
    `${label}: environment boundary missing`,
  );
  assertMatch(
    text,
    /Fresh holdout\s*false/i,
    `${label}: fresh-holdout flag missing`,
  );
  for (const boundary of [
    "flight validation",
    "deployment readiness",
    "certification",
    "OEM",
    "HIL",
  ]) {
    assert(
      text.toLowerCase().includes(boundary.toLowerCase()),
      `${label}: missing boundary ${boundary}`,
    );
  }
  assert.equal(
    (html.match(/<h1\b/g) || []).length,
    1,
    `${label}: expected one h1`,
  );
  assertMatch(html, /<html[^>]*\blang="en"/);
  assertMatch(html, /<main\b/);
  assertMatch(html, /name="description"/);
  assertMatch(html, /property="og:image"/);
  const imageUrl = html.match(/property="og:image" content="([^"]+)"/)[1];
  await checkLocalLink(imageUrl, origin, `${label} OpenGraph image`);
  assertMatch(html, /name="twitter:card" content="summary_large_image"/);
  assertMatch(html, /name="theme-color"/);
}
assertMatch(
  home,
  /<title>MEHWAR — Autonomy-Assurance Evaluation for Navigation Controllers<\/title>/,
);
assertMatch(home, /property="og:image"[^>]+opengraph-image\.png/);
assertMatch(
  home,
  /rel="canonical" href="https:\/\/mehwar-deftech\.vercel\.app\/?"/,
);
assertMatch(
  snapshot,
  /rel="canonical" href="https:\/\/mehwar-deftech\.vercel\.app\/deftech-2026"/,
);
assertMatch(renderedText(home), /Latest Validated Build/);
assertMatch(renderedText(snapshot), /September 2026/);
assertMatch(renderedText(snapshot), /historical record preserves/i);

// V3 is progressively enhanced recorded-evidence inspection. The export must
// already show the complete selected failure, retain the secondary record in
// its no-JS fallback, and expose real native controls with accessible names.
const homeText = renderedText(home);
const homeInputs = elements(home, "input");
const scenarioRadios = homeInputs.filter(
  ({ attrs }) => attrs.type === "radio" && attrs.name === "selected-scenario",
);
assert.deepEqual(
  scenarioRadios.map(({ attrs }) => attrs.value),
  ["C4-0001", "C4-0000"],
  "Both accepted scenarios need native selection controls.",
);
assert.deepEqual(
  scenarioRadios
    .filter(({ attrs }) => hasAttribute(attrs, "checked"))
    .map(({ attrs }) => attrs.value),
  ["C4-0001"],
  "C4-0001 must be the default recorded scenario.",
);
const scenarioFieldset = [
  ...home.matchAll(/<fieldset\b[^>]*>([\s\S]*?)<\/fieldset>/gi),
].find((match) => match[1].includes('name="selected-scenario"'))?.[1];
assert(
  scenarioFieldset &&
    /<legend\b[^>]*>\s*Select recorded evidence\s*<\/legend>/i.test(
      scenarioFieldset,
    ),
  "Scenario selection needs a native fieldset legend.",
);

const slider = homeInputs.find(({ attrs }) => attrs.id === "trace-step")?.attrs;
assert(slider, "Recorded-step scrubber is missing.");
assert.equal(
  slider.type,
  "range",
  "Use a native range input for keyboard step inspection.",
);
assert.equal(slider.min, "0", "Step zero is the initial recorded position.");
assert.equal(slider.max, "28", "Default trace has 28 completed moves.");
assert.equal(
  slider.value,
  "28",
  "Server-rendered evidence must settle on the meaningful final state.",
);
assert.equal(
  slider.step ?? "1",
  "1",
  "Playback selects recorded positions, not invented fractional coordinates.",
);
assert.equal(
  slider["aria-valuetext"],
  "Step 28 of 28, row 13, column 0",
  "Scrubber must describe the exact recorded position.",
);
assertMatch(
  home,
  /<label\b[^>]*\bfor="trace-step"[^>]*>\s*Recorded controller step\s*<\/label>/i,
  "Scrubber requires an associated visible or screen-reader label.",
);
const buttons = elements(home, "button");
for (const name of [
  "Replay recorded trajectory",
  "Previous recorded step",
  "Next recorded step",
]) {
  assert(
    buttons.some(({ attrs }) => attrs["aria-label"] === name),
    `Native playback button missing: ${name}`,
  );
}
assert(
  buttons.some(
    ({ attrs, tag }) =>
      attrs["aria-pressed"] === "false" && /reference-toggle/.test(tag),
  ),
  "Reference overlay needs an initially unpressed native toggle.",
);
assertMatch(
  homeText,
  /RECORDED FINAL-RUN EVIDENCE\s+Independent of playback position/i,
  "Keep supplied final-run outcomes distinct from the playback cursor.",
);
assertMatch(
  homeText,
  /Recorded final-run total\./i,
  "Invalid actions must remain clearly labeled as a final-run diagnostic.",
);
assertMatch(
  homeText,
  /Replay of frozen coordinates\s*·\s*illustrative timing/i,
  "Playback timing must not masquerade as a recorded runtime measurement.",
);
assertMatch(
  homeText,
  /Controller steps\s+28\s+Invalid actions\s+0\s+Mission outcome\s+Not completed\s+Recorded classification\s+two_cell_loop/i,
  "Default final-run evidence must preserve the exact outcome and separate diagnostics.",
);
assertMatch(
  homeText,
  /Classifications are read from frozen evidence; this website does not run an evaluator\./i,
);

const technicalDetails = elements(home, "details").find(({ attrs }) =>
  (attrs.class ?? "").split(/\s+/).includes("technical-record"),
);
assert(
  technicalDetails,
  "Exact evidence must use a native technical disclosure.",
);
assertMatch(
  home,
  /<summary\b[^>]*>[\s\S]*?Inspect the evidence fingerprint[\s\S]*?<\/summary>/i,
);
assertMatch(
  homeText,
  /Read all recorded coordinates/i,
  "A textual coordinate equivalent must remain available.",
);
const fallback = elements(home, "div").find(({ attrs }) =>
  (attrs.class ?? "").split(/\s+/).includes("static-evidence-fallback"),
);
assert(fallback, "The enhanced evidence experience needs a static fallback.");
assert(
  !hasAttribute(fallback.attrs, "hidden"),
  "Secondary evidence must be server-visible until successful enhancement, including when scripts fail or are blocked.",
);
const fallbackStart = home.indexOf(fallback.tag);
const divTags = /<\/?div\b[^>]*>/gi;
divTags.lastIndex = fallbackStart;
let depth = 0;
let fallbackEnd;
for (let match; (match = divTags.exec(home)); ) {
  depth += match[0].startsWith("</") ? -1 : 1;
  if (depth === 0) {
    fallbackEnd = divTags.lastIndex;
    break;
  }
}
assert(fallbackEnd, "Static fallback markup must have a complete closing tag.");
const noJs = home.slice(fallbackStart, fallbackEnd);
const noJsText = renderedText(noJs);
for (const fact of [
  "C4-0000",
  "NO FAILURE OBSERVED IN SELECTED DEMO RUN",
  "Mission completed",
  "success",
  "16 controller steps",
  "0 invalid actions",
  "17.242640687119284",
  "15 steps",
  "16.65685424949238",
])
  assert(
    noJsText.includes(fact),
    `Secondary evidence must remain readable without JavaScript: ${fact}`,
  );
assertMatch(
  noJs,
  /href="\/deftech-2026"/,
  "No-JS readers need access to both full historical records.",
);

const dialogs = elements(home, "dialog");
assert.equal(
  dialogs.length,
  1,
  "Original evaluator evidence needs one native modal viewer.",
);
assert.equal(
  dialogs[0].attrs["aria-labelledby"],
  "viewer-title",
  "Evidence viewer needs an accessible title.",
);
assert(
  !hasAttribute(dialogs[0].attrs, "open"),
  "The evidence viewer must not cover the initial page.",
);
assertMatch(
  home,
  /<form\b[^>]*\bmethod="dialog"/i,
  "Evidence viewer needs a native close interaction.",
);
assert(
  buttons.some(
    ({ attrs }) => attrs["aria-label"] === "Close original evidence viewer",
  ),
  "Evidence viewer needs a named close button.",
);
assert(
  elements(home, "a").some(
    ({ attrs }) =>
      attrs.href === "/c4-0001-liveness-degradation.png" &&
      attrs.target === "_blank",
  ),
  "Original evidence needs a working full-resolution new-tab fallback.",
);

// The V3 specification explicitly approved these two public founder contacts.
// No other recipient may be silently introduced in visible copy or mailto URLs.
const config = await readFile(resolve(siteRoot, "content/site.ts"), "utf8");
const approvedEmails = ["muzzammilsajid1@gmail.com", "simraimran158@gmail.com"];
const emailPattern = /\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b/gi;
const publicEmails = (content) =>
  [...new Set(decode(content).match(emailPattern) ?? [])].sort();
assert.deepEqual(
  publicEmails(config),
  [...approvedEmails].sort(),
  "Founder config must use only the two explicitly approved emails.",
);
assert.deepEqual(
  publicEmails(home),
  [...approvedEmails].sort(),
  "Homepage must expose both approved contacts and no additional email addresses.",
);
assert.deepEqual(
  publicEmails(snapshot),
  [],
  "The historical snapshot must not inherit newer founder contact details.",
);
const mailtoLinks = elements(home, "a").filter(({ attrs }) =>
  /^mailto:/i.test(attrs.href ?? ""),
);
const recipients = [];
for (const { attrs } of mailtoLinks) {
  const mailto = new URL(attrs.href);
  const recipient = decodeURIComponent(mailto.pathname);
  assert(
    approvedEmails.includes(recipient),
    "Unexpected public contact recipient.",
  );
  assert(
    [...mailto.searchParams.keys()].every(
      (key) => key.toLowerCase() === "subject",
    ),
    "Contact action must not silently add recipients or unapproved fields.",
  );
  recipients.push(recipient);
}
assert.deepEqual(
  [...new Set(recipients)].sort(),
  [...approvedEmails].sort(),
  "Both founders need usable, explicit role-specific contact actions.",
);
for (const credential of [
  "Faculty of Mechanical Engineering",
  "Ghulam Ishaq Khan Institute of Engineering Sciences and Technology",
  "Topi, Pakistan",
  "School of Electrical Engineering and Computer Science",
  "National University of Sciences and Technology",
  "Islamabad, Pakistan",
])
  assert(
    homeText.includes(credential),
    `Approved founder credential missing: ${credential}`,
  );
assertMatch(homeText, /Discuss Technical Validation/);
assertNoMatch(
  homeText,
  /A public contact channel is not yet listed\./,
  "Approved founder contacts supersede the old missing-contact state.",
);

// Missing optional media/archive settings should still produce a complete page.
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
  [
    "GitHub credential",
    /\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b/,
  ],
  [
    "service credential",
    /\b(?:sk_live_[A-Za-z0-9]{20,}|sk-proj-[A-Za-z0-9_-]{30,}|AKIA[A-Z0-9]{16})\b/,
  ],
  [
    "credential assignment",
    /(?:API_KEY|VERCEL_TOKEN|GITHUB_TOKEN|PRIVATE_KEY)\s*[=:]\s*["'][^"'\s]{8,}["']/i,
  ],
  [
    "checkpoint filename",
    /\b[^\s"'<>\\/]*(?:checkpoint|maskableppo|ppo_seed)[^\s"'<>\\/]*\.(?:zip|pt|pth|ckpt|pkl)\b/i,
  ],
  ["national identity number", /\b\d{5}-\d{7}-\d\b/],
  [
    "private phone number",
    /(?:\+92[ -]?3\d{2}[ -]?\d{7}|\b03\d{2}[- ]\d{7}\b)/,
  ],
];
for (const [file, content] of contents) {
  for (const [label, pattern] of denied)
    assertNoMatch(content, pattern, `${label} in ${relative(root, file)}`);
  if (extname(file) === ".html") {
    assert(
      publicEmails(content).every((email) => approvedEmails.includes(email)),
      `Unapproved email in ${relative(root, file)}`,
    );
  }
}
const exportJson = contents.get(resolve(root, "evidence/selected-runs.json"));
assertNoMatch(
  exportJson,
  /checkpoint_filename|checkpoint_path|local_path|\bemail\b|\bphone\b/i,
);
assert.equal(
  exportJson,
  await readFile(
    resolve(siteRoot, "public/evidence/selected-runs.json"),
    "utf8",
  ),
  "Published evidence must be byte-identical to the checked source export.",
);
for (const screenshot of [
  "c4-0000-success.png",
  "c4-0001-liveness-degradation.png",
]) {
  assert.deepEqual(
    await readFile(resolve(root, screenshot)),
    await readFile(resolve(siteRoot, "public", screenshot)),
    `Published original screenshot changed: ${screenshot}`,
  );
}
console.log(
  `PASS: ${files.length} exported files; ${checkedLinks} local links/assets/fragments; unique IDs and accessible references; exact static facts and boundaries on both routes; native playback and viewer controls; no-JS evidence; approved founder contacts; metadata, privacy and immutable published artifacts.`,
);
