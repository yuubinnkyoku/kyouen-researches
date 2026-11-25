"""Supervise a fresh fixed-pair MaxSAT probe; timeout is UNKNOWN, never UNSAT."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent


def worker_runtime():
    # Bypass Windows venv redirectors so killing this PID kills the native solver.
    executable = getattr(sys, "_base_executable", None) or sys.executable
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(str(Path(p or os.getcwd()).resolve()) for p in sys.path)
    return executable, env


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prime", type=int, default=2647)
    ap.add_argument("--double", type=int, default=1323)
    inputs = ap.add_mutually_exclusive_group(required=True)
    inputs.add_argument("--edges", type=Path)
    inputs.add_argument("--cnf", type=Path)
    ap.add_argument("--timeout", type=float, default=60)
    ap.add_argument("--output-dir", type=Path, default=HERE / "output")
    args = ap.parse_args()
    if args.timeout <= 0:
        raise ValueError("positive timeout required")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    out = args.output_dir / f"rc2-p{args.prime}-d{args.double}-{stamp}.json"
    executable, env = worker_runtime()
    cmd = [executable, str(HERE / "probe_worker.py"), "--prime", str(args.prime),
           "--double", str(args.double), "--out", str(out)]
    cmd += ["--edges", str(args.edges)] if args.edges else ["--cnf", str(args.cnf)]
    started = time.monotonic()
    try:
        run = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=args.timeout)
        report = {"returncode": run.returncode, "status": "FINISHED" if run.returncode == 0 else "ERROR",
                  "stdout": run.stdout, "stderr": run.stderr}
    except subprocess.TimeoutExpired as exc:
        def decoded(value):
            return value.decode(errors="replace") if isinstance(value, bytes) else (value or "")
        report = {"status": "UNKNOWN", "timeout_seconds": args.timeout,
                  "stdout": decoded(exc.stdout), "stderr": decoded(exc.stderr)}
    report.update({"elapsed_seconds": time.monotonic()-started,
                   "base_interpreter_used": True, "result_path": str(out),
                   "model_file_exists": out.exists()})
    out.with_suffix(".run.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if report.get("status") == "ERROR":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
