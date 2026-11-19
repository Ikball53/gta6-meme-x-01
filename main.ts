// Wake Me Up When GTA 6 Drops — entry program for gta6-meme-x-01.
//
// The meme itself lives in the X post named by POST.json; the house reads
// that post directly. This program's only job is to surface the post's
// address to the gate: it reads POST.json, checks the link looks like an
// X status URL, writes it into the output directory, and exits.

import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const POST_FILE = "POST.json";
const CAPTION_FILE = "caption.txt";
const OUTPUT_NAME = "post-url.txt";
const CAPTION_OUTPUT_NAME = "caption.txt";

function loadPostAddress(): string {
  const raw = readFileSync(POST_FILE, "utf8");
  const parsed = JSON.parse(raw) as { url?: unknown };
  if (typeof parsed.url !== "string" || parsed.url.length === 0) {
    throw new Error("POST.json carries no url string");
  }
  return parsed.url;
}

function looksLikeStatusLink(address: string): boolean {
  return /^https:\/\/x\.com\/[^/]+\/status\/\d+$/.test(address);
}

function loadCaption(): string {
  return readFileSync(CAPTION_FILE, "utf8");
}

function findPlayCode(caption: string): string | null {
  const match = caption.match(/makefun-[a-z]+-[a-z]+-[a-z]+/);
  return match ? match[0] : null;
}

function main(): void {
  const address = loadPostAddress();
  if (!looksLikeStatusLink(address)) {
    throw new Error(`unexpected post address: ${address}`);
  }
  const caption = loadCaption();
  const playCode = findPlayCode(caption);
  if (playCode === null) {
    throw new Error("caption.txt carries no play code");
  }
  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  mkdirSync(outDir, { recursive: true });
  writeFileSync(join(outDir, OUTPUT_NAME), address + "\n", "utf8");
  writeFileSync(join(outDir, CAPTION_OUTPUT_NAME), caption, "utf8");
  console.log(`post: ${address}`);
  console.log(`play code: ${playCode}`);
}

main();
