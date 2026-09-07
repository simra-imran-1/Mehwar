import { createServer } from "node:http";
import { readFile, stat } from "node:fs/promises";
import { resolve, extname, sep } from "node:path";
import { fileURLToPath } from "node:url";
import { gzipSync } from "node:zlib";

// Local static-export QA only. ?nojs=1 verifies the native controls with scripts blocked.
const root = fileURLToPath(new URL("../out", import.meta.url));
const types = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css",
  ".js": "text/javascript",
  ".json": "application/json",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".woff2": "font/woff2",
  ".txt": "text/plain",
  ".xml": "application/xml",
};
const port = Number(process.argv[2] || 4175);
createServer(async (request, response) => {
  try {
    const url = new URL(request.url, "http://127.0.0.1");
    const relative = decodeURIComponent(url.pathname).replace(/^\/+/, "");
    let file = resolve(root, relative || "index.html");
    if (file !== root && !file.startsWith(root + sep)) {
      response.writeHead(403);
      response.end();
      return;
    }
    try {
      if ((await stat(file)).isDirectory()) {
        const index = resolve(file, "index.html");
        try {
          await stat(index);
          file = index;
        } catch {
          file += ".html";
        }
      }
    } catch {
      if (!extname(file)) file += ".html";
    }
    let bytes = await readFile(file);
    const headers = {
      "Content-Type": types[extname(file)] || "application/octet-stream",
      "Cache-Control": "no-store",
    };
    if (url.searchParams.has("nojs"))
      headers["Content-Security-Policy"] = "script-src 'none'";
    if (
      /html|css|javascript|json|svg|plain|xml/.test(headers["Content-Type"]) &&
      request.headers["accept-encoding"]?.includes("gzip")
    ) {
      bytes = gzipSync(bytes);
      headers["Content-Encoding"] = "gzip";
      headers["Vary"] = "Accept-Encoding";
    }
    response.writeHead(200, headers);
    response.end(bytes);
  } catch {
    response.writeHead(404, { "Content-Type": "text/plain" });
    response.end("Not found");
  }
}).listen(port, "127.0.0.1", () =>
  console.log(`Static export preview: http://127.0.0.1:${port}`),
);
