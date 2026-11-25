"""Independently geometry-check and bounded-minimax-check a new S5 WIN replay."""
from __future__ import annotations

import csv
import gzip
import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
from independent import Board, solve_certificate  # noqa: E402

S4_KEY = (1297036692683751424, 16)
S5_KEY = (1297036692683751424, 67108880)
STATE_LIMIT = 30_000


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    preflight_path = EXP / "output/preflight.json"
    summary_path = EXP / "output/s5-probe15m-first/summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    rows = [row for row in summary["results"] if row.get("key") == list(S5_KEY)]
    if len(rows) != 1 or rows[0].get("verdict") != 1:
        raise SystemExit(f"expected exactly one positive-budget S5 WIN result: {rows}")
    result = rows[0]
    input_path = ROOT / result["input"]
    raw_path = ROOT / result["raw"]
    log_path = ROOT / result["log"]
    for path, expected in ((input_path, result["input_sha256"]),
                           (raw_path, result["raw_sha256"]),
                           (log_path, result["log_sha256"])):
        if sha(path) != expected:
            raise SystemExit(f"probe artifact hash mismatch: {path}")

    replay_rows = [row for row in csv.reader(raw_path.open(newline="", encoding="utf-8-sig"))
                   if row and row[0] == "replay"]
    if len(replay_rows) != 1 or len(replay_rows[0]) != 11:
        raise SystemExit(f"expected one raw exact replay row: {replay_rows}")
    raw = replay_rows[0]
    observed = [int(raw[i]) for i in (2, 3, 4, 5, 6, 7, 9, 10)]
    expected = [5, 81, 0, 15_000_000, 1, 14_920_591, *S5_KEY]
    if observed != expected:
        raise SystemExit(f"raw solver result fields differ: {observed} != {expected}")

    board = Board(11)
    parent = S4_KEY[0] | (S4_KEY[1] << 64)
    child = S5_KEY[0] | (S5_KEY[1] << 64)
    if board.canonical(parent) != parent or child not in board.children(parent):
        raise SystemExit("new S5 WIN is not a canonical legal child of the requested S4 class")
    legal_count = board.legal(child).bit_count()
    if child.bit_count() != 5 or legal_count != 81:
        raise SystemExit(f"independent S5 geometry mismatch: stones={child.bit_count()} legal={legal_count}")

    start = time.perf_counter()
    independent = solve_certificate(board, child, STATE_LIMIT)
    elapsed = time.perf_counter() - start
    if independent["verdict"] not in (0, 1, 2):
        raise SystemExit(f"invalid bounded independent result: {independent}")
    if independent["verdict"] == 2:
        verdict_text = "LOSS"
    elif independent["verdict"] == 1:
        verdict_text = "WIN"
    else:
        verdict_text = "UNKNOWN"

    report = {
        "schema": "n11-reply27-target-s5-win-independent-check-v1",
        "s4_key": list(S4_KEY),
        "s5_key": list(S5_KEY),
        "solver_replay": {
            "summary_path": summary_path.relative_to(ROOT).as_posix(),
            "summary_sha256": sha(summary_path),
            "input_path": result["input"], "input_sha256": result["input_sha256"],
            "raw_path": result["raw"], "raw_sha256": result["raw_sha256"],
            "log_path": result["log"], "log_sha256": result["log_sha256"],
            "solver_path": summary["solver_path"], "solver_sha256": summary["solver_sha256"],
            "source_sha256": summary["solver_source_sha256"],
            "budget": result["budget"], "nodes": result["nodes"], "verdict": "WIN",
        },
        "independent_geometry": {"s4_canonical": True, "s5_safe_canonical": True,
                                 "legal_s4_to_s5_edge": True, "s5_legal_moves": legal_count},
        "independent_minimax": {"method": "independent.py solve_certificate; terminal-only ranked DAG; no trusted leaves",
                                "state_limit": STATE_LIMIT, "visited": independent["visited"],
                                "verdict": verdict_text, "elapsed_seconds": elapsed,
                                "checker_source_sha256": sha(Path(__file__).resolve()),
                                "geometry_source_sha256": sha(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py")},
    }
    if independent["certificate"] is not None:
        cert_path = EXP / "output/s5-win-independent-certificate.json.gz"
        data = json.dumps(independent["certificate"], separators=(",", ":"), sort_keys=True).encode("utf-8") + b"\n"
        cert_path.write_bytes(gzip.compress(data, mtime=0))
        report["independent_minimax"]["certificate_path"] = cert_path.relative_to(ROOT).as_posix()
        report["independent_minimax"]["certificate_sha256"] = sha(cert_path)
        report["independent_minimax"]["certificate_nodes"] = len(independent["certificate"]["nodes"])
    out = EXP / "output/independent-win-check.json"
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"solver_verdict": "WIN", "independent_verdict": verdict_text,
                      "independent_states": independent["visited"], "seconds": elapsed,
                      "certificate_nodes": len(independent["certificate"]["nodes"]) if independent["certificate"] else 0,
                      "report_sha256": sha(out)}, sort_keys=True))
    if independent["verdict"] == 2:
        raise SystemExit("CONFLICT: independent checker returned LOSS for solver WIN")


if __name__ == "__main__":
    main()
