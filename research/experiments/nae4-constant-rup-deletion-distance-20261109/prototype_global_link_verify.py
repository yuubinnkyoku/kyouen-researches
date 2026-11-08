"""Exhaustive small signed-NAE4 scores and a common 15-line RUP proof."""
from __future__ import annotations

import argparse
import hashlib
from itertools import product
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
CHECKER = ROOT / "research/experiments/parabola-p2207-no-equality-witness-20261107/drat_check_incremental.cpp"


def formula(m, k):
    if not 1 <= k <= m:
        raise ValueError("require 1 <= k <= m")
    out = []
    for block in range(m):
        variables = tuple(range(4 * block + 1, 4 * block + 5))
        for signs in product((-1, 1), repeat=4):
            if block >= k and len(set(signs)) == 1:
                continue
            out.append(tuple(s * v for s, v in zip(signs, variables)))
        if block >= k:
            mixed = (1, -variables[0], -variables[1], -variables[2])
            out.extend((mixed, tuple(-lit for lit in mixed)))
    return out


def literal_value(assignment, lit):
    return bool(assignment & (1 << (abs(lit) - 1))) == (lit > 0)


def exact_scores(nvars, clauses, pairs):
    best_clauses = len(clauses)
    best_nae = len(pairs)
    for assignment in range(1 << nvars):
        bad_clauses = sum(not any(literal_value(assignment, lit) for lit in clause)
                          for clause in clauses)
        bad_nae = 0
        for constraint in pairs:
            values = [literal_value(assignment, lit) for lit in constraint]
            bad_nae += all(v == values[0] for v in values)
        assert bad_clauses == bad_nae
        best_clauses = min(best_clauses, bad_clauses)
        best_nae = min(best_nae, bad_nae)
    return best_clauses, best_nae


def rup_proof():
    return [tuple(s * (i + 1) for i, s in enumerate(signs))
            for width in (3, 2, 1, 0) for signs in product((-1, 1), repeat=width)]


def dimacs_lines(clauses):
    return "".join(" ".join([*(str(lit) for lit in clause), "0"]) + "\n" for clause in clauses)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tmp", type=Path, default=Path(tempfile.gettempdir()))
    args = ap.parse_args()
    args.tmp.mkdir(parents=True, exist_ok=True)
    proof = rup_proof()
    assert len(proof) == 15 and proof[-1] == ()
    proof_bytes = dimacs_lines(proof).encode("ascii")
    rows = []
    with tempfile.TemporaryDirectory(prefix="nae4-distance-", dir=args.tmp) as td:
        tmp = Path(td)
        exe = tmp / "checker.exe"
        subprocess.run(["g++", "-O2", "-std=c++17", str(CHECKER), "-o", str(exe)], check=True)
        proof_path = tmp / "common.drat"
        proof_path.write_bytes(proof_bytes)
        for m in range(1, 4):
            for k in range(1, m + 1):
                clauses = formula(m, k)
                clause_set = set(clauses)
                assert len(clauses) == len(clause_set) == 16 * m
                assert all(len(c) == len({abs(lit) for lit in c}) == 4 for c in clauses)
                assert {abs(lit) for c in clauses for lit in c} == set(range(1, 4 * m + 1))
                assert {tuple(-lit for lit in c) for c in clauses} == clause_set
                pairs = sorted({min(c, tuple(-lit for lit in c)) for c in clauses})
                assert len(pairs) == 8 * m
                clause_score, nae_score = exact_scores(4 * m, clauses, pairs)
                assert clause_score == nae_score == k
                cnf = tmp / "input.cnf"
                cnf.write_bytes((f"p cnf {4*m} {len(clauses)}\n" + dimacs_lines(clauses)).encode("ascii"))
                replay = subprocess.run([str(exe), str(cnf), str(proof_path)],
                                        capture_output=True, text=True, timeout=30)
                assert replay.returncode == 0 and replay.stdout.splitlines()[-1] == "VERIFIED"
                rows.append({"m": m, "k": k, "variables": 4 * m, "clauses": len(clauses),
                             "literal_occurrences": 64 * m, "nae_constraints": len(pairs),
                             "assignments_enumerated": 1 << (4 * m),
                             "minimum_violated_clauses": clause_score,
                             "minimum_violated_nae_constraints": nae_score,
                             "proof_lines": len(proof), "checker_rc": replay.returncode,
                             "checker_stdout": replay.stdout.strip(),
                             "cnf_sha256": hashlib.sha256(cnf.read_bytes()).hexdigest()})
    print(json.dumps({"checker_source_sha256": hashlib.sha256(CHECKER.read_bytes()).hexdigest(),
                      "common_proof_ascii": proof_bytes.decode("ascii"),
                      "proof_sha256": hashlib.sha256(proof_bytes).hexdigest(),
                      "cases": rows, "checked_cases": len(rows),
                      "scope": "m=1..3 exact assignment enumeration and proof replay; all-m proof is separate."},
                     indent=2))


if __name__ == "__main__":
    main()
