"""Measure shared exact replay with/without capture using one solver binary."""
import argparse
import csv
import gzip
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] /
                       "n11-proof-dag-engine-20261011" / "scripts"))
from certify import process_peak_rss  # noqa: E402


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def rows(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return [row for row in csv.reader(stream) if row and row[0] == "replay"]


def run(binary, replay, run_dir, budget, capture, poll_seconds):
    run_dir.mkdir()
    raw, log = run_dir / "solver-raw.csv", run_dir / "solver.log"
    trace_dir = run_dir / "solver-traces"
    command = [str(binary), "--n=11", "--memo=22",
               f"--exact-replay={replay}", "--only=5", "--exact-order=count",
               f"--exact-replay-budget={budget}", "--exact-replay-share-tt",
               f"--csv={raw}"]
    if capture:
        command.append(f"--proof-dag-dir={trace_dir}")
    peak = 0
    start = time.monotonic()
    with log.open("x", encoding="utf-8") as stream:
        process = subprocess.Popen(command, stdout=stream, stderr=subprocess.STDOUT)
        while process.poll() is None:
            peak = max(peak, process_peak_rss(process) or 0)
            time.sleep(poll_seconds)
    elapsed = time.monotonic() - start
    if process.returncode:
        raise RuntimeError(f"solver failed with {process.returncode}: {log}")
    result_rows = rows(raw)
    if len(result_rows) != 3 or any(int(row[6]) != 2 for row in result_rows):
        raise ValueError(f"expected three exact LOSS results: {result_rows}")
    item = {"command": command, "wall_seconds": elapsed,
            "peak_rss_bytes": peak or None, "rows": [
                {"stones": int(row[2]), "legal": int(row[3]),
                 "is_or": int(row[4]), "budget": int(row[5]),
                 "verdict": int(row[6]), "nodes": int(row[7]),
                 "reported_seconds": int(row[8]),
                 "root_lo": int(row[9]), "root_hi": int(row[10])}
                for row in result_rows], "total_nodes": sum(int(row[7]) for row in result_rows),
            "raw_csv_sha256": sha256(raw), "log_sha256": sha256(log)}
    if capture:
        traces = list(trace_dir.glob("proof-bundle.csv"))
        if len(traces) != 1:
            raise ValueError("capture mode did not produce exactly one bundle trace")
        source = traces[0]
        item.update({"trace_raw_bytes": source.stat().st_size,
                     "trace_raw_sha256": sha256(source)})
        compressed = source.with_suffix(source.suffix + ".gz")
        with source.open("rb") as src, compressed.open("xb") as dst:
            with gzip.GzipFile(filename="", mode="wb", fileobj=dst, mtime=0) as zipped:
                for block in iter(lambda: src.read(1024 * 1024), b""):
                    zipped.write(block)
        source.unlink()
        item.update({"trace_gzip_path": str(compressed.relative_to(run_dir)),
                     "trace_gzip_bytes": compressed.stat().st_size,
                     "trace_gzip_sha256": sha256(compressed)})
    return item


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--replay", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--budget", type=int, default=15_000_000)
    parser.add_argument("--poll-ms", type=float, default=5)
    parser.add_argument("--expected-raw-trace-sha256", required=True)
    args = parser.parse_args()
    binary, replay, out = (path.resolve() for path in
                           (args.solver, args.replay, args.out))
    if not binary.is_file() or not replay.is_file() or out.exists():
        parser.error("solver/replay must exist and output directory must be new")
    if args.budget <= 0 or args.poll_ms <= 0:
        parser.error("budget and poll interval must be positive")
    out.mkdir(parents=True)
    source_sha = sha256(binary)
    shared = run(binary, replay, out / "capture-off", args.budget, False,
                 args.poll_ms / 1000)
    captured = run(binary, replay, out / "capture-on", args.budget, True,
                   args.poll_ms / 1000)
    if [row["nodes"] for row in shared["rows"]] != [
            row["nodes"] for row in captured["rows"]]:
        raise ValueError("capture changed exact-search node counts")
    if captured["trace_raw_sha256"] != args.expected_raw_trace_sha256:
        raise ValueError("captured trace differs from the previously verified bytes")
    summary = {"schema": "n11-proof-capture-cost-same-binary-v1",
               "board_size": 11, "budget_per_root": args.budget,
               "solver_sha256": source_sha, "replay_sha256": sha256(replay),
               "expected_verified_raw_trace_sha256": args.expected_raw_trace_sha256,
               "capture_off": shared, "capture_on": captured}
    path = out / "summary.json"
    path.write_text(json.dumps(summary, sort_keys=True, separators=(",", ":")) + "\n",
                    encoding="utf-8")
    print(json.dumps(summary, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
