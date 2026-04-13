#!/usr/bin/env python3
"""
Legacy compatibility hook for older cron tasks.

Current policy: do NOT rewrite lede commentary here.
The baseball pipeline already generates commentary in src/picks markdown.
This script intentionally performs no content mutation.
"""

from pathlib import Path

ROOT = Path('/Users/asmith/.openclaw/workspace/sportzballz.io')
FILES = [
    '2026-04-08.html',
    '2026-04-08-plus-money.html',
    '2026-04-08-run-line.html',
    '2026-04-08-run-totals.html',
]

for f in FILES:
    p = ROOT / f
    print(f"noop: {p.name} exists={p.exists()}")
