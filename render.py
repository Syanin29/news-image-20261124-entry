#!/usr/bin/env python3
"""Front page for Tuesday 24 November 2026 — 35 sourced stories, one image.

A single deterministic 1024x1024 PNG: masthead, photo hero, three feature
cards, a photo mini-card, a 22-story dense list, a dotted world map built
from Natural Earth coastline data, a four-story "more" band, a day-in-numbers
bar, a UTC timeline of the day, and a footer ticker. Fixed fonts, fixed
geometry, no clock, no randomness — running the script twice with the same
variant yields a byte-identical file, and the file stays under the 1 MiB cap.

Three variants, one layout engine (--variant paper | night | numbers):
- paper   : light newspaper front page (the main entry).
- night   : same layout, dark palette.
- numbers : paper palette, but the hero is a dark big-numbers band instead
            of the photo, and the masthead is red — a stat-led front page.

Usage: python3 render.py [--variant paper|night|numbers]
"""

import argparse
import json
import struct
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
W, H = 1024, 1024
BYTE_CAP = 1024 * 1024

# ---------------------------------------------------------------------------
# Palettes. paper is the main entry; night recolors the same geometry.
# ---------------------------------------------------------------------------
PALETTES = {
    "paper": {
        "INK": (30, 30, 30), "FAINT": (80, 80, 80), "PAPER": (255, 255, 255),
        "BAND": (245, 245, 245), "RED": (220, 50, 50), "DARK": (25, 25, 25),
        "TICKER_GREY": (220, 220, 220), "HERO_BAR": (0, 0, 0),
        "HERO_SUB": (200, 230, 255), "MASTHEAD_BG": (245, 245, 245),
        "MASTHEAD_FG": (30, 30, 30),
    },
    "night": {
        "INK": (235, 235, 238), "FAINT": (168, 168, 175),
        "PAPER": (16, 18, 24), "BAND": (34, 38, 50), "RED": (255, 92, 80),
        "DARK": (8, 8, 12), "TICKER_GREY": (40, 44, 56),
        "HERO_BAR": (0, 0, 0), "HERO_SUB": (190, 215, 255),
        "MASTHEAD_BG": (34, 38, 50), "MASTHEAD_FG": (235, 235, 238),
    },
    "numbers": {
        "INK": (30, 30, 30), "FAINT": (80, 80, 80), "PAPER": (255, 255, 255),
        "BAND": (245, 245, 245), "RED": (200, 30, 30), "DARK": (25, 25, 25),
        "TICKER_GREY": (220, 220, 220), "HERO_BAR": (18, 18, 22),
        "HERO_SUB": (200, 230, 255), "MASTHEAD_BG": (200, 30, 30),
        "MASTHEAD_FG": (255, 255, 255),
    },
}

# Active palette (set in main).
P = PALETTES["paper"]


def font(name, size):
    return ImageFont.truetype(str(HERE / "fonts" / name), size)


# ---------------------------------------------------------------------------
# The day's news. One dict per story: n = printed number, h = headline,
# d = one-line explainer, s = big stat, p = photo asset or None,
# k = map-marker key (see PLACES). Every story is sourced in NEWS-SOURCES.md.
# ---------------------------------------------------------------------------

STORIES = [
    {"n": 1, "h": "UKRAINE SINKS RUSSIAN WARSHIP OFF LIBYA", "d": "7 sea drones sink corvette Merkury at Benghazi; Ka-27 helicopter destroyed; cargo ship MV Angara hit", "s": "7 SEA DRONES", "p": "earth-night.jpg", "k": 1},
    {"n": 2, "h": "HUANG IS BACK AT NVIDIA", "d": "Nvidia reinstates Jensen Huang as CEO; shares +31.5%, biggest jump since 2003", "s": "+31.5%", "p": None, "k": 2},
    {"n": 3, "h": "DOW +1,448; NASDAQ +6.5%", "d": "Wall Street's best day since April 2025 on the Nvidia rally; S&P +4.7%", "s": "DOW +1,448", "p": None, "k": 2},
    {"n": 4, "h": "CROWDSTRIKE BUYS ZSCALER FOR $44B", "d": "Biggest cyber deal as threats mount; CrowdStrike snaps up Zscaler", "s": "$44B", "p": None, "k": 2},
    {"n": 5, "h": "COP31 COLLAPSES, NO DEAL", "d": "Climate talks in Antalya end with no agreement; ~200 countries reject the Antalya Pact", "s": "NO DEAL", "p": "earth-night.jpg", "k": 19},
    {"n": 6, "h": "TRUMP: NEW IRAN STRIKES AFTER NEW YEAR", "d": "Trump 'inclined' to restart strikes if talks fail; dares Iran to test blockade", "s": "AFTER JAN 1", "p": None, "k": 2},
    {"n": 7, "h": "DEMOCRATS TAKE 258 HOUSE SEATS", "d": "Largest House majority since 1992; Hubbard beats Foxx by 330 votes", "s": "258 SEATS", "p": None, "k": 2},
    {"n": 8, "h": "CANADA–QATAR SIGN INVESTMENT PACT", "d": "Deal to unlock Qatari investment pledged in January; signing on Tuesday", "s": "TUESDAY SIGNING", "p": None, "k": 4},
    {"n": 9, "h": "NORTH KOREA MAY SHUT SWISS OFFICE", "d": "Pyongyang condemns Swiss sanctions on a children's camp; closure weighed", "s": "KCNA", "p": None, "k": 5},
    {"n": 10, "h": "CAS TO RULE ON SENEGAL AFCON APPEAL", "d": "Decision due Tuesday afternoon on the stripped Africa Cup of Nations title", "s": "TODAY", "p": None, "k": 6},
    {"n": 11, "h": "INDIA EYES 20% RICE EXPORT DUTY", "d": "New Delhi weighs duty to cool domestic prices; decision after talks", "s": "~20%", "p": None, "k": 7},
    {"n": 12, "h": "DEPUTY FBI DIRECTOR TO RETIRE", "d": "Christopher Raia to leave in December, latest departure under Trump", "s": "DECEMBER", "p": None, "k": 2},
    {"n": 13, "h": "SOUTH KOREA SECURITY RESHUFFLE", "d": "Lee replaces foreign, spy and unification chiefs; first woman NIS chief", "s": "5 POSTS", "p": None, "k": 16},
    {"n": 14, "h": "INDIA GIVES NEPAL $1.62B", "d": "Flood-hit Nepal package, one of India's largest-ever aid commitments", "s": "$1.62B", "p": None, "k": 7},
    {"n": 15, "h": "EBOLA IN DRC TOPS 11,000 CASES", "d": "5,400 deaths; WHO says outbreak more than doubled in three months", "s": "11,000+ CASES", "p": None, "k": 8},
    {"n": 16, "h": "NIGERIA BOAT CAPSIZE KILLS 24", "d": "Mourners' boat capsizes in Bayelsa State; 24 rescued", "s": "24 DEAD", "p": None, "k": 9},
    {"n": 17, "h": "IRAN HITS SITE IN BAHRAIN", "d": "Industrial site struck; two tankers hit by projectiles in the Strait of Hormuz", "s": "2 TANKERS", "p": None, "k": 10},
    {"n": 18, "h": "KYIV FLAT BLAST KILLS 11", "d": "Russian strike on a Kyiv apartment building; rescue under way", "s": "11 KILLED", "p": None, "k": 11},
    {"n": 19, "h": "POLAND: 3 CRASHED OBJECTS WERE KH-101s", "d": "Prosecutors say debris was Russian Kh-101 cruise missiles", "s": "KH-101", "p": None, "k": 12},
    {"n": 20, "h": "TAIWAN COUNTS 24 PLA AIRCRAFT", "d": "17 cross the median line; 11 warships, 10 balloons", "s": "24 JETS", "p": None, "k": 13},
    {"n": 21, "h": "BRUSSELS FLIGHTS AXED", "d": "Strike cancels 429 airport flights Monday; 59,000 passengers hit", "s": "429 FLIGHTS", "p": None, "k": 14},
    {"n": 22, "h": "IRAN INFLATION 76.8%", "d": "October prices rose 4.8% in the month", "s": "76.8%", "p": None, "k": 10},
    {"n": 23, "h": "SUDAN DRONES HIT HOMES", "d": "Strikes across Khartoum and Omdurman kill children, hit aid building", "s": "KHARTOUM", "p": None, "k": 15},
    {"n": 24, "h": "GAZA: 6 KILLED IN 24 HOURS", "d": "Health officials: 6 killed, 33 wounded, incl. 2 at aid sites", "s": "6 KILLED", "p": None, "k": 3},
    {"n": 25, "h": "SPARTA II ADRIFT IN BALTIC", "d": "Russian cargo vessel damaged by drones; Finnish rescue under way", "s": "BALTIC RESCUE", "p": None, "k": 12},
    {"n": 26, "h": "TAJIKISTAN QUITS THE ICC", "d": "Dushanbe withdraws from the International Criminal Court", "s": "ICC EXIT", "p": None, "k": 17},
    {"n": 27, "h": "ARMENIA DROPS KARABAKH CLAIM", "d": "New constitution proposal removes Nagorno-Karabakh claims", "s": "NEW CHARTER", "p": None, "k": 18},
    {"n": 28, "h": "GAZA STRIKE KILLS 3", "d": "Israeli airstrike near police outpost in Khan Younis, medics say", "s": "3 KILLED", "p": None, "k": 3},
    {"n": 29, "h": "PSG 6–0 VILLARREAL", "d": "PSG top of Champions League league phase, 12 points", "s": "6–0", "p": None, "k": 14},
    {"n": 30, "h": "COMO 9–1 LENS", "d": "Record-equalling Champions League win; Douvikas hat-trick", "s": "9–1", "p": None, "k": 14},
    {"n": 31, "h": "BARCA 4–2 SLAVIA", "d": "Fermin Lopez double; Slavia eliminated", "s": "LOPEZ ×2", "p": None, "k": 14},
    {"n": 32, "h": "SORLOTH HAT-TRICK SEALS ATLETICO", "d": "4–1 over Club Brugge, 7–4 on aggregate", "s": "HAT-TRICK", "p": None, "k": 14},
    {"n": 33, "h": "GOLD $3,650; BITCOIN $61,200", "d": "Gold +4% in the Nvidia rally; BTC under +1%", "s": "GOLD +4%", "p": None, "k": 2},
    {"n": 34, "h": "ARGENTINA INFLATION 2.2%", "d": "October prices +2.2%, fastest rise since April", "s": "2.2%", "p": None, "k": 21},
    {"n": 35, "h": "AUSTRALIA WARNS ON AI MEDDLING", "d": "Canberra: AI will be exploited by foreign actors", "s": "AI WARNING", "p": None, "k": 20},
]

# Map places keyed by the marker number printed on the map. 21 places drawn.
PLACES = {
    1: (20.1, 32.1), 2: (-77.0, 38.9), 3: (34.4, 31.3), 4: (-75.7, 45.4),
    5: (125.8, 39.0), 6: (6.6, 46.5), 7: (77.2, 28.6), 8: (15.3, -4.3),
    9: (6.3, 4.9), 10: (56.3, 26.5), 11: (30.5, 50.4), 12: (21.0, 52.2),
    13: (121.6, 25.0), 14: (4.4, 50.8), 15: (32.5, 15.6), 16: (127.0, 37.5),
    17: (68.8, 38.6), 18: (44.5, 40.2), 19: (30.7, 36.9), 20: (149.1, -35.3),
    21: (-58.4, -34.6),
}

# Display-only nudges for the tightest marker pairs (circles r=9 would
# otherwise overlap). Geography underneath is unchanged.
NUDGE = {
    1: (0, -6), 3: (0, 6), 2: (0, 7), 4: (0, -7),
    6: (0, 8), 14: (0, -8), 11: (2, 7), 12: (-2, -7),
    5: (0, -8), 16: (0, 8),
}

# The day, hour by hour (UTC). Times are approximate except the CAS
# afternoon window; the strip says so on the image.
DAY_EVENTS = [
    (0.5, "00:30 GAZA STRIKE", "down"),
    (14.0, "14:00 CANADA–QATAR PACT", "up"),
    (15.0, "15:00 CAS RULES SENEGAL", "down"),
    (18.0, "18:00 US 2-YR AUCTION", "up"),
]

# Big numbers for the "numbers" variant hero.
BIG_NUMBERS = [
    ("35", "STORIES"), ("7", "SEA DRONES"), ("+31.5%", "NVIDIA"),
    ("258", "HOUSE SEATS"), ("11,000+", "EBOLA CASES"), ("$44B", "CYBER DEAL"),
]

# Vertical plan for the page (pixels from the top).
Y_MASTHEAD = (0, 50)
Y_HERO = (50, 190)
Y_FEATURES = (190, 320)
Y_MINI = (320, 370)
Y_LOWER = 370
X_SPLIT = 500          # dense list left of this, map right of it
Y_MAP_END = 740
Y_MORE = (748, 896)
Y_COUNTS = (904, 948)
Y_CLOCK = (956, 996)
Y_TICKER = (996, 1024)


def text_w(d, s, f):
    return d.textlength(s, font=f)


def text_h(d, s, f):
    box = d.textbbox((0, 0), s, font=f)
    return box[3] - box[1]


def wrap(d, s, f, width, limit=None):
    """Greedy wrap; every returned line fits inside width."""
    out, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if text_w(d, trial, f) <= width:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out[:limit] if limit is not None else out


def rect(d, x, y, w, h, fill):
    d.rectangle([x, y, x + w, y + h], fill=fill)


def put(d, x, y, s, f, fill=None):
    d.text((x, y), s, font=f, fill=fill if fill is not None else P["INK"])


def put_centre(d, cx, y, s, f, fill=None):
    d.text((cx, y), s, font=f, fill=fill if fill is not None else P["INK"],
           anchor="ma")


def fit_size(d, s, sizes, width, name="Inter.ttf"):
    """Largest size from sizes whose rendering of s fits width."""
    for size in sizes:
        f = font(name, size)
        if text_w(d, s, f) <= width:
            return f
    return font(name, sizes[-1])


def project(lon, lat, x0, y0, w, h):
    """Equirectangular projection of lon/lat into the map rectangle."""
    return x0 + (lon + 180.0) / 360.0 * w, y0 + (90.0 - lat) / 180.0 * h


# ---------------------------------------------------------------------------
# Sections. Each draws one band of the page and returns nothing; the caller
# owns the vertical plan above, so no section may paint outside its band.
# ---------------------------------------------------------------------------

def draw_masthead(d):
    y0, y1 = Y_MASTHEAD
    rect(d, 0, y0, W, y1 - y0, P["MASTHEAD_BG"])
    line = "TUESDAY, 24 NOVEMBER 2026 • 35 STORIES • 6 CONTINENTS"
    f = font("PlayfairDisplay.ttf", 34)
    assert text_w(d, line, f) <= W - 20, "masthead too wide"
    put_centre(d, W // 2, y0 + 8, line, f, P["MASTHEAD_FG"])


def draw_hero(im, d):
    y0, y1 = Y_HERO
    photo = HERE / "assets" / "earth-night.jpg"
    if photo.exists():
        shot = Image.open(photo).resize((W, y1 - y0), Image.LANCZOS).convert("RGB")
        im.paste(shot, (0, y0))
    else:
        rect(d, 0, y0, W, y1 - y0, (20, 20, 50))
    top = STORIES[0]
    rect(d, 0, y1 - 40, W, 40, P["HERO_BAR"])
    put(d, 20, y1 - 39, top["h"], font("Archivo.ttf", 24), (255, 255, 255))
    put(d, 20, y1 - 15, top["d"], font("Inter.ttf", 12), P["HERO_SUB"])


def draw_numbers_hero(d):
    """Stat-led hero for the numbers variant: dark band, six big numbers."""
    y0, y1 = Y_HERO
    rect(d, 0, y0, W, y1 - y0, P["HERO_BAR"])
    top = STORIES[0]
    put(d, 20, y0 + 8, top["h"], font("Archivo.ttf", 24), (255, 255, 255))
    put(d, 20, y0 + 38, top["d"], font("Inter.ttf", 12), P["HERO_SUB"])
    slot = W / 6
    big_f = font("Archivo.ttf", 30)
    lab_f = font("Inter.ttf", 11)
    for i, (num, lab) in enumerate(BIG_NUMBERS):
        cx = slot * i + slot / 2
        put_centre(d, cx, y0 + 66, num, big_f, P["RED"])
        put_centre(d, cx, y0 + 104, lab, lab_f, (255, 255, 255))


def draw_features(d):
    y0, y1 = Y_FEATURES
    card_w, gap = 310, 20
    total = 3 * card_w + 2 * gap
    x = (W - total) // 2
    for story in STORIES[1:4]:
        rect(d, x, y0, card_w, y1 - y0, P["PAPER"])
        inner = card_w - 16
        cy = y0 + 6
        head = f"{story['n']}. {story['h']}"
        hf = fit_size(d, head, (18, 16, 14, 12), inner)
        for ln in wrap(d, head, hf, inner, limit=2):
            put(d, x + 8, cy, ln, hf)
            cy += text_h(d, ln, hf) + 2
        ef = font("Inter.ttf", 12)
        for ln in wrap(d, story["d"], ef, inner, limit=2):
            put(d, x + 8, cy, ln, ef, P["FAINT"])
            cy += text_h(d, ln, ef) + 2
        put(d, x + 8, cy + 2, story["s"], font("Inter.ttf", 13), P["RED"])
        x += card_w + gap


def draw_mini(im, d):
    y0, y1 = Y_MINI
    photo = HERE / "assets" / "earth-night.jpg"
    if photo.exists():
        # A different crop of the same Earth photo (Asia side) so the
        # thumbnail does not duplicate the hero frame.
        src = Image.open(photo).convert("RGB")
        w, h = src.size
        crop = src.crop((int(w * 0.55), int(h * 0.15),
                         int(w * 0.55) + 320, int(h * 0.15) + 160))
        shot = crop.resize((80, 40), Image.LANCZOS)
        im.paste(shot, (20, y0 + 5))
    else:
        rect(d, 20, y0 + 5, 80, 40, (180, 180, 220))
    story = STORIES[4]
    put(d, 110, y0 + 5, f"5. {story['h']}", font("Archivo.ttf", 20))
    put(d, 110, y0 + 27, story["d"], font("Inter.ttf", 12), P["FAINT"])
    put(d, 110, y0 + 41, story["s"], font("Inter.ttf", 13), P["RED"])


def draw_dense_list(d):
    """Stories 6-27 in the left column: headline, then one explainer line.
    Rows are 24 px so all 22 fit above the count bar (which starts at 904)."""
    y = Y_LOWER + 2
    head_f = font("Inter.ttf", 12)
    expl_f = font("Inter.ttf", 9)
    for story in STORIES[5:27]:
        head = f"{story['n']}. {story['h']}"
        if text_w(d, head, head_f) <= X_SPLIT - 24:
            put(d, 8, y, head, head_f)
            y += 12
        else:
            for ln in wrap(d, head, head_f, X_SPLIT - 24, limit=2):
                put(d, 8, y, ln, head_f)
                y += 12
        put(d, 8, y + 3, story["d"], expl_f, P["FAINT"])
        y += 12
    assert y <= Y_COUNTS[0], f"dense list overran: ends at {y}"
    return y


def draw_map(d):
    """Dotted continents from Natural Earth, then numbered place markers."""
    x0, y0, x1, y1 = X_SPLIT, Y_LOWER, W, Y_MAP_END
    geo = HERE / "ne_110m_land.geojson"
    land = json.loads(geo.read_text())
    for feat in land["features"]:
        rings = feat["geometry"]["coordinates"]
        for ring in rings:
            pts = [(project(lon, lat, x0, y0, x1 - x0, y1 - y0))
                   for lon, lat in ring]
            for j in range(0, len(pts), 4):
                px, py = pts[j]
                d.rectangle([px - 1, py - 1, px + 1, py + 1], fill=P["INK"])
    num_f = font("Inter.ttf", 10)
    for key in sorted(PLACES):
        lon, lat = PLACES[key]
        px, py = project(lon, lat, x0, y0, x1 - x0, y1 - y0)
        dx, dy = NUDGE.get(key, (0, 0))
        px, py = px + dx, py + dy
        r = 9
        d.ellipse([px - r, py - r, px + r, py + r], fill=P["BAND"],
                  outline=P["INK"], width=2)
        d.text((px, py), str(key), font=num_f, fill=P["INK"], anchor="mm")


def draw_more(d):
    """Stories 32-35: two columns under the map, headline + explainer each."""
    y0, y1 = Y_MORE
    head_f = font("Archivo.ttf", 12)
    put(d, X_SPLIT + 8, y0 + 2, "MORE FROM THE DAY — EVERY STORY SOURCED",
        head_f)
    cols = [(X_SPLIT + 8, STORIES[31:33]), (X_SPLIT + 256, STORIES[33:35])]
    hf = font("Inter.ttf", 11)
    ef = font("Inter.ttf", 9)
    for cx, group in cols:
        ry = y0 + 24
        for story in group:
            head = f"{story['n']}. {story['h']}"
            assert text_w(d, head, hf) <= 248, head
            assert text_w(d, story["d"], ef) <= 248, story["d"]
            put(d, cx, ry, head, hf)
            put(d, cx, ry + 13, story["d"], ef, P["FAINT"])
            ry += 27
    return y1


def draw_counts(d):
    y0, y1 = Y_COUNTS
    rect(d, 0, y0, W, y1 - y0, P["DARK"])
    line = "35 STORIES  •  6 CONTINENTS  •  21 PLACES MAPPED  •  2 PHOTOS  •  ALL SOURCED"
    f = font("Inter.ttf", 13)
    assert text_w(d, line, f) <= W - 20, "count bar too wide"
    put_centre(d, W // 2, y0 + 13, line, f, (255, 255, 255))


def draw_clock(d):
    """UTC timeline of the day across the right column, times approximate."""
    y0, y1 = Y_CLOCK
    x0, x1 = X_SPLIT + 16, W - 16
    axis_y = y0 + 22
    put(d, x0, y0 + 2, "THE DAY IN UTC — TIMES APPROXIMATE",
        font("Archivo.ttf", 10), P["FAINT"])
    d.line([x0, axis_y, x1, axis_y], fill=P["INK"], width=2)
    small = font("Inter.ttf", 8)
    d.text((x0, axis_y + 4), "00", font=small, fill=P["FAINT"])
    d.text((x1 - 12, axis_y + 4), "24", font=small, fill=P["FAINT"])
    for hour, label, side in DAY_EVENTS:
        ex = x0 + hour / 24.0 * (x1 - x0)
        d.ellipse([ex - 4, axis_y - 4, ex + 4, axis_y + 4], fill=P["RED"])
        lw = text_w(d, label, small)
        lx = max(x0, min(ex - lw / 2, x1 - lw))
        if side == "up":
            d.text((lx, axis_y - 16), label, font=small, fill=P["INK"])
        else:
            d.text((lx, axis_y + 6), label, font=small, fill=P["INK"])


def draw_ticker(d):
    y0, y1 = Y_TICKER
    rect(d, 0, y0, W, y1 - y0, P["TICKER_GREY"])
    items = ["28 GAZA STRIKE KILLS 3", "29 PSG 6–0 VILLARREAL",
             "30 COMO 9–1 LENS", "31 BARCA 4–2 SLAVIA"]
    tf = font("Inter.ttf", 11)
    slot = W / 4
    for i, item in enumerate(items):
        assert text_w(d, item, tf) <= slot - 20, item
        put(d, i * slot + 10, y0 + 7, item, tf)


# ---------------------------------------------------------------------------
# Assembly, PNG validation, entry point
# ---------------------------------------------------------------------------

def build(variant):
    global P
    P = PALETTES[variant]
    im = Image.new("RGB", (W, H), P["PAPER"])
    d = ImageDraw.Draw(im)
    draw_masthead(d)
    if variant == "numbers":
        draw_numbers_hero(d)
    else:
        draw_hero(im, d)
    draw_features(d)
    draw_mini(im, d)
    draw_dense_list(d)
    draw_map(d)
    draw_more(d)
    draw_counts(d)
    draw_clock(d)
    draw_ticker(d)
    out = HERE / "entry.png"
    im.save(str(out), "PNG")
    variant_path = HERE / "variants" / f"{variant}-entry.png"
    variant_path.parent.mkdir(parents=True, exist_ok=True)
    im.save(str(variant_path), "PNG")
    print(f"rendered {out} ({W}x{H}) variant={variant}")
    return im


def check_png(path):
    """PNG magic, IHDR size, trailing IEND, byte cap — all must hold."""
    raw = Path(path).read_bytes()
    if len(raw) > BYTE_CAP:
        raise SystemExit(f"PNG is {len(raw)} bytes, over the 1 MiB cap")
    if not raw.startswith(b"\x89PNG\r\n\x1a\n"):
        raise SystemExit("bad PNG signature")
    if len(raw) < 33 or raw[12:16] != b"IHDR":
        raise SystemExit("missing IHDR chunk")
    w, h = struct.unpack(">II", raw[16:24])
    if (w, h) != (W, H):
        raise SystemExit(f"PNG is {w}x{h}, expected {W}x{H}")
    if raw[-12:] != b"\x00\x00\x00\x00IEND\xaeB`\x82":
        raise SystemExit("missing IEND chunk")
    return raw


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", default="paper",
                    choices=["paper", "night", "numbers"])
    args = ap.parse_args()
    build(args.variant)
    check_png(HERE / "entry.png")
    print("entry.png valid: 1024x1024, under 1 MiB, IEND present")
