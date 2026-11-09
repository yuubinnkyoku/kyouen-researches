"""Generate one class CNF and its DRAT; UNSAT remains unaudited here."""
from __future__ import annotations
import argparse
import gzip
import hashlib
import importlib.metadata
import json
from pathlib import Path
import time
from pysat.solvers import Cadical195
from encoding import encode, dimacs, SHAPES

HERE = Path(__file__).resolve().parent


def save_gz(path, raw):
    with path.open("wb") as stream:
        with gzip.GzipFile(filename="", fileobj=stream, mode="wb", mtime=0) as zipped:
            zipped.write(raw)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shape", choices=SHAPES, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--budget", type=int, default=20000000)
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    raw_edges = gzip.decompress((HERE.parent/"parabola-hplus1-drat-20261109/input/verified_edges.txt.gz").read_bytes())
    rows = raw_edges.decode("ascii").splitlines()
    p, count = map(int, rows[0].split())
    edges = [tuple(map(int, line.split())) for line in rows[1:]]
    assert p == 2647 and len(edges) == count
    clauses, nv, point_base, used = encode(p, args.shape, edges)
    raw = dimacs(clauses, nv)
    save_gz(args.output/"input.cnf.gz", raw)
    report = {"p": p, "h": (p-1)//2, "target_size": (p-1)//2,
              "shape": args.shape, "origin_both_none": SHAPES[args.shape],
              "variables": nv, "clauses": len(clauses), "point_base": point_base,
              "provided_edges": count, "used_edges": used, "conflict_budget": args.budget,
              "input_sha256": hashlib.sha256(raw).hexdigest(),
              "edge_input_sha256": hashlib.sha256(raw_edges).hexdigest(),
              "encoding_source_sha256": hashlib.sha256((HERE/"encoding.py").read_bytes()).hexdigest(),
              "encoding_snapshot_sha256": hashlib.sha256((HERE/"encoding_snapshot.py").read_bytes()).hexdigest(),
              "generator_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "python_sat": importlib.metadata.version("python-sat"), "solver": "Cadical195"}
    (args.output/"init.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8", newline="\n")
    print(f"READY shape={args.shape} vars={nv} clauses={len(clauses)}", flush=True)
    started = time.monotonic()
    with Cadical195(bootstrap_with=clauses, with_proof=True) as solver:
        solver.conf_budget(args.budget)
        answer = solver.solve_limited()
        proof = solver.get_proof() if answer is False else None
        model = solver.get_model() if answer is True else None
        stats = solver.accum_stats()
    report.update(solve_seconds=time.monotonic()-started, statistics=stats,
                  solver_status="SAT" if answer is True else "SOLVER_UNSAT" if answer is False else "UNKNOWN")
    if proof:
        data = ("\n".join(proof)+"\n").encode("ascii")
        save_gz(args.output/"proof.drat.gz", data)
        report.update(proof_sha256=hashlib.sha256(data).hexdigest(), proof_lines=len(proof))
    if model is not None:
        (args.output/"model.json").write_text(json.dumps(model)+"\n", encoding="utf-8", newline="\n")
    (args.output/"solver.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: report.get(k) for k in ("shape", "solver_status", "solve_seconds", "proof_lines")}), flush=True)


if __name__ == "__main__":
    main()
