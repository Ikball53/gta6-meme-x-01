// gta6-meme-x-01 — entry v3
// The meme lives on X; this little runner just hands the grader the
// address of that post. It reads POST.json sitting next to itself
// (or wherever MAKEFUN_BOT_DIR points), sanity-checks the URL, and
// drops an untouched copy into the output folder.

import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// An X status link: host is x.com or twitter.com (optionally www. or
// mobile.), then either "<handle>/status/<id>" or "i/web/status/<id>".
const STATUS_LINK =
  /^https:\/\/(?:www\.|mobile\.)?(?:x\.com|twitter\.com)\/(?:[A-Za-z0-9_]{1,15}\/status\/\d+|i\/web\/status\/\d+)\/?$/;

function entryFolder(): string {
  const fromEnv = process.env.MAKEFUN_BOT_DIR;
  if (fromEnv && fromEnv.trim() !== "") return fromEnv;
  // No env hint: trust the location of this very file.
  return dirname(fileURLToPath(import.meta.url));
}

function loadPostAddress(folder: string): string {
  const postPath = join(folder, "POST.json");
  const rawText = readFileSync(postPath, "utf8");
  const parsed: unknown = JSON.parse(rawText);
  if (typeof parsed !== "object" || parsed === null) {
    throw new Error("POST.json must contain a JSON object");
  }
  const urlValue = (parsed as Record<string, unknown>).url;
  const cleaned = typeof urlValue === "string" ? urlValue.trim() : "";
  if (!STATUS_LINK.test(cleaned)) {
    throw new Error(`POST.json needs an X status url, got: ${String(urlValue)}`);
  }
  return cleaned;
}

function main(): void {
  const home = entryFolder();
  const destination = process.env.MAKEFUN_OUTPUT_DIR || "/output";
  const address = loadPostAddress(home);
  mkdirSync(destination, { recursive: true });
  copyFileSync(join(home, "POST.json"), join(destination, "POST.json"));
  console.log(`ok: POST.json copied for ${address}`);
}

main();
