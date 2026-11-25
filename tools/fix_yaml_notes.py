"""Repair unquoted colons inside multi-line YAML values in knowledge items.

Some items have front-matter values like

    note: 2026-11-12監査: blocker 総数は...
      2系統幾何で確認）。...

A plain scalar cannot contain ": " in YAML, so the value must be a single quoted
line.  This script joins a key's continuation lines, and quotes the value when it
contains ": ".  Existing quoted or block values are left untouched.

Usage: fix_yaml_notes.py [--check-only] [files...]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ITEMS = ROOT / "research" / "knowledge" / "items"
KEY = re.compile(r"^(\s+)([A-Za-z_]+):\s(.*)$")


def repair(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    parts = text.split("---")
    if len(parts) < 3:
        return False
    fm = parts[1]
    lines = fm.splitlines()
    out: list[str] = []
    changed = False
    i = 0
    while i < len(lines):
        line = lines[i]
        m = KEY.match(line)
        if not m:
            out.append(line)
            i += 1
            continue
        indent, key, value = m.group(1), m.group(2), m.group(3)
        # gather continuation lines (more indented than the key, not a new key)
        j = i + 1
        cont = []
        while j < len(lines):
            nxt = lines[j]
            if nxt.strip() == "":
                break
            nm = KEY.match(nxt)
            if nm and len(nm.group(1)) <= len(indent):
                break
            if nxt.lstrip().startswith("- ") and len(nxt) - len(nxt.lstrip()) <= len(indent):
                break
            cont.append(nxt.strip())
            j += 1
        if ": " in (value + " " + " ".join(cont)) and not value.startswith(("'", '"', ">", "|")):
            joined = " ".join([value] + cont)
            out.append(f"{indent}{key}: '{joined.replace(chr(39), chr(39) * 2)}'")
            changed = True
            i = j
            continue
        out.append(line)
        i += 1
    if changed:
        new = "---".join([parts[0], "\n".join(out) + "\n", "---".join(parts[2:])])
        path.write_text(new, encoding="utf-8", newline="\n")
    return changed


def main() -> int:
    names = [a for a in sys.argv[1:] if not a.startswith("--")]
    files = [ITEMS / n for n in names] if names else sorted(ITEMS.glob("K*.md"))
    fixed = []
    for f in files:
        if f.exists() and repair(f):
            fixed.append(f.name)
    print("repaired:", fixed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
