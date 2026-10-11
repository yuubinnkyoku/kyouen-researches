"""Compare cold per-root exact replay with persistent transposition sharing."""
import argparse
import csv
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] /
                       "n11-proof-dag-engine-20261011" / "scripts"))
from certify import process_peak_rss

REPO = Path(__file__).resolve().parents[4]


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def make_replay_input(path, positions):
    with path.open("x", encoding="utf-8", newline="") as f:
        for index, item in enumerate(positions):
            f.write(",".join(map(str, (
                f"resolved-{item['id']}", index, 5, item["lo"], item["hi"],
                item["legal"], 0, 0, 0, 0, 0))) + "\n")


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


def run_variant(binary, variant, positions, out, budget, poll_seconds):
    out.mkdir()
    replay_input = out / "replay-input.csv"
    make_replay_input(replay_input, positions)
    raw, log = out / "solver-raw.csv", out / "solver.log"
    command = [str(binary), "--n=11", "--memo=22",
               f"--exact-replay={replay_input}", "--only=5",
               "--exact-order=count", f"--exact-replay-budget={budget}",
               f"--csv={raw}"]
    if variant.startswith("shared"):
        command.append("--exact-replay-share-tt")
    started = time.monotonic()
    peak = 0
    with log.open("x", encoding="utf-8") as stream:
        proc = subprocess.Popen(command, stdout=stream, stderr=subprocess.STDOUT)
        while proc.poll() is None:
            peak = max(peak, process_peak_rss(proc) or 0)
            time.sleep(poll_seconds)
    wall = time.monotonic() - started
    if proc.returncode != 0:
        raise RuntimeError(f"{variant} failed ({proc.returncode}); inspect {log}")
    rows = []
    with raw.open(encoding="utf-8", newline="") as stream:
        for row in csv.reader(stream):
            if row and row[0] == "replay":
                if len(row) != 11:
                    raise ValueError(f"malformed solver row: {row}")
                rows.append({
                    "id": positions[len(rows)]["id"],
                    "stones": int(row[2]), "legal": int(row[3]),
                    "is_or": int(row[4]), "budget": int(row[5]),
                    "verdict": int(row[6]), "nodes": int(row[7]),
                    "reported_seconds": int(row[8]),
                    "root_lo": int(row[9]), "root_hi": int(row[10]),
                })
    if len(rows) != len(positions):
        raise ValueError(f"expected {len(positions)} result rows, got {len(rows)}")
    for row, expected in zip(rows, positions):
        if (row["root_lo"], row["root_hi"], row["verdict"]) != (
                expected["lo"], expected["hi"], expected["expected_verdict"]):
            raise ValueError(f"verdict/root mismatch for {expected['id']}: {row}")
    return {
        "variant": variant,
        "command": command,
        "root_order": [p["id"] for p in positions],
        "wall_seconds": wall,
        "peak_rss_bytes": peak or None,
        "total_nodes": sum(r["nodes"] for r in rows),
        "rows": rows,
        "input_path": replay_input.name,
        "input_sha256": sha256(replay_input),
        "raw_path": raw.name,
        "raw_sha256": sha256(raw),
        "log_path": log.name,
        "log_sha256": sha256(log),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--solver", type=Path, required=True)
    ap.add_argument("--positions", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--budget", type=int, default=15_000_000)
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
    positions = data["positions"]
    source_receipts = [audit_source(item) for item in positions]
    out.mkdir(parents=True)
    variants = [
        ("independent", positions),
        ("shared-forward", positions),
        ("shared-reverse", list(reversed(positions))),
    ]
    runs = [run_variant(solver, name, order, out / name, args.budget,
                        args.poll_ms / 1000)
            for name, order in variants]
    baseline = runs[0]["total_nodes"]
    for run in runs:
        run["node_ratio_to_independent"] = run["total_nodes"] / baseline
        run["node_reduction_percent"] = 100 * (1 - run["total_nodes"] / baseline)
    result = {
        "schema": "n11-resolved-s5-cross-root-tt-benchmark-v1",
        "board_size": data["board_size"],
        "common_s4": data["common_s4"],
        "solver_sha256": sha256(solver),
        "positions_path": str(positions_path),
        "positions_sha256": sha256(positions_path),
        "source_receipts": source_receipts,
        "budget_per_root": args.budget,
        "poll_ms": args.poll_ms,
        "runs": runs,
    }
    summary = out / "summary.json"
    summary.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n",
                       encoding="utf-8")
    artifacts = []
    for path in sorted(p for p in out.rglob("*") if p.is_file()):
        artifacts.append({"path": str(path.relative_to(out)),
                          "bytes": path.stat().st_size,
                          "sha256": sha256(path)})
    (out / "artifact-manifest.json").write_text(
        json.dumps({"schema": "n11-shared-roots-artifacts-v1", "files": artifacts},
                   sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8")
    print(json.dumps(runs, sort_keys=True))


if __name__ == "__main__":
    main()
