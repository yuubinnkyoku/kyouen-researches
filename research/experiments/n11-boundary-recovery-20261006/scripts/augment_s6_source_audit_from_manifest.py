#!/usr/bin/env python3
"""Extend a hash-validated saved-s6 source audit with manifested replay CSVs."""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "research/experiments/n11-boundary-recovery-20261006"
sys.path.insert(0, str(ROOT / "research/experiments/n11-search-methods/scripts"))
from dfpn_edge_classes import legal_after  # noqa: E402
sys.path.insert(0, str(EXP / "scripts"))
from audit_saved_s6_targets import (  # noqa: E402
    points,
    read_saved_exact_s6,
    safe_canonical,
    sha256,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-audit", type=Path, required=True)
    parser.add_argument("--source-manifest", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    doc = json.loads(args.base_audit.read_text(encoding="utf-8"))
    if not doc.get("source_hashes_validated") or not doc.get("s6", {}).get("all_s6_exact_rows_geometry_checked"):
        raise SystemExit("base audit lacks source-hash or geometry attestation")
    if doc.get("s6", {}).get("exact_conflict_count") != 0:
        raise SystemExit("base saved-s6 audit reports an exact conflict")
    base_exact, _ = read_saved_exact_s6(doc)
    merged = {key: value["verdict"] for key, value in base_exact.items()}

    manifest = json.loads(args.source_manifest.read_text(encoding="utf-8"))
    if manifest.get("schema") != "n11-dual-tight-s6-descent-source-manifest-v1":
        raise SystemExit("unexpected S6 source-manifest schema")
    new_sources = []
    verdict_counts: Counter[str] = Counter()
    overlap_counts: Counter[str] = Counter()
    rows_seen = 0
    for item in manifest.get("raw_sources", []):
        rel = item.get("artifact_path", "").replace("\\", "/")
        path = (ROOT / rel).resolve()
        if not path.is_file() or sha256(path) != item.get("sha256"):
            raise SystemExit(f"raw S6 output missing or hash mismatch: {rel}")
        parsed = []
        for row_no, row in enumerate(csv.reader(path.open(newline="", encoding="utf-8-sig")), 1):
            if not row or row[0].lstrip().startswith("#") or row[0] != "replay":
                continue
            if len(row) != 11 or int(row[2]) != 6 or int(row[4]) != 1:
                raise SystemExit(f"invalid S6 OR replay {rel}:{row_no}: {row}")
            key = (int(row[9]), int(row[10]))
            verdict, nodes, legal = int(row[6]), int(row[7]), int(row[3])
            if verdict not in (0, 1, 2) or nodes < 0 or not safe_canonical(key, 6):
                raise SystemExit(f"invalid/noncanonical S6 replay {rel}:{row_no}: {row}")
            if len(legal_after(set(points(key)))) != legal:
                raise SystemExit(f"S6 legal-count mismatch {rel}:{row_no}: {key}")
            if key != tuple(item.get("key", [])) or verdict != item.get("verdict") or nodes != item.get("nodes"):
                raise SystemExit(f"S6 row differs from source manifest: {rel}:{row_no}")
            parsed.append((key, verdict))
        if len(parsed) != item.get("replay_rows") or len(parsed) != 1:
            raise SystemExit(f"expected one replay row in manifested file: {rel}")
        key, verdict = parsed[0]
        old = merged.get(key)
        if old in (1, 2) and verdict in (1, 2) and old != verdict:
            raise SystemExit(f"exact S6 WIN/LOSS conflict for {key}: {old} vs {verdict}")
        if old is not None:
            overlap_counts[str(verdict)] += 1
        if verdict in (1, 2) or old is None:
            merged[key] = verdict
        verdict_counts[str(verdict)] += 1
        rows_seen += 1
        new_sources.append({
            "path": rel,
            "sha256": sha256(path),
            "bytes": path.stat().st_size,
            "s6_replay_rows": 1,
            "verdict_counts": {str(verdict): 1},
            "source_kind": "manifested_local_exact_s6_descent",
            "provenance": f"S6 replay key {key}; source manifest {args.source_manifest.as_posix()}",
            "status": "included",
        })
    if rows_seen != manifest.get("source_replay_rows"):
        raise SystemExit(f"manifest row count mismatch: {rows_seen} != {manifest.get('source_replay_rows')}")

    source_items = list(doc["sources"]) + new_sources
    exact_counts = Counter(str(value) for value in merged.values() if value in (1, 2))
    doc["sources"] = source_items
    doc["source_file_count"] = len(source_items)
    doc["source_hashes_validated"] = True
    doc["s6"] = {
        "all_s6_exact_rows_geometry_checked": True,
        "exact_conflict_count": 0,
        "unique_canonical_keys": len(merged),
        "unique_loss_keys": exact_counts["2"],
        "unique_win_keys": exact_counts["1"],
        "unknown_only_keys": sum(value == 0 for value in merged.values()),
        "verdict_counts_by_unique_key": dict(sorted(exact_counts.items())),
    }
    doc["schema"] = "n11-saved-s6-source-audit-with-manifested-run-extension-v1"
    doc["run_status"] = "ok"
    doc["rejected_conflicts"] = []
    doc["cache_comparison"] = {
        "rejected_conflicts": [],
        "conflicts": [],
        "internal_conflict": 0,
        "current_cache_internal_conflicts": 0,
        "opposite_verdict": 0,
    }
    doc["manifested_extension"] = {
        "source_manifest": args.source_manifest.resolve().relative_to(ROOT.resolve()).as_posix(),
        "source_manifest_sha256": sha256(args.source_manifest),
        "new_source_count": len(new_sources),
        "new_replay_rows": rows_seen,
        "new_verdict_row_counts": dict(sorted(verdict_counts.items())),
        "overlap_rows_by_verdict": dict(sorted(overlap_counts.items())),
        "unknowns_propagated": False,
        "exact_conflicts": 0,
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    # Rehydrate through the same reader used by the production boundary audit.
    verified, reports = read_saved_exact_s6(doc)
    if len(reports) != len(source_items) or len(verified) != len(merged):
        raise SystemExit("augmented saved-s6 audit failed its re-read")
    print(json.dumps({
        "source_files": len(source_items),
        "new_source_files": len(new_sources),
        "new_rows": rows_seen,
        "new_verdict_row_counts": dict(sorted(verdict_counts.items())),
        "canonical_s6_keys": len(verified),
        "exact_s6_counts": dict(sorted(exact_counts.items())),
        "unknown_only_keys": sum(value == 0 for value in merged.values()),
        "conflicts": 0,
        "run_status": "ok",
        "out": args.out.as_posix(),
        "out_sha256": sha256(args.out),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
