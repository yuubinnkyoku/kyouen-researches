"""Run the frozen S5-direct, known-witness, and ranked S6 cost comparison."""
from __future__ import annotations

import argparse
import ctypes
import csv
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
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
        for sequence, row in enumerate(rows):
            stream.write(",".join(map(str, (f"cost-{sequence}", sequence, row["stones"],
                row["lo"], row["hi"], row["legal"], 0, 0, 0, 0, 0))) + "\n")


def read_raw(path: Path, expected: list[dict], per_row_cap: int) -> tuple[list[dict], list[str]]:
    rows, profiles = [], []
    with path.open(encoding="utf-8", newline="") as stream:
        for fields in csv.reader(stream):
            if not fields:
                continue
            if fields[0] == "replay":
                if len(fields) != 11:
                    raise ValueError(f"malformed exact replay row: {fields}")
                sequence = int(fields[1])
                if sequence >= len(expected):
                    raise ValueError(f"unexpected replay row {sequence}")
                source = expected[sequence]
                row = {"sequence": sequence, "stones": int(fields[2]), "legal": int(fields[3]),
                    "is_or": int(fields[4]), "budget": int(fields[5]), "verdict": int(fields[6]),
                    "nodes": int(fields[7]), "reported_seconds": int(fields[8]),
                    "lo": int(fields[9]), "hi": int(fields[10]), "key": source["key"]}
                if (row["stones"], row["legal"], row["lo"], row["hi"]) != (
                        source["stones"], source["legal"], source["lo"], source["hi"]):
                    raise ValueError(f"solver replay row does not match fixed input: {row}")
                if row["budget"] != per_row_cap or row["nodes"] > per_row_cap or row["verdict"] not in (0, 1, 2):
                    raise ValueError(f"invalid result or per-row budget overrun: {row}")
                rows.append(row)
            elif fields[0].startswith("# exact-profile"):
                profiles.append(fields[0])
    if not rows or [row["sequence"] for row in rows] != list(range(len(rows))):
        raise ValueError(f"replay rows are missing or not a contiguous prefix: {rows}")
    if any(row["verdict"] == 2 for row in rows[:-1]):
        raise ValueError("solver continued after an exact S6 LOSS witness")
    return rows, profiles


def profile_summary(lines: list[str]) -> list[dict]:
    parsed = []
    for line in lines:
        values = dict(re.findall(r"([A-Za-z0-9_]+)=([A-Za-z0-9_.-]+)", line))
        if "exact-profile-child" in line:
            parsed.append({"kind": "root_child", "row": int(values["row"]),
                           "lo": int(values["lo"]), "hi": int(values["hi"]),
                           "legal": int(values["legal"]), "nodes": int(values["nodes"]),
                           "verdict": values["verdict"]})
        elif "exact-profile-rank" in line:
            rank_match = re.search(r"\bs(\d+)\b", line)
            parsed.append({"kind": "rank", "stones": int(rank_match.group(1)) if rank_match else None,
                           "row": int(values["row"]), **{k: int(v) for k, v in values.items()
                           if k not in {"row"}}})
        else:
            parsed.append({"kind": "table", "row": int(values["row"]),
                           "counters": {k: (float(v) if k == "avg_probe" else int(v))
                                        for k, v in values.items() if k != "row"}})
    return parsed


def run_one(binary: Path, out: Path, label: str, rows: list[dict], *,
            node_cap: int, share_tt: bool, stop_on_loss: bool,
            exact_order: str = "count") -> dict:
    run_dir = out / label
    run_dir.mkdir(parents=True)
    replay, raw, log = run_dir / "replay-input.csv", run_dir / "solver-raw.csv", run_dir / "solver.log"
    write_replay(replay, rows)
    stones = rows[0]["stones"]
    if any(row["stones"] != stones for row in rows):
        raise ValueError("one exact replay batch must contain one stone rank")
    command = [str(binary), "--n=11", "--memo=22", f"--exact-replay={replay}",
               f"--only={stones}", f"--exact-order={exact_order}", f"--exact-replay-budget={node_cap}",
               "--exact-replay-profile", f"--csv={raw}"]
    if stop_on_loss:
        command.append("--exact-replay-stop-on-loss")
    if share_tt:
        command.append("--exact-replay-share-tt")
    started = time.perf_counter()
    max_rss = 0
    with log.open("x", encoding="utf-8") as stream:
        proc = subprocess.Popen(command, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT)
        while proc.poll() is None:
            max_rss = max(max_rss, peak_rss(proc) or 0)
            time.sleep(0.01)
        max_rss = max(max_rss, peak_rss(proc) or 0)
    wall = time.perf_counter() - started
    if proc.returncode != 0:
        raise RuntimeError(f"solver failed in {label} ({proc.returncode}); see {log}")
    actual, profiles = read_raw(raw, rows, node_cap)
    total_nodes = sum(row["nodes"] for row in actual)
    return {
        "label": label, "command": command, "node_cap_per_row": node_cap,
        "exact_order": exact_order,
        "cache_mode": "one cold TT shared across replay rows" if share_tt else "fresh cold TT per replay row",
        "stop_on_exact_loss": stop_on_loss,
        "rows": actual, "total_nodes": total_nodes, "wall_seconds": wall,
        "peak_rss_bytes": max_rss or None,
        "profile": profile_summary(profiles),
        "input_sha256": sha256(replay), "raw_sha256": sha256(raw), "log_sha256": sha256(log),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--solver", type=Path, required=True)
    ap.add_argument("--build", type=Path, default=EXP / "input/build.json")
    ap.add_argument("--schedule", type=Path, default=EXP / "input/comparison-schedule.json")
    ap.add_argument("--out", type=Path, default=EXP / "output/stage1-6m")
    args = ap.parse_args()
    binary, build_path, schedule_path, out = (
        path.resolve() for path in (args.solver, args.build, args.schedule, args.out))
    if out.exists() or not binary.is_file() or not schedule_path.is_file():
        ap.error("solver and frozen schedule must exist; output directory must be new")
    schedule = json.loads(schedule_path.read_text(encoding="utf-8"))
    if schedule.get("schema") != "n11-s5-loss-cost-driver-schedule-v1":
        ap.error("unsupported frozen schedule")
    if sha256(schedule_path) != "b1cbb0930d594bdac9d1fd63975d53b68c4b2c37829bd470c34d945e6a4ca36d":
        ap.error("frozen schedule SHA-256 differs from the reviewed pre-run input")
    source = ROOT / "cpp/solvers/kyouen_dfpn_root.cpp"
    build = json.loads(build_path.read_text(encoding="utf-8"))
    if (build.get("source_sha256") != sha256(source)
            or build.get("binary_sha256") != sha256(binary)
            or build.get("binary_path") != str(binary.relative_to(ROOT)).replace("\\", "/")):
        ap.error("solver binary does not match the recorded source/build manifest")
    cap = schedule["budget_protocol"]["stage1_s5_root_node_cap"]
    child_cap = schedule["budget_protocol"]["stage1_ranked_s6_candidate_cap_per_candidate"]
    prefix = schedule["budget_protocol"]["stage1_ranked_prefix_length"]
    out.mkdir(parents=True)
    runs = {"A": [], "B": [], "C1": [], "C2": []}
    target_run_lookup = {}
    for target in schedule["targets"]:
        target_id = target["id"]
        s5 = target["s5"]
        s5_row = {"key": s5["key"], "lo": s5["lo"], "hi": s5["hi"],
                  "stones": 5, "legal": s5["legal"]}
        a = run_one(binary, out, f"A--{target_id.replace('/', '--')}", [s5_row],
                    node_cap=cap, share_tt=False, stop_on_loss=False)
        if a["rows"][0]["verdict"] == 1:
            raise ValueError(f"direct S5 exact WIN conflicts with pinned independent LOSS proof: {target_id}")
        runs["A"].append({"target_id": target_id, **a})

        for candidate_index, candidate in enumerate(target["saved_s6_loss_candidates"]):
            s6_row = {key: candidate[key] for key in ("s6_key", "s6_lo", "s6_hi", "s6_stones", "s6_legal")}
            row = {"key": s6_row["s6_key"], "lo": s6_row["s6_lo"], "hi": s6_row["s6_hi"],
                   "stones": s6_row["s6_stones"], "legal": s6_row["s6_legal"]}
            label = f"B--{target_id.replace('/', '--')}--candidate-{candidate_index}"
            result = run_one(binary, out, label, [row], node_cap=cap,
                             share_tt=False, stop_on_loss=False)
            actual = result["rows"][0]["verdict"]
            if actual == 1:
                raise ValueError(f"known S6 LOSS candidate returned exact WIN: {candidate['s6_key']}")
            runs["B"].append({"target_id": target_id, "candidate_index": candidate_index,
                              "candidate": candidate, **result})

        blind_rows = target["blind_legal_count_prefix"][:prefix]
        if len(blind_rows) != prefix:
            raise ValueError(f"short preregistered blind candidate prefix: {target_id}")
        for arm, share_tt in (("C1", False), ("C2", True)):
            label = f"{arm}--{target_id.replace('/', '--')}"
            result = run_one(binary, out, label, blind_rows, node_cap=child_cap,
                             share_tt=share_tt, stop_on_loss=True)
            if sum(row["nodes"] for row in result["rows"]) > cap:
                raise ValueError(f"ranked S6 total budget exceeded for {target_id}/{arm}")
            known_loss_keys = {candidate["s6_key"] for candidate in target["saved_s6_loss_candidates"]}
            if any(row["key"] in known_loss_keys and row["verdict"] == 1 for row in result["rows"]):
                raise ValueError(f"solver WIN conflicts with a pinned S6 LOSS proof: {target_id}")
            runs[arm].append({"target_id": target_id,
                "known_saved_loss_candidate_keys": sorted(known_loss_keys), **result})
        target_run_lookup[target_id] = {arm: runs[arm][-1] for arm in ("A", "C1", "C2")}

    arm_aggregates = {}
    for arm, results in runs.items():
        rows = [row for result in results for row in result["rows"]]
        counts = {"WIN": sum(row["verdict"] == 1 for row in rows),
                  "LOSS": sum(row["verdict"] == 2 for row in rows),
                  "UNKNOWN": sum(row["verdict"] == 0 for row in rows)}
        arm_aggregates[arm] = {
            "runs": len(results), "rows": len(rows), "verdict_counts": counts,
            "total_nodes": sum(result["total_nodes"] for result in results),
            "total_wall_seconds": sum(result["wall_seconds"] for result in results),
            "max_peak_rss_bytes": max((result["peak_rss_bytes"] or 0 for result in results), default=0) or None,
        }

    root_comparisons = []
    for target in schedule["targets"]:
        target_id = target["id"]
        a = next(result for result in runs["A"] if result["target_id"] == target_id)
        a_row = a["rows"][0]
        root_comparisons.append({
            "target_id": target_id,
            "direct_s5": {"verdict": a_row["verdict"], "nodes": a["total_nodes"],
                          "wall_seconds": a["wall_seconds"], "peak_rss_bytes": a["peak_rss_bytes"]},
            "known_s6_witnesses": [{"key": result["candidate"]["s6_key"],
                "proof_dag_nodes": result["candidate"]["proof_dag_nodes"],
                "proof_dag_edges": result["candidate"]["proof_dag_edges"],
                "nodes": result["total_nodes"], "verdict": result["rows"][0]["verdict"],
                "wall_seconds": result["wall_seconds"], "peak_rss_bytes": result["peak_rss_bytes"]}
                for result in runs["B"] if result["target_id"] == target_id],
            "ranked_s6": {arm: {"nodes": result["total_nodes"],
                "wall_seconds": result["wall_seconds"],
                "peak_rss_bytes": result["peak_rss_bytes"],
                "tested_candidates": len(result["rows"]),
                "loss_witness_key": next((row["key"] for row in result["rows"] if row["verdict"] == 2), None),
                "loss_witness_was_saved_candidate": any(
                    row["verdict"] == 2 and row["key"] in result["known_saved_loss_candidate_keys"]
                    for row in result["rows"])} for arm in ("C1", "C2")
                for result in runs[arm] if result["target_id"] == target_id},
        })

    result = {
        "schema": "n11-s5-loss-cost-driver-benchmark-v1",
        "schedule_path": str(schedule_path.relative_to(ROOT)).replace("\\", "/"),
        "schedule_sha256": sha256(schedule_path),
        "solver_source_path": "cpp/solvers/kyouen_dfpn_root.cpp",
        "solver_source_sha256": sha256(source),
        "solver_binary_path": str(binary), "solver_binary_sha256": sha256(binary),
        "build_manifest_path": str(build_path.relative_to(ROOT)).replace("\\", "/"),
        "build_manifest_sha256": sha256(build_path),
        "environment": {"platform": platform.platform(), "processor": platform.processor(),
                        "python": sys.version, "sequential": True,
                        "same_binary_for_all_arms": True},
        "initial_cache_condition": "No persistent cache or external verdict layer was loaded. Every A/B row has a cold new TT. C1 creates a cold new TT for each candidate row. C2 begins each S5 batch with one cold TT shared only within that batch.",
        "arm_aggregates": arm_aggregates,
        "root_comparisons": root_comparisons,
        "per_run_results": runs,
        "interpretation_limits": [
            "solver exact replay nodes measure search effort, not independent proof-DAG nodes",
            "B supplies the correct S6 witness from the already verified certificate and is a proof-cost reference only",
            "C1/C2 candidate ordering sees only legal-S7 count and canonical key; saved witness keys are consulted after the run for audit",
            "stage 2 has not run; no UNKNOWN result is extrapolated to an exact solve cost",
        ],
        "trust_note": "Only the pinned K0375/K0378 terminal-only DAGs establish the S5/S6 LOSS facts independently. New solver outputs are measurements, not imported proof evidence.",
    }
    summary_path = out / "summary.json"
    summary_path.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    files = []
    for path in sorted(item for item in out.rglob("*") if item.is_file()):
        files.append({"path": str(path.relative_to(out)).replace("\\", "/"),
                      "bytes": path.stat().st_size, "sha256": sha256(path)})
    manifest = {"schema": "n11-s5-loss-cost-driver-artifacts-v1", "files": files}
    (out / "artifact-manifest.json").write_text(
        json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(summary_path.relative_to(ROOT)).replace("\\", "/"),
                      "summary_sha256": sha256(summary_path), "arm_aggregates": arm_aggregates,
                      "root_comparisons": root_comparisons}, sort_keys=True))


if __name__ == "__main__":
    main()
