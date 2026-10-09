#!/usr/bin/env python3
"""Merge one collected exact S5 delta into a frozen exact cache with a receipt."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def cache_rows(path: Path) -> dict[tuple[int, int], tuple[int, int]]:
    rows: dict[tuple[int, int], tuple[int, int]] = {}
    with path.open(newline="", encoding="utf-8-sig") as handle:
        for line_number, row in enumerate(csv.reader(handle), 1):
            if not row or row[0].startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict":
                raise SystemExit(f"invalid cache row {path}:{line_number}: {row!r}")
            key = (int(row[1]), int(row[2]))
            if int(row[3]) != 5 or int(row[4]) not in (1, 2):
                raise SystemExit(f"non-exact S5 cache row {path}:{line_number}: {row!r}")
            verdict, nodes = int(row[4]), int(row[5])
            old = rows.get(key)
            if old is not None and old[0] != verdict:
                raise SystemExit(f"conflict inside {path}: {key}: {old[0]} vs {verdict}")
            if old is not None:
                raise SystemExit(f"duplicate key inside {path}: {key}")
            rows[key] = (verdict, nodes)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True, type=Path)
    parser.add_argument("--delta", required=True, type=Path)
    parser.add_argument("--raw", required=True, type=Path)
    parser.add_argument("--out-cache", required=True, type=Path)
    parser.add_argument("--out-receipt", required=True, type=Path)
    args = parser.parse_args()

    base = cache_rows(args.base)
    delta = cache_rows(args.delta)
    raw: dict[tuple[int, int], tuple[int, int]] = {}
    with args.raw.open(newline="", encoding="utf-8-sig") as handle:
        for line_number, row in enumerate(csv.reader(handle), 1):
            if not row or row[0].startswith("#"):
                continue
            if len(row) != 11 or row[0] != "replay":
                raise SystemExit(f"invalid exact raw row {args.raw}:{line_number}: {row!r}")
            if int(row[5]) != 15_000_000 or int(row[6]) not in (1, 2):
                raise SystemExit(f"raw row is not exact at requested budget: {row!r}")
            key = (int(row[9]), int(row[10]))
            value = (int(row[6]), int(row[7]))
            if key in raw:
                raise SystemExit(f"duplicate raw exact key: {key}")
            raw[key] = value

    if set(raw) != set(delta):
        raise SystemExit(
            f"raw/delta key mismatch: raw-only={sorted(set(raw)-set(delta))}, "
            f"delta-only={sorted(set(delta)-set(raw))}"
        )
    for key, (verdict, nodes) in raw.items():
        if delta[key] != (verdict, nodes):
            raise SystemExit(f"raw/delta row mismatch for {key}: {raw[key]} vs {delta[key]}")

    overlap = set(base) & set(delta)
    conflict = [key for key in sorted(overlap) if base[key][0] != delta[key][0]]
    if conflict:
        raise SystemExit(f"verdict conflict with base cache: {conflict}")
    if overlap:
        raise SystemExit(f"delta unexpectedly repeats base exact keys: {sorted(overlap)}")

    merged = dict(base)
    merged.update(delta)
    args.out_cache.parent.mkdir(parents=True, exist_ok=True)
    with args.out_cache.open("w", newline="", encoding="utf-8") as handle:
        handle.write("# s5 verdict cache: n=11 schema=1 (exact base plus collected probe8 rows)\n")
        writer = csv.writer(handle, lineterminator="\n")
        for (lo, hi), (verdict, nodes) in sorted(merged.items()):
            writer.writerow(("s5verdict", lo, hi, 5, verdict, nodes))

    def counts(rows: dict[tuple[int, int], tuple[int, int]]) -> dict[str, int]:
        tally = Counter(value[0] for value in rows.values())
        return {"rows": len(rows), "WIN": tally[1], "LOSS": tally[2], "conflict": 0}

    receipt = {
        "schema": "n11-exact-s5-cache-merge-receipt-v1",
        "base": {"path": str(args.base), "sha256": sha256(args.base), **counts(base)},
        "delta": {
            "path": str(args.delta),
            "sha256": sha256(args.delta),
            **counts(delta),
            "raw_path": str(args.raw),
            "raw_sha256": sha256(args.raw),
        },
        "merged": {"path": str(args.out_cache), "sha256": sha256(args.out_cache), **counts(merged)},
        "overlap_keys": 0,
        "verdict_conflicts": 0,
        "unknown_rows_merged": 0,
        "not_dispatched_keys": [
            [1152921642181066752, 68719476736],
            [5908863448599494656, 0],
            [10378545341275312128, 65536],
        ],
    }
    args.out_receipt.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
