#!/usr/bin/env python3
"""Run the frozen first S5 batch, one cold solver process per root."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "research/experiments/n11-s4-boundary-direct-20261012"
SELECTION = EXP / "input/first-batch-selection.json"
RUN = EXP / "output/first-batch-run.json"


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def replay_row(path: Path):
    rows = []
    with path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.reader(f):
            if row and row[0] == "replay":
                rows.append(row)
    return rows


def parse_target_output(raw_path: Path, target: dict):
    rows = replay_row(raw_path)
    if len(rows) != 1 or len(rows[0]) != 11:
        raise ValueError(f"solver did not produce exactly one replay row: {raw_path}")
    row = rows[0]
    parsed = {
        "solver_row_sequence": int(row[1]), "stones": int(row[2]), "legal": int(row[3]),
        "is_or": int(row[4]), "budget": int(row[5]), "verdict_code": int(row[6]),
        "nodes": int(row[7]), "reported_seconds": float(row[8]),
        "key": [int(row[9]), int(row[10])],
    }
    expected_code = {0: "UNKNOWN", 1: "WIN", 2: "LOSS"}.get(parsed["verdict_code"])
    if (parsed["solver_row_sequence"] != 0 or parsed["key"] != target["key"]
            or parsed["stones"] != 5 or parsed["is_or"] != 0
            or parsed["legal"] != target["legal"] or parsed["budget"] != 15_000_000
            or parsed["nodes"] > 15_000_000 or expected_code is None):
        raise ValueError(f"solver raw disagrees with frozen target: {parsed}")
    return parsed, expected_code


def write_manifest(run_path: Path, value):
    run_path.parent.mkdir(parents=True, exist_ok=True)
    temp = run_path.with_suffix(".json.tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temp.replace(run_path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selection", type=Path, default=SELECTION,
                        help="frozen selection JSON (defaults to the first batch)")
    parser.add_argument("--run-manifest", type=Path,
                        help="run receipt JSON; defaults in the selection's experiment output directory")
    args = parser.parse_args()
    selection_path = args.selection if args.selection.is_absolute() else ROOT / args.selection
    run_path = (args.run_manifest if args.run_manifest and args.run_manifest.is_absolute()
                else ROOT / args.run_manifest if args.run_manifest
                else selection_path.parent.parent / "output" / selection_path.name.replace("-selection.json", "-run.json"))
    exp = selection_path.parent.parent
    if not selection_path.is_file():
        raise FileNotFoundError("run prepare_batch.py first; selection must be frozen before exploration")
    selection = json.loads(selection_path.read_text(encoding="utf-8"))
    binary = ROOT / json.loads((ROOT / selection["solver"]["frozen_build_manifest"]).read_text(encoding="utf-8"))["binary_path"]
    if sha(binary) != selection["solver"]["binary_sha256"]:
        raise ValueError("solver binary changed after selection was frozen")
    raw_dir, log_dir = exp / "output/raw", exp / "output/log"
    raw_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)
    state = {
        "schema": "n11-s4-direct-s5-batch-run-v1",
        "selection_sha256": sha(selection_path), "solver_binary_sha256": sha(binary),
        "node_limit": 15_000_000, "cold_process_per_root": True,
        "stop_reason": None, "runs": [],
    }
    if run_path.exists():
        state = json.loads(run_path.read_text(encoding="utf-8"))
        if state["selection_sha256"] != sha(selection_path) or state["solver_binary_sha256"] != sha(binary):
            raise ValueError("existing run manifest does not match frozen inputs/binary")

    for target in selection["selected"]:
        sequence = target["sequence"]
        raw_path = raw_dir / f"s5-{sequence:02}.csv"
        log_path = log_dir / f"s5-{sequence:02}.log"
        already = next((r for r in state["runs"] if r["sequence"] == sequence), None)
        if already:
            if not raw_path.is_file() or sha(raw_path) != already["raw_sha256"]:
                raise ValueError(f"run manifest/raw mismatch; refusing rerun for target {sequence}")
            rows = replay_row(raw_path)
            if len(rows) != 1:
                raise ValueError(f"existing raw is incomplete; refusing same-setting rerun: {raw_path}")
            print(f"skip verified prior completion s5-{sequence:02}: {already['verdict']}", flush=True)
            if already["verdict"] == 1:
                state["stop_reason"] = f"S5 WIN at sequence {sequence} makes target S4 WIN"
                break
            continue
        if raw_path.exists() or log_path.exists():
            if not raw_path.is_file() or not log_path.is_file():
                raise FileExistsError(f"unmanifested partial solver output exists; inspect, do not overwrite: {raw_path}")
            parsed, expected_code = parse_target_output(raw_path, target)
            adopted = {
                **parsed, "sequence": sequence, "verdict": expected_code,
                "elapsed_seconds": parsed["reported_seconds"], "adopted_completed_output": True,
                "raw_path": str(raw_path.relative_to(ROOT)), "raw_sha256": sha(raw_path),
                "log_path": str(log_path.relative_to(ROOT)), "log_sha256": sha(log_path),
                "command": [binary.name, "--n=11", "--memo=22", "--only=5", "--exact-order=count",
                            f"--exact-replay={ROOT / target['input_path']}", "--exact-replay-budget=15000000",
                            f"--csv={raw_path}", f"--log={log_path}"],
            }
            state["runs"].append(adopted)
            state["runs"].sort(key=lambda r: r["sequence"])
            if expected_code == "WIN":
                state["stop_reason"] = f"S5 WIN at sequence {sequence} makes target S4 WIN"
            write_manifest(run_path, state)
            print(json.dumps({"adopted_completed_raw": adopted}, ensure_ascii=False), flush=True)
            if expected_code == "WIN":
                break
            continue

        source_input = ROOT / target["input_path"]
        if sha(source_input) != target["input_sha256"]:
            raise ValueError(f"frozen target input hash mismatch: {source_input}")
        command = [
            str(binary), "--n=11", "--memo=22", "--only=5", "--exact-order=count",
            f"--exact-replay={source_input}", "--exact-replay-budget=15000000",
            f"--csv={raw_path}", f"--log={log_path}",
        ]
        start = time.perf_counter()
        result = subprocess.run(command, cwd=ROOT, check=False)
        elapsed = time.perf_counter() - start
        if result.returncode != 0:
            raise RuntimeError(f"solver returned {result.returncode} for sequence {sequence}; preserve raw/log and inspect")
        parsed, expected_code = parse_target_output(raw_path, target)
        record = {
            **parsed, "sequence": sequence, "verdict": expected_code, "elapsed_seconds": elapsed,
            "raw_path": str(raw_path.relative_to(ROOT)), "raw_sha256": sha(raw_path),
            "log_path": str(log_path.relative_to(ROOT)), "log_sha256": sha(log_path),
            "command": [Path(command[0]).name, *command[1:]],
        }
        state["runs"].append(record)
        state["runs"].sort(key=lambda r: r["sequence"])
        if expected_code == "WIN":
            state["stop_reason"] = f"S5 WIN at sequence {sequence} makes target S4 WIN"
        write_manifest(run_path, state)
        print(json.dumps(record, ensure_ascii=False), flush=True)
        if expected_code == "WIN":
            break
    else:
        state["stop_reason"] = f"all {len(selection['selected'])} frozen targets completed without an S5 WIN"
    if not state["stop_reason"]:
        state["stop_reason"] = "batch interrupted after the last completed target; resume only from manifest"
    write_manifest(run_path, state)
    print(json.dumps({"completed": len(state["runs"]), "stop_reason": state["stop_reason"], "manifest": str(run_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
