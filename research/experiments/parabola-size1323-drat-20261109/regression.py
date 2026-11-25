"""Counterexample to selector aliasing and exhaustive tests of the repaired builder."""
from __future__ import annotations
import gzip
import hashlib
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path
import subprocess
import tempfile
from pysat.solvers import Cadical195
from encoding import encode as legacy_encode
from corrected import encode, dimacs, SHAPES

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SHARED = HERE.parent/"parabola-p2207-no-equality-witness-20261107/search_shape_class.py"
spec = importlib.util.spec_from_file_location("independent_geometry", HERE.parent/"parabola-local-repair-20261109/verify.py")
geometry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(geometry)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    destination = HERE/"input"
    destination.mkdir(exist_ok=True)
    legacy, old_nv, old_base, _ = legacy_encode(5, "000", [])
    fixed, new_nv, new_base, _ = encode(5, "000", [])
    with Cadical195(bootstrap_with=legacy, with_proof=True) as solver:
        assert solver.solve() is False
        proof = ("\n".join(solver.get_proof())+"\n").encode("ascii")
    with Cadical195(bootstrap_with=fixed) as solver:
        assert solver.solve() is True
        model = solver.get_model()
    positive = {v for v in model if v > 0}
    assert all(any((lit > 0) == (abs(lit) in positive) for lit in c) for c in fixed)
    points = [t for t in range(1, 5) if new_base+t in positive]
    assert len(points) == 2 and {min(t, 5-t) for t in points} == {1, 2}
    old_raw, new_raw = dimacs(legacy, old_nv), dimacs(fixed, new_nv)
    (destination/"legacy-p5-000.cnf").write_bytes(old_raw)
    (destination/"legacy-p5-000.drat").write_bytes(proof)
    (destination/"fixed-p5-000.cnf").write_bytes(new_raw)
    checker_source = HERE.parent/"parabola-p2207-no-equality-witness-20261107/drat_check_incremental.cpp"
    checker = Path(tempfile.gettempdir())/"shape-alias-counterexample.exe"
    subprocess.run(["g++", "-O2", "-std=c++17", str(checker_source), "-o", str(checker)], check=True, timeout=60)
    checked = subprocess.run([str(checker), str(destination/"legacy-p5-000.cnf"),
                              str(destination/"legacy-p5-000.drat")], capture_output=True, text=True, timeout=10, check=True)
    assert checked.stdout.splitlines()[-1] == "VERIFIED"
    counterexample = {"p": 5, "class": [0, 0, 0], "intended_size": 2, "forbidden_edges": [],
                      "intended_shape_is_satisfiable": True, "legacy_solver_unsat": True,
                      "legacy_variables": old_nv, "legacy_point_base": old_base,
                      "last_pair_selector_ids": [7, 8], "aliased_point_ids": [old_base+1, old_base+2],
                      "fixed_variables": new_nv, "fixed_point_base": new_base,
                      "fixed_signed_model": model, "fixed_parameters": points,
                      "legacy_cnf_sha256": sha(old_raw), "fixed_cnf_sha256": sha(new_raw),
                      "legacy_drat_sha256": sha(proof), "legacy_drat_checker_stdout": checked.stdout,
                      "scope": "The old CNF really is UNSAT, but it incorrectly represents an obviously feasible two-point shape. This is an encoding bug, not a solver or DRAT-checker false verdict."}
    (HERE/"counterexample.json").write_text(json.dumps(counterexample, indent=2)+"\n", encoding="utf-8", newline="\n")

    assert SHAPES == {"000": (0, 0, 0), "011": (0, 1, 1), "101": (1, 0, 1), "112": (1, 1, 2)}
    cases = []
    for p in (3, 5, 7, 11, 13, 17):
        h = (p-1)//2
        coords = [(t, t*t % p) for t in range(p)]
        full_edges = [q for q in combinations(range(p), 4)
                      if geometry.determinant([coords[t] for t in q]) == 0]
        subset = [q for q in full_edges if len({min(t, p-t) for t in q if t}) == sum(t != 0 for t in q)]
        for key, (origin, both, empty) in SHAPES.items():
            clauses, nv, base, _ = encode(p, key, subset)
            assert base >= 4*h
            valid, unsafe = 0, 0
            with Cadical195(bootstrap_with=clauses) as solver:
                for states in product(("B", "N", "L", "H"), repeat=h):
                    if states.count("B") != both or states.count("N") != empty:
                        continue
                    points = {0} if origin else set()
                    assumptions = []
                    for i, chosen in enumerate(states, 1):
                        for j, state in enumerate(("B", "N", "L", "H"), 1):
                            variable = 4*(i-1)+j
                            assumptions.append(variable if state == chosen else -variable)
                        if chosen in ("B", "L"):
                            points.add(i)
                        if chosen in ("B", "H"):
                            points.add(p-i)
                    assert len(points) == h
                    assumptions += [base+t if t in points else -base-t for t in range(1, p)]
                    safe = not any(set(q) <= points for q in full_edges)
                    assert solver.solve(assumptions=assumptions) == safe, (p, key, states)
                    valid += 1
                    unsafe += not safe
                if not valid:
                    assert solver.solve() is False
            cases.append({"p": p, "class": key, "valid_assignments": valid, "unsafe": unsafe})
    assert sha(SHARED.read_bytes()) == sha((HERE/"encoding_fixed.py").read_bytes())
    edge_dir = HERE.parent/"parabola-hplus1-drat-20261109/input"
    edge_raw = gzip.decompress((edge_dir/"verified_edges.txt.gz").read_bytes())
    edges = [tuple(map(int, line.split())) for line in edge_raw.decode("ascii").splitlines()[1:]]
    legacy_comparison = []
    for key in SHAPES:
        fixed_clauses, fixed_nv, fixed_base, _ = encode(2647, key, edges)
        legacy_clauses, legacy_nv, legacy_base, _ = legacy_encode(2647, key, edges)
        identical = dimacs(fixed_clauses, fixed_nv) == dimacs(legacy_clauses, legacy_nv)
        assert identical == (key in ("011", "112"))
        legacy_comparison.append({"class": key, "same_cnf": identical, "legacy_base": legacy_base,
                                  "fixed_base": fixed_base, "fixed_variables": fixed_nv})
    report = {"counterexample": "PASS", "valid_assignments": sum(c["valid_assignments"] for c in cases),
              "cases": cases, "shared_source_matches_fixed_snapshot": True,
              "large_cnf_comparison": legacy_comparison,
              "scope": "Finite implementation tests. Legacy 000/101 UNSAT receipts do not certify the intended geometric classes; legacy 011/112 inputs are byte-identical to the repaired encoder."}
    (HERE/"regression.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: report[k] for k in ("counterexample", "valid_assignments", "large_cnf_comparison")}, indent=2))


if __name__ == "__main__":
    main()
