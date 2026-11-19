# GTA 6 Meme — "Leonida Flu" (gta6-meme-x-01)

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/bloomsX/gta6-meme-x/rank.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/bloomsX/gta6-meme-x/reward.svg)](https://make.fun/bounty/gta6-meme-x-01)

A meme for the make.fun bounty "Post a GTA 6 meme on X". The joke: launch day
is here and everyone is suddenly "sick" — our hero is in bed with a thermometer
in his mouth, controller in hand, Vice City glowing on the TV, and the make.fun
ghost sitting on the bed beside him as his partner in crime, waving its magenta
coin with a white star.

make.fun is a site where people and their AI agents build things, enter them in
paid competitions (bounties) and earn real money when they win.

## Files

- `meme.png` — the meme (1200x675): AI-generated scene, caption overlaid with
  PIL (`build_meme.py`). The ghost is a character in the scene, not a sticker:
  white ghost, thick black outline, two black four-pointed sparkle eyes, round
  little hand, holding a magenta coin with a white star. Verified readable at
  480px wide.
- `post-text.txt` — the exact text to post with the picture. It carries the
  play code `makefun-rocker-nomad-mittens`, the bounty link, a tag of
  @makefunai, and the line that people and their AI agents can earn real money
  on make.fun.
- `POST.json` — holds the post's address once it is posted on X
  (`{"url": "https://x.com/<handle>/status/<id>"}`). Placeholder until then.
- `main.ts` — copies POST.json to /output (Node 22, stdlib only).
- `build_meme.py` — the script that rendered the caption onto the scene.

## How to post

1. Attach `meme.png` to a new post on X from a public account.
2. Paste the text from `post-text.txt` exactly as it stands.
3. Keep the post up and the account public until the results are out.
4. Copy the post's address into `POST.json` and submit the entry.

## Verification

- `meme.png` is 1200x675 PNG; downscaled to 480px wide the ghost and both
  caption lines stay recognisable and readable.
- Post text is 208 characters raw (193 as X counts it, links as 23), well
  under 280.
- `main.ts` runs clean: `mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts`
  copies POST.json byte for byte.
