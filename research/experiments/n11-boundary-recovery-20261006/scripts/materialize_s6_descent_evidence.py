#!/usr/bin/env python3
"""Preserve and hash-bind the exact outputs of one completed local s6 descent."""
from __future__ import annotations

import argparse
import csv
import json
import shutil
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research/experiments/n11-search-methods/scripts"))
from dfpn_edge_classes import legal_after  # noqa: E402

EXP = ROOT / "research/experiments/n11-boundary-recovery-20261006"
sys.path.insert(0, str(EXP / "scripts"))
from audit_local_s6_boundary_history import (  # noqa: E402
    check_full_detail,
    make_boundary,
    read_parent,
    relpath,
)
from audit_saved_s6_targets import points, safe_canonical, sha256  # noqa: E402


def read_one_target(path: Path) -> tuple[tuple[int, int], int, list[str]]:
    found = []
    with path.open(newline="", encoding="utf-8-sig") as stream:
        for line_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 11 or row[0] != "target" or int(row[2]) != 6 or int(row[7]) != 1:
                raise ValueError(f"invalid s6 solver input {path}:{line_no}: {row}")
            key = (int(row[3]), int(row[4]))
            legal = len(legal_after(set(points(key))))
            if not safe_canonical(key, 6) or int(row[5]) != legal:
                raise ValueError(f"unsafe/noncanonical s6 input or legal count mismatch: {key}")
            found.append((key, legal, row))
    if len(found) != 1:
        raise ValueError(f"expected exactly one s6 target row in {path}, got {len(found)}")
    return found[0]


def read_one_output(path: Path, key: tuple[int, int], legal: int, budget: int) -> tuple[list[str], int, int]:
    rows = []
    with path.open(newline="", encoding="utf-8-sig") as stream:
        for line_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if (len(row) != 11 or row[0] != "replay" or int(row[2]) != 6 or int(row[4]) != 1
                    or (int(row[9]), int(row[10])) != key or int(row[3]) != legal
                    or int(row[5]) != budget or int(row[6]) not in (0, 1, 2) or int(row[7]) < 0):
                raise ValueError(f"unexpected/mismatched s6 output {path}:{line_no}: {row}")
            rows.append(row)
    if len(rows) != 1:
        raise ValueError(f"expected one S6 replay row in {path}, got {len(rows)}")
    return rows[0], int(rows[0][6]), int(rows[0][7])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--parent", type=Path, required=True)
    parser.add_argument("--saved-full-detail", type=Path, required=True)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--dispatch-main-commit", required=True)
    parser.add_argument("--budget", type=int, required=True)
    parser.add_argument("--raw-dir", type=Path, required=True)
    parser.add_argument("--inputs-out", type=Path, required=True)
    parser.add_argument("--raw-exact-out", type=Path, required=True)
    parser.add_argument("--s6-cache-out", type=Path, required=True)
    parser.add_argument("--runner-summary-out", type=Path, required=True)
    parser.add_argument("--manifest-out", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    args = parser.parse_args()
    if args.budget <= 0:
        parser.error("budget must be positive")

    output_files = [args.inputs_out, args.raw_exact_out, args.s6_cache_out,
                    args.runner_summary_out, args.manifest_out, args.summary_out]
    if any(path.exists() for path in output_files) or args.raw_dir.exists():
        raise SystemExit("refusing to overwrite an existing evidence artifact or raw directory")
    if not args.run_dir.is_dir() or not args.solver.is_file():
        raise SystemExit("run directory or exact solver is missing")

    parent = read_parent(args.parent)
    boundary = make_boundary(parent)
    full_detail = check_full_detail(args.saved_full_detail, parent, boundary)
    runner_summary_path = args.run_dir / "summary.json"
    runner = json.loads(runner_summary_path.read_text(encoding="utf-8"))
    parent_rows = runner.get("parents", [])
    if (len(parent_rows) != 1 or tuple(parent_rows[0].get("key", [])) != parent
            or parent_rows[0].get("outcome") != "WIN"
            or parent_rows[0].get("child_count") != len(boundary)
            or parent_rows[0].get("counts") != {"0": 0, "1": len(boundary), "2": 0}
            or parent_rows[0].get("unresolved_children") != []
            or runner.get("unresolved_boundary_count") != 0):
        raise SystemExit("local runner summary does not prove this full S6 boundary WIN")
    solver_digest = sha256(args.solver)
    if runner.get("budget") != args.budget:
        raise SystemExit("local runner budget differs from the requested materialization budget")

    sources = runner.get("new_solver_sources", [])
    if len(sources) != len(boundary) or runner.get("new_solver_exact") != len(boundary):
        raise SystemExit("runner's new exact S6 outputs do not cover the full boundary")
    listed = set()
    raw_rows = []
    input_rows = []
    source_items = []
    verdict_counts: Counter[int] = Counter()
    nodes_total = 0
    args.raw_dir.mkdir(parents=True, exist_ok=False)
    for source in sources:
        key = tuple(source.get("key", []))
        out_path = Path(source.get("path", ""))
        if not out_path.is_file() or sha256(out_path) != source.get("sha256"):
            raise SystemExit(f"local S6 raw output missing or hash mismatch: {out_path}")
        input_path = out_path.with_name(out_path.name.replace(".out.csv", ".input.csv"))
        if not input_path.is_file():
            raise SystemExit(f"local S6 input CSV missing: {input_path}")
        input_key, legal, input_row = read_one_target(input_path)
        raw_row, verdict, nodes = read_one_output(out_path, key, legal, args.budget)
        if key != input_key or key not in boundary or key in listed:
            raise SystemExit(f"unexpected, duplicate, or non-child S6 result: {key}")
        if verdict != 1:
            raise SystemExit(f"S6 boundary is not all exact WIN; found verdict={verdict} for {key}")
        if source.get("verdict") != verdict or source.get("nodes") != nodes:
            raise SystemExit(f"runner source record disagrees with S6 output: {key}")

        dest = args.raw_dir / out_path.name
        shutil.copyfile(out_path, dest)
        if sha256(dest) != source["sha256"]:
            raise SystemExit(f"preserved S6 raw copy hash differs from local source: {key}")
        listed.add(key)
        raw_rows.append(raw_row)
        input_rows.append(input_row)
        verdict_counts[verdict] += 1
        nodes_total += nodes
        source_items.append({
            "artifact_path": relpath(dest),
            "sha256": sha256(dest),
            "bytes": dest.stat().st_size,
            "source_local_path": relpath(out_path),
            "source_local_sha256": sha256(out_path),
            "input_local_path": relpath(input_path),
            "input_local_sha256": sha256(input_path),
            "key": list(key),
            "verdict": verdict,
            "nodes": nodes,
            "replay_rows": 1,
        })
    if listed != boundary:
        raise SystemExit(f"runner S6 rows differ from the complete geometry boundary: {len(listed)} != {len(boundary)}")

    inputs_text = ("# Complete canonical safe/legal S6 boundary input for one exact S5 AND parent.\n"
                   "# Each row is the exact target row format passed to dfpn.exe.\n"
                   + "".join(",".join(row) + "\n" for row in sorted(input_rows, key=lambda row: (int(row[3]), int(row[4])))))
    raw_text = ("# Raw exact S6 replay rows copied byte-for-byte into per-position files under raw/.\n"
                "# Aggregate contains the 87 solver replay rows; use source manifest to verify each raw copy.\n"
                + "".join(",".join(row) + "\n" for row in sorted(raw_rows, key=lambda row: (int(row[9]), int(row[10])))))
    cache_text = ("# exact s6 verdict cache: n=11 schema=1 (exact WIN rows from complete S5 boundary descent)\n"
                  + "".join(f"s6verdict,{row[9]},{row[10]},6,1,0\n"
                           for row in sorted(raw_rows, key=lambda row: (int(row[9]), int(row[10])))))
    args.inputs_out.parent.mkdir(parents=True, exist_ok=True)
    args.inputs_out.write_text(inputs_text, encoding="utf-8", newline="\n")
    args.raw_exact_out.write_text(raw_text, encoding="utf-8", newline="\n")
    args.s6_cache_out.write_text(cache_text, encoding="utf-8", newline="\n")
    shutil.copyfile(runner_summary_path, args.runner_summary_out)

    source_manifest = {
        "schema": "n11-dual-tight-s6-descent-source-manifest-v1",
        "dispatch_main_commit": args.dispatch_main_commit,
        "budget_per_target": args.budget,
        "worker_count": runner.get("workers"),
        "solver": {"path": relpath(args.solver), "sha256": solver_digest},
        "local_run_dir": relpath(args.run_dir),
        "parent": {"path": relpath(args.parent), "sha256": sha256(args.parent), "key": list(parent)},
        "saved_full_boundary_detail": full_detail,
        "runner_summary": {"path": relpath(args.runner_summary_out),
                           "sha256": sha256(args.runner_summary_out),
                           "reported_s5_outcome": "WIN", "new_exact_s6_rows": len(raw_rows)},
        "input_artifact": {"path": relpath(args.inputs_out), "sha256": sha256(args.inputs_out),
                           "s6_target_rows": len(input_rows)},
        "raw_aggregate": {"path": relpath(args.raw_exact_out), "sha256": sha256(args.raw_exact_out),
                          "s6_replay_rows": len(raw_rows)},
        "exact_s6_cache": {"path": relpath(args.s6_cache_out), "sha256": sha256(args.s6_cache_out),
                           "rows": len(raw_rows)},
        "raw_sources": source_items,
        "source_replay_rows": len(source_items),
        "verdict_counts": {"WIN": verdict_counts[1], "LOSS": verdict_counts[2], "UNKNOWN": verdict_counts[0]},
        "exact_conflicts": 0,
        "unknowns_propagated": False,
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(json.dumps(source_manifest, indent=2, sort_keys=True) + "\n",
                                 encoding="utf-8", newline="\n")

    summary = {
        "schema": "n11-reply27-s6-descent-evidence-summary-v1",
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "dispatch_main_commit": args.dispatch_main_commit,
        "parent_s5": list(parent),
        "complete_canonical_s6_boundary": len(boundary),
        "exact_s6_verdict_counts": {"WIN": verdict_counts[1], "LOSS": verdict_counts[2], "UNKNOWN": verdict_counts[0]},
        "new_s6_rows": len(raw_rows),
        "nodes": nodes_total,
        "budget_per_target": args.budget,
        "workers": runner.get("workers"),
        "solver_sha256": solver_digest,
        "s5_outcome_from_complete_s6_boundary": "WIN",
        "class_outcome_not_assigned_here": True,
        "conflicts": 0,
        "unknowns_propagated": False,
        "artifacts": {
            "inputs": {"path": relpath(args.inputs_out), "sha256": sha256(args.inputs_out)},
            "raw_exact": {"path": relpath(args.raw_exact_out), "sha256": sha256(args.raw_exact_out)},
            "s6_exact_cache": {"path": relpath(args.s6_cache_out), "sha256": sha256(args.s6_cache_out)},
            "runner_summary": {"path": relpath(args.runner_summary_out), "sha256": sha256(args.runner_summary_out)},
            "source_manifest": {"path": relpath(args.manifest_out), "sha256": sha256(args.manifest_out)},
            "raw_directory_file_count": len(source_items),
        },
    }
    args.summary_out.parent.mkdir(parents=True, exist_ok=True)
    args.summary_out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n",
                                encoding="utf-8", newline="\n")
    print(json.dumps({"parent_s5": list(parent), "boundary_s6": len(boundary),
                      "s6_verdict_counts": summary["exact_s6_verdict_counts"], "new_rows": len(raw_rows),
                      "nodes": nodes_total, "conflicts": 0, "summary": relpath(args.summary_out),
                      "manifest_sha256": sha256(args.manifest_out)}, indent=2))


if __name__ == "__main__":
    main()
