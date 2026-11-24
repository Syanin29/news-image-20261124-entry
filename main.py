#!/usr/bin/env python3
"""Ship the rendered front page.

Reads entry.png from this directory, checks it is really the 1024x1024
PNG the renderer produced (magic, IHDR size, IEND tail, 1 MiB cap), then
copies it to $MAKEFUN_OUTPUT_DIR/entry.png. Stdlib only; installs nothing.

Usage: MAKEFUN_OUTPUT_DIR=/some/dir python3 main.py
"""

import os
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SIZE = (1024, 1024)
CAP = 1024 * 1024
IEND_TAIL = b"\x00\x00\x00\x00IEND\xaeB`\x82"


class ShipError(Exception):
    """Raised when the entry image fails validation."""


def load_entry():
    png = HERE / "entry.png"
    if not png.is_file():
        raise ShipError("entry.png is missing — run python3 render.py first")
    raw = png.read_bytes()
    if len(raw) > CAP:
        raise ShipError(f"entry.png is {len(raw)} bytes, over the 1 MiB cap")
    if not raw.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ShipError("entry.png has a bad PNG signature")
    if len(raw) < 33 or raw[12:16] != b"IHDR":
        raise ShipError("entry.png has no IHDR chunk")
    dims = struct.unpack(">II", raw[16:24])
    if dims != SIZE:
        raise ShipError(f"entry.png is {dims[0]}x{dims[1]}, expected 1024x1024")
    if raw[-12:] != IEND_TAIL:
        raise ShipError("entry.png has no IEND chunk")
    return raw


def main():
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    raw = load_entry()
    dest = Path(target_dir) / "entry.png"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(raw)
    print(f"wrote {dest} ({len(raw)} bytes)")


if __name__ == "__main__":
    try:
        main()
    except ShipError as err:
        print(f"error: {err}", file=sys.stderr)
        raise SystemExit(1)
