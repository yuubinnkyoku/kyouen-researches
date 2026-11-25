"""Check a new S5 WIN replay against independent geometry and bounded minimax."""
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

S4_KEY = (1224979098645823488, 536870912)
S5_KEY = (1224979098645823488, 536870976)
SUMMARY_PATH = EXP / "output/candidate-s5-probe15m-third/summary.json"
STATE_LIMIT = 30_000


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
    matches = [r for r in summary["results"] if tuple(r.get("key", ())) == S5_KEY]
    if len(matches) != 1 or matches[0].get("verdict") != 1:
        raise SystemExit(f"expected one direct S5 WIN result: {matches}")
    result = matches[0]
    for field in ("input", "raw", "log"):
        if sha(ROOT / result[field]) != result[field + "_sha256"]:
            raise SystemExit(f"{field} hash mismatch: {result[field]}")
    rows = [r for r in csv.reader((ROOT / result["raw"]).open(newline="", encoding="utf-8-sig"))
            if r and r[0] == "replay"]
    expected = [5, 84, 0, 15_000_000, 1, 9_611_717, *S5_KEY]
    if len(rows) != 1 or len(rows[0]) != 11:
        raise SystemExit(f"malformed replay output: {rows}")
    observed = [int(rows[0][i]) for i in (2, 3, 4, 5, 6, 7, 9, 10)]
    if observed != expected:
        raise SystemExit(f"raw solver verdict mismatch: {observed} != {expected}")

    board = Board(11)
    parent, child = S4_KEY[0] | (S4_KEY[1] << 64), S5_KEY[0] | (S5_KEY[1] << 64)
    if board.canonical(parent) != parent or child not in board.children(parent):
        raise SystemExit("S5 WIN is not an independently confirmed legal canonical child")
    if board.legal(child).bit_count() != 84:
        raise SystemExit("independent legal-move count mismatch")

    started = time.perf_counter()
    checked = solve_certificate(board, child, STATE_LIMIT)
    elapsed = time.perf_counter() - started
    verdict = {0: "UNKNOWN", 1: "WIN", 2: "LOSS"}[checked["verdict"]]
    out = {
        "schema": "n11-reply27-candidate-s5-win-independent-check-v1",
        "s4_key": list(S4_KEY), "s5_key": list(S5_KEY),
        "solver_replay": {"summary_path": SUMMARY_PATH.relative_to(ROOT).as_posix(),
                          "summary_sha256": sha(SUMMARY_PATH), "input_path": result["input"],
                          "input_sha256": result["input_sha256"], "raw_path": result["raw"],
                          "raw_sha256": result["raw_sha256"], "log_path": result["log"],
                          "log_sha256": result["log_sha256"], "solver_path": summary["solver_path"],
                          "solver_sha256": summary["solver_sha256"],
                          "source_sha256": summary["solver_source_sha256"],
                          "budget": result["budget"], "nodes": result["nodes"], "verdict": "WIN"},
        "independent_geometry": {"s4_canonical": True, "s5_safe_canonical": True,
                                 "legal_s4_to_s5_edge": True, "s5_legal_moves": 84},
        "independent_minimax": {"method": "terminal-only ranked DAG, no trusted leaves",
                                "state_limit": STATE_LIMIT, "visited": checked["visited"],
                                "verdict": verdict, "elapsed_seconds": elapsed,
                                "checker_source_sha256": sha(Path(__file__).resolve()),
                                "geometry_source_sha256": sha(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py")},
    }
    if checked["certificate"] is not None:
        cert_path = EXP / "output/candidate-s5-win-independent-certificate.json.gz"
        cert_path.write_bytes(gzip.compress(json.dumps(checked["certificate"], sort_keys=True,
                                                        separators=(",", ":")).encode() + b"\n", mtime=0))
        out["independent_minimax"].update(certificate_path=cert_path.relative_to(ROOT).as_posix(),
                                          certificate_sha256=sha(cert_path),
                                          certificate_nodes=len(checked["certificate"]["nodes"]))
    report_path = EXP / "output/candidate-s5-win-independent-check.json"
    report_path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"solver_verdict": "WIN", "independent_verdict": verdict,
                      "states": checked["visited"], "seconds": elapsed,
                      "report_sha256": sha(report_path)}, sort_keys=True))
    if checked["verdict"] == 2:
        raise SystemExit("CONFLICT: bounded independent checker returned LOSS for solver WIN")


if __name__ == "__main__":
    main()
