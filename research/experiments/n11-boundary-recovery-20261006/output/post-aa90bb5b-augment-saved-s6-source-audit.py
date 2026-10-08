#!/usr/bin/env python3
"""Add the newly archived exact s6 descent to a validated saved-s6 audit."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SCRIPT_DIR = ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts"
sys.path.insert(0, str(SCRIPT_DIR))
from audit_saved_s6_targets import (  # noqa: E402
    points,
    read_saved_exact_s6,
    safe_canonical,
    sha256,
)
from dfpn_edge_classes import has_forbidden_quad, legal_after  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-audit", type=Path, required=True)
    parser.add_argument("--new-raw", type=Path, required=True)
    parser.add_argument("--new-source-manifest", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    doc = json.loads(args.base_audit.read_text(encoding="utf-8"))
    old, _ = read_saved_exact_s6(doc)
    new: dict[tuple[int, int], dict] = {}
    row_count = 0
    node_total = 0
    counts: Counter[str] = Counter()
    with args.new_raw.open(newline="", encoding="utf-8-sig") as stream:
        for line_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 11 or row[0] != "replay" or int(row[2]) != 6 or int(row[4]) != 1:
                raise SystemExit(f"invalid s6 AND replay {args.new_raw}:{line_no}: {row}")
            key = (int(row[9]), int(row[10]))
            if not safe_canonical(key, 6):
                raise SystemExit(f"unsafe/noncanonical s6 key: {key}")
            verdict, nodes, legal = int(row[6]), int(row[7]), int(row[3])
            if verdict not in (1, 2) or nodes < 0 or key in new:
                raise SystemExit(f"non-exact/duplicate new s6 result: {key} {row}")
            actual_legal = len(legal_after(set(points(key))))
            if legal != actual_legal:
                raise SystemExit(f"s6 legal-count mismatch: {key} {legal} != {actual_legal}")
            new[key] = {"verdict": verdict, "nodes": nodes, "legal": legal}
            row_count += 1
            node_total += nodes
            counts[str(verdict)] += 1
    if not row_count:
        raise SystemExit("new s6 raw evidence is empty")

    manifest = json.loads(args.new_source_manifest.read_text(encoding="utf-8"))
    if manifest.get("schema") != "n11-s6-descent-source-manifest-v1":
        raise SystemExit("unexpected new s6 source-manifest schema")
    if manifest.get("outputs", []) == []:
        raise SystemExit("new s6 source manifest does not attest outputs")
    attested = {item["path"]: item["sha256"] for item in manifest["outputs"]}
    raw_rel = args.new_raw.resolve().relative_to(ROOT.resolve()).as_posix()
    if attested.get(raw_rel) != sha256(args.new_raw):
        raise SystemExit("new s6 raw hash is not attested by its source manifest")
    if manifest.get("parent_outcome") != "WIN" or manifest.get("s6_children") is None:
        raise SystemExit("new s6 manifest does not attest the exact descent")
    if len(manifest["s6_children"]) != row_count:
        raise SystemExit("new source manifest row count differs from archived s6 replay")

    combined: dict[tuple[int, int], int] = {
        key: row["verdict"] for key, row in old.items()
    }
    for key, row in new.items():
        value = row["verdict"]
        previous = combined.get(key)
        if previous in (1, 2) and previous != value:
            raise SystemExit(f"exact s6 conflict for {key}: {previous} vs {value}")
        if previous is None or previous == 0:
            combined[key] = value

    sources = doc["sources"]
    for item in sources:
        if item.get("path", "").replace("\\", "/") == raw_rel:
            raise SystemExit("new s6 raw file is already present in base source audit")
    sources.append({
        "path": raw_rel,
        "sha256": sha256(args.new_raw),
        "bytes": args.new_raw.stat().st_size,
        "s6_replay_rows": row_count,
        "node_total": node_total,
        "normalized_noncanonical_rows": 0,
        "verdict_counts": dict(sorted(counts.items())),
        "source_kind": "exact_s6_descent_raw_all",
        "provenance": f"s5={manifest['parent_s5']} complete canonical s6 boundary; see {args.new_source_manifest.as_posix()}",
        "status": "included",
    })
    unique_counts = Counter(str(value) for value in combined.values() if value in (1, 2))
    unknown_only = sum(value == 0 for value in combined.values())
    doc["source_file_count"] = len(sources)
    doc["source_hashes_validated"] = True
    doc["s6"] = {
        "all_s6_exact_rows_geometry_checked": True,
        "exact_conflict_count": 0,
        "unique_canonical_keys": len(combined),
        "unique_loss_keys": unique_counts["2"],
        "unique_win_keys": unique_counts["1"],
        "unknown_only_keys": unknown_only,
        "verdict_counts_by_unique_key": dict(sorted(unique_counts.items())),
    }
    doc["new_s6_extension"] = {
        "source_manifest": args.new_source_manifest.resolve().relative_to(ROOT.resolve()).as_posix(),
        "source_manifest_sha256": sha256(args.new_source_manifest),
        "new_raw_path": raw_rel,
        "new_raw_sha256": sha256(args.new_raw),
        "new_rows": row_count,
        "new_exact_verdict_counts": dict(sorted(counts.items())),
        "new_unique_keys": len(new),
        "exact_conflicts": 0,
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8", newline="\n")
    print(json.dumps({"source_files": len(sources), "unique_canonical_s6": len(combined),
                      "unique_win": unique_counts["1"], "unique_loss": unique_counts["2"],
                      "unknown_only": unknown_only, "new_s6_rows": row_count,
                      "new_verdicts": dict(sorted(counts.items())), "conflicts": 0,
                      "out": args.out.as_posix()}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
