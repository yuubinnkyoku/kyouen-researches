#!/usr/bin/env python3
"""Collect an adaptively stopped dual-tight probe after an exact s5 WIN."""
from __future__ import annotations

import argparse
import csv
import json
import shutil
import sys
from collections import Counter
from pathlib import Path

import collect_dual_tight_completed_probe_v2 as common

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research/experiments/n11-search-methods/scripts"))
from dfpn_edge_classes import d4_canonical_key, has_forbidden_quad, legal_after  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--class-lo", type=int, required=True)
    ap.add_argument("--class-hi", type=int, required=True)
    ap.add_argument("--scheduled-targets", type=Path, required=True)
    ap.add_argument("--schedule-manifest", type=Path, required=True)
    ap.add_argument("--run-dir", type=Path, required=True)
    ap.add_argument("--base-cache", type=Path, required=True)
    ap.add_argument("--full-targets", type=Path, required=True)
    ap.add_argument("--ranking", type=Path, required=True)
    ap.add_argument("--solver", type=Path, required=True)
    ap.add_argument("--solver-source", type=Path, required=True)
    ap.add_argument("--runner", type=Path, required=True)
    ap.add_argument("--main-commit", required=True)
    ap.add_argument("--out-prefix", type=Path, required=True)
    ap.add_argument("--budget", type=int, default=15_000_000)
    args = ap.parse_args()

    class_key = (args.class_lo, args.class_hi)
    class_points = tuple([i for i in range(64) if (class_key[0] >> i) & 1]
                         + [64 + i for i in range(57) if (class_key[1] >> i) & 1])
    if (len(class_points) != 4 or has_forbidden_quad(class_points)
            or tuple(d4_canonical_key(class_points)) != class_key):
        raise SystemExit(f"unsafe or noncanonical s4 class: {class_key}")

    suffixes = ("-raw-all.csv", "-raw-exact.csv", "-exact-targets.csv",
                "-new-exact-s5.cache", "-merged-s5.cache", "-summary.json",
                "-runner-summary.json", "-merge-receipt.json", "-sources.json")
    outputs = {suffix: args.out_prefix.with_name(args.out_prefix.name + suffix)
               for suffix in suffixes}
    raw_copy_dir = args.out_prefix.with_name(args.out_prefix.name + "-raw")
    if any(path.exists() for path in outputs.values()) or raw_copy_dir.exists():
        raise SystemExit("refusing to overwrite collected evidence")

    schedule = json.loads(args.schedule_manifest.read_text(encoding="utf-8"))
    if (schedule.get("class_key") != list(class_key)
            or schedule.get("probe_target_sha256") != common.sha256(args.scheduled_targets)
            or schedule.get("budget_per_target") != args.budget):
        raise SystemExit("schedule manifest does not bind this class, input, and budget")
    for path in (args.solver, args.solver_source, args.runner):
        rel = common.relative(path)
        if not any(item.get("path", "").replace("\\", "/") == rel
                   and item.get("sha256") == common.sha256(path)
                   for item in schedule.get("sources", [])):
            raise SystemExit(f"schedule does not bind an unchanged source: {rel}")
    for item in schedule.get("sources", []):
        source = (ROOT / Path(item["path"])).resolve()
        if not source.is_file() or common.sha256(source) != item.get("sha256"):
            raise SystemExit(f"scheduled source is missing or changed: {item.get('path')}")

    targets: dict[tuple[int, int], list[str]] = {}
    for row_no, row in enumerate(common.rows(args.scheduled_targets), 1):
        if len(row) != 11 or int(row[2]) != 5 or int(row[7]) != 0:
            raise SystemExit(f"invalid scheduled s5 target at row {row_no}: {row}")
        key = (int(row[3]), int(row[4]))
        points = common.key_points(key)
        if int(row[5]) != len(legal_after(set(points))) or key in targets:
            raise SystemExit(f"scheduled target geometry mismatch or duplicate: {key}")
        targets[key] = row
    schedule_keys = [tuple(map(int, key)) for key in schedule.get("probe_targets", [])]
    if list(targets) != schedule_keys or len(targets) != schedule.get("probe_count"):
        raise SystemExit("scheduled target keys/order disagree with the source manifest")

    base = common.read_exact_cache(args.base_cache)
    full_keys = set()
    for row in common.rows(args.full_targets):
        if len(row) != 11 or int(row[2]) != 5:
            raise SystemExit(f"invalid full s5 boundary target: {row}")
        key = (int(row[3]), int(row[4]))
        if key in full_keys:
            raise SystemExit(f"duplicate full-boundary target: {key}")
        full_keys.add(key)
    child_keys = set()
    for move in legal_after(set(class_points)):
        child_points = tuple(sorted((*class_points, move)))
        if not has_forbidden_quad(child_points):
            child_keys.add(tuple(d4_canonical_key(child_points)))
    base_children = child_keys & set(base)
    if (base_children | full_keys != child_keys or base_children & full_keys
            or any(base[key][0] != 2 for key in base_children)):
        raise SystemExit("base cache and UNKNOWN targets do not partition the full class boundary")
    if not set(targets) <= full_keys:
        raise SystemExit("scheduled target is not in the complete UNKNOWN class boundary")

    runner_summary_path = args.run_dir / "summary.json"
    runner_summary = json.loads(runner_summary_path.read_text(encoding="utf-8"))
    not_dispatched = {tuple(map(int, key)) for key in runner_summary.get("not_dispatched", [])}
    if (runner_summary.get("targets") != len(targets)
            or runner_summary.get("budget") != args.budget
            or not not_dispatched or not not_dispatched < set(targets)
            or runner_summary.get("scheduled") != len(targets) - len(not_dispatched)
            or runner_summary.get("class_status") != "WIN"):
        raise SystemExit("runner summary is not an adaptive stop after an exact class WIN")

    completed = set(targets) - not_dispatched
    raw_all: list[list[str]] = []
    exact_rows: list[list[str]] = []
    exact_targets: list[list[str]] = []
    delta: dict[tuple[int, int], tuple[int, int]] = {}
    per_target = []
    copies = []
    for key, target in targets.items():
        stem = f"s5-{key[0]}-{key[1]}"
        input_path = args.run_dir / f"{stem}.input.csv"
        output_path = args.run_dir / f"{stem}.out.csv"
        log_path = args.run_dir / f"{stem}.log"
        temp_path = output_path.with_suffix(output_path.suffix + ".tmp")
        if key in not_dispatched:
            if any(path.exists() for path in (input_path, output_path, log_path, temp_path)):
                raise SystemExit(f"runner marked a target not dispatched but created files: {key}")
            continue
        if (not input_path.is_file() or not output_path.is_file()
                or temp_path.exists() or common.rows(input_path) != [target]):
            raise SystemExit(f"incomplete or mismatched dispatched target: {key}")
        replay = common.rows(output_path)
        if len(replay) != 1:
            raise SystemExit(f"expected one raw solver row for {key}, got {len(replay)}")
        row = replay[0]
        verdict, nodes = int(row[6]), int(row[7])
        if (len(row) != 11 or row[0] != "replay" or int(row[2]) != 5
                or int(row[3]) != int(target[5]) or int(row[4]) != 0
                or int(row[5]) != args.budget or (int(row[9]), int(row[10])) != key
                or verdict not in (0, 1, 2) or nodes < 0):
            raise SystemExit(f"raw replay row does not match dispatched target {key}: {row}")
        raw_all.append(row)
        if verdict in (1, 2):
            exact_rows.append(row)
            exact_targets.append(target)
            delta[key] = (verdict, nodes)
        copy_path = raw_copy_dir / f"{stem}.out.csv"
        copies.append((output_path, copy_path))
        per_target.append({
            "key": list(key), "verdict": verdict, "nodes": nodes,
            "input": {"path": common.relative(input_path), "sha256": common.sha256(input_path),
                      "bytes": input_path.stat().st_size},
            "output": {"path": common.relative(output_path), "sha256": common.sha256(output_path),
                       "bytes": output_path.stat().st_size},
            "log": {"path": common.relative(log_path), "sha256": common.sha256(log_path),
                    "bytes": log_path.stat().st_size} if log_path.is_file() else None,
            "archived_raw_copy": common.relative(copy_path),
        })

    counts = Counter(int(row[6]) for row in raw_all)
    nodes_all = sum(int(row[7]) for row in raw_all)
    unresolved = {tuple(map(int, key)) for key in runner_summary.get("unresolved", [])}
    expected_unresolved = not_dispatched | {tuple(int(x) for x in row[9:11])
                                             for row in raw_all if int(row[6]) == 0}
    if (completed != set(targets) - not_dispatched
            or len(completed) != runner_summary.get("scheduled")
            or set(delta) != {tuple(map(int, row[9:11])) for row in exact_rows}
            or len(delta) != runner_summary.get("new_exact")
            or counts[1] != runner_summary.get("new_win")
            or counts[2] != runner_summary.get("new_loss")
            or counts[0] != runner_summary.get("unknown")
            or nodes_all != runner_summary.get("nodes_total")
            or unresolved != expected_unresolved
            or counts[1] < 1):
        raise SystemExit("dispatched raw rows disagree with the adaptive runner summary")

    local_cache_path = (ROOT / Path(runner_summary["new_exact_cache"])).resolve()
    local_delta = common.read_exact_cache(local_cache_path)
    if local_delta != delta:
        raise SystemExit("runner's exact cache differs from raw exact replay rows")

    merged = dict(base)
    for key, (value, _) in delta.items():
        if key in merged:
            raise SystemExit(f"probe exact row duplicates a base cache key: {key}")
        merged[key] = (value, 0)

    for path in outputs.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    raw_copy_dir.mkdir(parents=True)
    for original, copied in copies:
        shutil.copyfile(original, copied)

    def write_csv(path: Path, content: list[list[str]], heading: str) -> None:
        with path.open("w", newline="", encoding="utf-8") as stream:
            stream.write(heading + "\n")
            csv.writer(stream, lineterminator="\n").writerows(content)

    write_csv(outputs["-raw-all.csv"], raw_all,
              "# completed adaptive replay rows; unstarted scheduled rows are listed in the summary")
    write_csv(outputs["-raw-exact.csv"], exact_rows,
              "# exact completed replay rows only; UNKNOWN excluded")
    write_csv(outputs["-exact-targets.csv"], exact_targets,
              "# exact-completed subset of scheduled targets; unstarted targets excluded")
    with outputs["-new-exact-s5.cache"].open("w", encoding="utf-8", newline="\n") as stream:
        stream.write("# s5 verdict cache: n=11 schema=1 (dispatched exact rows only)\n")
        for key in sorted(delta):
            value, nodes = delta[key]
            stream.write(f"s5verdict,{key[0]},{key[1]},5,{value},{nodes}\n")
    with outputs["-merged-s5.cache"].open("w", encoding="utf-8", newline="\n") as stream:
        stream.write("# s5 verdict cache: n=11 schema=1 (base exact cache plus adaptive probe delta)\n")
        for key in sorted(merged):
            stream.write(f"s5verdict,{key[0]},{key[1]},5,{merged[key][0]},0\n")

    summary = {
        "schema": "n11-dual-tight-adaptive-win-probe-summary-v1",
        "root": [60, 27], "class_key": list(class_key), "budget_per_target": args.budget,
        "scheduled_targets": len(targets), "dispatched_targets": len(completed),
        "not_dispatched_after_win": [list(key) for key in sorted(not_dispatched)],
        "completed_targets": len(raw_all),
        "exact_replay_counts": {"WIN": counts[1], "LOSS": counts[2], "UNKNOWN": counts[0]},
        "new_exact": len(delta), "nodes_exact": sum(int(row[7]) for row in exact_rows),
        "nodes_all_completed_rows": nodes_all, "class_status_from_exact_witness": "WIN",
        "stop_reason": "first exact s5 WIN; only already-running workers were drained",
        "raw_output": {"path": common.relative(outputs["-raw-exact.csv"]),
                       "rows": len(exact_rows), "sha256": common.sha256(outputs["-raw-exact.csv"])},
        "raw_all_output": {"path": common.relative(outputs["-raw-all.csv"]),
                           "rows": len(raw_all), "sha256": common.sha256(outputs["-raw-all.csv"])},
        "new_exact_cache": {"path": common.relative(outputs["-new-exact-s5.cache"]),
                            "rows": len(delta), "sha256": common.sha256(outputs["-new-exact-s5.cache"])},
        "merged_cache": {"path": common.relative(outputs["-merged-s5.cache"]),
                         "rows": len(merged), "sha256": common.sha256(outputs["-merged-s5.cache"])},
        "unknown_keys": [list((int(row[9]), int(row[10]))) for row in raw_all if int(row[6]) == 0],
    }
    outputs["-summary.json"].write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n",
                                        encoding="utf-8", newline="\n")
    outputs["-runner-summary.json"].write_text(
        json.dumps(runner_summary, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    base_hist = Counter(value for value, _nodes in base.values())
    merged_hist = Counter(value for value, _nodes in merged.values())
    receipt = {
        "schema": "n11-dual-tight-adaptive-probe-merge-receipt-v1",
        "base_cache": {"path": common.relative(args.base_cache), "sha256": common.sha256(args.base_cache),
                       "rows": len(base), "WIN": base_hist[1], "LOSS": base_hist[2]},
        "delta_cache": {"path": common.relative(outputs["-new-exact-s5.cache"]),
                         "sha256": common.sha256(outputs["-new-exact-s5.cache"]),
                         "rows": len(delta), "WIN": counts[1], "LOSS": counts[2]},
        "merged_cache": {"path": common.relative(outputs["-merged-s5.cache"]),
                         "sha256": common.sha256(outputs["-merged-s5.cache"]),
                         "rows": len(merged), "WIN": merged_hist[1], "LOSS": merged_hist[2]},
        "dispatched_targets": len(completed), "not_dispatched_after_win": [list(key) for key in sorted(not_dispatched)],
        "duplicate_verdicts": 0, "conflicts": 0, "unknown_rows_excluded_from_cache": counts[0],
    }
    outputs["-merge-receipt.json"].write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n",
                                              encoding="utf-8", newline="\n")

    input_paths = [args.scheduled_targets, args.schedule_manifest, runner_summary_path,
                   local_cache_path, args.base_cache, args.full_targets, args.ranking,
                   args.solver, args.solver_source, args.runner, Path(__file__).resolve(),
                   Path(common.__file__).resolve(),
                   ROOT / "research/experiments/n11-search-methods/scripts/dfpn_edge_classes.py"]
    source_doc = {
        "schema": "n11-dual-tight-adaptive-win-probe-sources-v1",
        "claim": "The four dispatched s5 rows are exact solver results. The runner stopped dispatch after an exact WIN; four scheduled targets remain explicitly unstarted and unknown.",
        "main_at_dispatch": args.main_commit,
        "class_key": list(class_key),
        "inputs": [{"path": common.relative(path), "sha256": common.sha256(path),
                    "bytes": path.stat().st_size} for path in input_paths],
        "schedule_bound_sources": schedule.get("sources", []),
        "dispatched_targets": per_target,
        "not_dispatched_after_win": [list(key) for key in sorted(not_dispatched)],
        "outputs": [{"path": common.relative(path), "sha256": common.sha256(path),
                     "bytes": path.stat().st_size}
                    for path in outputs.values() if path.name != outputs["-sources.json"].name]
                   + [{"path": common.relative(copied), "sha256": common.sha256(copied),
                       "bytes": copied.stat().st_size} for _original, copied in copies],
        "probe_target_sha256": common.sha256(outputs["-exact-targets.csv"]),
        "scheduled_target_sha256": common.sha256(args.scheduled_targets),
    }
    outputs["-sources.json"].write_text(json.dumps(source_doc, indent=2, sort_keys=True) + "\n",
                                        encoding="utf-8", newline="\n")
    print(json.dumps({"class_key": class_key, "class_status": "WIN", "scheduled": len(targets),
                      "dispatched": len(completed), "not_dispatched": len(not_dispatched),
                      "counts": dict(sorted(counts.items())), "nodes": nodes_all,
                      "merged_rows": len(merged), "conflicts": 0,
                      "outputs": {key: common.relative(value) for key, value in outputs.items()}},
                     sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
