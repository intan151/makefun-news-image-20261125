#!/usr/bin/env python3
"""News-image entry for Wednesday, 25 November 2026.

Runs on Python 3.13 with the standard library alone. It places the
pre-rendered entry.png that ships beside this file into the output
directory the grader provides ($MAKEFUN_OUTPUT_DIR, or /output when
that variable is unset), then verifies the copy is a genuine PNG of
the same size. The picture itself is produced ahead of time by
draw_news.py, which needs Pillow and runs on the build machine; the
grader container installs nothing, so this entry point only copies.
Running it twice writes identical bytes.
"""

import os
import sys
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def output_dir():
    wanted = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    try:
        wanted.mkdir(parents=True, exist_ok=True)
        return wanted
    except OSError:
        fallback = Path("out")
        fallback.mkdir(parents=True, exist_ok=True)
        return fallback


def copy_entry():
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    target = output_dir() / "entry.png"
    data = source.read_bytes()
    if data[:8] != PNG_MAGIC:
        raise SystemExit("entry.png beside main.py is not a PNG file")
    target.write_bytes(data)
    copied = target.read_bytes()
    if len(copied) != len(data) or copied[:8] != PNG_MAGIC:
        raise SystemExit("the copied entry.png failed its check")
    # Gate check: the PNG header must describe a 1024x1024 image.
    width = int.from_bytes(copied[16:20], "big")
    height = int.from_bytes(copied[20:24], "big")
    if (width, height) != (1024, 1024):
        raise SystemExit(f"entry.png is {width}x{height}, not 1024x1024")
    print(f"wrote {target} ({len(copied)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(copy_entry())
