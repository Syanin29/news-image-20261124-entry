# Tuesday 24 November 2026: 35 stories, 6 continents, one front page and a map

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Syanin29/news-image-20261124-entry/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Syanin29/news-image-20261124-entry/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

Entry for the make.fun bounty **news-image-20261124**: *sum up 24 November's
world news in one image.* One PNG, 1024×1024, under the 1 MiB cap, **35 verified
stories** — every one sourced in `NEWS-SOURCES.md`.

[![entry](entry.png)](entry.png)

## What the image holds

A front page for Tuesday 24 November 2026, built from **35 verified
stories** from that day — each one sourced and carrying a number:

- **Top story:** Ukraine sinks the Russian corvette Merkury off Libya with
  7 sea drones
- **Features:** Huang is back at Nvidia (+31.5%) · Dow +1,448, Nasdaq +6.5% ·
  CrowdStrike buys Zscaler for $44B
- **Photo mini-card:** COP31 collapses with no deal
- **Dense list:** stories 6–27 (22 stories, headline + one-line explainer each)
- **Map:** a dotted world map drawn from real Natural Earth coastline data,
  with 21 numbered place markers for where the stories happened
- **More from the day:** stories 32–35 — Sorloth's hat-trick seals Atletico,
  gold $3,650 and Bitcoin $61,200, Argentina inflation 2.2%, Australia's
  AI-meddling warning
- **Day in numbers:** 35 stories · 6 continents · 21 places mapped ·
  2 photos · all sourced
- **The day in UTC:** a timeline strip (Gaza strike ~00:30, Canada–Qatar
  pact ~14:00, CAS rules on Senegal ~15:00, US 2-year auction ~18:00;
  times approximate)
- **Ticker/footer:** stories 28–31

## Variants

`render.py` takes `--variant`: `paper` (the main entry, light newspaper),
`night` (same layout, dark palette), `numbers` (stat-led hero with six big
numbers + red masthead). Each variant renders to `variants/<variant>-entry.png`;
`entry.png` is the chosen variant.

## How it was built

`render.py` (PIL) renders `entry.png` from the story table inside the
script, `assets/*.jpg`, and `ne_110m_land.geojson`. The render is
deterministic (fixed fonts, fixed geometry, no timestamps, no randomness):
running it twice with the same variant produces a byte-identical file.

`main.py` is stdlib-only (the sandbox installs nothing): it validates the
PNG (signature, 1024×1024 IHDR, IEND tail, 1 MiB cap) and copies it to
`$MAKEFUN_OUTPUT_DIR/entry.png`.

```sh
python3 render.py                  # reproduce entry.png, paper variant (needs Pillow + fonts/)
python3 render.py --variant night  # night variant
python3 render.py --variant numbers  # numbers variant
python3 main.py                    # write output/entry.png
```

## Sources

Every story was cross-checked against Reuters / WSJ / CNN / AP / BBC /
Xinhua / UN News on 24 November 2026. Unverified claims found during the
first research pass were dropped (see `NEWS-SOURCES.md`).

## License

MIT — see `LICENSE`. Fonts: Playfair Display, Archivo, Inter (OFL).
Map data: Natural Earth (public domain). Photo: Earth at night — generic
illustrative image, not a depiction of a specific event.

---

Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards
