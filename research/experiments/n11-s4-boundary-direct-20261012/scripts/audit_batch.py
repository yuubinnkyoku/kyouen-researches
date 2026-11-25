#!/usr/bin/env python3
"""Audit first-batch raw outcomes, materialize exact-only worker cache, and reclassify all S4s."""
from __future__ import annotations

import csv
import gzip
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "research/experiments/n11-s4-boundary-direct-20261012"
SELECTION = EXP / "input/first-batch-selection.json"
RUN = EXP / "output/first-batch-run.json"
GEOMETRY = ROOT / "research/experiments/n11-strategy-redesign-20261010/output/geometry.json.gz"
BASELINE = EXP / "input/baseline-exact-s5.cache"
WORKER = EXP / "output/worker-exact-s5.cache"
CURRENT = EXP / "output/current-exact-s5.cache"
TARGET = (1297036692683752448, 0)


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_replay(path: Path):
    rows = []
    with path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.reader(f):
            if row and row[0] == "replay":
                if len(row) != 11:
                    raise ValueError(f"malformed replay row in {path}: {row}")
                rows.append(row)
    if len(rows) != 1:
        raise ValueError(f"expected one replay row in {path}, got {len(rows)}")
    row = rows[0]
    sequence, stones, legal, is_or, budget, verdict, nodes, seconds, lo, hi = map(int, row[1:])
    return {
        "solver_row_sequence": sequence, "stones": stones, "legal": legal, "is_or": is_or,
        "budget": budget, "verdict_code": verdict, "nodes": nodes,
        "reported_seconds": float(seconds), "key": (lo, hi),
    }


def load_cache(path: Path, quarantine: set[tuple[int, int]]):
    result = {}
    with path.open(encoding="utf-8-sig", newline="") as f:
        for lineno, row in enumerate(csv.reader(f), 1):
            if not row or row[0].strip().startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict":
                raise ValueError(f"invalid S5 cache row {path}:{lineno}: {row}")
            lo, hi, stones, verdict, nodes = map(int, row[1:])
            key = (lo, hi)
            if stones != 5 or verdict not in (1, 2) or nodes < 0:
                raise ValueError(f"invalid exact S5 cache value at {path}:{lineno}")
            if key in quarantine:
                raise ValueError(f"quarantined cache key in {path}: {key}")
            previous = result.get(key)
            if previous is not None and previous[0] != verdict:
                raise ValueError(f"cache conflict in {path} for {key}")
            result[key] = (verdict, nodes if previous is None else min(nodes, previous[1]))
    return result


def main() -> None:
    if not SELECTION.is_file() or not RUN.is_file():
        raise FileNotFoundError("run the frozen first batch before auditing")
    selection = json.loads(SELECTION.read_text(encoding="utf-8"))
    run = json.loads(RUN.read_text(encoding="utf-8"))
    if run.get("selection_sha256") != sha(SELECTION):
        raise ValueError("run manifest does not match frozen selection")
    build_manifest = json.loads((ROOT / selection["solver"]["frozen_build_manifest"]).read_text(encoding="utf-8"))
    binary = ROOT / build_manifest["binary_path"]
    if sha(binary) != selection["solver"]["binary_sha256"] or run.get("solver_binary_sha256") != sha(binary):
        raise ValueError("solver binary provenance mismatch")
    sys.path.insert(0, str(ROOT / "research/experiments/n11-frontier-selection-20261005/scripts"))
    from s5_evidence_policy import quarantined_cache_keys
    quarantine = quarantined_cache_keys()
    sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
    from independent import Board

    board = Board(11)
    base = load_cache(BASELINE, quarantine)
    if len(base) != 5785:
        raise ValueError(f"unexpected frozen baseline exact rows: {len(base)}")
    expected_by_sequence = {item["sequence"]: item for item in selection["selected"]}
    runs_by_sequence = {item["sequence"]: item for item in run["runs"]}
    if len(runs_by_sequence) != len(run["runs"]):
        raise ValueError("duplicate sequence in run manifest")
    if not runs_by_sequence:
        raise ValueError("no completed solver runs")
    if set(runs_by_sequence) != set(range(len(runs_by_sequence))):
        raise ValueError("batch runs must be a contiguous prefix; unexpected completion gap")

    outcomes = []
    exact = {}
    for sequence in sorted(runs_by_sequence):
        target = expected_by_sequence.get(sequence)
        record = runs_by_sequence[sequence]
        if target is None:
            raise ValueError(f"unexpected run sequence {sequence}")
        raw = ROOT / record["raw_path"]
        log = ROOT / record["log_path"]
        if not raw.is_file() or not log.is_file() or sha(raw) != record["raw_sha256"] or sha(log) != record["log_sha256"]:
            raise ValueError(f"raw/log missing or SHA-256 mismatch for sequence {sequence}")
        parsed = parse_replay(raw)
        key = tuple(target["key"])
        mask = key[0] | (key[1] << 64)
        if mask.bit_count() != 5 or board.canonical(mask) != mask:
            raise ValueError(f"noncanonical S5 selected key: {key}")
        legal = board.legal(mask).bit_count()
        verdict = {0: "UNKNOWN", 1: "WIN", 2: "LOSS"}.get(parsed["verdict_code"])
        if (parsed["solver_row_sequence"] != 0 or record["sequence"] != sequence
                or record.get("solver_row_sequence", 0) != parsed["solver_row_sequence"]
                or parsed["key"] != key or parsed["stones"] != 5
                or parsed["is_or"] != 0 or parsed["budget"] != 15_000_000
                or parsed["legal"] != legal or legal != target["legal"]
                or parsed["nodes"] > 15_000_000 or verdict is None
                or record["verdict"] != verdict or record["nodes"] != parsed["nodes"]):
            raise ValueError(f"independent raw/geometry/manifest mismatch for sequence {sequence}: {parsed}")
        if key in base:
            raise ValueError(f"selected S5 unexpectedly already exact in baseline: {key}")
        if verdict in ("WIN", "LOSS"):
            exact[key] = (parsed["verdict_code"], parsed["nodes"])
        outcomes.append({
            "sequence": sequence, "key": list(key), "sharing": target["sharing"],
            "live_parent_count": target["live_parent_count"], "legal": legal,
            "verdict": verdict, "nodes": parsed["nodes"],
            "elapsed_seconds": record["elapsed_seconds"], "raw_path": record["raw_path"],
            "raw_sha256": sha(raw), "log_path": record["log_path"], "log_sha256": sha(log),
        })
    wins = [r for r in outcomes if r["verdict"] == "WIN"]
    if len(wins) > 1 or (wins and wins[0]["sequence"] != max(r["sequence"] for r in outcomes)):
        raise ValueError("solver continued after an S5 WIN that should prove target S4 WIN")
    if wins and len(outcomes) != wins[0]["sequence"] + 1:
        raise ValueError("non-prefix run after S5 WIN")
    if not wins and len(outcomes) == 8 and run.get("stop_reason") != "all eight frozen targets completed without an S5 WIN":
        raise ValueError("completed batch stop reason is inconsistent")

    rows = ["# exact-only worker cache; UNKNOWN omitted; raw/manifest audited by audit_batch.py\n"]
    for (lo, hi), (verdict, nodes) in sorted(exact.items()):
        rows.append(f"s5verdict,{lo},{hi},5,{verdict},{nodes}\n")
    worker_text = "".join(rows)
    if WORKER.exists() and WORKER.read_text(encoding="utf-8") != worker_text:
        raise ValueError("existing worker exact cache differs; refusing overwrite")
    WORKER.parent.mkdir(parents=True, exist_ok=True)
    if not WORKER.exists():
        WORKER.write_text(worker_text, encoding="utf-8", newline="")
    worker = load_cache(WORKER, quarantine)
    if worker != exact:
        raise ValueError("worker exact cache failed read-back check")

    with gzip.open(GEOMETRY, "rt", encoding="utf-8") as f:
        geometry = json.load(f)
    if len(geometry) != 3384:
        raise ValueError(f"geometry classes changed: {len(geometry)}")
    frontier = {
        "schema": "n11-s4-direct-s5-frontier-after-batch-v1",
        "source_main_commit": selection["source_main_commit"],
        "selection_sha256": sha(SELECTION), "run_manifest_sha256": sha(RUN),
        "solver_binary_sha256": sha(binary), "solver_source_sha256": selection["solver"]["source_sha256"],
        "independent_geometry_sha256": sha(GEOMETRY),
        "raw_inventory": outcomes,
    }
    if CURRENT.exists():
        cache = load_cache(CURRENT, quarantine)
        expected = dict(base)
        for key, val in exact.items():
            prior = expected.get(key)
            if prior is not None and prior[0] != val[0]:
                raise ValueError(f"merged cache conflicts with frozen baseline: {key}")
            expected[key] = val if prior is None else (val[0], min(prior[1], val[1]))
        if cache != expected:
            raise ValueError("current merged cache does not equal baseline union exact batch")
        class_counts = Counter()
        coverage_union = set()
        secured = set()
        classes = {}
        target_children = set()
        for item in geometry:
            parent = tuple(item["key"])
            mask = parent[0] | (parent[1] << 64)
            generated = {(k & ((1 << 64) - 1), k >> 64) for k in board.children(mask)}
            stored = {tuple(k) for k in item["children"]}
            if generated != stored or len(stored) != len(item["children"]):
                raise ValueError(f"independent S4 boundary mismatch: {parent}")
            vals = [cache.get(child, (0, 0))[0] for child in generated]
            status = "WIN" if 1 in vals else ("LOSS" if vals and all(v == 2 for v in vals) else "UNKNOWN")
            cov = set(item["coverage"])
            if status == "LOSS":
                secured.update(cov)
            class_counts[status] += 1
            coverage_union.update(cov)
            classes[parent] = {"status": status, "coverage": cov, "children": generated}
            if parent == TARGET:
                target_children = generated
        if len(classes) != 3384 or len(coverage_union) != 119:
            raise ValueError("full S4 classification/third-move coverage mismatch")
        target_counts = Counter(cache.get(k, (0, 0))[0] for k in target_children)
        live = [k for k, row in classes.items() if row["status"] == "UNKNOWN"]
        remaining = sorted(coverage_union - secured)
        frontier.update({
            "exact_cache_rows": len(cache),
            "cache_verdict_counts": {"WIN": sum(v[0] == 1 for v in cache.values()), "LOSS": sum(v[0] == 2 for v in cache.values())},
            "all_s4_class_status_counts": dict(sorted(class_counts.items())),
            "all_s4_class_count": len(classes), "third_move_count": len(coverage_union),
            "secured_third_moves": len(secured), "secured_third_move_ids": sorted(secured),
            "remaining_third_move_ids": remaining,
            "target_s4_children": len(target_children),
            "target_s4_child_counts": {"LOSS": target_counts[2], "WIN": target_counts[1], "UNKNOWN": target_counts[0]},
            "target_s4_status": classes[TARGET]["status"],
            "unknown_class_count": len(live),
        })
        write_json(EXP / "output/frontier-after-batch.json", frontier)
    else:
        frontier["merge_pending"] = "Use the tested dfpn_s5_merge.sh to atomically union baseline and exact worker cache into current-exact-s5.cache, then rerun this audit."
        write_json(EXP / "output/raw-audit-before-merge.json", frontier)

    receipt = {
        "schema": "n11-s4-direct-s5-first-batch-audit-v1",
        "selection_sha256": sha(SELECTION), "run_manifest_sha256": sha(RUN),
        "worker_cache_path": str(WORKER.relative_to(ROOT)), "worker_cache_sha256": sha(WORKER),
        "exact_worker_verdict_counts": {"WIN": sum(v[0] == 1 for v in worker.values()), "LOSS": sum(v[0] == 2 for v in worker.values())},
        "unknown_raw_count": sum(r["verdict"] == "UNKNOWN" for r in outcomes),
        "total_nodes": sum(r["nodes"] for r in outcomes),
        "total_elapsed_seconds": sum(r["elapsed_seconds"] for r in outcomes),
        "cold_process_per_root": True,
        "solver_outcomes_are": "solver-trusted exact; geometry independently audited; not terminal-only independent minimax proofs",
        "results": outcomes,
        "frontier_path": str((EXP / ("output/frontier-after-batch.json" if CURRENT.exists() else "output/raw-audit-before-merge.json")).relative_to(ROOT)),
    }
    write_json(EXP / "output/audit-receipt.json", receipt)
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
