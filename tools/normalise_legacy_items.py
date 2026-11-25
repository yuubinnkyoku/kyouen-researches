"""Normalise legacy front matter (status: established, depends:, machine:, ...).

Some items were written with a non-standard header:

    status: established / established: DATE / evidence: complete-enumeration /
    verification: deterministic-machine / machine: PATH / depends: [K..., ...]

This script rewrites that header into the schema used by tools/knowledge:
kind/status/topics/aliases/relations/artifacts/scope/evidence.  The body and the
original wording are preserved; only the header is converted.

Usage: normalise_legacy_items.py [files...]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ITEMS = ROOT / "research" / "knowledge" / "items"
LEGACY = ("established", "machine", "depends", "verification")


def convert(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    parts = text.split("---")
    if len(parts) < 3:
        return False
    fm_lines = parts[1].splitlines()
    fields: dict[str, str] = {}
    for line in fm_lines:
        m = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if m:
            fields[m.group(1)] = m.group(2).strip()
    if not any(k in fields for k in LEGACY):
        return False
    kid = fields.get("id", path.name[:5])
    title = fields.get("title", "")
    machine = fields.get("machine", "").strip()
    depends = fields.get("depends", "")
    deps = re.findall(r"K\d{4}", depends)
    verification = fields.get("verification", "").strip()
    evidence = fields.get("evidence", "").strip()
    kind = "proposition"
    status = "computed"
    topics = "[rectangles, maximal-safe]"
    lines = ["", f"id: {kid}", f"title: {title}", f"kind: {kind}", f"status: {status}",
             f"topics: {topics}", "aliases: []", "relations:"]
    for d in deps:
        lines += ["- type: depends_on", f"  target: {d}"]
    if machine:
        lines += ["artifacts:", f"- path: {machine}", "  role: solver",
                  "  note: 完全列挙ランナー（旧front matterから移行）"]
    if evidence:
        lines.append(f"scope: '旧front matterの evidence を移行: {evidence}'")
    lines.append(f"evidence: {evidence}（verification: {verification or 'n/a'}）。"
                 "本文の完全列挙・監査記述を参照。")
    new_fm = "\n".join(lines) + "\n"
    path.write_text("---" + new_fm + "---" + "---".join(parts[2:]), encoding="utf-8", newline="\n")
    return True


def main() -> int:
    names = sys.argv[1:]
    files = [ITEMS / n for n in names] if names else sorted(ITEMS.glob("K*.md"))
    done = [f.name for f in files if f.exists() and convert(f)]
    print("converted:", done)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
