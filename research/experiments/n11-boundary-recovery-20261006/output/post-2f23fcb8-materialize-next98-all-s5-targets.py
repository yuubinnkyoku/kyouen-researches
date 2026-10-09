#!/usr/bin/env python3
"""Materialize all canonical S5 children from an audited S4 boundary JSON."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research/experiments/n11-search-methods/scripts"))
from dfpn_edge_classes import d4_canonical_key, legal_after  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--boundary-audit", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    audit = json.loads(args.boundary_audit.read_text(encoding="utf-8"))
    children = audit["boundary"]["children"]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as fp:
        fp.write("# all canonical s5 children from the exact geometry boundary audit\n")
        writer = csv.writer(fp, lineterminator="\n")
        seen: set[tuple[int, int]] = set()
        for seq, child in enumerate(sorted(children, key=lambda row: tuple(row["key"])), 1):
            key = tuple(map(int, child["key"]))
            if len(key) != 2 or key in seen:
                raise SystemExit(f"duplicate or malformed canonical child: {key}")
            seen.add(key)
            lo, hi = key
            points = {p for p in range(64) if (lo >> p) & 1}
            points.update(64 + p for p in range(57) if (hi >> p) & 1)
            if len(points) != 5 or tuple(d4_canonical_key(points)) != key:
                raise SystemExit(f"unsafe or noncanonical S5 key: {key}")
            legal = len(legal_after(points))
            writer.writerow(("reply27-dual-tight", seq, 5, lo, hi, legal, 0, 0, 0, 0, 0))

    if len(seen) != int(audit["boundary"]["canonical_children"]):
        raise SystemExit("boundary cardinality differs from materialized targets")
    print(json.dumps({"targets": len(seen), "path": str(args.out)}, indent=2))


if __name__ == "__main__":
    main()
