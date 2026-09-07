import { readdir, readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { join, relative, sep } from "node:path";

// Package only the validated static export and its Vercel routing configuration.
// This prints a payload for the authenticated Vercel connector; it does not deploy.
const root = fileURLToPath(new URL("../out/", import.meta.url));
const files = [];
async function visit(directory) {
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const path = join(directory, entry.name);
    if (entry.isDirectory()) await visit(path);
    else if (entry.isFile()) {
      files.push({
        file: relative(root, path).split(sep).join("/"),
        data: (await readFile(path)).toString("base64"),
        encoding: "base64",
      });
    }
  }
}
await visit(root);
files.push({
  file: "vercel.json",
  data: (await readFile(new URL("../vercel.json", import.meta.url))).toString("base64"),
  encoding: "base64",
});
console.log(JSON.stringify({ target: "production", name: "mehwar-deftech", files }));
