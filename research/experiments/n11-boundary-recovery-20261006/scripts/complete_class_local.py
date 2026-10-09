#!/usr/bin/env python3
"""Complete a supplied subset of an s5 class with bounded local workers.

The target file is an exact-replay input (11 columns). Existing exact cache
entries and saved per-root replay outputs are reused. UNKNOWN results remain
unresolved for a later boundary handoff and are never retried by this runner.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import subprocess
import sys
import time
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
FRONTIER_SCRIPTS = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts"
sys.path.insert(0, str(FRONTIER_SCRIPTS))
from derive_shared_s6_witness_cache import canonical_safe_key  # noqa: E402
from s5_evidence_policy import quarantined_cache_keys


def fail(message: str) -> None:
    raise SystemExit(message)


def read_targets(path: Path) -> dict[tuple[int, int], list[str]]:
    targets: dict[tuple[int, int], list[str]] = {}
    with path.open(newline="", encoding="utf-8") as stream:
        for line_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].startswith("#"):
                continue
            if len(row) != 11:
                fail(f"target row must have 11 columns: {path}:{line_no}: {row}")
            try:
                stones, lo, hi, legal, is_or = (
                    int(row[2]), int(row[3]), int(row[4]), int(row[5]), int(row[7])
                )
            except ValueError:
                fail(f"target row has non-integer fields: {path}:{line_no}: {row}")
            if stones != 5 or is_or != 0:
                fail(f"target is not an s5 AND row: {path}:{line_no}: {row}")
            key = (lo, hi)
            if canonical_safe_key(key, 5) != key:
                fail(f"target key is noncanonical: {path}:{line_no}: {key}")
            if legal < 0:
                fail(f"negative legal count: {path}:{line_no}: {legal}")
            if key in targets:
                fail(f"duplicate target key at {path}:{line_no}: {key}")
            targets[key] = row
    if not targets:
        fail(f"no targets in {path}")
    return targets


def read_caches(paths: list[Path]) -> tuple[dict[tuple[int, int], int], dict[tuple[int, int], int], list[dict]]:
    verdicts: dict[tuple[int, int], int] = {}
    nodes_by_key: dict[tuple[int, int], int] = {}
    receipts = []
    origins: dict[tuple[int, int], Path] = {}
    quarantine = quarantined_cache_keys()
    for path in paths:
        rows = wins = losses = nodes_total = 0
        with path.open(newline="", encoding="utf-8") as stream:
            for line_no, row in enumerate(csv.reader(stream), 1):
                if not row or row[0].startswith("#"):
                    continue
                if len(row) != 6 or row[0] != "s5verdict":
                    fail(f"not an s5 cache row: {path}:{line_no}: {row}")
                try:
                    key = (int(row[1]), int(row[2]))
                    stones, value, nodes = int(row[3]), int(row[4]), int(row[5])
                except ValueError:
                    fail(f"cache row has non-integer fields: {path}:{line_no}: {row}")
                if stones != 5 or value not in (1, 2) or nodes < 0:
                    fail(f"not exact safe s5 cache evidence: {path}:{line_no}: {row}")
                if canonical_safe_key(key, 5) != key:
                    fail(f"noncanonical s5 cache key: {path}:{line_no}: {key}")
                if key in quarantine:
                    continue
                old = verdicts.get(key)
                if old is not None and old != value:
                    fail(f"CONFLICT {key}: {old} from {origins[key]} vs {value} from {path}")
                verdicts[key] = value
                origins.setdefault(key, path)
                nodes_by_key[key] = max(nodes_by_key.get(key, 0), nodes)
                rows += 1
                wins += value == 1
                losses += value == 2
                nodes_total += nodes
        receipts.append({"path": str(path), "rows": rows, "win": wins, "loss": losses,
                         "nodes": nodes_total, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    return verdicts, nodes_by_key, receipts


def parse_saved_output(path: Path, key: tuple[int, int]) -> tuple[int, int] | None:
    """Validate and return (verdict, nodes), including UNKNOWN without retry."""
    result = None
    seen = False
    with path.open(newline="", encoding="utf-8") as stream:
        for line_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].startswith("#"):
                continue
            if row[0] == "replay_error":
                fail(f"saved solver output contains replay_error: {path}:{line_no}: {row}")
            if row[0] != "replay":
                fail(f"unexpected saved solver output row: {path}:{line_no}: {row}")
            if len(row) != 11:
                fail(f"bad saved replay row: {path}:{line_no}: {row}")
            try:
                stones, is_or, verdict, nodes = int(row[2]), int(row[4]), int(row[6]), int(row[7])
                row_key = (int(row[9]), int(row[10]))
            except ValueError:
                fail(f"saved replay row has non-integer fields: {path}:{line_no}: {row}")
            if stones != 5 or is_or != 0 or row_key != key or verdict not in (0, 1, 2) or nodes < 0:
                fail(f"saved replay row does not match target: {path}:{line_no}: {row}")
            if canonical_safe_key(row_key, 5) != row_key:
                fail(f"saved replay key is noncanonical/unsafe: {path}:{line_no}: {row_key}")
            if seen:
                fail(f"multiple replay rows in per-root output: {path}")
            seen, result = True, (verdict, nodes)
    if not seen:
        fail(f"saved solver output has no replay row: {path}")
    return result


def paths_for(key: tuple[int, int], out_dir: Path) -> tuple[Path, Path, Path]:
    stem = f"s5-{key[0]}-{key[1]}"
    return out_dir / f"{stem}.input.csv", out_dir / f"{stem}.out.csv", out_dir / f"{stem}.log"


def run_root(key: tuple[int, int], row: list[str], solver: Path, out_dir: Path,
             budget: int) -> dict:
    input_path, output_path, log_path = paths_for(key, out_dir)
    # Exact replay consumes stones/lo/hi; preserve the supplied provenance row.
    with input_path.open("w", newline="", encoding="utf-8") as stream:
        csv.writer(stream, lineterminator="\n").writerow(row)
    tmp_output = output_path.with_suffix(output_path.suffix + ".tmp")
    prefix = [sys.executable, str(solver)] if solver.suffix.lower() == ".py" else [str(solver)]
    command = prefix + ["--n=11", "--memo=22", f"--exact-replay={input_path}",
               "--only=5", "--exact-order=count", f"--exact-replay-budget={budget}",
               f"--csv={tmp_output}"]
    started = time.monotonic()
    with log_path.open("w", encoding="utf-8") as log:
        proc = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=False)
    elapsed = time.monotonic() - started
    if proc.returncode != 0:
        fail(f"solver exited {proc.returncode} for {key}; see {log_path}")
    if not tmp_output.exists():
        fail(f"solver did not create output for {key}; see {log_path}")
    parsed = parse_saved_output(tmp_output, key)
    os.replace(tmp_output, output_path)
    verdict, nodes = parsed
    return {"key": key, "verdict": verdict, "nodes": nodes, "elapsed_seconds": elapsed,
            "output": str(output_path), "log": str(log_path)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--targets", type=Path, required=True)
    parser.add_argument("--cache", type=Path, action="append", default=[])
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--budget", type=int, default=15_000_000)
    args = parser.parse_args()
    if args.workers < 1 or args.budget < 1:
        fail("--workers and --budget must be positive")
    if not args.solver.is_file():
        fail(f"solver does not exist: {args.solver}")

    targets = read_targets(args.targets)
    cache, cache_nodes, cache_receipts = read_caches(args.cache)
    target_keys = set(targets)

    verdicts: dict[tuple[int, int], int] = {}
    node_counts: dict[tuple[int, int], int] = {}
    source_by_key: dict[tuple[int, int], str] = {}
    for key in target_keys & cache.keys():
        verdicts[key] = cache[key]
        node_counts[key] = cache_nodes.get(key, 0)
        source_by_key[key] = "cache"

    # Existing per-root output takes precedence only when consistent with cache.
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for key in sorted(target_keys):
        _, output_path, _ = paths_for(key, args.out_dir)
        if not output_path.exists():
            continue
        saved, nodes = parse_saved_output(output_path, key)
        if key in verdicts and saved in (1, 2) and verdicts[key] != saved:
            fail(f"CONFLICT {key}: cache={verdicts[key]} vs saved output={saved}")
        if key not in verdicts and saved in (1, 2):
            verdicts[key] = saved
            node_counts[key] = nodes
            source_by_key[key] = "saved_output"
        elif key not in verdicts and saved == 0:
            verdicts[key] = 0
            node_counts[key] = nodes
            source_by_key[key] = "saved_unknown"
        elif key in verdicts and saved == 0:
            node_counts[key] = max(node_counts.get(key, 0), nodes)

    initial_cache_win = any(cache.get(key) == 1 for key in target_keys)
    # Preserve the materializer's low-legal-first schedule, rather than
    # accidentally replacing its cost order with numeric bitset order.
    work = [key for key in targets if key not in verdicts]
    # A saved UNKNOWN is a terminal handoff state; it is in verdicts and is not retried.
    scheduled = 0
    newly_exact: dict[tuple[int, int], int] = {}
    newly_nodes: dict[tuple[int, int], int] = {}
    active = {}
    cursor = 0
    stop_dispatch = initial_cache_win or any(verdicts.get(key) == 1 for key in target_keys)

    def record_completed(info: dict) -> None:
        key, result = info["key"], info["verdict"]
        verdicts[key] = result
        node_counts[key] = info["nodes"]
        source_by_key[key] = "new_run"
        if result in (1, 2):
            newly_exact[key] = result
            newly_nodes[key] = info["nodes"]
        print(json.dumps({"completed": list(key), "verdict": result, "nodes": info["nodes"],
                          "elapsed_seconds": round(info["elapsed_seconds"], 3)}, sort_keys=True), flush=True)

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        while not stop_dispatch or active:
            while not stop_dispatch and len(active) < args.workers and cursor < len(work):
                key = work[cursor]
                cursor += 1
                future = executor.submit(run_root, key, targets[key], args.solver, args.out_dir, args.budget)
                active[future] = key
                scheduled += 1
            if not active:
                break
            done, _ = wait(active, return_when=FIRST_COMPLETED)
            for future in done:
                key = active.pop(future)
                info = future.result()
                record_completed(info)
                if info["verdict"] == 1:
                    stop_dispatch = True
            # If one future reports WIN, no additional roots are submitted;
            # all already-running futures are still drained and preserved.

    unresolved = [key for key in sorted(target_keys) if verdicts.get(key) in (None, 0)]
    exact = {key: value for key, value in verdicts.items() if value in (1, 2)}
    class_status = "WIN" if any(v == 1 for v in verdicts.values()) else (
        "LOSS" if len(exact) == len(targets) and all(v == 2 for v in exact.values()) else "UNKNOWN"
    )
    not_dispatched = [key for key in work[cursor:] if key not in verdicts]
    cache_out_dir = args.out_dir / "cache-out"
    cache_out_dir.mkdir(parents=True, exist_ok=True)
    new_cache = cache_out_dir / "new-exact-s5.cache"
    new_cache.write_text(
        "# s5 verdict cache: n=11 schema=1 (new exact verdicts from this run)\n" +
        "".join(f"s5verdict,{lo},{hi},5,{verdict},{newly_nodes[(lo, hi)]}\n"
                for (lo, hi), verdict in sorted(newly_exact.items())),
        encoding="utf-8",
    )
    summary = {
        "boundary_scope": "supplied targets only",
        "class_status": class_status,
        "targets": len(targets),
        "existing_exact": sum(v in (1, 2) for k, v in verdicts.items() if source_by_key.get(k) != "new_run"),
        "existing_cache_exact": sum(k in cache and cache[k] in (1, 2) for k in target_keys),
        "existing_output_exact": sum(source_by_key.get(k) == "saved_output" for k in target_keys),
        "new_exact": len(newly_exact),
        "new_win": sum(v == 1 for v in newly_exact.values()),
        "new_loss": sum(v == 2 for v in newly_exact.values()),
        "unknown": sum(verdicts.get(k) == 0 for k in target_keys),
        "unresolved": [list(k) for k in unresolved],
        "scheduled": scheduled,
        "not_dispatched": [list(k) for k in not_dispatched],
        "workers": args.workers,
        "budget": args.budget,
        "nodes_existing": sum(node_counts.get(k, 0) for k in target_keys if source_by_key.get(k) != "new_run"),
        "nodes_new": sum(node_counts.get(k, 0) for k in target_keys if source_by_key.get(k) == "new_run"),
        "nodes_total": sum(node_counts.values()),
        "new_exact_cache": str(new_cache),
        "cache_sources": cache_receipts,
    }
    summary_path = args.out_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
