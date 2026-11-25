#!/usr/bin/env python3
"""Compose exact s5 solver and geometry-derived rows with conflict checks."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research/experiments/n11-frontier-selection-20261005/scripts"))
from derive_shared_s6_witness_cache import canonical_safe_key  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path: Path):
    result = {}
    for line_no, row in enumerate(csv.reader(path.open(newline="", encoding="utf-8-sig")), 1):
        if not row or row[0].lstrip().startswith("#"):
            continue
        if len(row) != 6 or row[0] != "s5verdict" or int(row[3]) != 5:
            raise SystemExit(f"invalid s5 row {path}:{line_no}: {row}")
        key, verdict, nodes = (int(row[1]), int(row[2])), int(row[4]), int(row[5])
        if verdict not in (1, 2) or nodes < 0 or canonical_safe_key(key, 5) != key:
            raise SystemExit(f"unsafe/non-exact s5 row {path}:{line_no}: {row}")
        if key in result and result[key][0] != verdict:
            raise SystemExit(f"internal cache conflict in {path}: {key}")
        result[key] = (verdict, max(nodes, result.get(key, (0, 0))[1]))
    return result


def counts(rows):
    return {"rows": len(rows), "WIN": sum(v == 1 for v, _ in rows.values()),
            "LOSS": sum(v == 2 for v, _ in rows.values())}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--loss-cache", type=Path, required=True)
    ap.add_argument("--derived-cache", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--manifest", type=Path, required=True)
    args = ap.parse_args()
    if args.out.exists() or args.manifest.exists():
        raise SystemExit("refusing to overwrite existing delta or manifest")
    loss, derived = read(args.loss_cache), read(args.derived_cache)
    merged = dict(loss)
    for key, value in derived.items():
        old = merged.get(key)
        if old is not None and old[0] != value[0]:
            raise SystemExit(f"conflict while composing exact s5 delta: {key}")
        merged[key] = value
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write("# s5 verdict cache: exact-only combined delta from s5 replay and complete s6 boundary\n")
        for (lo, hi), (verdict, nodes) in sorted(merged.items()):
            stream.write(f"s5verdict,{lo},{hi},5,{verdict},{nodes}\n")
    manifest = {
        "schema": "n11-reply27-s5-combined-exact-delta-v1",
        "conflicts": 0,
        "sources": [{"path": str(path), "sha256": sha256(path), **counts(rows)}
                    for path, rows in ((args.loss_cache, loss), (args.derived_cache, derived))],
        "output": {"path": str(args.out), "sha256": sha256(args.out), **counts(merged)},
        "claim": "Contains exact solver verdicts only; derived parent WIN is admitted only from the separately geometry-verified complete all-WIN s6 boundary.",
    }
    args.manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n",
                             encoding="utf-8", newline="\n")
    print(json.dumps({"sources": [counts(loss), counts(derived)],
                      "delta": counts(merged), "conflicts": 0}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
