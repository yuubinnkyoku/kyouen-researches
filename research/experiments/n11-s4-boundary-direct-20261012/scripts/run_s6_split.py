#!/usr/bin/env python3
"""Run a frozen direct S6 batch, one cold exact solver process per child."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def read_replay(path: Path, target: dict) -> tuple[dict, str]:
    rows = []
    with path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.reader(f):
            if row and row[0] == "replay":
                rows.append(row)
    if len(rows) != 1 or len(rows[0]) != 11:
        raise ValueError(f"expected one complete S6 replay row: {path}")
    row = rows[0]
    parsed = {
        "solver_row_sequence": int(row[1]), "stones": int(row[2]),
        "legal": int(row[3]), "is_or": int(row[4]), "budget": int(row[5]),
        "verdict_code": int(row[6]), "nodes": int(row[7]),
        "reported_seconds": float(row[8]), "key": [int(row[9]), int(row[10])],
    }
    verdict = {0: "UNKNOWN", 1: "WIN", 2: "LOSS"}.get(parsed["verdict_code"])
    if (parsed["solver_row_sequence"] != 0 or parsed["key"] != target["key"]
            or parsed["stones"] != 6 or parsed["is_or"] != 1
            or parsed["legal"] != target["legal"] or parsed["budget"] != target["budget"]
            or parsed["nodes"] < 0 or parsed["nodes"] > target["budget"] or verdict is None):
        raise ValueError(f"solver raw disagrees with frozen S6 child: {parsed}")
    return parsed, verdict


def write_manifest(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--selection", type=Path, required=True)
    ap.add_argument("--run-manifest", type=Path)
    args = ap.parse_args()
    selection_path = resolve(args.selection)
    if not selection_path.is_file():
        raise FileNotFoundError(selection_path)
    selection = json.loads(selection_path.read_text(encoding="utf-8"))
    exp = selection_path.parent.parent
    run_path = resolve(args.run_manifest) if args.run_manifest else exp / "output" / selection_path.name.replace("-selection.json", "-run.json")
    build_path = resolve(Path(selection["solver"]["frozen_build_manifest"]))
    build = json.loads(build_path.read_text(encoding="utf-8"))
    binary = resolve(Path(build["binary_path"]))
    if sha(binary) != selection["solver"]["binary_sha256"] or build["binary_sha256"] != sha(binary):
        raise ValueError("pinned solver binary hash mismatch")
    raw_dir, log_dir = exp / "output/raw", exp / "output/log"
    raw_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)
    state = {
        "schema": "n11-s4-final-s5-s6-split-run-v1",
        "selection_sha256": sha(selection_path), "solver_binary_sha256": sha(binary),
        "budget": selection["solver"]["budget"], "cold_process_per_child": True,
        "stop_reason": None, "runs": [],
    }
    if run_path.exists():
        state = json.loads(run_path.read_text(encoding="utf-8"))
        if state["selection_sha256"] != sha(selection_path) or state["solver_binary_sha256"] != sha(binary):
            raise ValueError("existing run manifest does not match frozen selection/binary")

    selected = sorted(selection["selected"], key=lambda r: r["sequence"])
    for target in selected:
        seq = target["sequence"]
        raw_path, log_path = raw_dir / f"s6-{seq:03}.csv", log_dir / f"s6-{seq:03}.log"
        prior = next((r for r in state["runs"] if r["sequence"] == seq), None)
        if prior:
            if not raw_path.is_file() or sha(raw_path) != prior["raw_sha256"]:
                raise ValueError(f"manifest/raw mismatch; refusing to rerun sequence {seq}")
            _, verdict = read_replay(raw_path, target)
            if verdict != prior["verdict"]:
                raise ValueError(f"manifest verdict/raw mismatch at sequence {seq}")
            print(f"skip verified S6 completion sequence={seq} verdict={verdict}", flush=True)
            if verdict == "LOSS":
                state["stop_reason"] = f"S6 LOSS witness at sequence {seq} proves parent S5 LOSS"
                break
            continue
        if raw_path.exists() or log_path.exists():
            if not raw_path.is_file() or not log_path.is_file():
                raise FileExistsError(f"unmanifested partial output exists; preserve and inspect: {raw_path}")
            parsed, verdict = read_replay(raw_path, target)
            record = {**parsed, "sequence": seq, "verdict": verdict,
                      "elapsed_seconds": parsed["reported_seconds"], "adopted_completed_output": True,
                      "raw_path": str(raw_path.relative_to(ROOT)), "raw_sha256": sha(raw_path),
                      "log_path": str(log_path.relative_to(ROOT)), "log_sha256": sha(log_path)}
            state["runs"].append(record)
            state["runs"].sort(key=lambda r: r["sequence"])
            write_manifest(run_path, state)
            print(json.dumps(record, ensure_ascii=False), flush=True)
            if verdict == "LOSS":
                state["stop_reason"] = f"S6 LOSS witness at sequence {seq} proves parent S5 LOSS"
                break
            continue

        input_path = resolve(Path(target["input_path"]))
        if sha(input_path) != target["input_sha256"]:
            raise ValueError(f"frozen input hash mismatch: {input_path}")
        command = [str(binary), "--n=11", "--memo=22", "--only=6", "--exact-order=count",
                   f"--exact-replay={input_path}", f"--exact-replay-budget={target['budget']}",
                   f"--csv={raw_path}", f"--log={log_path}"]
        start = time.perf_counter()
        completed = subprocess.run(command, cwd=ROOT, check=False)
        elapsed = time.perf_counter() - start
        if completed.returncode != 0:
            raise RuntimeError(f"solver exit={completed.returncode} at sequence {seq}; preserve raw/log")
        parsed, verdict = read_replay(raw_path, target)
        record = {**parsed, "sequence": seq, "verdict": verdict, "elapsed_seconds": elapsed,
                  "raw_path": str(raw_path.relative_to(ROOT)), "raw_sha256": sha(raw_path),
                  "log_path": str(log_path.relative_to(ROOT)), "log_sha256": sha(log_path),
                  "command": [binary.name, *command[1:]]}
        state["runs"].append(record)
        state["runs"].sort(key=lambda r: r["sequence"])
        if verdict == "LOSS":
            state["stop_reason"] = f"S6 LOSS witness at sequence {seq} proves parent S5 LOSS"
        write_manifest(run_path, state)
        print(json.dumps(record, ensure_ascii=False), flush=True)
        if verdict == "LOSS":
            break
    else:
        state["stop_reason"] = f"all {len(selected)} frozen S6 children completed without an S6 LOSS"
    if not state["stop_reason"]:
        state["stop_reason"] = "batch interrupted after last completed child; resume only from manifest"
    write_manifest(run_path, state)
    print(json.dumps({"completed": len(state["runs"]), "stop_reason": state["stop_reason"],
                      "manifest": str(run_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
