"""Run exact S5 roots with shared TT, then emit and verify one shared DAG."""
import argparse
import csv
import gzip
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(Path(__file__).resolve().parents[2] /
                       "n11-proof-dag-engine-20261011" / "scripts"))
from certify import process_peak_rss  # noqa: E402


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def audit_source(item):
    path = REPO / item["source_csv"]
    with path.open(encoding="utf-8", newline="") as stream:
        rows = [row for row in csv.reader(stream) if row and row[0] == "replay"]
    match = [row for row in rows if len(row) == 11 and
             (int(row[9]), int(row[10])) == (item["lo"], item["hi"])]
    if len(match) != 1:
        raise ValueError(f"expected one provenance row for {item['id']} in {path}")
    row = match[0]
    if (int(row[6]), int(row[7]), int(row[3])) != (
            item["expected_verdict"], item["prior_nodes"], item["legal"]):
        raise ValueError(f"provenance mismatch for {item['id']}: {row}")
    return {"id": item["id"], "path": str(path.relative_to(REPO)),
            "bytes": path.stat().st_size, "sha256": sha256(path),
            "verdict": int(row[6]), "nodes": int(row[7]),
            "reported_seconds": int(row[8])}


def write_replay_input(path, positions):
    with path.open("x", encoding="utf-8", newline="") as f:
        for index, item in enumerate(positions):
            row = (f"shared-{item['id']}", index, 5, item["lo"], item["hi"],
                   item["legal"], 0, 0, 0, 0, 0)
            f.write(",".join(map(str, row)) + "\n")


def read_results(path):
    rows = []
    with path.open(encoding="utf-8", newline="") as stream:
        for row in csv.reader(stream):
            if row and row[0] == "replay":
                if len(row) != 11:
                    raise ValueError(f"malformed solver row: {row}")
                rows.append({"stones": int(row[2]), "legal": int(row[3]),
                             "is_or": int(row[4]), "budget": int(row[5]),
                             "verdict": int(row[6]), "nodes": int(row[7]),
                             "reported_seconds": int(row[8]),
                             "root_lo": int(row[9]), "root_hi": int(row[10])})
    return rows


def run_measured(command, log_path, poll_seconds):
    peak = 0
    started = time.monotonic()
    with log_path.open("x", encoding="utf-8") as stream:
        proc = subprocess.Popen(command, stdout=stream, stderr=subprocess.STDOUT)
        while proc.poll() is None:
            peak = max(peak, process_peak_rss(proc) or 0)
            time.sleep(poll_seconds)
    return {"returncode": proc.returncode, "wall_seconds": time.monotonic() - started,
            "peak_rss_bytes": peak or None}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--solver", type=Path, required=True)
    ap.add_argument("--positions", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--budget", type=int, default=15_000_000)
    ap.add_argument("--order", choices=("forward", "reverse"), default="reverse")
    ap.add_argument("--solver-order", choices=("count", "countd", "key"), default="count")
    ap.add_argument("--poll-ms", type=float, default=5)
    args = ap.parse_args()
    solver, positions_path, out = (p.resolve() for p in
                                   (args.solver, args.positions, args.out))
    if out.exists():
        ap.error(f"refusing to overwrite {out}")
    if not solver.is_file() or not positions_path.is_file():
        ap.error("solver and positions file must exist")
    if args.budget <= 0 or args.poll_ms <= 0:
        ap.error("budget and poll interval must be positive")
    data = json.loads(positions_path.read_text(encoding="utf-8"))
    source_positions = data["positions"]
    source_receipts = [audit_source(item) for item in source_positions]
    positions = source_positions if args.order == "forward" else list(reversed(source_positions))
    out.mkdir(parents=True)
    replay_input, raw, solver_log = out / "replay-input.csv", out / "solver-raw.csv", out / "solver.log"
    trace_dir = out / "solver-traces"
    certificate_path = out / "proof-dag-bundle.json.gz"
    verification_path = out / "verification.json"
    write_replay_input(replay_input, positions)
    solver_command = [str(solver), "--n=11", "--memo=22",
                      f"--exact-replay={replay_input}", "--only=5",
                      f"--exact-order={args.solver_order}",
                      f"--exact-replay-budget={args.budget}",
                      "--exact-replay-share-tt", f"--proof-dag-dir={trace_dir}",
                      f"--csv={raw}"]
    solver_run = run_measured(solver_command, solver_log, args.poll_ms / 1000)
    if solver_run["returncode"] != 0:
        raise RuntimeError(f"shared replay failed; inspect {solver_log}")
    results = read_results(raw)
    if len(results) != len(positions):
        raise ValueError(f"expected {len(positions)} solver results, got {len(results)}")
    by_root = {}
    for item, result in zip(positions, results):
        key = (result["root_lo"], result["root_hi"])
        if key != (item["lo"], item["hi"]) or result["verdict"] != item["expected_verdict"]:
            raise ValueError(f"solver/root result mismatch for {item['id']}: {result}")
        by_root[key] = {"id": item["id"], **result}

    trace_path = trace_dir / "proof-bundle.csv"
    if not trace_path.is_file():
        raise ValueError("solver produced no closed proof bundle")
    verifier_script = SCRIPTS / "verify_shared_bundle.py"
    verifier_command = [sys.executable, str(verifier_script), "--trace", str(trace_path),
                        "--out", str(certificate_path), "--receipt", str(verification_path)]
    verifier_log = out / "verifier.log"
    verifier_run = run_measured(verifier_command, verifier_log, args.poll_ms / 1000)
    if verifier_run["returncode"] != 0:
        raise RuntimeError(f"independent bundle verifier failed; inspect {verifier_log}")
    receipt = json.loads(verification_path.read_text(encoding="utf-8"))
    expected_roots = {(r["root"], r["verdict"]) for r in receipt["roots"]}
    expected_set = {(str(lo | (hi << 64)), by_root[(lo, hi)]["verdict"])
                    for lo, hi in by_root}
    if expected_roots != expected_set or len(receipt["roots"]) != len(positions):
        raise ValueError("independent verifier root set does not match solved input rows")
    if receipt["trusted_leaves"] != 0:
        raise ValueError("independent verification reported a trusted leaf")

    trace_raw_bytes = trace_path.stat().st_size
    trace_raw_sha256 = sha256(trace_path)
    trace_compressed = trace_path.with_suffix(trace_path.suffix + ".gz")
    compress_start = time.monotonic()
    with trace_path.open("rb") as source, trace_compressed.open("xb") as target:
        with gzip.GzipFile(filename="", mode="wb", fileobj=target, mtime=0) as compressed:
            while True:
                block = source.read(1024 * 1024)
                if not block:
                    break
                compressed.write(block)
    trace_compression_seconds = time.monotonic() - compress_start
    trace_path.unlink()
    trace_path = trace_compressed

    result = {
        "schema": "n11-shared-s5-proof-bundle-run-v1", "board_size": 11,
        "common_s4": data["common_s4"], "order": args.order,
        "solver_order": args.solver_order, "budget_per_root": args.budget,
        "solver_sha256": sha256(solver), "positions_sha256": sha256(positions_path),
        "source_receipts": source_receipts,
        "replay_input_sha256": sha256(replay_input),
        "solver_wall_seconds": solver_run["wall_seconds"],
        "solver_peak_rss_bytes": solver_run["peak_rss_bytes"],
        "solver_total_nodes": sum(row["nodes"] for row in results),
        "solver_rows": [{"id": p["id"], **r} for p, r in zip(positions, results)],
        "trace_path": str(trace_path.relative_to(out)),
        "trace_bytes": trace_path.stat().st_size,
        "trace_sha256": sha256(trace_path),
        "trace_raw_bytes": trace_raw_bytes,
        "trace_raw_sha256": trace_raw_sha256,
        "trace_compression_seconds": trace_compression_seconds,
        "verifier_wall_seconds": verifier_run["wall_seconds"],
        "verifier_peak_rss_bytes": verifier_run["peak_rss_bytes"],
        "certificate_path": certificate_path.name,
        "certificate_bytes": certificate_path.stat().st_size,
        "certificate_sha256": sha256(certificate_path),
        "unique_proof_nodes": receipt["nodes"], "proof_edges": receipt["edges"],
        "terminal_nodes": receipt["terminal_nodes"], "trusted_leaves": 0,
        "roots": receipt["roots"], "commands": [solver_command, verifier_command],
    }
    summary_path = out / "summary.json"
    summary_path.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n",
                            encoding="utf-8")
    files = []
    for path in sorted(p for p in out.rglob("*") if p.is_file()):
        files.append({"path": str(path.relative_to(out)), "bytes": path.stat().st_size,
                      "sha256": sha256(path)})
    (out / "artifact-manifest.json").write_text(
        json.dumps({"schema": "n11-shared-s5-proof-bundle-files-v1", "files": files},
                   sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8")
    print(json.dumps({"solver_total_nodes": result["solver_total_nodes"],
                      "solver_wall_seconds": result["solver_wall_seconds"],
                      "solver_peak_rss_bytes": result["solver_peak_rss_bytes"],
                      "verifier_wall_seconds": result["verifier_wall_seconds"],
                      "verifier_peak_rss_bytes": result["verifier_peak_rss_bytes"],
                      "certificate_bytes": result["certificate_bytes"],
                      "trace_bytes": result["trace_bytes"],
                      "trace_raw_bytes": result["trace_raw_bytes"],
                      "unique_proof_nodes": result["unique_proof_nodes"],
                      "trusted_leaves": result["trusted_leaves"],
                      "roots": result["roots"]}, sort_keys=True))


if __name__ == "__main__":
    main()
