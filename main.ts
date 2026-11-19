// Entry program for the gta6-meme-x-01 bounty.
//
// The judged artifact is the X post itself, which the house reads on
// its own. This program has exactly one job: take POST.json from the
// repository root and copy it into the output directory so the gate
// can read the post address from there.

import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const repoRoot: string = process.env.MAKEFUN_BOT_DIR ?? ".";
const outputDir: string = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const sourcePath: string = join(repoRoot, "POST.json");
const targetPath: string = join(outputDir, "POST.json");

// Fail loudly here rather than hand the gate a file it cannot read:
// POST.json must be a JSON object carrying the post address as a string.
const parsed: unknown = JSON.parse(readFileSync(sourcePath, "utf8"));
if (
  typeof parsed !== "object" ||
  parsed === null ||
  typeof (parsed as { url?: unknown }).url !== "string"
) {
  throw new Error("POST.json must be a JSON object with a string \"url\"");
}

mkdirSync(outputDir, { recursive: true });
copyFileSync(sourcePath, targetPath);

console.log(`POST.json copied to ${targetPath}`);
