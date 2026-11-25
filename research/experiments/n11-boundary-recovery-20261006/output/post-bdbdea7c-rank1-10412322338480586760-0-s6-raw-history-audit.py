#!/usr/bin/env python3
"""Audit saved and local s6 replay history against one complete s5 boundary."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research/experiments/n11-search-methods/scripts"))
sys.path.insert(0, str(ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts"))
from dfpn_edge_classes import d4_canonical_key, has_forbidden_quad, legal_after  # noqa: E402
from audit_saved_s6_targets import points, read_saved_exact_s6, safe_canonical  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def load_boundary(path: Path, meta_path: Path):
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    children = {tuple(item["key"]): item for item in meta["canonical_children"]}
    rows = []
    with path.open(newline="", encoding="utf-8-sig") as stream:
        for line_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 11 or int(row[2]) != 6 or int(row[7]) != 1:
                raise SystemExit(f"invalid canonical s6 target {path}:{line_no}: {row}")
            key = (int(row[3]), int(row[4]))
            if not safe_canonical(key, 6) or key in {r[0] for r in rows}:
                raise SystemExit(f"unsafe, noncanonical, or duplicate s6 key {key}")
            if int(row[5]) != len(legal_after(set(points(key)))):
                raise SystemExit(f"legal-count mismatch for s6 key {key}")
            rows.append((key, int(row[5])))
    if set(children) != {key for key, _ in rows}:
        raise SystemExit("boundary CSV keys differ from complete geometry metadata")
    if len(rows) != meta.get("complete_boundary_count"):
        raise SystemExit("boundary CSV cardinality differs from complete geometry metadata")
    return rows, meta


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--boundary", type=Path, required=True)
    parser.add_argument("--boundary-meta", type=Path, required=True)
    parser.add_argument("--saved-audit", type=Path, required=True)
    parser.add_argument("--raw-root", type=Path, action="append", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise SystemExit(f"refusing to overwrite existing audit: {args.out}")
    boundary_rows, boundary_meta = load_boundary(args.boundary, args.boundary_meta)
    boundary = {key for key, _ in boundary_rows}
    saved_audit = json.loads(args.saved_audit.read_text(encoding="utf-8"))
    saved, saved_sources = read_saved_exact_s6(saved_audit)
    observations: dict[tuple[int, int], list[dict]] = {key: [] for key in boundary}
    for key in boundary & saved.keys():
        for item in saved[key]["observations"]:
            observations[key].append({"source": item["source"], "row": item["row"],
                                      "verdict": item["verdict"], "nodes": item["nodes"],
                                      "kind": "saved-source-audit"})

    file_manifest = []
    raw_match_files = set()
    files = sorted({path.resolve() for root in args.raw_root
                    for path in root.rglob("*.csv") if path.is_file()})
    for path in files:
        digest = sha256(path)
        file_manifest.append({"path": rel(path), "bytes": path.stat().st_size, "sha256": digest})
        found = False
        with path.open(newline="", encoding="utf-8-sig", errors="replace") as stream:
            for row_no, row in enumerate(csv.reader(stream), 1):
                if not row or row[0].lstrip().startswith("#") or row[0] != "replay":
                    continue
                if len(row) < 3 or not row[2].isdigit() or int(row[2]) != 6:
                    continue
                if len(row) != 11 or int(row[4]) != 1:
                    raise SystemExit(f"invalid s6 OR replay row {rel(path)}:{row_no}: {row}")
                raw_key = (int(row[9]), int(row[10]))
                raw_points = points(raw_key)
                if len(raw_points) != 6 or has_forbidden_quad(raw_points):
                    raise SystemExit(f"unsafe raw s6 replay {rel(path)}:{row_no}: {raw_key}")
                key = tuple(d4_canonical_key(raw_points))
                if not safe_canonical(key, 6):
                    raise SystemExit(f"canonicalized raw s6 is unsafe: {key}")
                if int(row[3]) != len(legal_after(set(raw_points))):
                    raise SystemExit(f"raw s6 legal-count mismatch {rel(path)}:{row_no}: {raw_key}")
                if key not in boundary:
                    continue
                verdict, nodes = int(row[6]), int(row[7])
                if verdict not in (0, 1, 2) or nodes < 0:
                    raise SystemExit(f"invalid s6 solver result {rel(path)}:{row_no}: {row}")
                observations[key].append({"source": rel(path), "source_sha256": digest,
                                          "row": row_no, "raw_key": list(raw_key),
                                          "verdict": verdict, "nodes": nodes,
                                          "kind": "raw-csv-scan"})
                found = True
        if found:
            raw_match_files.add(rel(path))

    children = []
    conflicts = []
    counts = {"exact_WIN": 0, "exact_LOSS": 0, "prior_UNKNOWN": 0, "unseen": 0}
    for key in sorted(boundary):
        rows = observations[key]
        exact = {row["verdict"] for row in rows if row["verdict"] in (1, 2)}
        if len(exact) > 1:
            conflicts.append({"key": list(key), "verdicts": sorted(exact), "observations": rows})
        verdict = next(iter(exact)) if exact else (0 if rows else None)
        label = {1: "WIN", 2: "LOSS", 0: "UNKNOWN", None: "UNSEEN"}[verdict]
        counts[{"WIN": "exact_WIN", "LOSS": "exact_LOSS", "UNKNOWN": "prior_UNKNOWN",
                "UNSEEN": "unseen"}[label]] += 1
        children.append({"key": list(key), "verdict": label, "observations": rows})
    if conflicts:
        raise SystemExit(f"exact verdict conflict in s6 history: {conflicts[:3]}")
    parent_outcome = ("LOSS" if counts["exact_LOSS"] else
                      "WIN" if counts["exact_WIN"] == len(boundary) else "UNKNOWN")
    source_manifest = {
        "saved_audit": {"path": rel(args.saved_audit), "sha256": sha256(args.saved_audit),
                        "source_file_count": len(saved_sources)},
        "boundary": {"path": rel(args.boundary), "sha256": sha256(args.boundary),
                     "meta_path": rel(args.boundary_meta), "meta_sha256": sha256(args.boundary_meta),
                     "parent_keys": boundary_meta["parent_keys"],
                     "canonical_children": len(boundary)},
        "raw_roots": [rel(root) for root in args.raw_root],
        "raw_csv_files": file_manifest,
    }
    result = {
        "schema": "n11-reply27-s6-boundary-history-audit-v1",
        "claim": "Exact s6 verdicts are reused; prior UNKNOWN rows are held out; absent children alone are eligible for exact dispatch.",
        "parent_key": boundary_meta["parent_keys"][0] if len(boundary_meta["parent_keys"]) == 1 else None,
        "complete_canonical_s6_children": len(boundary),
        "counts": counts,
        "parent_outcome_from_s6": parent_outcome,
        "prior_unknown_keys": [child["key"] for child in children if child["verdict"] == "UNKNOWN"],
        "dispatch_ready_keys": [child["key"] for child in children if child["verdict"] == "UNSEEN"],
        "conflicts": 0,
        "raw_csv_files_scanned": len(file_manifest),
        "raw_csv_files_with_boundary_rows": sorted(raw_match_files),
        "children": children,
        "source_manifest": source_manifest,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8", newline="\n")
    print(json.dumps({"children": len(boundary), "counts": counts,
                      "parent_outcome": parent_outcome,
                      "raw_csv_files_scanned": len(file_manifest),
                      "raw_match_files": len(raw_match_files), "conflicts": 0}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
