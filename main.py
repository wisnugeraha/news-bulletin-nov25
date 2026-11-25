#!/usr/bin/env python3
"""Sum up 25 November's world news in one image — make.fun entry.

The bulletin page is drawn once, by hand, from that day's reporting and lives
in the repository as entry.png; this program delivers it to the grader's
output directory byte for byte, so both runs write identical bytes.
"""
import shutil
from pathlib import Path
import struct

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
TARGET = Path("/output/entry.png")
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576
MAX_SIDE = 1024


def read_header(path: Path) -> tuple[int, int]:
    with open(path, "rb") as fh:
        head = fh.read(24)
    if head[:8] != PNG_MAGIC:
        raise SystemExit("entry.png is not a whole PNG")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def audit() -> None:
    size = SOURCE.stat().st_size
    if size > MAX_BYTES:
        raise SystemExit(f"image is {size} bytes, gate allows {MAX_BYTES}")
    width, height = read_header(SOURCE)
    if width > MAX_SIDE or height > MAX_SIDE:
        raise SystemExit(f"image {width}x{height} exceeds the {MAX_SIDE}px box")


def main() -> None:
    audit()
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, TARGET)
    delivered = TARGET.stat().st_size
    print(f"bulletin delivered: {delivered} bytes, {read_header(TARGET)[0]}x{read_header(TARGET)[1]}")


if __name__ == "__main__":
    main()
