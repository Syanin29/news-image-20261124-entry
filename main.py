#!/usr/bin/env python3
"""Copy the validated news-image entry to the make.fun output directory.

Standard library only. No network access, no permission changes on any
directory. The entry image is read from the same directory as this script,
validated as a genuine 1024x1024 PNG under 1 MiB, then copied byte-for-byte
to $MAKEFUN_OUTPUT_DIR/entry.png.
"""

import os
import struct
import sys

MAX_BYTES = 1048576
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print("error: " + message, file=sys.stderr)
    return 1


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")

    try:
        with open(source, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        return fail("cannot read entry.png: " + str(exc))

    if len(data) > MAX_BYTES:
        return fail(
            "entry.png is %d bytes, over the 1 MiB limit" % len(data)
        )
    if len(data) < 8 or data[:8] != PNG_MAGIC:
        return fail("entry.png is not a PNG file (bad magic bytes)")

    # IHDR chunk: 4-byte length, 4-byte type, then width and height.
    if len(data) < 33 or data[12:16] != b"IHDR":
        return fail("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if width != EXPECTED_WIDTH or height != EXPECTED_HEIGHT:
        return fail(
            "entry.png is %dx%d, expected 1024x1024" % (width, height)
        )

    # The IEND chunk is the last 12 bytes: zero length, "IEND", CRC.
    if len(data) < 12 or data[-8:-4] != b"IEND":
        return fail("entry.png is missing its IEND chunk")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        out_dir = os.path.join(here, "output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    with open(dest, "wb") as handle:
        handle.write(data)

    print("wrote %s (%d bytes)" % (dest, len(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
