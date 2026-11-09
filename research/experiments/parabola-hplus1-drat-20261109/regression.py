"""Small exhaustive class/geometry checks and frozen certificate consistency."""
from __future__ import annotations
import gzip
from collections import Counter
import hashlib
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path
import subprocess
import tempfile
from pysat.solvers import Cadical195
from encoding import encode, dimacs, SHAPES, state_var

HERE = Path(__file__).resolve().parent
GENERIC = HERE.parent/"parabola-local-repair-20261109/verify_subset.cpp"
spec = importlib.util.spec_from_file_location("independent_geometry", HERE.parent/"parabola-local-repair-20261109/verify.py")
geometry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(geometry)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def selected_edges(p, edges):
    return [edge for edge in edges if len({min(t, p-t) for t in edge if t}) == sum(t != 0 for t in edge)]


def manual_encoding(p, shape, edges):
    """Independent clause schemas, including an explicit prefix counter."""
    h = (p-1)//2
    origin, count_b, count_n = {"a": (1, 0, 0), "b": (0, 1, 0), "c": (1, 1, 1)}[shape]
    clauses = []
    for i in range(1, h+1):
        group = list(range(4*i-3, 4*i+1))
        clauses.append(group)
        clauses += [[-a, -b] for a, b in combinations(group, 2)]
    top = 4*h
    for offset, count in ((1, count_b), (2, count_n)):
        flags = [4*(i-1)+offset for i in range(1, h+1)]
        if count == 0:
            clauses += [[-v] for v in flags]
        else:
            clauses.append(flags)
            if h == 2:
                clauses.append([-flags[0], -flags[1]])
            elif h > 2:
                clauses.append([-flags[0], top+1])
                for j in range(1, h-1):
                    previous, current = top+j, top+j+1
                    clauses += [[-previous, current], [-flags[j], -previous], [-flags[j], current]]
                clauses.append([-flags[-1], -(top+h-1)])
                top += h-1
    for t in range(1, p):
        i = min(t, p-t)
        both, side = 4*i-3, 4*i-1 if t <= h else 4*i
        point = top+t
        clauses += [[-point, side, both], [point, -side], [point, -both]]
    clauses += [[-top-t for t in edge if t] for edge in edges if origin or 0 not in edge]
    return clauses, top+p-1


def main():
    assert SHAPES == {"a": (1, 0, 0), "b": (0, 1, 0), "c": (1, 1, 1)}
    small = []
    for p in (3, 5, 7, 11, 13, 17):
        h = (p-1)//2
        coords = [(t, t*t % p) for t in range(p)]
        full_edges = [q for q in combinations(range(p), 4)
                      if geometry.determinant([coords[t] for t in q]) == 0]
        partial_edges = selected_edges(p, full_edges)
        for shape, (origin, both, empty) in SHAPES.items():
            clauses, nv, point_base, _ = encode(p, shape, partial_edges)
            valid, unsafe = 0, 0
            with Cadical195(bootstrap_with=clauses) as solver:
                for states in product(("B", "N", "L", "H"), repeat=h):
                    if states.count("B") != both or states.count("N") != empty:
                        continue
                    points = {0} if origin else set()
                    for i, state in enumerate(states, 1):
                        if state in ("B", "L"):
                            points.add(i)
                        if state in ("B", "H"):
                            points.add(p-i)
                    assert len(points) == h+1
                    assumptions = [state_var(i, state) if state == chosen else -state_var(i, state)
                                   for i, chosen in enumerate(states, 1) for state in ("B", "N", "L", "H")]
                    assumptions += [point_base+t if t in points else -point_base-t for t in range(1, p)]
                    safe = not any(set(q) <= points for q in full_edges)
                    assert solver.solve(assumptions=assumptions) == safe, (p, shape, states)
                    valid += 1
                    unsafe += not safe
                if not valid:
                    assert solver.solve() is False
            small.append({"p": p, "shape": shape, "valid_assignments": valid,
                          "geometrically_unsafe": unsafe, "provided_edges": len(partial_edges)})

    raw_edges = gzip.decompress((HERE/"input/verified_edges.txt.gz").read_bytes())
    receipt = json.loads((HERE/"input/geometry.json").read_text())
    rows = raw_edges.decode("ascii").splitlines()
    p, count = map(int, rows[0].split())
    edges = [tuple(map(int, row.split())) for row in rows[1:]]
    assert p == 2647 and count == len(edges) == 53886
    assert sha(raw_edges) == receipt["edge_input_sha256"] and receipt["returncode"] == 0
    assert sha((HERE/"verify_edges.cpp").read_bytes()) == receipt["wrapper_sha256"]
    assert sha(GENERIC.read_bytes()) == receipt["included_verifier_sha256"]
    exe = Path(tempfile.gettempdir())/f"upper-edges-regression-{receipt['wrapper_sha256'][:8]}.exe"
    subprocess.run(["g++", "-O2", "-std=c++17", str(HERE/"verify_edges.cpp"), "-o", str(exe)], check=True, timeout=60)
    controls = [("actual-edge", b"5 1\n1 2 3 4\n", 0),
                ("nonedge", b"5 1\n0 1 2 3\n", 4),
                ("duplicate-point", b"5 1\n1 2 2 4\n", 3),
                ("out-of-range", b"5 1\n1 2 3 5\n", 3),
                ("missing-point", b"5 1\n1 2 3\n", 2),
                ("extra-data", b"5 1\n1 2 3 4\n9\n", 2)]
    with tempfile.TemporaryDirectory(prefix="upper-edges-regression-") as temporary:
        path = Path(temporary)/"edges.txt"
        for name, raw, expected in controls:
            path.write_bytes(raw)
            run = subprocess.run([str(exe), str(path)], capture_output=True, timeout=10)
            assert run.returncode == expected, name
        path.write_bytes(raw_edges)
        checked = subprocess.run([str(exe), str(path)], capture_output=True, text=True, timeout=60, check=True)
        assert checked.stdout.strip() == "VERIFIED_EDGES 2647 53886"

    audits = []
    for shape in SHAPES:
        out = HERE/"output"/f"shape-{shape}"
        solver = json.loads((out/"solver.json").read_text())
        audit = json.loads((out/"audit.json").read_text())
        cnf = gzip.decompress((out/"input.cnf.gz").read_bytes())
        proof = gzip.decompress((out/"proof.drat.gz").read_bytes())
        clauses, nv, point_base, used = encode(p, shape, edges)
        manual, manual_nv = manual_encoding(p, shape, edges)
        assert manual_nv == nv
        assert Counter(tuple(sorted(c)) for c in manual) == Counter(tuple(sorted(c)) for c in clauses)
        assert dimacs(clauses, nv) == cnf
        assert sha(cnf) == solver["input_sha256"] == audit["input_sha256"]
        assert sha(proof) == solver["proof_sha256"] == audit["proof_sha256"]
        assert len(proof.splitlines()) == solver["proof_lines"] == audit["proof_lines"]
        assert sha((HERE/"encoding.py").read_bytes()) == solver["encoding_source_sha256"]
        assert sha((HERE/"generate.py").read_bytes()) == solver["generator_source_sha256"]
        assert solver["edge_input_sha256"] == sha(raw_edges)
        assert solver["p"] == p and solver["target_size"] == 1324 and solver["shape"] == shape
        assert solver["solver_status"] == "SOLVER_UNSAT"
        assert audit["verified"] is True and audit["returncode"] == 0 and not audit["timed_out"]
        assert audit["stdout"].splitlines()[-1] == "VERIFIED"
        source = HERE.parent/"parabola-p2207-no-equality-witness-20261107/drat_check_incremental.cpp"
        assert sha(source.read_bytes()) == audit["checker_source_sha256"] == "34249932790a9e9d924e9403b75563a2ff051277923301e34ace33e2a5a3650b"
        audits.append({"shape": shape, "variables": nv, "clauses": len(clauses),
                       "proof_lines": solver["proof_lines"], "verified": True,
                       "input_sha256": sha(cnf), "proof_sha256": sha(proof)})
    report = {"small_cases": small, "valid_assignments": sum(r["valid_assignments"] for r in small),
              "edge_controls": [c[0] for c in controls], "provided_edges_rechecked": count,
              "edge_input_sha256": sha(raw_edges), "audits": audits,
              "independent_full_clause_schemas_and_prefix_counters": "PASS for all three 2647 inputs",
              "scope": "Small class/geometry equivalence, replay of supplied-edge geometry, and exact reconstruction/hash binding of existing DRAT audits. DRAT proofs themselves were not replayed in this regression."}
    (HERE/"regression.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8", newline="\n")
    print(json.dumps({"valid_assignments": report["valid_assignments"], "audits": audits,
                      "provided_edges_rechecked": count, "edge_controls": report["edge_controls"]}, indent=2))


if __name__ == "__main__":
    main()
