"""Run one bounded native walk and directly evaluate its saved original model."""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CNF = ROOT / "research/experiments/parabola-cnf-deletion-distance-20261109/output/rc2-p2647-d1323-20261108T184724Z.cnf"
EXPECTED = "0f09fc6efce1ba1b3df795eef24e4bb014fcfad836f31d4e6ba7e99b242ff0b3"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=1000000)
    ap.add_argument("--seed", type=int, default=20261109)
    ap.add_argument("--timeout", type=float, default=60)
    ap.add_argument("--source", type=Path, default=HERE / "walk.cpp")
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    raw = CNF.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED
    source = args.source
    sha = hashlib.sha256(source.read_bytes()).hexdigest()
    exe = Path(tempfile.gettempdir()) / f"parabola-walk-{sha[:16]}.exe"
    compile_run = subprocess.run(["g++", "-O2", "-std=c++17", str(source), "-o", str(exe)],
                                 capture_output=True, text=True, timeout=60, check=True)
    model_path = args.output / "model.json"
    started = time.monotonic()
    try:
        result = subprocess.run([str(exe), str(CNF), str(model_path), str(args.steps), str(args.seed)],
                                capture_output=True, text=True, timeout=args.timeout)
        status, code, stdout, stderr = "FINISHED", result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired as exc:
        def text(value):
            return value.decode(errors="replace") if isinstance(value, bytes) else value or ""
        status, code, stdout, stderr = "TIMEOUT", None, text(exc.stdout), text(exc.stderr)
    elapsed = time.monotonic()-started
    (args.output / "trace.txt").write_text(stdout, encoding="ascii", newline="\n")
    (args.output / "stderr.txt").write_text(stderr, encoding="utf-8", newline="\n")
    report = {"status": status, "returncode": code, "elapsed_seconds": elapsed,
              "steps_requested": args.steps, "seed": args.seed, "timeout_seconds": args.timeout,
              "cnf_sha256": EXPECTED, "source_sha256": sha,
              "compile_stderr": compile_run.stderr,
              "scope": "Verified model upper bound only; no MaxSAT optimality or geometric verification."}
    if model_path.exists():
        model = json.loads(model_path.read_text())
        positive = set(model["positive"])
        clauses = [tuple(map(int, line.split()[:-1])) for line in raw.decode("ascii").splitlines()
                   if line and line[0] not in "cp"]
        bad = [c for c in clauses if all((lit > 0) != (abs(lit) in positive) for lit in c)]
        assert len(clauses) == model["clauses"] == 53886
        assert len(bad) == model["violations"]
        p, d, h = 2647, 1323, 1323
        parameters = {0, d, p-d} | {p-i if i in positive else i for i in range(1, h+1) if i != d}
        supports = [{lit if lit > 0 else p+lit for lit in clause} for clause in bad]
        removed = []
        while supports:
            counts = Counter(t for support in supports for t in support)
            point = min(counts, key=lambda t: (-counts[t], t))
            assert point in parameters
            parameters.remove(point)
            removed.append(point)
            supports = [support for support in supports if point not in support]
        report.update(p=p, d=d, direct_violations=len(bad), candidate_size=len(parameters),
                      removed_parameters=removed, candidate_parameters=sorted(parameters))
        (args.output / "candidate.txt").write_text(
            f"{p} {len(parameters)}\n"+" ".join(map(str, sorted(parameters)))+"\n", encoding="ascii", newline="\n")
    (args.output / "assessment.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8", newline="\n")
    print(json.dumps({key: report.get(key) for key in
                      ("status", "returncode", "elapsed_seconds", "direct_violations", "candidate_size")}, indent=2))


if __name__ == "__main__":
    main()
