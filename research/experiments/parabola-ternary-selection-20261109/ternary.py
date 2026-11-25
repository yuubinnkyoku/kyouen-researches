"""Select low/high/empty per pair, with 0 and one complete pair fixed."""
from __future__ import annotations
import argparse
import gzip
import hashlib
import importlib.metadata
import json
from pathlib import Path
import time

from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical195

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASE = ROOT / "research/experiments/parabola-cnf-deletion-distance-20261109/output/rc2-p2647-d1323-20261108T184724Z.cnf"
WARM = ROOT / "research/experiments/parabola-local-repair-20261109/output/walk-1000000-seed20261109/candidate.txt"
BASE_SHA = "0f09fc6efce1ba1b3df795eef24e4bb014fcfad836f31d4e6ba7e99b242ff0b3"


def encode(p, d, original):
    h = (p-1)//2
    free = [i for i in range(1, h+1) if i != d]
    # Variables i, h+i, 2h+i mean low, high, empty, respectively.
    clauses = [[-lit if lit > 0 else -h+lit for lit in c] for c in original]
    for i in free:
        low, high, empty = i, h+i, 2*h+i
        clauses.extend([[low, high, empty], [-low, -high], [-low, -empty], [-high, -empty]])
    return clauses, [2*h+i for i in free]


def parameters(p, d, positive):
    h = (p-1)//2
    return sorted({0, d, p-d} | {t for i in range(1, h+1) if i != d
                               for variable, t in ((i, i), (h+i, p-i)) if variable in positive})


def phases(p, d, params):
    h = (p-1)//2
    chosen = set(params)
    result = []
    for i in range(1, h+1):
        if i != d:
            states = (i in chosen, p-i in chosen, i not in chosen and p-i not in chosen)
            result.extend(v if state else -v for v, state in zip((i, h+i, 2*h+i), states))
    return result


def write(path, value):
    path.write_text(json.dumps(value, indent=2)+"\n", encoding="utf-8", newline="\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=int, required=True)
    ap.add_argument("--budget", type=int, default=100000)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    p, d, h = 2647, 1323, 1323
    if not 3 <= args.target <= h+2 or args.budget <= 0:
        raise ValueError("invalid target or budget")
    args.output.mkdir(parents=True, exist_ok=False)
    base = BASE.read_bytes()
    assert hashlib.sha256(base).hexdigest() == BASE_SHA
    original = [list(map(int, line.split()[:-1])) for line in base.decode("ascii").splitlines()
                if line and line[0] not in "cp"]
    clauses, empty_vars = encode(p, d, original)
    card = CardEnc.atmost(empty_vars, bound=h+2-args.target, top_id=3*h, encoding=EncType.seqcounter)
    clauses.extend(card.clauses)
    nv = max(3*h, card.nv)
    dimacs = (f"p cnf {nv} {len(clauses)}\n"+"".join(
        " ".join(map(str, c))+" 0\n" for c in clauses)).encode("ascii")
    with (args.output/"input.cnf.gz").open("wb") as stream:
        with gzip.GzipFile(filename="", mode="wb", fileobj=stream, mtime=0) as compressed:
            compressed.write(dimacs)
    warm_bytes = WARM.read_bytes()
    warm = list(map(int, warm_bytes.split()))
    assert warm[0] == p and warm[1] == len(warm)-2 == 1292
    report = {"p": p, "d": d, "target": args.target, "empty_bound": h+2-args.target,
              "conflict_budget": args.budget, "variables": nv, "clauses": len(clauses),
              "base_cnf_sha256": BASE_SHA, "encoded_cnf_sha256": hashlib.sha256(dimacs).hexdigest(),
              "warm_input_sha256": hashlib.sha256(warm_bytes).hexdigest(),
              "worker_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "python_sat": importlib.metadata.version("python-sat"), "solver": "Cadical195",
              "scope": "0 and complete pair d fixed; all other pairs low/high/empty. Solver UNSAT is unaudited and restricted to this d."}
    write(args.output/"init.json", report)
    print(f"READY target={args.target} clauses={len(clauses)} variables={nv}", flush=True)
    started = time.monotonic()
    with Cadical195(bootstrap_with=clauses) as solver:
        solver.set_phases(phases(p, d, warm[2:]))
        solver.conf_budget(args.budget)
        answer = solver.solve_limited()
        model = solver.get_model() if answer is True else None
        stats = solver.accum_stats()
    report.update(status="SAT" if answer is True else "SOLVER_UNSAT" if answer is False else "UNKNOWN",
                  solve_seconds=time.monotonic()-started, statistics=stats)
    if model is not None:
        positive = {v for v in model if v > 0}
        assert all(any((lit > 0) == (abs(lit) in positive) for lit in c) for c in clauses)
        result = parameters(p, d, positive)
        empties = [i for i in range(1, h+1) if i != d and 2*h+i in positive]
        assert len(result) >= args.target and len(result) == h+2-len(empties)
        report.update(size=len(result), empty_pairs=empties, parameters=result,
                      direct_encoded_clause_violations=0, geometry="UNCHECKED")
        write(args.output/"model.json", {"signed_model": model})
        (args.output/"candidate.txt").write_text(f"{p} {len(result)}\n"+" ".join(map(str, result))+"\n", encoding="ascii", newline="\n")
    write(args.output/"result.json", report)
    print(json.dumps({k: report.get(k) for k in ("status", "solve_seconds", "size")}), flush=True)


if __name__ == "__main__":
    main()
