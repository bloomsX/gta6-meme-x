// gta6-meme-x-01 — round 2 hand-in ("Speed Waits, Agent Gets Paid").
//
// The entry itself is the X post: IShowSpeed screaming after 13 years of
// waiting for GTA 6 while the make.fun ghost already got paid. The house
// reads that post live from X — its first picture and its text — and puts
// them in front of the judge. This script only hands the house the post's
// address, which lives in POST.json next to this file.
//
// What it does, in order:
//   1. read POST.json and check it carries a usable X status URL,
//   2. create the output directory,
//   3. copy POST.json there byte for byte, so the grader finds it.
//
// Run it outside the grader container with the two directories faked:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const POST_PATH = join(BOT_DIR, 'POST.json');
const DEST_PATH = join(OUTPUT_DIR, 'POST.json');

function fail(message: string): never {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

function readPostUrl(): string {
  if (!existsSync(POST_PATH)) {
    fail(`POST.json not found at ${POST_PATH} — post the meme on X first and write its URL into POST.json.`);
  }
  let parsed: unknown;
  try {
    parsed = JSON.parse(readFileSync(POST_PATH, 'utf8'));
  } catch (err) {
    fail(`POST.json at ${POST_PATH} is not valid JSON: ${(err as Error).message}`);
  }
  const url = (parsed as { url?: unknown } | null)?.url;
  if (typeof url !== 'string' || url.length === 0) {
    fail('POST.json must contain a non-empty string `url` — post the meme on X first and write its URL into POST.json.');
  }
  if (!/^https?:\/\/(x\.com|twitter\.com)\/\w+\/status\/\d+/.test(url)) {
    fail(`POST.json url does not look like a public X status: ${url}`);
  }
  return url;
}

const postUrl = readPostUrl();
console.log(`Handing in X post: ${postUrl}`);

mkdirSync(OUTPUT_DIR, { recursive: true });
copyFileSync(POST_PATH, DEST_PATH);
const bytes = statSync(DEST_PATH).size;
console.log(`Copied POST.json (${bytes} bytes) to ${DEST_PATH}`);

// Prove the hand-in is the post we validated: read the copy back and
// confirm it still names the same URL. A truncated or swapped copy
// must fail loudly here, not silently in front of the grader.
const handedIn = JSON.parse(readFileSync(DEST_PATH, 'utf8')) as { url?: unknown };
if (handedIn.url !== postUrl) {
  fail(`copied POST.json does not name ${postUrl} — hand-in is corrupt, refusing to continue.`);
}
console.log('Hand-in verified: the copied POST.json names the same X post.');
