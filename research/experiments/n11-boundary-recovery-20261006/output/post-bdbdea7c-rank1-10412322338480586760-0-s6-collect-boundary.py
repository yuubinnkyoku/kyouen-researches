#!/usr/bin/env python3
"""Preserve and audit exact s6 evidence for one complete canonical boundary."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research/experiments/n11-search-methods/scripts"))
sys.path.insert(0, str(ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts"))
from dfpn_edge_classes import d4_canonical_key, has_forbidden_quad, legal_after  # noqa: E402
from audit_saved_s6_targets import points, safe_canonical  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def read_one_replay(path: Path, key: tuple[int, int], budget: int | None = None):
    found = None
    with path.open(newline="", encoding="utf-8-sig") as stream:
        for line_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if row[0] != "replay" or len(row) != 11 or int(row[2]) != 6 or int(row[4]) != 1:
                raise SystemExit(f"invalid exact s6 replay {path}:{line_no}: {row}")
            actual_key = (int(row[9]), int(row[10]))
            if actual_key != key:
                continue
            if not safe_canonical(actual_key, 6):
                raise SystemExit(f"unsafe s6 key in {path}: {actual_key}")
            if int(row[3]) != len(legal_after(set(points(key)))):
                raise SystemExit(f"s6 legal-count mismatch in {path}: {row}")
            verdict, nodes = int(row[6]), int(row[7])
            if verdict not in (0, 1, 2) or nodes < 0:
                raise SystemExit(f"invalid s6 verdict/nodes in {path}: {row}")
            if budget is not None and int(row[5]) != budget:
                raise SystemExit(f"budget mismatch in {path}: {row[5]} != {budget}")
            if found is not None:
                raise SystemExit(f"multiple s6 replay rows in {path}")
            found = {"key": key, "row": row, "verdict": verdict, "nodes": nodes,
                     "legal_count": int(row[3]), "budget": int(row[5]), "path": path}
    if found is None:
        raise SystemExit(f"no replay row in {path}")
    return found


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--boundary", type=Path, required=True)
    ap.add_argument("--boundary-meta", type=Path, required=True)
    ap.add_argument("--preaudit", type=Path, required=True)
    ap.add_argument("--s6-run-summary", type=Path, required=True)
    ap.add_argument("--s6-run-dir", type=Path, required=True)
    ap.add_argument("--high-input", type=Path, required=True)
    ap.add_argument("--high-raw", type=Path, required=True)
    ap.add_argument("--high-budget", type=int, required=True)
    ap.add_argument("--raw-dir", type=Path, required=True)
    ap.add_argument("--combined-raw", type=Path, required=True)
    ap.add_argument("--exact-cache", type=Path, required=True)
    ap.add_argument("--derived-s5-cache", type=Path, required=True)
    ap.add_argument("--summary-out", type=Path, required=True)
    ap.add_argument("--sources-out", type=Path, required=True)
    ap.add_argument("--s5-parent", type=Path, required=True)
    ap.add_argument("--solver", type=Path, required=True)
    ap.add_argument("--solver-source", type=Path, required=True)
    args = ap.parse_args()
    outputs = [args.combined_raw, args.exact_cache, args.derived_s5_cache,
               args.summary_out, args.sources_out]
    if any(path.exists() for path in outputs) or args.raw_dir.exists():
        raise SystemExit("refusing to overwrite existing evidence outputs")

    meta = json.loads(args.boundary_meta.read_text(encoding="utf-8"))
    parent_keys = [tuple(key) for key in meta.get("parent_keys", [])]
    if len(parent_keys) != 1:
        raise SystemExit(f"expected one s5 parent in boundary metadata, got {parent_keys}")
    parent = parent_keys[0]
    boundary = {tuple(row["key"]) for row in meta["canonical_children"]}
    if len(boundary) != meta.get("complete_boundary_count") or len(boundary) != 83:
        raise SystemExit("unexpected or duplicate canonical s6 boundary cardinality")
    if not all(safe_canonical(key, 6) for key in boundary):
        raise SystemExit("boundary metadata contains unsafe/noncanonical s6 key")

    preaudit = json.loads(args.preaudit.read_text(encoding="utf-8"))
    if (preaudit.get("parent_outcome_from_s6") != "UNKNOWN"
            or preaudit.get("counts") != {"exact_WIN": 1, "exact_LOSS": 0,
                                          "prior_UNKNOWN": 0, "unseen": 82}
            or preaudit.get("conflicts") != 0):
        raise SystemExit("pre-dispatch s6 history audit did not match the expected safe frontier")
    previous_rows = [child for child in preaudit["children"]
                     if child["verdict"] == "WIN"]
    if len(previous_rows) != 1:
        raise SystemExit("expected one saved exact WIN in the pre-dispatch boundary")
    previous_key = tuple(previous_rows[0]["key"])
    previous_observations = previous_rows[0]["observations"]
    if (not previous_observations
            or {item["verdict"] for item in previous_observations} != {1}):
        raise SystemExit("saved s6 WIN witness lacks consistent exact source rows")
    direct_source = next((item for item in previous_observations
                          if item["kind"] == "saved-source-audit"), previous_observations[0])
    previous_source = ROOT / direct_source["source"].replace("/", "\\")
    previous = read_one_replay(previous_source, previous_key)
    if previous["verdict"] != 1:
        raise SystemExit("saved s6 witness row no longer matches its audited WIN")

    run = json.loads(args.s6_run_summary.read_text(encoding="utf-8"))
    expected_dispatch = {tuple(key) for key in preaudit["dispatch_ready_keys"]}
    new_sources = run.get("new_solver_sources", [])
    if (run.get("boundary_canonical_s6_count") != 83
            or run.get("new_solver_rows") != 82 or run.get("new_solver_exact") != 81
            or len(new_sources) != 82):
        raise SystemExit("2M s6 runner summary differs from the expected 82-row result")
    if {tuple(item["key"]) for item in new_sources} != expected_dispatch:
        raise SystemExit("2M s6 run did not cover exactly the pre-audited unseen children")
    if previous_key in expected_dispatch or expected_dispatch & {previous_key}:
        raise SystemExit("2M dispatch unexpectedly repeats a saved exact child")

    raw_dir = args.raw_dir
    raw_dir.mkdir(parents=True)
    exact_rows: dict[tuple[int, int], dict] = {previous_key: previous}
    copied = []
    unknown_2m = []
    for item in sorted(new_sources, key=lambda x: tuple(x["key"])):
        key = tuple(item["key"])
        source = Path(item["path"])
        raw = read_one_replay(source, key, 2_000_000)
        if raw["verdict"] != item["verdict"] or raw["nodes"] != item["nodes"]:
            raise SystemExit(f"s6 runner summary disagrees with raw output: {key}")
        destination = raw_dir / f"s6-{key[0]}-{key[1]}-budget2m.out.csv"
        shutil.copyfile(source, destination)
        copied.append({"key": list(key), "budget": 2_000_000,
                       "source_path": rel(source), "source_sha256": sha256(source),
                       "path": rel(destination), "sha256": sha256(destination),
                       "bytes": destination.stat().st_size, "verdict": raw["verdict"],
                       "nodes": raw["nodes"]})
        if raw["verdict"] == 0:
            unknown_2m.append(key)
        else:
            exact_rows[key] = raw

    high_in_rows = list(csv.reader(args.high_input.open(newline="", encoding="utf-8-sig")))
    high_in_rows = [row for row in high_in_rows if row and not row[0].lstrip().startswith("#")]
    if len(high_in_rows) != 1:
        raise SystemExit("higher-budget input must contain exactly one replay target")
    high_key = (int(high_in_rows[0][3]), int(high_in_rows[0][4]))
    if len(unknown_2m) != 1 or high_key != unknown_2m[0]:
        raise SystemExit(f"higher-budget target is not the unique 2M UNKNOWN: {high_key} vs {unknown_2m}")
    high = read_one_replay(args.high_raw, high_key, args.high_budget)
    if high["verdict"] not in (1, 2):
        raise SystemExit("higher-budget s6 replay remained UNKNOWN")
    old = exact_rows.get(high_key)
    if old is not None and old["verdict"] != high["verdict"]:
        raise SystemExit(f"higher-budget exact verdict conflicts with existing exact row for {high_key}")
    exact_rows[high_key] = high
    high_copy = raw_dir / f"s6-{high_key[0]}-{high_key[1]}-budget{args.high_budget}.out.csv"
    shutil.copyfile(args.high_raw, high_copy)
    copied.append({"key": list(high_key), "budget": args.high_budget,
                   "source_path": rel(args.high_raw), "source_sha256": sha256(args.high_raw),
                   "path": rel(high_copy), "sha256": sha256(high_copy),
                   "bytes": high_copy.stat().st_size, "verdict": high["verdict"],
                   "nodes": high["nodes"], "supersedes_prior_unknown": True})

    if set(exact_rows) != boundary or any(row["verdict"] != 1 for row in exact_rows.values()):
        raise SystemExit("the complete s6 boundary is not all exact WIN after the higher-budget replay")

    args.combined_raw.parent.mkdir(parents=True, exist_ok=True)
    with args.combined_raw.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write("# complete canonical s6 boundary raw rows; exact WIN only\n")
        for key in sorted(exact_rows):
            stream.write(",".join(str(value) for value in exact_rows[key]["row"]) + "\n")
    with args.exact_cache.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write("# s6 verdict cache: n=11 schema=1 (complete canonical boundary exact WIN rows)\n")
        for key in sorted(exact_rows):
            stream.write(f"s6verdict,{key[0]},{key[1]},6,1,{exact_rows[key]['nodes']}\n")

    parent_points = points(parent)
    if not safe_canonical(parent, 5) or has_forbidden_quad(parent_points):
        raise SystemExit("s5 parent geometry is unsafe/noncanonical")
    args.derived_s5_cache.write_text(
        "# s5 verdict cache: n=11 schema=1 (derived from complete all-WIN exact s6 boundary)\n"
        f"s5verdict,{parent[0]},{parent[1]},5,1,0\n", encoding="utf-8", newline="\n")
    summary = {
        "schema": "n11-reply27-s6-complete-parent-summary-v1",
        "parent_key": list(parent), "boundary_s6_canonical_count": len(boundary),
        "new_solver_rows_2m": len(new_sources), "new_exact_win_2m": 81,
        "unknown_2m_retried_once_at_higher_budget": [list(high_key)],
        "higher_budget": args.high_budget, "higher_budget_verdict": high["verdict"],
        "new_solver_rows_higher_budget": 1,
        "parents": [{"key": list(parent), "outcome": "WIN", "child_count": len(boundary),
                     "counts": {"0": 0, "1": len(boundary), "2": 0},
                     "loss_witnesses": [], "unresolved_children": []}],
        "exact_child_count": len(exact_rows), "exact_child_verdicts": {"WIN": len(exact_rows), "LOSS": 0},
        "nodes_2m": sum(item["nodes"] for item in new_sources),
        "nodes_high_budget": high["nodes"],
        "raw_output": {"path": rel(args.combined_raw), "sha256": sha256(args.combined_raw)},
        "exact_cache": {"path": rel(args.exact_cache), "sha256": sha256(args.exact_cache)},
        "derived_s5_cache": {"path": rel(args.derived_s5_cache), "sha256": sha256(args.derived_s5_cache)},
    }
    args.summary_out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n",
                                encoding="utf-8", newline="\n")
    source_paths = [args.boundary, args.boundary_meta, args.preaudit, args.s6_run_summary,
                    args.high_input, args.high_raw, args.s5_parent, args.solver,
                    args.solver_source, Path(__file__).resolve()]
    source_manifest = {
        "schema": "n11-reply27-s6-complete-boundary-sources-v1",
        "parent_key": list(parent), "canonical_children": len(boundary),
        "solver": {"path": rel(args.solver), "sha256": sha256(args.solver)},
        "sources": [{"path": rel(path), "sha256": sha256(path), "bytes": path.stat().st_size}
                    for path in source_paths],
        "raw_solver_outputs": copied,
        "raw_dir": rel(raw_dir),
        "raw_dir_file_count": len(copied),
        "claim": "All canonical s6 children of the parent have exact WIN verdicts. The single 2M UNKNOWN was replayed once at a higher 15M budget; no 2M UNKNOWN was repeated at the same budget.",
        "summary": {"path": rel(args.summary_out), "sha256": sha256(args.summary_out)},
        "combined_raw": {"path": rel(args.combined_raw), "sha256": sha256(args.combined_raw)},
        "exact_cache": {"path": rel(args.exact_cache), "sha256": sha256(args.exact_cache)},
        "derived_s5_cache": {"path": rel(args.derived_s5_cache), "sha256": sha256(args.derived_s5_cache)},
    }
    args.sources_out.write_text(json.dumps(source_manifest, indent=2, sort_keys=True) + "\n",
                                encoding="utf-8", newline="\n")
    print(json.dumps({"parent": list(parent), "s6_children": len(boundary),
                      "exact_win": len(exact_rows), "exact_loss": 0,
                      "copied_raw_outputs": len(copied), "higher_budget_key": list(high_key),
                      "higher_budget_nodes": high["nodes"], "s5_outcome": "WIN"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
