// Entry program for the gta6-meme-x-01 competition (Node 22, stdlib only).
//
// The graded entry is the public X post named in POST.json; the house
// reads that post itself. This program validates POST.json and copies it
// into the grader's output directory. No network access is used.

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// The entry folder comes from MAKEFUN_BOT_DIR when the harness sets it;
// otherwise fall back to the folder this script file lives in.
const botDir: string =
  process.env.MAKEFUN_BOT_DIR ?? dirname(fileURLToPath(import.meta.url));
const outDir: string = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const sourcePath: string = join(botDir, "POST.json");
const raw: string = readFileSync(sourcePath, "utf8");

// Fail loudly on a malformed post file instead of copying garbage:
// the gate reads POST.json, so it must be JSON with a string url
// pointing at an x.com status over https.
const parsed: unknown = JSON.parse(raw);
const url: unknown = (parsed as { url?: unknown }).url;
if (typeof url !== "string") {
  throw new Error('POST.json must hold {"url": "https://x.com/<handle>/status/<id>"}');
}
const parsedUrl: URL = new URL(url);
if (parsedUrl.protocol !== "https:" || !parsedUrl.hostname.endsWith("x.com")) {
  throw new Error(`POST.json url must be an https x.com link, got: ${url}`);
}

mkdirSync(outDir, { recursive: true });
const targetPath: string = join(outDir, "POST.json");
writeFileSync(targetPath, raw.endsWith("\n") ? raw : raw + "\n", "utf8");

console.log(`POST.json copied to ${targetPath}`);
console.log(`entry url: ${url}`);
console.log("done");
