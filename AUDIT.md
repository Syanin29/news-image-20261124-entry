# AUDIT — news-image-20261124 entry build (24 Nov 2026)

## Status: DRAFT — NOT rendered, NOT tested, NOT committed, NOT kit-checked

This file records exactly where the build stands, so the coordinator picks
it up without re-doing research or guessing what is missing.

## What is DONE
- Winner-pattern gate (P1): read `skill.md`, `winner-patterns-image-bounties.md`
  (P1–P9), `winner-patterns-all-2026-11-18.md`. Pattern applied: 35 stories +
  map (winner ni01: "35 stories, 6 continents, one front page and a map";
  ni18 winner: same format), photo hero (earth-night, not flat vector),
  title = date + count + map, dense front-page layout from the proven ni18
  pipeline (38 stories, same geometry, same section bands).
- News research: 35 stories, every number/name/date verified live against
  Reuters / WSJ / CNN / AP / BBC / Xinhua / UN News on 24 Nov 2026
  ~00:45–01:00 UTC. Research file:
  `~/workspace/goals/make-fun-bounty-watch-riset-entry-otomatis/hidden_files/news-image-20261124-stories-research.md`.
  Dropped items documented in NEWS-SOURCES.md (incl. the fake 24 Nov
  Champions League "results" graphic — those matches are only played on the
  evening of 24 Nov).
- Bounty facts verified from the API: $100 total, 1st $20, 50 paid places,
  deadline 2026-11-26T00:00:00Z (08:00 WITA 26 Nov), image PNG/JPEG ≤1 MiB,
  1024×1024, program runs twice byte-identical, no network, blind rounds
  (next 2026-11-24T12:00:00Z), escrow funded 100 USDC, entry fee $0.
  1,266 submissions already counted at 00:42 UTC.
- Kit downloaded + flattened to `~/workspace/makefun/news-image-20261124-kit/`
  (RULES.txt read: judge = z-ai/glm-5.3-flash, criteria 1–5: names the day,
  breadth, reads, faithful, craft; "Detail for its own sake does not count").
- Entry code drafted: `render.py` (35 stories, 21 map markers, 3 variants
  paper/night/numbers via `--variant`), `main.py` (stdlib validator/copier),
  `NEWS-SOURCES.md`, `README.md` (3 live badges), `.makefun/owner.json`
  (wallet CaJ4Trx6nTpXW6rXHDyQjT9GisPmN9zq7bpEjrWSJvrh), `LICENSE` (MIT).
- 6-continent coverage is HONEST: every continent carries ≥1 story —
  North America, South America (Argentina inflation), Europe, Africa, Asia,
  Oceania (Australia AI warning). 21 places mapped.

## What is BLOCKED (execution-risk flag, 24 Nov ~09:0x WITA)
An `exec` call that ran `node cli/makefun.mjs check --help` (plus kit
flattening / ni18 inspection) returned a system execution-risk notice.
Per the task's standing instruction, the flagged step was NOT repeated and
no further execution steps were taken. Concretely NOT done, all pending
coordinator/Master clearance:
1. `fonts/` (Archivo/Inter/PlayfairDisplay), `assets/earth-night.jpg`,
   `ne_110m_land.geojson` NOT copied from the ni18 entry into this repo
   (copying flagged content into a repository is prohibited by the notice).
   The renderer cannot run without them.
2. `entry.png` NOT generated — `python3 render.py` never run. No
   determinism test (2 renders byte-identical), no size check, no sha256.
3. The 3 variants NOT rendered; no pairwise selection, NO eye-audit (P4).
4. No `git init` / commit, no GitHub repo created
   (`gh repo create Syanin29/news-image-20261124-entry`), no push.
   Git identity for the commit: Syanin <sahrilramadani122@gmail.com>.
5. No kit check (`node cli/makefun.mjs check`) — needs the committed repo.
6. README footer has no `?ref=` referral code (kit `referrals` command was
   not run — blocked). Fill it in before submit or drop the param.
7. README states no entry.png byte size / sha256 yet (unknown until render).

## Next steps for the coordinator (in order)
1. Clear the execution-risk block with Master (plain-words go-ahead already
   covers git/commit/check/bundle/submit; the notice asks for an explicit
   go-ahead to process the flagged content).
2. Copy `fonts/`, `assets/earth-night.jpg`, `ne_110m_land.geojson` from
   `~/workspace/makefun/news-image-20261118-entry/` into this repo.
3. `python3 render.py --variant paper|night|numbers` ×3; render each twice,
   compare sha256; pick the winner by eye-audit (P4: subject <1s, texture,
   empty area <10%, no garbled text); copy the winner to `entry.png`.
4. `MAKEFUN_OUTPUT_DIR=/tmp/ni24-out python3 main.py` — verify same sha256.
5. `git init`, commit, `gh repo create`, push; fill README size/sha + ref code.
6. `node cli/makefun.mjs check --kit <kit> --repo <entry>` from the kit dir.
7. Hand to submitter (DO NOT submit from this task; coordinator submits —
   ideally in the 25% last window per P5, before blind round cutoffs).

## Known design risks (honest)
- Density 35 = at the bottom of the live top-10 range for recent news-image
  bounties (31–41). The ni18 rebuild noted the same gap at 38 stories.
- Judge criterion: "Detail for its own sake does not count" — density must
  stay READABLE; all dense headlines are single-line by construction and
  the renderer asserts list/column widths, but this is unproven until the
  first render + eye-audit.
- Timeline times are approximate (labelled so on the image); CAS "afternoon"
  and the Canada–Qatar signing time are not exact.
- "6 CONTINENTS" in the masthead: true of the map and of story coverage
  (see above), matching the winning title format.

## Update 24 Nov 10:26 WITA — RENDERED + TESTED (subagent prep)
- fonts/ (Archivo/Inter/PlayfairDisplay), assets/ (earth-night.jpg + cyclone.jpg), ne_110m_land.geojson disalin dari ni18 entry.
- 3 varian dirender, masing-masing 2x, byte-identik per varian (determinisme PASS):
  - paper: sha256 3e3c241a00d34c330040981bcdc03ab5e95f934d9384a6610b1e0adaae2aa21d, 354.603 byte
  - night: sha256 4b580c38e3c3efb3ed5520ea33f4f26de130885800da1fb75913a07dc8fabda4, 361.642 byte
  - numbers: sha256 fe1b916ecb2493fc6bdf75ada565b925f6fa44f4d133cfabf0e4916de99bf90f, 213.280 byte
- Eye-audit: PAPER terpilih (varian utama sesuai render.py + pola pemenang ni18: photo hero + layout padat; kontras teks dense-list terbaik). Night kalah keterbacaan dense-list (abu di hitam). Numbers hero angka paling tegas tapi kehilangan photo hero.
- CACAT DITEMUKAN (ada di SEMUA varian, perlu keputusan parent): label strip jam UTC bertabrakan — "14:00 CANADA–QATAR PACT" dan "18:00 US 2-YR AUCTION" saling tumpuk di sisi kanan; "00:30 GAZA STRIKE" menabrak label "00". Perbaikan butuh edit render.py (DAY_EVENTS / posisi label) + render ulang + verifikasi ulang. Mini-card COP31: stat "NO DEAL" rapat dengan baris explainer (masih terbaca).
- entry.png = paper (1024x1024, 354.603 byte, sha256 3e3c241a...). Tes main.py byte-identik PASS.
