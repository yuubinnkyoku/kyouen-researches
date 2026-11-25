"""Exhaustive small integer-geometry regressions for MaxSAT model decoding."""
from __future__ import annotations

from itertools import combinations, permutations, product
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import probe_worker as worker

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "parabola-p2207-no-equality-witness-20261107"))
from maxsat_probe import decode_model


def determinant(points):
    rows = [(x*x+y*y, x, y, 1) for x, y in points]
    total = 0
    for order in permutations(range(4)):
        inversions = sum(order[i] > order[j] for i in range(4) for j in range(i+1, 4))
        term = (-1)**inversions
        for i, j in enumerate(order):
            term *= rows[i][j]
        total += term
    return total


def bad_geometry(params, points):
    return [edge for edge in combinations(sorted(params), 4)
            if determinant([points[t] for t in edge]) == 0]


def main():
    # This failed in the original helper: -1 is false when x1 is true.
    bad, chosen, remaining, removed = decode_model(7, 3, [(-1,)], [1, -2, -3, 99])
    assert bad == [(-1,)] and chosen == {0, 3, 4, 6, 2}
    assert removed == [6] and remaining == chosen - {6}
    assert worker.violated([(-1,)], {1}) == [(-1,)]
    assert worker.repair(7, sorted(chosen), bad) == (sorted(remaining), [6])

    rows = []
    for p in (5, 7, 11, 13, 17):
        points = [(t, t*t % p) for t in range(p)]
        # No modular sum filter or cached edge generator participates here.
        edges = bad_geometry(range(p), points)
        templates = violating = 0
        for d in range(1, (p-1)//2+1):
            free = [i for i in range(1, (p-1)//2+1) if i != d]
            clauses = worker.clauses_for_pair(p, edges, d)
            for values in product((False, True), repeat=len(free)):
                positive = {i for i, value in zip(free, values) if value}
                model = [i if i in positive else -i for i in range(1, (p-1)//2+1)]
                params = worker.selected_parameters(p, d, positive)
                bad = worker.violated(clauses, positive)
                geom = bad_geometry(params, points)
                assert bool(bad) == bool(geom)
                for clause in bad:
                    support = {lit if lit > 0 else p+lit for lit in clause}
                    assert support <= set(params)
                repaired, removed = worker.repair(p, params, bad)
                assert set(repaired) == set(params) - set(removed)
                assert len(removed) <= len(bad)
                assert not bad_geometry(repaired, points)
                old_bad, old_params, old_repaired, old_removed = decode_model(p, d, clauses, model)
                assert old_bad == bad and old_params == set(params)
                assert old_repaired == set(params) - set(old_removed)
                assert len(old_removed) <= len(bad)
                assert not bad_geometry(old_repaired, points)
                templates += 1
                violating += bool(bad)
        rows.append({"p": p, "templates": templates, "violating_templates": violating,
                     "integer_forbidden_quadruples": len(edges)})

    assert sum(r["violating_templates"] for r in rows) > 0
    cnf = HERE / "output/rc2-p2647-d1323-20261108T184724Z.cnf"
    clauses = worker.read_cnf(cnf, 1323)
    assert len(clauses) == len(set(clauses)) == 53886
    canonical = (f"p cnf 1323 {len(clauses)}\n" + "".join(
        " ".join([*(str(lit) for lit in c), "0"]) + "\n" for c in sorted(clauses))).encode("ascii")
    digest = hashlib.sha256(canonical).hexdigest()
    assert canonical == cnf.read_bytes()
    assert digest == json.loads(cnf.with_suffix(".init.json").read_text())["cnf_sha256"]

    # A toy objective exercises the installed RC2 API and parent runtime only.
    # This is deliberately not a second p=2647 optimization attempt.
    with tempfile.TemporaryDirectory(prefix="parabola-maxsat-smoke-") as tmp:
        tmp = Path(tmp)
        toy = tmp / "toy.cnf"
        toy.write_text("p cnf 3 1\n-1 0\n", encoding="ascii")
        executable, env = __import__("run_probe").worker_runtime()
        run = subprocess.run([executable, str(HERE / "run_probe.py"), "--prime", "7",
                              "--double", "3", "--cnf", str(toy), "--timeout", "15",
                              "--output-dir", str(tmp / "out")],
                             env=env, capture_output=True, text=True, timeout=20, check=True)
        receipt = json.loads(run.stdout)
        result = json.loads(Path(receipt["result_path"]).read_text())
        assert receipt["status"] == "FINISHED" and receipt["model_file_exists"]
        assert result["verified_violation_count"] == result["rc2_reported_cost"] == 0
        assert result["safe_by_cached_edges"] is None and result["stage"] == "MODEL"
    report = {"small_primes": rows, "total_templates": sum(r["templates"] for r in rows),
              "negative_literal_regression": "PASS", "saved_cnf_sha256": digest,
              "supervised_toy_rc2": "PASS (geometry unchecked)",
              "scope": "Finite regression; no bound for p=2647 is inferred."}
    (HERE / "regression_results.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
