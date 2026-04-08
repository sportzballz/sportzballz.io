#!/usr/bin/env python3
import re
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

TS_RE = re.compile(r"(Updated\s+)(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}\s+[AP]M)")


def current_et_stamp() -> str:
    return datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %I:%M %p")


def update_file(path: Path, stamp: str) -> bool:
    if not path.exists() or not path.is_file() or path.suffix.lower() != ".html":
        return False
    src = path.read_text(encoding="utf-8", errors="ignore")
    dst = TS_RE.sub(rf"\1{stamp}", src)
    if dst != src:
        path.write_text(dst, encoding="utf-8")
        return True
    return False


def main(argv):
    stamp = current_et_stamp()
    if len(argv) > 1:
        files = [Path(a) for a in argv[1:]]
    else:
        files = list(Path('.').glob('*.html'))

    changed = 0
    scanned = 0
    for f in files:
        scanned += 1
        if update_file(f, stamp):
            changed += 1
            print(f"updated timestamp: {f}")

    print(f"timestamp={stamp} scanned={scanned} changed={changed}")


if __name__ == "__main__":
    main(sys.argv)
