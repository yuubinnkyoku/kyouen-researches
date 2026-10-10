"""Paired same-position benchmark of baseline and native proof capture."""
import argparse
import csv
import hashlib
import json
import statistics
import subprocess
import sys
import time
from pathlib import Path

from certify import process_peak_rss


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def replay_row(path):
    rows = [r for r in csv.reader(path.open(encoding="utf-8", newline=""))
            if r and r[0] == "replay"]
    if len(rows) != 1 or len(rows[0]) != 11:
        raise ValueError(f"invalid solver output: {path}")
    r = rows[0]
    return dict(stones=int(r[2]), legal=int(r[3]), is_or=int(r[4]),
                budget=int(r[5]), verdict=int(r[6]), nodes=int(r[7]),
                reported_seconds=int(r[8]), root_lo=int(r[9]), root_hi=int(r[10]))


def run_one(binary, input_path, out, n, stones, order, budget, native, poll_seconds):
    raw, log = out / "solver-raw.csv", out / "solver.log"
    trace = out / "solver-proof-trace.csv"
    command = [str(binary), f"--n={n}", "--memo=22",
               f"--exact-replay={input_path}", f"--only={stones}",
               f"--exact-order={order}", f"--exact-replay-budget={budget}",
               f"--csv={raw}"]
    if native:
        command.append(f"--proof-dag={trace}")
    started = time.monotonic()
    peak = 0
    with log.open("x", encoding="utf-8") as f:
        proc = subprocess.Popen(command, stdout=f, stderr=subprocess.STDOUT)
        while proc.poll() is None:
            peak = max(peak, process_peak_rss(proc) or 0)
            time.sleep(poll_seconds)
    elapsed = time.monotonic() - started
    if proc.returncode != 0:
        raise RuntimeError(f"solver failed ({proc.returncode}): {command}; see {log}")
    result = replay_row(raw)
    if result["verdict"] not in (1, 2):
        raise RuntimeError(f"solver returned UNKNOWN: {result}")
    return dict(command=command, wall_seconds=elapsed, peak_rss_bytes=peak or None,
                result=result, raw_path=raw.name, raw_sha256=sha(raw),
                log_path=log.name, log_sha256=sha(log),
                trace_path=trace.name if trace.exists() else None,
                trace_bytes=trace.stat().st_size if trace.exists() else 0,
                trace_sha256=sha(trace) if trace.exists() else None)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--baseline-solver", type=Path, required=True)
    ap.add_argument("--native-solver", type=Path, required=True)
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--n", type=int, default=11)
    ap.add_argument("--stones", type=int, default=6)
    ap.add_argument("--order", choices=("count", "countd", "key"), default="count")
    ap.add_argument("--budget", type=int, default=100000)
    ap.add_argument("--repeats", type=int, default=5)
    ap.add_argument("--poll-ms", type=float, default=5)
    ap.add_argument("--out-dir", type=Path, required=True)
    args = ap.parse_args()
    baseline, native, inp, out = (p.resolve() for p in
                                  (args.baseline_solver, args.native_solver,
                                   args.input, args.out_dir))
    if out.exists():
        ap.error(f"refusing to overwrite {out}")
    if not all(p.is_file() for p in (baseline, native, inp)):
        ap.error("solver binaries and input file must exist")
    if args.repeats < 1 or args.budget < 1 or args.poll_ms <= 0:
        ap.error("repeats and budget must be positive")
    out.mkdir(parents=True)
    runs = []
    for rep in range(args.repeats):
        for name, binary, capture in (("baseline", baseline, False),
                                      ("native", native, True)):
            run_dir = out / f"{rep:02d}-{name}"
            run_dir.mkdir()
            item = run_one(binary, inp, run_dir, args.n, args.stones,
                           args.order, args.budget, capture, args.poll_ms / 1000)
            runs.append(dict(rep=rep, variant=name, **item))
    by_variant = {}
    for name in ("baseline", "native"):
        subset = [r for r in runs if r["variant"] == name]
        by_variant[name] = dict(
            median_wall_seconds=statistics.median(r["wall_seconds"] for r in subset),
            median_peak_rss_bytes=statistics.median(
                r["peak_rss_bytes"] for r in subset if r["peak_rss_bytes"] is not None),
            solver_nodes=[r["result"]["nodes"] for r in subset],
            verdicts=[r["result"]["verdict"] for r in subset],
            trace_bytes=[r["trace_bytes"] for r in subset])
    result = dict(schema="n11-proof-capture-overhead-v1", n=args.n,
                  stones=args.stones, order=args.order, budget=args.budget,
                  repeats=args.repeats, poll_ms=args.poll_ms,
                  input=str(inp), input_sha256=sha(inp),
                  baseline_solver_sha256=sha(baseline), native_solver_sha256=sha(native),
                  variants=by_variant, runs=runs)
    summary = out / "summary.json"
    summary.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n",
                       encoding="utf-8")
    files = [p for p in out.rglob("*") if p.is_file()]
    manifest = dict(schema="n11-proof-capture-overhead-files-v1",
                    files=[dict(path=str(p.relative_to(out)), bytes=p.stat().st_size,
                                sha256=sha(p)) for p in sorted(files)])
    (out / "artifact-manifest.json").write_text(
        json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps(by_variant, sort_keys=True))


if __name__ == "__main__":
    main()
