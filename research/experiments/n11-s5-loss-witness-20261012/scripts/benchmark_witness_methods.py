"""Run the preregistered same-binary S5/S6 witness-search comparison."""
from __future__ import annotations

import argparse
import csv
import ctypes
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def peak_rss(proc: subprocess.Popen) -> int | None:
    if os.name == "nt":
        class Counters(ctypes.Structure):
            _fields_ = [("cb", ctypes.c_ulong), ("faults", ctypes.c_ulong)] + [
                (name, ctypes.c_size_t) for name in
                ("peak_rss", "rss", "peak_pool_paged", "pool_paged",
                 "peak_pool_nonpaged", "pool_nonpaged", "pagefile", "peak_pagefile")]
        counters = Counters()
        counters.cb = ctypes.sizeof(counters)
        fn = ctypes.windll.psapi.GetProcessMemoryInfo
        fn.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong]
        if fn(int(proc._handle), ctypes.byref(counters), counters.cb):
            return int(counters.peak_rss)
    elif Path(f"/proc/{proc.pid}/status").exists():
        for line in Path(f"/proc/{proc.pid}/status").read_text().splitlines():
            if line.startswith("VmHWM:"):
                return int(line.split()[1]) * 1024
    return None


def write_replay(path: Path, rows: list[dict]) -> None:
    with path.open("x", encoding="utf-8", newline="") as stream:
        for i, row in enumerate(rows):
            stream.write(",".join(map(str, (f"candidate-{i}", i, row["stones"], row["lo"],
                                                    row["hi"], row["legal"], 0, 0, 0, 0, 0))) + "\n")


def read_rows(raw: Path, expected: list[dict], allowed_counts: set[int]) -> list[dict]:
    rows = []
    with raw.open(encoding="utf-8", newline="") as stream:
        for row in csv.reader(stream):
            if not row or row[0] != "replay":
                continue
            if len(row) != 11:
                raise ValueError(f"malformed replay row: {row}")
            i = int(row[1])
            if i >= len(expected):
                raise ValueError(f"unexpected replay sequence {i}")
            want = expected[i]
            actual = {"sequence": i, "stones": int(row[2]), "legal": int(row[3]),
                      "is_or": int(row[4]), "budget": int(row[5]), "verdict": int(row[6]),
                      "nodes": int(row[7]), "reported_seconds": int(row[8]),
                      "lo": int(row[9]), "hi": int(row[10]), "key": want["key"]}
            if (actual["stones"], actual["lo"], actual["hi"], actual["legal"]) != (
                    want["stones"], want["lo"], want["hi"], want["legal"]):
                raise ValueError(f"solver input/output mismatch: {actual} vs {want}")
            if actual["verdict"] not in (0, 1, 2) or actual["nodes"] > allowed_counts[i]:
                raise ValueError(f"invalid result or budget overrun: {actual}")
            rows.append(actual)
    if not rows or len(rows) > len(expected):
        raise ValueError(f"missing or extra result rows: {len(rows)}")
    if [r["sequence"] for r in rows] != list(range(len(rows))):
        raise ValueError("replay rows are not a contiguous prefix")
    if any(r["verdict"] == 2 for r in rows[:-1]):
        raise ValueError("solver continued after the first exact LOSS witness")
    return rows


def cache_stats(log: Path) -> dict:
    stats = {"exact_layer_hits": 0, "exact_layer_stores": 0, "exact_layer_size": 0}
    with log.open(encoding="utf-8") as stream:
        for line in stream:
            if not line.startswith("# residual_shadow "):
                continue
            for token in line.split():
                if "=" not in token:
                    continue
                name, value = token.split("=", 1)
                if name in stats:
                    stats[name] += int(value)
    return stats


def run_one(binary: Path, variant: dict, root_entry: dict, out_dir: Path,
            budget: dict) -> dict:
    out_dir.mkdir()
    target = root_entry["target"]
    if variant["name"] == "A":
        inputs = [{"key": str((target["hi"] << 64) | target["lo"]), "lo": target["lo"],
                   "hi": target["hi"], "stones": 5, "legal": target["legal"]}]
        row_budget = budget["per_s5_total_node_cap"]
        only = "5"
    else:
        source = (root_entry["key_order_screen"] if variant["name"] == "B"
                  else root_entry["legal_count_order_screen"])
        inputs = [{k: child[k] for k in ("key", "lo", "hi", "stones", "legal")} for child in source]
        row_budget = budget["s6_child_node_cap"]
        only = "6"

    replay = out_dir / "replay-input.csv"
    raw = out_dir / "solver-raw.csv"
    log = out_dir / "solver.log"
    write_replay(replay, inputs)
    command = [str(binary), "--n=11", "--memo=22", f"--exact-replay={replay}",
               f"--only={only}", "--exact-order=count", f"--exact-replay-budget={row_budget}",
               "--csv=" + str(raw)]
    if variant.get("stop_on_loss"):
        command.append("--exact-replay-stop-on-loss")
    if variant.get("share_tt"):
        command.append("--exact-replay-share-tt")
    if variant.get("share_layer"):
        command.append(f"--exact-share-layer={variant['share_layer']}")
    started = time.perf_counter()
    max_rss = 0
    with log.open("x", encoding="utf-8") as stream:
        proc = subprocess.Popen(command, stdout=stream, stderr=subprocess.STDOUT)
        while proc.poll() is None:
            max_rss = max(max_rss, peak_rss(proc) or 0)
            time.sleep(0.01)
        max_rss = max(max_rss, peak_rss(proc) or 0)
    wall = time.perf_counter() - started
    if proc.returncode != 0:
        raise RuntimeError(f"{variant['name']} failed for {target['id']} ({proc.returncode}); see {log}")
    per_row_budgets = {i: row_budget for i in range(len(inputs))}
    rows = read_rows(raw, inputs, per_row_budgets)
    if variant["name"] == "A" and len(rows) != 1:
        raise ValueError("direct S5 arm must return exactly one row")
    if variant["name"] != "A" and any(r["budget"] != row_budget for r in rows):
        raise ValueError("S6 row budget differs from preregistered per-child cap")
    nodes = sum(row["nodes"] for row in rows)
    total_cap = budget["per_s5_total_node_cap"]
    if nodes > total_cap:
        raise ValueError(f"aggregate per-S5 cap exceeded: {nodes} > {total_cap}")
    witness = next((row for row in rows if row["verdict"] == 2), None)
    return {
        "variant": variant["name"], "target_id": target["id"],
        "target_s5_key": str((target["hi"] << 64) | target["lo"]),
        "expected_s5_verdict": target["expected_verdict"],
        "root_budget_cap": total_cap, "per_row_budget": row_budget,
        "candidate_count": len(inputs), "tested_candidates": len(rows),
        "stop_reason": "exact_s6_loss_witness" if witness else "screened_prefix_exhausted",
        "solver_exact_s6_loss_witness_key": witness["key"] if witness else None,
        "rows": rows, "total_nodes": nodes, "wall_seconds": wall,
        "peak_rss_bytes": max_rss or None,
        "cache_mode": variant["cache_mode"],
        "exact_layer_stats": cache_stats(log),
        "commands": command,
        "input_sha256": sha256(replay), "raw_sha256": sha256(raw),
        "log_sha256": sha256(log),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--solver", type=Path, required=True)
    ap.add_argument("--schedule", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    binary, schedule_path, out = (p.resolve() for p in (args.solver, args.schedule, args.out))
    if out.exists():
        ap.error(f"refusing to overwrite {out}")
    if not binary.is_file() or not schedule_path.is_file():
        ap.error("solver and fixed schedule must exist")
    schedule = json.loads(schedule_path.read_text(encoding="utf-8"))
    if schedule["schema"] != "n11-s5-loss-witness-schedule-v1":
        ap.error("unsupported schedule schema")
    budget = schedule["budget_protocol"]
    variants = [
        {"name": "A", "cache_mode": "fresh TT per S5"},
        {"name": "B", "stop_on_loss": True, "cache_mode": "fresh TT per S6; key order"},
        {"name": "C", "stop_on_loss": True, "cache_mode": "fresh TT per S6; legal-count order"},
        {"name": "D", "stop_on_loss": True, "share_tt": True,
         "cache_mode": "shared TT among tested S6 roots of one S5"},
        {"name": "E", "stop_on_loss": True, "share_layer": 7,
         "cache_mode": "fresh TT per S6; share exact 7-stone verdicts"},
    ]
    out.mkdir(parents=True)
    results = []
    for variant in variants:
        variant_dir = out / variant["name"]
        variant_dir.mkdir()
        for root_entry in schedule["roots"]:
            results.append(run_one(binary, variant, root_entry,
                                   variant_dir / root_entry["target"]["id"].replace("/", "--"), budget))
    aggregates = []
    for variant in variants:
        rows = [r for r in results if r["variant"] == variant["name"]]
        direct_counts = {"WIN": 0, "LOSS": 0, "UNKNOWN": 0}
        if variant["name"] == "A":
            for result in rows:
                value = result["rows"][0]["verdict"]
                direct_counts[{1: "WIN", 2: "LOSS", 0: "UNKNOWN"}[value]] += 1
        aggregates.append({
            "variant": variant["name"], "description": variant["cache_mode"],
            "roots": len(rows),
            "direct_s5_verdict_counts": direct_counts if variant["name"] == "A" else None,
            "s6_loss_witnesses_found": sum(1 for r in rows if r["solver_exact_s6_loss_witness_key"] is not None),
            "s6_exact_win_rows": sum(1 for r in rows for q in r["rows"] if q["verdict"] == 1),
            "s6_unknown_rows": sum(1 for r in rows for q in r["rows"] if q["verdict"] == 0),
            "total_nodes": sum(r["total_nodes"] for r in rows),
            "total_wall_seconds": sum(r["wall_seconds"] for r in rows),
            "max_peak_rss_bytes": max((r["peak_rss_bytes"] or 0 for r in rows), default=0) or None,
            "per_root": [{"id": r["target_id"], "nodes": r["total_nodes"],
                          "wall_seconds": r["wall_seconds"], "peak_rss_bytes": r["peak_rss_bytes"],
                          "tested_candidates": r["tested_candidates"], "stop_reason": r["stop_reason"]}
                         for r in rows],
        })
    summary = {
        "schema": "n11-s5-loss-witness-benchmark-v1",
        "schedule_path": str(schedule_path.relative_to(ROOT)),
        "schedule_sha256": sha256(schedule_path),
        "target_file_sha256": sha256(ROOT / "research/experiments/n11-s5-loss-witness-20261012/input/targets.json"),
        "solver_source_path": "cpp/solvers/kyouen_dfpn_root.cpp",
        "solver_source_sha256": sha256(ROOT / "cpp/solvers/kyouen_dfpn_root.cpp"),
        "solver_binary_path": str(binary), "solver_binary_sha256": sha256(binary),
        "environment": {"platform": platform.platform(), "processor": platform.processor(),
                        "python": sys.version, "pid_processes_serial": True},
        "budget_protocol": budget,
        "initial_cache_state": "fresh process for each S5 and variant; no external S5 cache or imported solver result",
        "variants": aggregates,
        "per_root_runs": results,
        "trust_note": "solver exact rows are measurement outputs only; existing terminal-only certificates independently establish the six target S5 LOSS values; no solver result was imported as an independent proof",
    }
    summary_path = out / "summary.json"
    summary_path.write_text(json.dumps(summary, sort_keys=True, separators=(",", ":")) + "\n",
                            encoding="utf-8")
    files = []
    for path in sorted(p for p in out.rglob("*") if p.is_file()):
        files.append({"path": str(path.relative_to(out)), "bytes": path.stat().st_size,
                      "sha256": sha256(path)})
    (out / "artifact-manifest.json").write_text(
        json.dumps({"schema": "n11-s5-loss-witness-artifacts-v1", "files": files},
                   sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps(aggregates, sort_keys=True))


if __name__ == "__main__":
    main()
