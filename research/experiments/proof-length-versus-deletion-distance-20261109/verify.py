"""Exact small clause-deletion distances and replay of a common one-line RUP proof."""
from __future__ import annotations

import argparse
import hashlib
from itertools import combinations
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
CHECKER = ROOT / "research/experiments/parabola-p2207-no-equality-witness-20261107/drat_check_incremental.cpp"


def formula(m, k):
    if not 1 <= k <= m:
        raise ValueError("require 1 <= k <= m")
    return [(i,) for i in range(1, m + 1)] + [(-i,) for i in range(1, k + 1)] + [
        (1, j) for j in range(k + 1, m + 1)]


def satisfiable(m, clauses):
    return any(all(any(bool(assignment & (1 << (abs(lit) - 1))) == (lit > 0)
                       for lit in clause) for clause in clauses)
               for assignment in range(1 << m))


def deletion_distance(m, clauses):
    for size in range(len(clauses) + 1):
        for removed in combinations(range(len(clauses)), size):
            remaining = [c for i, c in enumerate(clauses) if i not in removed]
            if satisfiable(m, remaining):
                return size
    raise RuntimeError("deleting every clause must produce SAT")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tmp", type=Path, default=Path(tempfile.gettempdir()))
    args = ap.parse_args()
    args.tmp.mkdir(parents=True, exist_ok=True)
    rows = []
    padded_rows = []
    proof = b"0\n"
    with tempfile.TemporaryDirectory(prefix="proof-distance-", dir=args.tmp) as td:
        tmp = Path(td)
        exe = tmp / "checker.exe"
        subprocess.run(["g++", "-O2", "-std=c++17", str(CHECKER), "-o", str(exe)], check=True)
        proof_path = tmp / "empty.drat"
        proof_path.write_bytes(proof)
        for m in range(1, 6):
            for k in range(1, m + 1):
                clauses = formula(m, k)
                assert len(clauses) == len(set(clauses)) == 2 * m
                assert {abs(lit) for c in clauses for lit in c} == set(range(1, m + 1))
                assert all(len(set(map(abs, c))) == len(c) for c in clauses)
                distance = deletion_distance(m, clauses)
                assert distance == k
                body = f"p cnf {m} {len(clauses)}\n" + "".join(
                    " ".join(map(str, c)) + " 0\n" for c in clauses)
                cnf = tmp / "input.cnf"
                cnf.write_bytes(body.encode("ascii"))
                result = subprocess.run([str(exe), str(cnf), str(proof_path)],
                                        capture_output=True, text=True, timeout=30)
                assert result.returncode == 0 and result.stdout.splitlines()[-1] == "VERIFIED"
                rows.append({"m": m, "k": k, "variables": m, "clauses": len(clauses),
                             "clause_deletion_distance": distance, "proof_lines": 1,
                             "cnf_sha256": hashlib.sha256(cnf.read_bytes()).hexdigest(),
                             "checker_rc": result.returncode, "checker_stdout": result.stdout.strip()})
                if m == 5 and k in (1, 5):
                    padded = b"1 0\n" * 7 + proof
                    proof_path.write_bytes(padded)
                    replay = subprocess.run([str(exe), str(cnf), str(proof_path)],
                                            capture_output=True, text=True, timeout=30)
                    assert replay.returncode == 0 and replay.stdout.splitlines()[-1] == "VERIFIED"
                    padded_rows.append({"m": m, "k": k, "clause_deletion_distance": distance,
                                        "proof_lines": 8, "checker_rc": replay.returncode,
                                        "proof_sha256": hashlib.sha256(padded).hexdigest()})
                    proof_path.write_bytes(proof)
    print(json.dumps({"checker_source_sha256": hashlib.sha256(CHECKER.read_bytes()).hexdigest(),
                      "common_proof_ascii": "0\n", "proof_sha256": hashlib.sha256(proof).hexdigest(),
                      "cases": rows, "checked_cases": len(rows),
                      "padded_proof_controls": padded_rows,
                      "scope": "m=1..5 finite checks; the all-m theorem has a separate elementary proof."},
                     indent=2))


if __name__ == "__main__":
    main()
