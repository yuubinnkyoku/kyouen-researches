"""One native-solver worker, with a wall-clock limit and preserved output."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=int, required=True)
    ap.add_argument("--budget", type=int, default=100000)
    ap.add_argument("--timeout", type=float, default=60)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    if args.output.exists() or args.timeout <= 0:
        raise ValueError("fresh output path and positive timeout required")
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(str(Path(p or os.getcwd()).resolve()) for p in sys.path)
    executable = getattr(sys, "_base_executable", None) or sys.executable
    command = [executable, str(HERE/"ternary.py"), "--target", str(args.target), "--budget", str(args.budget),
               "--output", str(args.output)]
    started = time.monotonic()
    try:
        result = subprocess.run(command, env=env, capture_output=True, text=True, timeout=args.timeout)
        report = {"returncode": result.returncode, "status": "FINISHED" if result.returncode == 0 else "ERROR",
                  "stdout": result.stdout, "stderr": result.stderr}
    except subprocess.TimeoutExpired as exc:
        def decoded(value):
            return value.decode(errors="replace") if isinstance(value, bytes) else value or ""
        report = {"status": "UNKNOWN", "stdout": decoded(exc.stdout), "stderr": decoded(exc.stderr)}
    report.update(elapsed_seconds=time.monotonic()-started, timeout_seconds=args.timeout,
                  result_exists=(args.output/"result.json").exists())
    args.output.mkdir(exist_ok=True, parents=True)
    (args.output/"run.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8", newline="\n")
    print(json.dumps(report, indent=2))
    if report["status"] == "ERROR":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
