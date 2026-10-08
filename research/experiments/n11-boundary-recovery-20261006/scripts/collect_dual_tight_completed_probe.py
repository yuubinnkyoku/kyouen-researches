#!/usr/bin/env python3
"""Collect a fully completed dual-tight probe, retaining UNKNOWN raw rows."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research/experiments/n11-search-methods/scripts"))
from dfpn_edge_classes import d4_canonical_key, has_forbidden_quad, legal_after  # noqa: E402


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def rows(path: Path) -> list[list[str]]:
    return [row for row in csv.reader(path.open(newline="", encoding="utf-8-sig"))
            if row and not row[0].lstrip().startswith("#")]


def key_points(key: tuple[int, int]) -> tuple[int, ...]:
    lo, hi = key
    pts = tuple([i for i in range(64) if (lo >> i) & 1]
                + [64 + i for i in range(57) if (hi >> i) & 1])
    if len(pts) != 5 or has_forbidden_quad(pts) or tuple(d4_canonical_key(pts)) != key:
        raise SystemExit(f"unsafe or noncanonical s5 key: {key}")
    return pts


def read_exact_cache(path: Path) -> dict[tuple[int, int], tuple[int, int]]:
    cache = {}
    for line_no, row in enumerate(csv.reader(path.open(newline="", encoding="utf-8-sig")), 1):
        if not row or row[0].lstrip().startswith("#"):
            continue
        if len(row) != 6 or row[0] != "s5verdict" or int(row[3]) != 5:
            raise SystemExit(f"invalid s5 cache row {path}:{line_no}: {row}")
        key = (int(row[1]), int(row[2]))
        key_points(key)
        value, nodes = int(row[4]), int(row[5])
        if value not in (1, 2) or nodes < 0 or key in cache:
            raise SystemExit(f"invalid or duplicate exact s5 cache row {path}:{line_no}: {row}")
        cache[key] = (value, nodes)
    return cache


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
    paths = {suffix: args.out_prefix.with_name(args.out_prefix.name + suffix)
             for suffix in suffixes}
    raw_copy_dir = args.out_prefix.with_name(args.out_prefix.name + "-raw")
    if any(path.exists() for path in paths.values()) or raw_copy_dir.exists():
        raise SystemExit("refusing to overwrite collected evidence")

    schedule = json.loads(args.schedule_manifest.read_text(encoding="utf-8"))
    if schedule.get("class_key") != list(class_key):
        raise SystemExit("schedule manifest identifies a different s4 class")
    if schedule.get("probe_target_sha256") != sha256(args.scheduled_targets):
        raise SystemExit("schedule manifest does not bind the scheduled target file")
    if schedule.get("budget_per_target") != args.budget:
        raise SystemExit("budget disagrees with the immutable schedule manifest")

    bound_sources = {item["path"]: item["sha256"] for item in schedule.get("sources", [])}
    required_bound = [args.solver, args.solver_source, args.runner]
    for path in required_bound:
        if bound_sources.get(relative(path)) != sha256(path):
            raise SystemExit(f"schedule source hash mismatch: {relative(path)}")
    for item in schedule.get("sources", []):
        source = ROOT / Path(item["path"])
        if not source.is_file() or sha256(source) != item["sha256"]:
            raise SystemExit(f"schedule source is missing or changed: {item['path']}")

    targets: dict[tuple[int, int], list[str]] = {}
    for line_no, target in enumerate(rows(args.scheduled_targets), 1):
        if len(target) != 11 or int(target[2]) != 5 or int(target[7]) != 0:
            raise SystemExit(f"invalid s5 target row {line_no}: {target}")
        key = (int(target[3]), int(target[4]))
        pts = key_points(key)
        if int(target[5]) != len(legal_after(set(pts))) or key in targets:
            raise SystemExit(f"target geometry mismatch or duplicate: {key}")
        targets[key] = target
    schedule_keys = [tuple(k) for k in schedule.get("probe_targets", [])]
    if list(targets) != schedule_keys or len(targets) != schedule.get("probe_count"):
        raise SystemExit("scheduled target keys/order disagree with manifest")

    base = read_exact_cache(args.base_cache)
    full_keys = set()
    for row in rows(args.full_targets):
        if len(row) != 11 or int(row[2]) != 5:
            raise SystemExit(f"invalid full-boundary target row: {row}")
        key = (int(row[3]), int(row[4]))
        if key in full_keys:
            raise SystemExit(f"duplicate full-boundary target: {key}")
        full_keys.add(key)
    child_keys = set()
    for move in legal_after(set(class_points)):
        points = tuple(sorted((*class_points, move)))
        if not has_forbidden_quad(points):
            child_keys.add(tuple(d4_canonical_key(points)))
    base_children = child_keys & set(base)
    if (base_children | full_keys != child_keys or base_children & full_keys
            or any(base[key][0] != 2 for key in base_children)):
        raise SystemExit("base cache and full UNKNOWN targets do not partition class geometry")

    runner_summary_path = args.run_dir / "summary.json"
    runner_summary = json.loads(runner_summary_path.read_text(encoding="utf-8"))
    if (runner_summary.get("targets") != len(targets)
            or runner_summary.get("scheduled") != len(targets)
            or runner_summary.get("not_dispatched") != []
            or runner_summary.get("unknown", 0) < 0
            or runner_summary.get("budget") != args.budget):
        raise SystemExit("runner summary does not describe a fully completed scheduled batch")

    raw_all: list[list[str]] = []
    exact_targets: list[list[str]] = []
    exact_rows: list[list[str]] = []
    delta: dict[tuple[int, int], tuple[int, int]] = {}
    run_evidence = []
    raw_copies = []
    for key, target in targets.items():
        stem = f"s5-{key[0]}-{key[1]}"
        input_path = args.run_dir / f"{stem}.input.csv"
        output_path = args.run_dir / f"{stem}.out.csv"
        log_path = args.run_dir / f"{stem}.log"
        partial_path = output_path.with_suffix(output_path.suffix + ".tmp")
        if not input_path.is_file() or not output_path.is_file() or partial_path.exists():
            raise SystemExit(f"scheduled solver row is incomplete: {key}")
        if rows(input_path) != [target]:
            raise SystemExit(f"solver input differs from scheduled target: {key}")
        replay = rows(output_path)
        if len(replay) != 1:
            raise SystemExit(f"expected one raw solver row for {key}: {len(replay)}")
        row = replay[0]
        verdict, nodes = int(row[6]), int(row[7])
        if (len(row) != 11 or row[0] != "replay" or int(row[2]) != 5
                or int(row[3]) != int(target[5]) or int(row[4]) != 0
                or int(row[5]) != args.budget or (int(row[9]), int(row[10])) != key
                or verdict not in (0, 1, 2) or nodes < 0):
            raise SystemExit(f"raw solver row does not match scheduled target {key}: {row}")
        if key not in full_keys or (key in base):
            raise SystemExit(f"scheduled key is not an unresolved s5 child: {key}")
        raw_all.append(row)
        if verdict in (1, 2):
            exact_rows.append(row)
            exact_targets.append(target)
            delta[key] = (verdict, nodes)
        copy_name = f"{stem}.out.csv"
        copied_path = raw_copy_dir / copy_name
        raw_copies.append((output_path, copied_path, key, verdict, nodes))
        run_evidence.append({
            "key": list(key), "verdict": verdict, "nodes": nodes,
            "input": {"path": relative(input_path), "sha256": sha256(input_path),
                      "bytes": input_path.stat().st_size},
            "output": {"path": relative(output_path), "sha256": sha256(output_path),
                       "bytes": output_path.stat().st_size},
            "log": {"path": relative(log_path), "sha256": sha256(log_path),
                    "bytes": log_path.stat().st_size} if log_path.is_file() else None,
            "archived_raw_copy": relative(copied_path),
        })

    counts = Counter(int(row[6]) for row in raw_all)
    nodes_all = sum(int(row[7]) for row in raw_all)
    if (len(delta) != runner_summary.get("new_exact")
            or counts[1] != runner_summary.get("new_win")
            or counts[2] != runner_summary.get("new_loss")
            or counts[0] != runner_summary.get("unknown")
            or nodes_all != runner_summary.get("nodes_total")):
        raise SystemExit("per-root rows disagree with local runner summary")
    expected_probe_status = "WIN" if counts[1] else "UNKNOWN"
    if runner_summary.get("class_status") != expected_probe_status:
        raise SystemExit("runner summary class status disagrees with its exact replay rows")
    local_cache_path = ROOT / Path(runner_summary["new_exact_cache"])
    local_delta = read_exact_cache(local_cache_path)
    if local_delta != delta:
        raise SystemExit("runner exact cache disagrees with raw exact rows")
    ranking = json.loads(args.ranking.read_text(encoding="utf-8"))
    if ranking.get("next_target", {}).get("key") != list(class_key):
        raise SystemExit("ranking artifact identifies a different s4 class")

    merged = dict(base)
    for key, value in delta.items():
        if key in merged and merged[key] != value:
            raise SystemExit(f"exact cache conflict for {key}: {merged[key]} vs {value}")
        if key in merged:
            raise SystemExit(f"scheduled delta duplicates an exact base key: {key}")
        merged[key] = value

    # All validation is complete. Create the immutable collected outputs.
    for path in paths.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    raw_copy_dir.mkdir(parents=True)
    for original, copied, _, _, _ in raw_copies:
        shutil.copyfile(original, copied)

    def write_csv(path: Path, content: list[list[str]], heading: str) -> None:
        with path.open("w", newline="", encoding="utf-8") as stream:
            stream.write(heading + "\n")
            csv.writer(stream, lineterminator="\n").writerows(content)

    write_csv(paths["-raw-all.csv"], raw_all,
              "# all completed scheduled replay rows; UNKNOWN is preserved and is not a verdict")
    write_csv(paths["-raw-exact.csv"], exact_rows,
              "# exact completed replay rows only; UNKNOWN excluded")
    write_csv(paths["-exact-targets.csv"], exact_targets,
              "# exact-completed subset of scheduled targets; UNKNOWN excluded")
    with paths["-new-exact-s5.cache"].open("w", encoding="utf-8", newline="\n") as stream:
        stream.write("# s5 verdict cache: n=11 schema=1 (exact rows only; UNKNOWN excluded)\n")
        for key in sorted(delta):
            verdict, nodes = delta[key]
            stream.write(f"s5verdict,{key[0]},{key[1]},5,{verdict},{nodes}\n")
    with paths["-merged-s5.cache"].open("w", encoding="utf-8", newline="\n") as stream:
        stream.write("# s5 verdict cache: n=11 schema=1 (base exact cache plus this probe delta)\n")
        for key in sorted(merged):
            verdict, nodes = merged[key]
            stream.write(f"s5verdict,{key[0]},{key[1]},5,{verdict},{nodes}\n")

    result_summary = {
        "schema": "n11-dual-tight-completed-probe-summary-v1",
        "root": [60, 27], "class_key": list(class_key), "budget_per_target": args.budget,
        "scheduled_targets": len(targets), "completed_targets": len(raw_all),
        "exact_replay_counts": {"WIN": counts[1], "LOSS": counts[2], "UNKNOWN": counts[0]},
        "new_exact": len(delta), "nodes_exact": sum(int(row[7]) for row in exact_rows),
        "nodes_all_completed_rows": nodes_all,
        "class_status_from_exact_witness": "WIN" if counts[1] else "UNKNOWN",
        "scope": "the scheduled bounded probe only; a class WIN is concluded only from an exact WIN s5 child and geometry audit",
        "raw_output": {"path": relative(paths["-raw-exact.csv"]), "rows": len(exact_rows),
                       "sha256": sha256(paths["-raw-exact.csv"])},
        "raw_all_output": {"path": relative(paths["-raw-all.csv"]), "rows": len(raw_all),
                           "sha256": sha256(paths["-raw-all.csv"])},
        "new_exact_cache": {"path": relative(paths["-new-exact-s5.cache"]),
                            "rows": len(delta), "sha256": sha256(paths["-new-exact-s5.cache"])},
        "unknown_keys": [list((int(row[9]), int(row[10]))) for row in raw_all if int(row[6]) == 0],
    }
    paths["-summary.json"].write_text(json.dumps(result_summary, indent=2, sort_keys=True) + "\n",
                                     encoding="utf-8", newline="\n")
    paths["-runner-summary.json"].write_text(json.dumps(runner_summary, indent=2, sort_keys=True) + "\n",
                                            encoding="utf-8", newline="\n")

    base_hist = Counter(value for value, _ in base.values())
    merged_hist = Counter(value for value, _ in merged.values())
    receipt = {
        "schema": "n11-dual-tight-probe-merge-receipt-v1",
        "base_cache": {"path": relative(args.base_cache), "sha256": sha256(args.base_cache),
                       "rows": len(base), "WIN": base_hist[1], "LOSS": base_hist[2]},
        "delta_cache": {"path": relative(paths["-new-exact-s5.cache"]),
                        "sha256": sha256(paths["-new-exact-s5.cache"]),
                        "rows": len(delta), "WIN": counts[1], "LOSS": counts[2]},
        "merged_cache": {"path": relative(paths["-merged-s5.cache"]),
                         "sha256": sha256(paths["-merged-s5.cache"]),
                         "rows": len(merged), "WIN": merged_hist[1], "LOSS": merged_hist[2]},
        "duplicate_verdicts": 0, "conflicts": 0,
        "unknown_rows_excluded_from_cache": counts[0],
    }
    paths["-merge-receipt.json"].write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n",
                                           encoding="utf-8", newline="\n")

    inputs = [args.scheduled_targets, args.schedule_manifest, args.run_dir / "summary.json",
              local_cache_path, args.base_cache, args.full_targets, args.ranking,
              args.solver, args.solver_source, args.runner, Path(__file__).resolve()]
    source_doc = {
        "schema": "n11-dual-tight-completed-probe-sources-v1",
        "claim": "All scheduled rows completed. Exact WIN/LOSS values are solver outputs; UNKNOWN rows are retained as raw evidence but excluded from caches.",
        "main_at_dispatch": "d538a68a85ece7d90b2b677e18447176acad9906",
        "class_key": list(class_key),
        "inputs": [{"path": relative(path), "sha256": sha256(path),
                    "bytes": path.stat().st_size} for path in inputs],
        "schedule_bound_sources": schedule.get("sources", []),
        "per_target": run_evidence,
        "outputs": [{"path": relative(path), "sha256": sha256(path),
                     "bytes": path.stat().st_size} for path in paths.values() if path.name != paths["-sources.json"].name]
                   + [{"path": relative(copied), "sha256": sha256(copied),
                       "bytes": copied.stat().st_size} for _, copied, _, _, _ in raw_copies],
        "probe_target_sha256": sha256(paths["-exact-targets.csv"]),
    }
    paths["-sources.json"].write_text(json.dumps(source_doc, indent=2, sort_keys=True) + "\n",
                                     encoding="utf-8", newline="\n")
    print(json.dumps({"class_key": class_key, "counts": dict(sorted(counts.items())),
                      "nodes": nodes_all, "merged_rows": len(merged),
                      "conflicts": 0, "class_status": result_summary["class_status_from_exact_witness"],
                      "outputs": {key: relative(value) for key, value in paths.items()}}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
