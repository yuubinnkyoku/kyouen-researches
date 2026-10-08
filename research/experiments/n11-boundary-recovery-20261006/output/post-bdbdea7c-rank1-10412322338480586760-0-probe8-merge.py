#!/usr/bin/env python3
"""Audited exact-only merge for one reply27 s5 cache checkpoint."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research/experiments/n11-frontier-selection-20261005/scripts"))
from derive_shared_s6_witness_cache import canonical_safe_key  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_cache(path: Path) -> dict[tuple[int, int], tuple[int, int]]:
    rows: dict[tuple[int, int], tuple[int, int]] = {}
    with path.open(newline="", encoding="utf-8-sig") as stream:
        for line_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict":
                raise SystemExit(f"invalid cache row {path}:{line_no}: {row}")
            key = (int(row[1]), int(row[2]))
            stones, verdict, nodes = int(row[3]), int(row[4]), int(row[5])
            if (stones != 5 or verdict not in (1, 2) or nodes < 0
                    or canonical_safe_key(key, 5) != key):
                raise SystemExit(f"non-exact s5 row {path}:{line_no}: {row}")
            old = rows.get(key)
            if old is not None and old[0] != verdict:
                raise SystemExit(f"internal verdict conflict in {path} for {key}: {old[0]} vs {verdict}")
            rows[key] = (verdict, max(nodes, old[1] if old else 0))
    return rows


def counts(rows: dict[tuple[int, int], tuple[int, int]]) -> dict[str, int]:
    return {"rows": len(rows), "WIN": sum(v == 1 for v, _ in rows.values()),
            "LOSS": sum(v == 2 for v, _ in rows.values())}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--delta", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists() or args.receipt.exists():
        raise SystemExit("refusing to overwrite existing output or receipt")
    base, delta = read_cache(args.base), read_cache(args.delta)
    merged = dict(base)
    conflicts = []
    for key, row in delta.items():
        old = merged.get(key)
        if old is not None and old[0] != row[0]:
            conflicts.append({"key": list(key), "base": old[0], "delta": row[0]})
        elif old is None:
            merged[key] = row
    if conflicts:
        raise SystemExit(f"merge refused: {len(conflicts)} verdict conflicts; first={conflicts[:3]}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    temp = args.out.with_suffix(args.out.suffix + ".tmp")
    with temp.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write("# s5 verdict cache: n=11 schema=1 (canonical key -> WIN/LOSS, UNKNOWN never stored)\n")
        for (lo, hi), (verdict, nodes) in sorted(merged.items()):
            stream.write(f"s5verdict,{lo},{hi},5,{verdict},{nodes}\n")
    os.replace(temp, args.out)
    script = Path(__file__).resolve()
    receipt = {
        "schema": "n11-reply27-s5-cache-merge-receipt-v1",
        "conflicts": len(conflicts),
        "unknown_rows_merged": 0,
        "sources": [
            {"path": str(args.base), "sha256": sha256(args.base), **counts(base)},
            {"path": str(args.delta), "sha256": sha256(args.delta), **counts(delta)},
        ],
        "implementation": {"path": str(script), "sha256": sha256(script)},
        "output": {"path": str(args.out), "sha256": sha256(args.out), **counts(merged)},
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n",
                            encoding="utf-8", newline="\n")
    print(json.dumps({"conflicts": 0, "base": counts(base), "delta": counts(delta),
                      "merged": counts(merged), "output_sha256": sha256(args.out)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
