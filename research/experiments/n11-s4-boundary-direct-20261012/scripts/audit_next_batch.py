#!/usr/bin/env python3
"""Verify second-batch solver raws against the frozen selection and geometry."""
from __future__ import annotations

import csv
import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "research/experiments/n11-s4-boundary-direct-20261012"
SELECTION = EXP / "input/second-batch-selection.json"
RUN = EXP / "output/second-batch-run.json"
CURRENT = EXP / "output/current-exact-s5.cache"
WORKER = EXP / "output/second-batch-exact-s5.cache"


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def replay(path: Path):
    rows = []
    with path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.reader(f):
            if row and row[0] == "replay":
                rows.append(row)
    if len(rows) != 1 or len(rows[0]) != 11:
        raise ValueError(f"expected exactly one replay row in {path}")
    row = rows[0]
    sequence, stones, legal, is_or, budget, verdict, nodes, seconds, lo, hi = map(int, row[1:])
    return {"row_sequence": sequence, "stones": stones, "legal": legal, "is_or": is_or,
            "budget": budget, "verdict_code": verdict, "nodes": nodes,
            "seconds": seconds, "key": [lo, hi]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selection", type=Path, default=SELECTION)
    parser.add_argument("--run-manifest", type=Path, default=RUN)
    parser.add_argument("--worker-cache", type=Path, default=WORKER)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    selection_path = args.selection if args.selection.is_absolute() else ROOT / args.selection
    run_path = args.run_manifest if args.run_manifest.is_absolute() else ROOT / args.run_manifest
    worker_path = args.worker_cache if args.worker_cache.is_absolute() else ROOT / args.worker_cache
    selection = json.loads(selection_path.read_text(encoding="utf-8"))
    run = json.loads(run_path.read_text(encoding="utf-8"))
    if run.get("selection_sha256") != sha(selection_path):
        raise ValueError("second run manifest does not match frozen selection")
    build = json.loads((ROOT / selection["solver"]["frozen_build_manifest"]).read_text(encoding="utf-8"))
    binary = ROOT / build["binary_path"]
    if sha(binary) != selection["solver"]["binary_sha256"] or run.get("solver_binary_sha256") != sha(binary):
        raise ValueError("solver build provenance mismatch")
    sys.path.insert(0, str(ROOT / "research/experiments/n11-frontier-selection-20261005/scripts"))
    from s5_evidence_policy import quarantined_cache_keys
    sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
    from independent import Board
    board = Board(11)

    runs = {r["sequence"]: r for r in run["runs"]}
    selected = {r["sequence"]: r for r in selection["selected"]}
    if set(runs) != set(selected):
        raise ValueError(f"second batch incomplete/mismatched: runs={sorted(runs)} selected={sorted(selected)}")
    existing = set()
    with CURRENT.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.reader(f):
            if row and row[0] == "s5verdict":
                existing.add((int(row[1]), int(row[2])))
    exact = {}
    records = []
    for seq in sorted(selected):
        target, entry = selected[seq], runs[seq]
        key = tuple(target["key"])
        raw, log = ROOT / entry["raw_path"], ROOT / entry["log_path"]
        if not raw.is_file() or not log.is_file() or sha(raw) != entry["raw_sha256"] or sha(log) != entry["log_sha256"]:
            raise ValueError(f"raw/log hash mismatch for sequence {seq}")
        parsed = replay(raw)
        mask = key[0] | (key[1] << 64)
        if mask.bit_count() != 5 or board.canonical(mask) != mask:
            raise ValueError(f"noncanonical S5 key {key}")
        legal = board.legal(mask).bit_count()
        verdict = {0: "UNKNOWN", 1: "WIN", 2: "LOSS"}.get(parsed["verdict_code"])
        if (parsed["row_sequence"] != 0 or parsed["key"] != list(key) or parsed["stones"] != 5
                or parsed["is_or"] != 0 or parsed["budget"] != 15_000_000 or parsed["nodes"] > 15_000_000
                or parsed["legal"] != legal or legal != target["legal"] or verdict != entry["verdict"]
                or parsed["nodes"] != entry["nodes"] or key in existing or key in quarantined_cache_keys()):
            raise ValueError(f"raw/geometry/manifest/existing-cache mismatch at sequence {seq}: {parsed}")
        if verdict in ("WIN", "LOSS"):
            exact[key] = (parsed["verdict_code"], parsed["nodes"])
        records.append({
            "sequence": seq, "key": list(key), "sharing": target["sharing"],
            "live_parent_count": target["live_parent_count"], "legal": legal,
            "verdict": verdict, "nodes": parsed["nodes"], "elapsed_seconds": entry["elapsed_seconds"],
            "raw_path": entry["raw_path"], "raw_sha256": sha(raw),
            "log_path": entry["log_path"], "log_sha256": sha(log),
        })
    if any(r["verdict"] == "WIN" for r in records) and records[-1]["verdict"] != "WIN":
        raise ValueError("runner continued after S5 WIN")
    content = "# exact-only worker cache; UNKNOWN omitted; independently audited\n" + "".join(
        f"s5verdict,{lo},{hi},5,{v},{nodes}\n" for (lo, hi), (v, nodes) in sorted(exact.items()))
    worker_path.parent.mkdir(parents=True, exist_ok=True)
    if worker_path.exists() and worker_path.read_text(encoding="utf-8") != content:
        raise ValueError("second worker cache differs; refusing overwrite")
    if not worker_path.exists():
        worker_path.write_text(content, encoding="utf-8", newline="")
    batch_name = selection_path.name.replace("-selection.json", "")
    receipt = {
        "schema": f"n11-s4-direct-s5-{batch_name}-audit-v1",
        "selection_path": str(selection_path.relative_to(ROOT)),
        "selection_sha256": sha(selection_path), "run_manifest_path": str(run_path.relative_to(ROOT)),
        "run_manifest_sha256": sha(run_path),
        "worker_cache_path": str(worker_path.relative_to(ROOT)), "worker_cache_sha256": sha(worker_path),
        "exact_verdict_counts": {"WIN": sum(v == 1 for v, _ in exact.values()), "LOSS": sum(v == 2 for v, _ in exact.values())},
        "unknown_count": sum(r["verdict"] == "UNKNOWN" for r in records),
        "total_nodes": sum(r["nodes"] for r in records),
        "total_elapsed_seconds": sum(r["elapsed_seconds"] for r in records),
        "independent_geometry_check": "Board(11) canonicality and legal count; fixed S5 AND polarity verified from raw is_or=0",
        "trust": "solver-trusted exact outcomes, not terminal-only independent proofs",
        "results": records,
    }
    path = args.receipt if args.receipt and args.receipt.is_absolute() else (
        ROOT / args.receipt if args.receipt else EXP / f"output/{batch_name}-audit.json")
    encoded = (json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    if path.exists() and path.read_bytes() != encoded:
        raise ValueError("second batch audit receipt differs; refusing overwrite")
    if not path.exists():
        path.write_bytes(encoded)
    print(json.dumps({k: v for k, v in receipt.items() if k != "results"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
