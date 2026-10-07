#!/usr/bin/env python3
"""Collect per-root exact s5 probe rows into durable, hash-bound artifacts."""
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


def points(key: tuple[int, int]) -> tuple[int, ...]:
    lo, hi = key
    return tuple([i for i in range(64) if lo >> i & 1]
                 + [64 + i for i in range(57) if hi >> i & 1])


def safe_canonical(key: tuple[int, int], stones: int) -> bool:
    pts = points(key)
    return len(pts) == stones and not has_forbidden_quad(pts) \
        and tuple(d4_canonical_key(pts)) == key


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--targets", type=Path, required=True)
    ap.add_argument("--run-dir", type=Path, required=True)
    ap.add_argument("--sources", type=Path, required=True)
    ap.add_argument("--raw-out", type=Path, required=True)
    ap.add_argument("--exact-cache-out", type=Path, required=True)
    ap.add_argument("--summary-out", type=Path, required=True)
    ap.add_argument("--runner-summary-out", type=Path, required=True)
    args = ap.parse_args()
    for path in (args.raw_out, args.exact_cache_out, args.summary_out, args.runner_summary_out):
        if path.exists():
            raise SystemExit(f"refusing to overwrite existing collected output: {path}")

    targets = []
    for line_no, row in enumerate(csv.reader(args.targets.open(newline="", encoding="utf-8-sig")), 1):
        if not row or row[0].lstrip().startswith("#"):
            continue
        if len(row) != 11 or int(row[2]) != 5 or int(row[7]) != 0:
            raise SystemExit(f"invalid s5 probe target {line_no}: {row}")
        key = (int(row[3]), int(row[4]))
        if not safe_canonical(key, 5) or int(row[5]) != len(legal_after(set(points(key)))):
            raise SystemExit(f"unsafe/noncanonical target or wrong legal count: {key}")
        targets.append((key, row))
    if not targets or len({key for key, _ in targets}) != len(targets):
        raise SystemExit("probe target list is empty or has duplicate keys")

    raw_rows = []
    raw_sources = []
    verdicts = {}
    nodes = 0
    for key, target in targets:
        raw_path = args.run_dir / f"s5-{key[0]}-{key[1]}.out.csv"
        if not raw_path.is_file():
            raise SystemExit(f"probe target was not completed: {key}")
        rows = [row for row in csv.reader(raw_path.open(newline="", encoding="utf-8-sig"))
                if row and not row[0].lstrip().startswith("#")]
        if len(rows) != 1:
            raise SystemExit(f"expected exactly one replay row for {key}: {raw_path}")
        row = rows[0]
        if len(row) != 11 or row[0] != "replay":
            raise SystemExit(f"invalid replay output: {raw_path}: {row}")
        replay_key = (int(row[9]), int(row[10]))
        verdict, paid_nodes = int(row[6]), int(row[7])
        if (replay_key != key or int(row[2]) != 5 or int(row[3]) != int(target[5])
                or int(row[4]) != 0 or int(row[5]) != 15_000_000
                or verdict not in (1, 2) or paid_nodes < 0
                or not safe_canonical(replay_key, 5)):
            raise SystemExit(f"replay row does not match exact probe target: {raw_path}: {row}")
        verdicts[key] = verdict
        nodes += paid_nodes
        raw_rows.append(row)
        raw_sources.append({"path": relative(raw_path), "sha256": sha256(raw_path),
                            "bytes": raw_path.stat().st_size, "key": list(key),
                            "verdict": verdict, "nodes": paid_nodes})

    runner_summary_path = args.run_dir / "summary.json"
    runner_summary = json.loads(runner_summary_path.read_text(encoding="utf-8"))
    if (runner_summary.get("targets") != len(targets)
            or runner_summary.get("new_exact") != len(targets)
            or runner_summary.get("new_win") != sum(v == 1 for v in verdicts.values())
            or runner_summary.get("new_loss") != sum(v == 2 for v in verdicts.values())
            or runner_summary.get("nodes_new") != nodes):
        raise SystemExit("per-root exact replay rows disagree with local runner summary")
    local_cache = Path(runner_summary["new_exact_cache"])
    if not local_cache.is_absolute():
        local_cache = ROOT / local_cache
    cached = {}
    for row in csv.reader(local_cache.open(newline="", encoding="utf-8-sig")):
        if not row or row[0].lstrip().startswith("#"):
            continue
        key, value = (int(row[1]), int(row[2])), int(row[4])
        if len(row) != 6 or row[0] != "s5verdict" or int(row[3]) != 5 \
                or not safe_canonical(key, 5) or key in cached:
            raise SystemExit(f"invalid/duplicate new exact cache row: {row}")
        cached[key] = value
    if cached != verdicts:
        raise SystemExit("new exact cache does not match the collected replay rows")

    args.raw_out.parent.mkdir(parents=True, exist_ok=True)
    with args.raw_out.open("w", newline="", encoding="utf-8") as stream:
        csv.writer(stream, lineterminator="\n").writerows(raw_rows)
    args.exact_cache_out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(local_cache, args.exact_cache_out)
    args.summary_out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(runner_summary_path, args.runner_summary_out)
    high_level = {
        "schema": "n11-dual-tight-class-probe-run-summary-v1",
        "target_count": len(targets),
        "exact_replay_counts": {"WIN": sum(v == 1 for v in verdicts.values()),
                                 "LOSS": sum(v == 2 for v in verdicts.values()), "UNKNOWN": 0},
        "nodes": nodes,
        "budget_per_target": runner_summary["budget"],
        "workers": runner_summary["workers"],
        "scheduled": runner_summary["scheduled"],
        "not_dispatched": runner_summary["not_dispatched"],
        "class_status_on_supplied_probe": runner_summary["class_status"],
        "scope": "The supplied low-legal-count probe only; the containing s4 class is WIN if any exact s5 child is WIN.",
        "runner_summary": {"path": relative(args.runner_summary_out),
                           "sha256": sha256(args.runner_summary_out)},
        "raw_output": {"path": relative(args.raw_out), "rows": len(raw_rows),
                       "sha256": sha256(args.raw_out)},
        "new_exact_cache": {"path": relative(args.exact_cache_out), "rows": len(cached),
                            "sha256": sha256(args.exact_cache_out)},
    }
    args.summary_out.write_text(json.dumps(high_level, indent=2, sort_keys=True) + "\n",
                                encoding="utf-8", newline="\n")

    source_doc = json.loads(args.sources.read_text(encoding="utf-8"))
    source_doc["execution_result"] = {
        "class_status_on_probe": runner_summary["class_status"],
        "exact_counts": dict(sorted(Counter(verdicts.values()).items())),
        "nodes": nodes,
        "scheduled": runner_summary["scheduled"],
        "not_dispatched": runner_summary["not_dispatched"],
        "raw_sources": raw_sources,
    }
    source_doc["outputs"] = [
        {"path": relative(args.raw_out), "sha256": sha256(args.raw_out), "rows": len(raw_rows)},
        {"path": relative(args.exact_cache_out), "sha256": sha256(args.exact_cache_out), "rows": len(cached)},
        {"path": relative(args.summary_out), "sha256": sha256(args.summary_out)},
        {"path": relative(args.runner_summary_out), "sha256": sha256(args.runner_summary_out)},
    ]
    source_doc["collector"] = {"path": relative(Path(__file__).resolve()),
                               "sha256": sha256(Path(__file__).resolve())}
    args.sources.write_text(json.dumps(source_doc, indent=2, sort_keys=True) + "\n",
                            encoding="utf-8", newline="\n")
    print(json.dumps({"rows": len(raw_rows), "counts": dict(Counter(verdicts.values())),
                      "nodes": nodes, "class_status": runner_summary["class_status"],
                      "raw_out": relative(args.raw_out),
                      "exact_cache": relative(args.exact_cache_out)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
