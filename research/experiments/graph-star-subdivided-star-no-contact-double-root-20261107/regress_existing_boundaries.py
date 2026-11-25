"""Regression: recompute the published odd-k boundaries for q = 6..200 from scratch.

Each ``graph-star-subdivided-star-q*-odd-transitions*`` note records, per q, the
largest odd k with no real root and the smallest odd k with exactly two simple
negative roots.  Here both numbers are recomputed with the exact integer
certificates of ``verify_no_contact_double_root.py`` and compared row by row.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from verify_no_contact_double_root import no_root_ok, roots_certified, threshold

HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)

ROW = re.compile(r"^\|\s*(\d+)\s*\|")


def published_rows() -> dict[int, dict]:
    rows: dict[int, dict] = {}
    for folder in sorted(EXPERIMENTS.iterdir()):
        if not folder.is_dir() or "subdivided-star-q" not in folder.name:
            continue
        if "odd-transition" not in folder.name:
            continue
        proof = folder / "proof.md"
        if not proof.exists():
            continue
        for line in proof.read_text(encoding="utf-8").splitlines():
            m = ROW.match(line.strip())
            if not m:
                continue
            q = int(m.group(1))
            numbers = [int(x) for x in re.findall(r"\d+", line.strip()[m.end():])]
            if not numbers:
                continue
            rows[q] = {
                "q": q,
                "source": folder.name,
                "k_plus_published": max(numbers),
                "row": line.strip(),
            }
    return rows


def main() -> int:
    rows = published_rows()
    mismatches = []
    checked = 0
    for q, rec in sorted(rows.items()):
        r = q - 3
        mine = threshold(r)
        checked += 1
        rec["k_plus_recomputed"] = mine["threshold"]
        rec["status"] = mine["status"]
        if mine["threshold"] != rec["k_plus_published"]:
            mismatches.append(rec)
        # the published k_minus must be certified rootless here as well
        rec["k_minus_certified"] = no_root_ok(r, rec["k_plus_published"] - 2)
        rec["k_plus_certified"] = roots_certified(r, rec["k_plus_published"])
    result = {
        "rows": checked,
        "q_range": [min(rows), max(rows)] if rows else None,
        "mismatches": mismatches,
        "all_k_plus_certified": all(rec["k_plus_certified"] for rec in rows.values()),
        "all_k_minus_certified": all(rec["k_minus_certified"] for rec in rows.values()),
        "table": rows,
    }
    OUT.joinpath("regression_existing_boundaries.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps({k: v for k, v in result.items() if k != "table"}, indent=2, ensure_ascii=False))
    if mismatches:
        print("MISMATCHES:")
        for rec in mismatches:
            print(rec)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
