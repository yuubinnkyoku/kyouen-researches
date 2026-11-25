"""Small native regressions, or an explicit independent audit of a saved subset."""
from __future__ import annotations
import argparse
import hashlib
from itertools import combinations, permutations, product
import json
import math
from pathlib import Path
import random
import subprocess
import tempfile
import time

HERE = Path(__file__).resolve().parent


def compile_source(name):
    source = HERE / name
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    exe = Path(tempfile.gettempdir()) / f"parabola-{source.stem}-{digest[:16]}.exe"
    subprocess.run(["g++", "-O2", "-std=c++17", str(source), "-o", str(exe)], check=True, timeout=60)
    return exe, digest


def determinant(points):
    matrix = [(1, x, y, x*x+y*y) for x, y in points]
    result = 0
    for order in permutations(range(4)):
        term = (-1)**sum(order[i] > order[j] for i in range(4) for j in range(i+1, 4))
        for i, j in enumerate(order):
            term *= matrix[i][j]
        result += term
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit", type=Path)
    ap.add_argument("--receipt", type=Path)
    args = ap.parse_args()
    verifier, verifier_sha = compile_source("verify_subset.cpp")
    if args.audit:
        if not args.receipt:
            raise ValueError("--receipt required for a full audit")
        raw = args.audit.read_bytes()
        tokens = list(map(int, raw.split()))
        if len(tokens) < 2 or tokens[1] < 0 or len(tokens) != tokens[1]+2:
            raise ValueError("one complete candidate required")
        started = time.monotonic()
        run = subprocess.run([str(verifier), "--modular-filter"], input=raw,
                             capture_output=True, timeout=120)
        if run.returncode == 0:
            values = list(map(int, run.stdout.split()))
            assert len(values) == 4 and values[:3] == [tokens[0], tokens[1], math.comb(tokens[1], 4)]
            assert 0 <= values[3] <= values[2]
        report = {"returncode": run.returncode, "stdout": run.stdout.decode(),
                  "stderr": run.stderr.decode(), "elapsed_seconds": time.monotonic()-started,
                  "verifier_source_sha256": verifier_sha,
                  "candidate_input_sha256": hashlib.sha256(raw).hexdigest(),
                  "scope": "Generic integer 4x4 determinant with proven complete modular filter, no cached edges or CNF."}
        args.receipt.write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8", newline="\n")
        print(json.dumps(report, indent=2))
        if run.returncode:
            raise SystemExit(1)
        return

    walk, walk_sha = compile_source("walk.cpp")
    toy_rows = []
    toys = [([[1]], 1, 0), ([[1], [-1]], 1, 1),
            ([[1], [-1], [2], [-2]], 2, 2),
            ([list(sign*i for i, sign in enumerate(signs, 1))
              for signs in product((-1, 1), repeat=5)], 5, 1)]
    with tempfile.TemporaryDirectory(prefix="parabola-walk-regress-") as temporary:
        for j, (clauses, n, expected) in enumerate(toys):
            cnf, model = Path(temporary)/f"toy{j}.cnf", Path(temporary)/f"toy{j}.json"
            cnf.write_text(f"p cnf {n} {len(clauses)}\n"+"".join(
                " ".join(map(str, clause))+" 0\n" for clause in clauses), encoding="ascii")
            subprocess.run([str(walk), str(cnf), str(model), "50000", "20261109"],
                           capture_output=True, check=True, timeout=15)
            value = json.loads(model.read_text())
            positive = set(value["positive"])
            actual = sum(not any((lit > 0) == (abs(lit) in positive) for lit in c) for c in clauses)
            optimum = min(sum(not any((lit > 0) == values[abs(lit)-1] for lit in c) for c in clauses)
                          for values in product((False, True), repeat=n))
            assert actual == value["violations"] == optimum == expected
            toy_rows.append({"variables": n, "clauses": len(clauses), "actual_cost": actual,
                             "exact_optimum_by_enumeration": optimum, "completed_steps": value["completed_steps"]})

    rng, total, unsafe = random.Random(20261109), 0, 0
    for p in (5, 7, 11, 17):
        subsets = [[], [0], [0, 1, 2], [1, 2, p-2, p-1]]
        subsets += [sorted(rng.sample(range(p), rng.randrange(min(p, 9)+1))) for _ in range(20)]
        for params in subsets:
            bad = any(determinant([(t, t*t % p) for t in q]) == 0 for q in combinations(params, 4))
            encoded = f"{p} {len(params)}\n"+" ".join(map(str, params))+"\n"
            for options in ([], ["--modular-filter"]):
                run = subprocess.run([str(verifier), *options], input=encoded,
                                     capture_output=True, text=True, timeout=10)
                assert run.returncode == (4 if bad else 0), (p, params, options, run)
                if not bad:
                    prime, count, covered, checked = map(int, run.stdout.split())
                    assert prime == p and count == len(params) and covered == math.comb(len(params), 4)
                    assert checked <= covered
                    if not options:
                        assert checked == covered
            total += 1
            unsafe += bad
    controls = [("duplicate", "5 3\n0 1 1\n", 3),
                ("out-of-range", "5 2\n0 5\n", 3),
                ("composite", "9 2\n0 1\n", 2),
                ("truncated-parameters", "5 3\n0 1\n", 2),
                ("oversized", "5 6\n", 2),
                ("truncated-header", "5\n", 2),
                ("missing-case", "", 2)]
    for name, encoded, code in controls:
        run = subprocess.run([str(verifier), "--modular-filter"], input=encoded,
                             capture_output=True, text=True, timeout=10)
        assert run.returncode == code, name
    saved = HERE / "output/walk-1000000-seed20261109"
    assessment = json.loads((saved/"assessment.json").read_text())
    assert hashlib.sha256((HERE/"walk_initial.cpp").read_bytes()).hexdigest() == assessment["source_sha256"]
    from run import CNF, EXPECTED
    raw_cnf = CNF.read_bytes()
    assert hashlib.sha256(raw_cnf).hexdigest() == EXPECTED
    saved_model = json.loads((saved/"model.json").read_text())
    positive = set(saved_model["positive"])
    assert len(positive) == len(saved_model["positive"]) and all(type(v) is int and 1 <= v <= 1323 for v in positive)
    clauses = [list(map(int, line.split()[:-1])) for line in raw_cnf.decode("ascii").splitlines() if line[0] not in "cp"]
    saved_cost = sum(not any((lit > 0) == (abs(lit) in positive) for lit in clause) for clause in clauses)
    assert saved_cost == saved_model["violations"] == assessment["direct_violations"] == 41
    geometry = json.loads((saved/"geometry.json").read_text())
    assert geometry["verifier_source_sha256"] == verifier_sha and geometry["returncode"] == 0
    assert geometry["candidate_input_sha256"] == hashlib.sha256((saved/"candidate.txt").read_bytes()).hexdigest()
    initial_geometry = json.loads((saved/"geometry_initial.json").read_text())
    assert initial_geometry["verifier_source_sha256"] == hashlib.sha256((HERE/"verify_subset_initial.cpp").read_bytes()).hexdigest()
    assert initial_geometry["returncode"] == 0 and initial_geometry["stdout"].split() == geometry["stdout"].split()
    assert initial_geometry["candidate_input_sha256"] == geometry["candidate_input_sha256"]
    assert list(map(int, geometry["stdout"].split())) == [2647, 1292, math.comb(1292, 4), 43730623]
    report = {"walk_source_sha256": walk_sha, "verifier_source_sha256": verifier_sha,
              "toy_walks": toy_rows, "geometry_subsets": total, "unsafe_subsets": unsafe,
              "geometry_modes": ["unfiltered", "modular-filter"],
              "rejected_controls": [c[0] for c in controls],
              "saved_original_cnf_violations": saved_cost,
              "saved_receipt_and_source_binding": "PASS",
              "scope": "Small exhaustive toy objectives and sampled integer geometry; not a general soundness proof."}
    (HERE/"regression.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8", newline="\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
