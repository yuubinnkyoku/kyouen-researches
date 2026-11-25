"""Measure the staged DAG integration process tree and peak output storage."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research/experiments/n11-proof-compact-20261011/scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_audit import read_json, sha256  # noqa: E402
from benchmark_verifier import process_tree_rss_bytes, tree_bytes  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True,
                        help="new directory for the integration outputs and receipt")
    parser.add_argument("--max-local-trials", type=int, default=100)
    parser.add_argument("--max-exact-combinations", type=int, default=4096)
    parser.add_argument("--poll-ms", type=int, default=250)
    args = parser.parse_args()
    if args.output_dir.exists():
        parser.error(f"refusing to overwrite {args.output_dir}")
    if args.max_local_trials < 0 or args.max_exact_combinations < 1 or args.poll_ms <= 0:
        parser.error("local trials must be nonnegative; exact combinations and poll interval must be positive")

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True)
    artifact_dir = output_dir / "artifacts"
    plan_path = output_dir / "integration-plan.json"
    log_path = output_dir / "integration.log"
    command = [
        sys.executable,
        str(Path(__file__).with_name("integrate.py")),
        "--output-dir", str(artifact_dir),
        "--max-local-trials", str(args.max_local_trials),
        "--max-exact-combinations", str(args.max_exact_combinations),
        "--receipt", str(plan_path),
    ]

    peak_rss = 0
    peak_tree_bytes = 0
    started = time.monotonic()
    with log_path.open("x", encoding="utf-8") as log:
        process = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT)
        while process.poll() is None:
            peak_rss = max(peak_rss, process_tree_rss_bytes(process) or 0)
            peak_tree_bytes = max(peak_tree_bytes, tree_bytes(output_dir))
            time.sleep(args.poll_ms / 1000)
        return_code = process.returncode
    elapsed = time.monotonic() - started
    plan = read_json(plan_path) if plan_path.is_file() else None
    result = {
        "schema": "n11-proof-integration-benchmark-v1",
        "returncode": return_code,
        "wall_seconds": round(elapsed, 3),
        "peak_process_tree_rss_bytes": peak_rss or None,
        "rss_measurement": "sampled_process_tree_working_set",
        "peak_output_tree_bytes": peak_tree_bytes,
        "poll_ms": args.poll_ms,
        "integration_plan": str(plan_path),
        "integration_plan_sha256": sha256(plan_path) if plan_path.is_file() else None,
        "optimizer_reported_seconds": plan.get("elapsed_optimizer_seconds") if plan else None,
        "command": command,
        "log": log_path.name,
    }
    benchmark_path = output_dir / "benchmark.json"
    benchmark_path.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n",
                              encoding="utf-8")
    print(json.dumps(result, sort_keys=True, separators=(",", ":")), flush=True)
    if return_code != 0 or plan is None or plan.get("schema") != "n11-incremental-proof-integration-run-v1":
        raise SystemExit(return_code or 1)


if __name__ == "__main__":
    main()
