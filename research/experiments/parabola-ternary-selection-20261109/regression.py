"""Exhaustively compare ternary selectors with small exact integer geometry."""
from __future__ import annotations
import importlib.util
import hashlib
import gzip
from itertools import combinations, product
import json
import math
from pathlib import Path
import sys

from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical195
from ternary import encode, parameters, phases, ROOT, BASE, BASE_SHA, WARM

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/"research/experiments/structural-lemmas-2026-10-02/checks"))
from parabola_half_bound import clauses_for_pair

spec = importlib.util.spec_from_file_location("independent_integer_geometry", HERE.parent/"parabola-local-repair-20261109/verify.py")
geometry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(geometry)


def main():
    rows, cardinality_cases = [], 0
    for p in (5, 7, 11, 13, 17):
        h = (p-1)//2
        points = [(t, t*t % p) for t in range(p)]
        edges = [edge for edge in combinations(range(p), 4)
                 if geometry.determinant([points[t] for t in edge]) == 0]
        total, unsafe = 0, 0
        for d in range(1, h+1):
            original = clauses_for_pair(p, edges, d)
            hard, empties = encode(p, d, original)
            free = [i for i in range(1, h+1) if i != d]
            for states in product(range(3), repeat=len(free)):
                selected = {0, d, p-d} | {i if state == 0 else p-i
                    for i, state in zip(free, states) if state != 2}
                positive = {i+state*h for i, state in zip(free, states)}
                projected = parameters(p, d, positive)
                assert set(projected) == selected
                assert {lit for lit in phases(p, d, selected) if lit > 0} == positive
                cnf_safe = all(any((lit > 0) == (abs(lit) in positive) for lit in clause) for clause in hard)
                integer_safe = not any(set(edge) <= selected for edge in edges)
                assert cnf_safe == integer_safe
                empty_count = sum(state == 2 for state in states)
                assert len(selected) == h+2-empty_count
                total += 1
                unsafe += not integer_safe
            # Test the actual sequential-counter encoding on every empty-flag
            # assignment; auxiliary variables remain free in the SAT query.
            if p <= 11:
                for bound in range(len(empties)+1):
                    card = CardEnc.atmost(empties, bound=bound, top_id=3*h, encoding=EncType.seqcounter)
                    with Cadical195(bootstrap_with=card.clauses) as solver:
                        for mask in product((False, True), repeat=len(empties)):
                            answer = solver.solve(assumptions=[v if value else -v for v, value in zip(empties, mask)])
                            assert answer == (sum(mask) <= bound)
                            cardinality_cases += 1
            # Invalid one-hot states cannot represent point choices.
            if free:
                i = free[0]
                backbone, _ = encode(p, d, [])
                for values in ((False, False, False), (True, True, False),
                               (True, False, True), (False, True, True), (True, True, True)):
                    partial = {v for v, value in zip((i, h+i, 2*h+i), values) if value}
                    local = [c for c in backbone if all(abs(lit) in (i, h+i, 2*h+i) for lit in c)]
                    assert not all(any((lit > 0) == (abs(lit) in partial) for lit in c) for c in local)
        rows.append({"p": p, "assignments": total, "unsafe": unsafe,
                     "integer_forbidden_quadruples": len(edges)})
    # A binary-equivalent simplification need not preserve empty-pair semantics.
    expanded, _ = encode(5, 2, [(1,), (-1,)])
    simplified, _ = encode(5, 2, [()])
    only_empty = {5}  # e1 = 2h+1, h=2
    evaluate = lambda clauses: all(any((lit > 0) == (abs(lit) in only_empty) for lit in c) for c in clauses)
    assert evaluate(expanded) and not evaluate(simplified)
    raw = BASE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == BASE_SHA
    original = [list(map(int, line.split()[:-1])) for line in raw.decode("ascii").splitlines() if line[0] not in "cp"]
    hard, empty_vars = encode(2647, 1323, original)
    warm = list(map(int, WARM.read_bytes().split()))
    seed = phases(2647, 1323, warm[2:])
    positive = {lit for lit in seed if lit > 0}
    assert all(any((lit > 0) == (abs(lit) in positive) for lit in clause) for clause in hard)
    assert sum(v in positive for v in empty_vars) == 33
    card = CardEnc.atmost(empty_vars, bound=33, top_id=3969, encoding=EncType.seqcounter)
    with Cadical195(bootstrap_with=hard+card.clauses) as solver:
        assert solver.solve(assumptions=seed) is True
        model_positive = {lit for lit in solver.get_model() if lit > 0}
        assert all(any((lit > 0) == (abs(lit) in model_positive) for lit in clause) for clause in hard+card.clauses)
    successful = HERE/"output/target1293-budget100000"
    init = json.loads((successful/"init.json").read_text())
    result = json.loads((successful/"result.json").read_text())
    encoded = gzip.decompress((successful/"input.cnf.gz").read_bytes())
    assert hashlib.sha256(encoded).hexdigest() == init["encoded_cnf_sha256"]
    assert hashlib.sha256((HERE/"ternary.py").read_bytes()).hexdigest() == init["worker_source_sha256"]
    card = CardEnc.atmost(empty_vars, bound=init["empty_bound"], top_id=3969, encoding=EncType.seqcounter)
    rebuilt = hard+card.clauses
    dimacs = (f"p cnf {max(3969, card.nv)} {len(rebuilt)}\n"+"".join(
        " ".join(map(str, c))+" 0\n" for c in rebuilt)).encode("ascii")
    assert encoded == dimacs
    model = json.loads((successful/"model.json").read_text())["signed_model"]
    assert len(model) == init["variables"] and {abs(v) for v in model} == set(range(1, init["variables"]+1))
    positive = {v for v in model if v > 0}
    assert all(any((lit > 0) == (abs(lit) in positive) for lit in clause) for clause in rebuilt)
    candidate = list(map(int, (successful/"candidate.txt").read_bytes().split()))
    selected = parameters(2647, 1323, positive)
    assert candidate[:2] == [2647, 1296] and candidate[2:] == selected == result["parameters"]
    assert sum(v in positive for v in empty_vars) == 29 and len(selected) == 1296
    audit = json.loads((successful/"geometry.json").read_text())
    assert audit["returncode"] == 0
    assert audit["candidate_input_sha256"] == hashlib.sha256((successful/"candidate.txt").read_bytes()).hexdigest()
    assert audit["verifier_source_sha256"] == hashlib.sha256((HERE.parent/"parabola-local-repair-20261109/verify_subset.cpp").read_bytes()).hexdigest()
    assert list(map(int, audit["stdout"].split())) == [2647, 1296, math.comb(1296, 4), 44277012]
    unsuccessful = HERE/"output/target1300-budget100000"
    assert json.loads((unsuccessful/"run.json").read_text())["status"] == "UNKNOWN"
    assert not (unsuccessful/"result.json").exists()
    report = {"small_primes": rows, "total_assignments": sum(r["assignments"] for r in rows),
              "cardinality_cases": cardinality_cases, "invalid_one_hot_states": "REJECTED",
              "arbitrary_binary_simplification_counterexample": "PASS",
              "known_1292_witness_in_full_encoder": "SAT, zero hard violations, 33 empty pairs",
              "saved_1296_witness": "PASS: reproduced CNF, model, 29 empty pairs, candidate and geometry hashes",
              "target1300": "UNKNOWN, no UNSAT conclusion",
              "scope": "Finite exhaustive regression of the edge-wise ternary encoding, not the general mathematical proof."}
    (HERE/"regression.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8", newline="\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
