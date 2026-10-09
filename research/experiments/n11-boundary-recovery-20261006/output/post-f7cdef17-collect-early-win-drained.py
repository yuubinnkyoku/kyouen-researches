#!/usr/bin/env python3
"""Collect an exact-WIN probe where remaining workers may have drained cleanly."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def replay_row(path: Path, key: tuple[int, int], target: list[str], budget: int) -> list[str]:
    rows = [row for row in csv.reader(path.open(newline="", encoding="utf-8-sig"))
            if row and not row[0].lstrip().startswith("#")]
    if len(rows) != 1:
        raise SystemExit(f"expected one completed solver row in {path}: {len(rows)}")
    row = rows[0]
    if (len(row) != 11 or row[0] != "replay" or int(row[2]) != 5 or int(row[4]) != 0
            or int(row[3]) != int(target[5]) or int(row[5]) != budget
            or (int(row[9]), int(row[10])) != key or int(row[6]) not in (0, 1, 2)
            or int(row[7]) < 0):
        raise SystemExit(f"invalid completed replay row for {key}: {row}")
    return row


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--scheduled-targets", type=Path, required=True)
    ap.add_argument("--run-dir", type=Path, required=True)
    ap.add_argument("--schedule-manifest", type=Path, required=True)
    ap.add_argument("--solver", type=Path, required=True)
    ap.add_argument("--solver-source", type=Path, required=True)
    ap.add_argument("--runner", type=Path, required=True)
    ap.add_argument("--raw-exact-out", type=Path, required=True)
    ap.add_argument("--raw-all-out", type=Path, required=True)
    ap.add_argument("--exact-targets-out", type=Path, required=True)
    ap.add_argument("--exact-cache-out", type=Path, required=True)
    ap.add_argument("--summary-out", type=Path, required=True)
    ap.add_argument("--runner-summary-out", type=Path, required=True)
    ap.add_argument("--partial-out", type=Path, required=True)
    ap.add_argument("--sources-out", type=Path, required=True)
    ap.add_argument("--budget", type=int, default=15_000_000)
    args = ap.parse_args()
    outputs = (args.raw_exact_out, args.raw_all_out, args.exact_targets_out,
               args.exact_cache_out, args.summary_out, args.runner_summary_out,
               args.partial_out, args.sources_out)
    if any(path.exists() for path in outputs):
        raise SystemExit("refusing to overwrite an existing collected artifact")
    if not all(path.is_file() for path in (args.solver, args.solver_source, args.runner)):
        raise SystemExit("solver or bound source file is missing")

    schedule = json.loads(args.schedule_manifest.read_text(encoding="utf-8"))
    if schedule.get("probe_target_sha256") != sha256(args.scheduled_targets):
        raise SystemExit("schedule manifest does not bind the scheduled target file")
    if schedule.get("budget_per_target") != args.budget:
        raise SystemExit("budget disagrees with the immutable schedule manifest")
    bound = {item["path"]: item["sha256"] for item in schedule.get("sources", [])}
    for path in (args.solver, args.solver_source, args.runner):
        if bound.get(rel(path)) != sha256(path):
            raise SystemExit(f"schedule manifest source hash mismatch: {rel(path)}")

    targets: dict[tuple[int, int], list[str]] = {}
    with args.scheduled_targets.open(newline="", encoding="utf-8-sig") as stream:
        for line_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 11 or int(row[2]) != 5 or int(row[7]) != 0:
                raise SystemExit(f"invalid scheduled s5 target {line_no}: {row}")
            key = (int(row[3]), int(row[4]))
            if key in targets:
                raise SystemExit(f"duplicate scheduled key: {key}")
            targets[key] = row
    expected_keys = [tuple(key) for key in schedule.get("probe_targets", [])]
    if list(targets) != expected_keys or len(targets) != schedule.get("probe_count"):
        raise SystemExit("scheduled target keys/order disagree with the source manifest")

    run_entries = []
    raw_rows: list[list[str]] = []
    exact_rows: list[list[str]] = []
    exact_targets: list[list[str]] = []
    exact_cache: dict[tuple[int, int], tuple[int, int]] = {}
    statuses: dict[tuple[int, int], str] = {}
    partial_records = []
    for key, target in targets.items():
        stem = f"s5-{key[0]}-{key[1]}"
        input_path = args.run_dir / f"{stem}.input.csv"
        output_path = args.run_dir / f"{stem}.out.csv"
        partial_path = output_path.with_suffix(output_path.suffix + ".tmp")
        log_path = args.run_dir / f"{stem}.log"
        started = input_path.is_file()
        if started:
            input_rows = [row for row in csv.reader(input_path.open(newline="", encoding="utf-8-sig"))
                          if row and not row[0].lstrip().startswith("#")]
            if input_rows != [target]:
                raise SystemExit(f"started input row differs from scheduled target: {key}")
        if output_path.is_file() and partial_path.exists():
            raise SystemExit(f"both final and partial outputs exist for {key}")
        entry = {"key": list(key), "started": started,
                 "input": ({"path": rel(input_path), "sha256": sha256(input_path),
                            "bytes": input_path.stat().st_size} if started else None),
                 "log": ({"path": rel(log_path), "sha256": sha256(log_path),
                          "bytes": log_path.stat().st_size} if log_path.is_file() else None)}
        if output_path.is_file():
            if not started:
                raise SystemExit(f"completed output exists without dispatched input: {key}")
            row = replay_row(output_path, key, target, args.budget)
            verdict, nodes = int(row[6]), int(row[7])
            status = {0: "completed_UNKNOWN", 1: "exact_WIN", 2: "exact_LOSS"}[verdict]
            entry.update(status=status, output={"path": rel(output_path),
                                                "sha256": sha256(output_path),
                                                "bytes": output_path.stat().st_size,
                                                "verdict": verdict, "nodes": nodes})
            raw_rows.append(row)
            if verdict in (1, 2):
                exact_rows.append(row)
                exact_targets.append(target)
                exact_cache[key] = (verdict, nodes)
        elif partial_path.is_file():
            if not started:
                raise SystemExit(f"partial output exists without dispatched input: {key}")
            data = partial_path.read_bytes()
            partial_copy = args.partial_out.with_name(
                f"{args.partial_out.stem}-{key[0]}-{key[1]}{args.partial_out.suffix}"
            )
            if partial_copy.exists():
                raise SystemExit(f"refusing to overwrite interrupted partial evidence: {partial_copy}")
            partial_records.append({
                "key": list(key), "source_path": rel(partial_path),
                "source_sha256": sha256(partial_path), "source_bytes": len(data),
                "path": rel(partial_copy), "sha256": hashlib.sha256(data).hexdigest(),
                "bytes": len(data), "status": "UNKNOWN; no completed replay row",
                "_copy_path": partial_copy,
            })
            entry.update(status="interrupted_partial", partial={
                "path": rel(partial_copy), "sha256": hashlib.sha256(data).hexdigest(),
                "bytes": len(data)})
        elif started:
            raise SystemExit(f"started solver has neither a final nor partial output: {key}")
        else:
            entry.update(status="not_dispatched")
        statuses[key] = entry["status"]
        run_entries.append(entry)

    wins = [key for key, status in statuses.items() if status == "exact_WIN"]
    if not wins:
        raise SystemExit("no completed exact s5 WIN witness; early-WIN collector is inapplicable")
    # complete_class_local.py stops submitting roots as soon as a WIN arrives,
    # then drains already active workers. Such a valid early-WIN run can have
    # not-dispatched targets and no partial output files.

    args.raw_exact_out.parent.mkdir(parents=True, exist_ok=True)
    def write_rows(path: Path, rows: list[list[str]]) -> None:
        with path.open("w", newline="", encoding="utf-8") as stream:
            stream.write("# collected replay rows; source per-root files are hash-bound in the manifest\n")
            writer = csv.writer(stream, lineterminator="\n")
            writer.writerows(rows)
    write_rows(args.raw_all_out, raw_rows)
    write_rows(args.raw_exact_out, exact_rows)
    with args.exact_targets_out.open("w", newline="", encoding="utf-8") as stream:
        stream.write("# exact-completed subset of the scheduled s5 probe; UNKNOWN and interrupted keys excluded\n")
        csv.writer(stream, lineterminator="\n").writerows(exact_targets)
    with args.exact_cache_out.open("w", encoding="utf-8", newline="") as stream:
        stream.write("# s5 verdict cache: n=11 schema=1 (exact rows only; UNKNOWN excluded)\n")
        for (lo, hi), (verdict, nodes) in sorted(exact_cache.items()):
            stream.write(f"s5verdict,{lo},{hi},5,{verdict},{nodes}\n")
    for partial in partial_records:
        partial["_copy_path"].write_bytes(Path(partial["source_path"]).read_bytes())
        del partial["_copy_path"]

    exact_counts = Counter(int(row[6]) for row in exact_rows)
    all_nodes = sum(int(row[7]) for row in raw_rows)
    exact_nodes = sum(int(row[7]) for row in exact_rows)
    not_dispatched = [list(key) for key, status in statuses.items() if status == "not_dispatched"]
    interrupted = [list(key) for key, status in statuses.items()
                   if status in ("interrupted_partial", "interrupted_no_result")]
    unresolved = [list(key) for key, status in statuses.items()
                  if status in ("completed_UNKNOWN", "interrupted_partial", "not_dispatched")]
    runner_summary = {
        "schema": "n11-dual-tight-early-win-runner-summary-v1",
        "scope": "the eight scheduled s5 probes only; remaining class children were not scheduled",
        "class_key": schedule["class_key"], "scheduled": len(targets),
        "started": sum(entry["started"] for entry in run_entries),
        "completed_output_rows": len(raw_rows), "new_exact": len(exact_rows),
        "new_win": exact_counts[1], "new_loss": exact_counts[2],
        "completed_unknown": exact_counts[0], "interrupted_partial_count": len(interrupted),
        "not_dispatched_count": len(not_dispatched), "exact_verdict_conflicts": 0,
        "workers": schedule["workers"], "budget": args.budget,
        "nodes_exact": exact_nodes, "nodes_all_completed_rows": all_nodes,
        "class_status_from_exact_witness": "WIN_WITNESS_PENDING_GEOMETRY_AUDIT",
        "exact_win_witness_candidates": [list(key) for key in wins],
        "interrupted": interrupted, "not_dispatched": not_dispatched,
        "unresolved_probe_keys": unresolved,
        "stop_reason": ("An exact s5 WIN row appeared. No further targets were dispatched; "
                        "the caller interrupted remaining active workers, whose partial rows are preserved."
                        if partial_records else
                        "An exact s5 WIN row appeared. No further targets were dispatched; "
                        "the runner drained already active workers and preserved their completed rows."),
        "target_statuses": run_entries,
    }
    args.runner_summary_out.parent.mkdir(parents=True, exist_ok=True)
    args.runner_summary_out.write_text(json.dumps(runner_summary, indent=2, sort_keys=True) + "\n",
                                      encoding="utf-8", newline="\n")

    exact_summary = {
        "schema": "n11-dual-tight-class-exact-subset-summary-v1",
        "target_count": len(exact_rows),
        "exact_replay_counts": {"WIN": exact_counts[1], "LOSS": exact_counts[2], "UNKNOWN": 0},
        "nodes": exact_nodes, "budget_per_target": args.budget,
        "scope": "completed exact replay rows only; the enclosing s4 WIN conclusion is recorded after geometry verification",
        "raw_output": {"path": rel(args.raw_exact_out), "rows": len(exact_rows),
                       "sha256": sha256(args.raw_exact_out)},
        "new_exact_cache": {"path": rel(args.exact_cache_out), "rows": len(exact_cache),
                            "sha256": sha256(args.exact_cache_out)},
    }
    args.summary_out.parent.mkdir(parents=True, exist_ok=True)
    args.summary_out.write_text(json.dumps(exact_summary, indent=2, sort_keys=True) + "\n",
                                encoding="utf-8", newline="\n")

    schedule_source_paths = [args.scheduled_targets, args.schedule_manifest,
                             args.solver, args.solver_source, args.runner,
                             Path(__file__).resolve()]
    output_paths = [args.raw_exact_out, args.raw_all_out, args.exact_targets_out,
                    args.exact_cache_out, args.summary_out, args.runner_summary_out,
                    ]
    manifest = {
        "schema": "n11-dual-tight-early-win-run-manifest-v1",
        "class_key": schedule["class_key"],
        "scheduled_probe_target_sha256": sha256(args.scheduled_targets),
        "probe_target_sha256": sha256(args.exact_targets_out),
        "schedule_manifest": {"path": rel(args.schedule_manifest),
                              "sha256": sha256(args.schedule_manifest)},
        "probe_targets": [[int(row[3]), int(row[4])] for row in exact_targets],
        "runner_summary": runner_summary,
        "partial_solver_outputs": partial_records,
        "source_inputs": [{"path": rel(path), "sha256": sha256(path),
                           "bytes": path.stat().st_size} for path in schedule_source_paths],
        "outputs": [{"path": rel(path), "sha256": sha256(path),
                     "bytes": path.stat().st_size} for path in output_paths]
                   + [{"path": item["path"], "sha256": item["sha256"],
                       "bytes": item["bytes"]} for item in partial_records],
        "claim": "Exact replay values are solver outputs. UNKNOWN, interrupted, and not-dispatched keys are not entered in the exact cache.",
    }
    args.sources_out.parent.mkdir(parents=True, exist_ok=True)
    args.sources_out.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n",
                                encoding="utf-8", newline="\n")
    print(json.dumps({"scheduled": len(targets), "started": runner_summary["started"],
                      "completed": len(raw_rows), "exact": len(exact_rows),
                      "counts": dict(exact_counts), "nodes_exact": exact_nodes,
                      "nodes_all_completed": all_nodes, "win_witnesses": [list(k) for k in wins],
                      "interrupted": interrupted, "not_dispatched": not_dispatched}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
