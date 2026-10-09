#!/usr/bin/env python3
"""Isolate one fully exact-WIN S5 parent from an audited multi-parent S6 run.

This writes a provenance-linked projection of the original batch summary. It
does not invoke the solver or alter any original runner/raw evidence.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "research/experiments/n11-boundary-recovery-20261006"
sys.path.insert(0, str(EXP / "scripts"))
from audit_local_s6_boundary_history import make_boundary  # noqa: E402
from audit_saved_s6_targets import read_saved_exact_s6, safe_canonical  # noqa: E402


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def rows(path: Path) -> list[list[str]]:
    with path.open(newline="", encoding="utf-8-sig") as stream:
        return [row for row in csv.reader(stream)
                if row and not row[0].lstrip().startswith("#")]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--batch-summary", type=Path, required=True)
    ap.add_argument("--parents", type=Path, required=True)
    ap.add_argument("--saved-audit", type=Path, required=True)
    ap.add_argument("--output-parent", type=Path, required=True)
    ap.add_argument("--output-run-dir", type=Path, required=True)
    ap.add_argument("--output-manifest", type=Path, required=True)
    ap.add_argument("--parent-lo", type=int, required=True)
    ap.add_argument("--parent-hi", type=int, required=True)
    args = ap.parse_args()

    destinations = (args.output_parent, args.output_run_dir, args.output_manifest)
    if any(path.exists() for path in destinations):
        raise SystemExit("refusing to overwrite projection evidence")
    batch = json.loads(args.batch_summary.read_text(encoding="utf-8"))
    if batch.get("schema") != "n11-complete-s5-via-s6-local-v1":
        raise SystemExit("unexpected source batch summary schema")
    if batch.get("parents_sha256") != digest(args.parents):
        raise SystemExit("source batch summary does not bind the original parent list")
    if batch.get("saved_audit_sha256") != digest(args.saved_audit):
        raise SystemExit("source batch summary does not bind the saved S6 audit")

    parent = (args.parent_lo, args.parent_hi)
    if not safe_canonical(parent, 5):
        raise SystemExit(f"unsafe/noncanonical S5 parent: {parent}")
    source_rows = [row for row in rows(args.parents)
                   if len(row) == 11 and int(row[2]) == 5
                   and (int(row[3]), int(row[4])) == parent]
    if len(source_rows) != 1 or int(source_rows[0][7]) != 0:
        raise SystemExit("target S5 parent is absent, duplicated, or not an UNKNOWN AND parent")

    parent_records = [item for item in batch.get("parents", [])
                      if tuple(item.get("key", [])) == parent]
    if (len(parent_records) != 1 or parent_records[0].get("outcome") != "WIN"
            or parent_records[0].get("counts") != {"0": 0, "1": parent_records[0].get("child_count"), "2": 0}
            or parent_records[0].get("unresolved_children") != []):
        raise SystemExit("source batch does not report a complete exact-WIN S5 boundary")

    boundary = make_boundary(parent)
    if (len(boundary) != parent_records[0].get("child_count")
            or not boundary):
        raise SystemExit("source batch S5 child count differs from regenerated geometry")
    saved_doc = json.loads(args.saved_audit.read_text(encoding="utf-8"))
    saved, _ = read_saved_exact_s6(saved_doc)
    if boundary & set(saved):
        raise SystemExit("winning S5 boundary intersects saved S6 rows; direct-only projection is invalid")

    batch_sources = {tuple(item.get("key", [])): item
                     for item in batch.get("new_solver_sources", [])}
    if len(batch_sources) != len(batch.get("new_solver_sources", [])):
        raise SystemExit("duplicate S6 source keys in source batch summary")
    selected = []
    for key in sorted(boundary):
        item = batch_sources.get(key)
        if item is None or item.get("verdict") != 1:
            raise SystemExit(f"missing/non-WIN direct solver source for S6 child {key}")
        raw = Path(item.get("path", ""))
        if not raw.is_file() or digest(raw) != item.get("sha256"):
            raise SystemExit(f"source S6 output missing/hash mismatch: {raw}")
        replay = rows(raw)
        if (len(replay) != 1 or replay[0][0] != "replay" or int(replay[0][2]) != 6
                or int(replay[0][4]) != 1 or int(replay[0][6]) != 1
                or (int(replay[0][9]), int(replay[0][10])) != key
                or int(replay[0][7]) != item.get("nodes")):
            raise SystemExit(f"raw S6 replay is not an exact WIN matching its source row: {key}")
        selected.append(item)

    args.output_parent.parent.mkdir(parents=True, exist_ok=True)
    args.output_parent.write_text(
        "# Exact UNKNOWN S5 parent isolated from the original 11-parent dispatch input.\n"
        + ",".join(source_rows[0]) + "\n", encoding="utf-8", newline="\n")
    args.output_run_dir.mkdir(parents=True, exist_ok=False)
    projection = {
        "schema": batch["schema"],
        "projection_kind": "single-parent-view-of-multi-parent-run",
        "projection_source": {
            "path": str(args.batch_summary.resolve()),
            "sha256": digest(args.batch_summary),
            "original_parent_list_path": str(args.parents.resolve()),
            "original_parent_list_sha256": digest(args.parents),
        },
        "parents_sha256": digest(args.output_parent),
        "saved_audit_sha256": digest(args.saved_audit),
        "budget": batch.get("budget"),
        "workers": batch.get("workers"),
        "parents": parent_records,
        "parent_count": 1,
        "unresolved_boundary_count": 0,
        "saved_unknown_boundary_count": 0,
        "reused_solver_sources": [],
        "new_solver_sources": selected,
        "new_solver_rows": len(selected),
        "new_solver_exact": len(selected),
        "new_solver_unknown": 0,
        "nodes_new": sum(item["nodes"] for item in selected),
        "derived_from_original_batch": True,
        "unknowns_propagated": False,
    }
    runner_path = args.output_run_dir / "summary.json"
    runner_path.write_text(json.dumps(projection, indent=2, sort_keys=True) + "\n",
                           encoding="utf-8", newline="\n")
    manifest = {
        "schema": "n11-reply27-s6-win-parent-projection-v1",
        "claim": "This is a one-parent projection of an existing audited batch; no solver was rerun.",
        "parent_s5": list(parent),
        "complete_canonical_s6_boundary": len(boundary),
        "s6_verdict_counts": {"WIN": len(selected), "LOSS": 0, "UNKNOWN": 0},
        "nodes": projection["nodes_new"],
        "budget": projection["budget"],
        "original_batch_summary": {"path": str(args.batch_summary.resolve()),
                                    "sha256": digest(args.batch_summary)},
        "original_parent_list": {"path": str(args.parents.resolve()),
                                  "sha256": digest(args.parents)},
        "saved_s6_source_audit": {"path": str(args.saved_audit.resolve()),
                                  "sha256": digest(args.saved_audit)},
        "projected_parent_input": {"path": str(args.output_parent.resolve()),
                                   "sha256": digest(args.output_parent)},
        "projected_runner_summary": {"path": str(runner_path.resolve()),
                                     "sha256": digest(runner_path)},
        "source_rows": [{"key": item["key"], "path": item["path"],
                         "sha256": item["sha256"], "verdict": item["verdict"],
                         "nodes": item["nodes"]} for item in selected],
        "exact_conflicts": 0,
        "unknowns_propagated": False,
    }
    args.output_manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n",
                                    encoding="utf-8", newline="\n")
    print(json.dumps({"parent_s5": list(parent), "boundary_s6": len(boundary),
                      "exact_s6_win": len(selected), "nodes": projection["nodes_new"],
                      "projection_manifest": str(args.output_manifest.resolve()),
                      "projection_manifest_sha256": digest(args.output_manifest)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
