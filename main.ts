// gta6-meme-x-01 — hand-in for the "Leonida Flu" GTA 6 meme X post.
// This script's only job is to pass the house the address of the X post
// that carries the meme, so the house can fetch that post itself and put
// its first picture and its text in front of the judge.
// POST.json holds just that address: one `url` field pointing at the
// public X status. Nothing written here about the meme is scored — the
// post on X is what counts, read live by the house, not by this script.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const POST_PATH = join(BOT_DIR, 'POST.json');

// Check the hand-in address before copying anything: POST.json must parse
// as JSON and carry a non-empty string `url` for an X status.
let postUrl = '';
try {
  const parsed: unknown = JSON.parse(readFileSync(POST_PATH, 'utf8'));
  const url = (parsed as { url?: unknown } | null)?.url;
  if (typeof url !== 'string' || url.length === 0 || !/^https?:\/\/(x\.com|twitter\.com)\//.test(url)) {
    throw new Error('POST.json must contain a non-empty string `url` starting with https://x.com/ or https://twitter.com/');
  }
  postUrl = url;
} catch (err) {
  console.error(`Invalid POST.json at ${POST_PATH}: ${(err as Error).message}`);
  process.exit(1);
}
console.log(`Handing in X post: ${postUrl}`);

mkdirSync(OUTPUT_DIR, { recursive: true });
try {
  copyFileSync(POST_PATH, join(OUTPUT_DIR, 'POST.json'));
} catch (err) {
  console.error(`POST.json could not be copied from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}
