"""Select low/high/empty per pair for an arbitrary fixed complete pair d.

Generalizes ternary.py. The stored base CNF is d=1323-specific because
clauses_for_pair() drops every edge requirement involving pair d; that is not
recoverable from the file. The d-independent edge list (53,886 edges, all
forbidden quadruples whose four parameters use at least three distinct pairs)
is stored in parabola-hplus1-drat-20261109/input/verified_edges.txt.gz, so the
base for any d is regenerated from it. At d=1323 the regenerated base is
byte-identical to the stored CNF (BASE_SHA), and the encoded CNF therefore
matches the recorded encoded_cnf_sha256.
"""
from __future__ import annotations
import argparse
import gzip
import hashlib
import importlib.metadata
import json
from pathlib import Path
import sys
import time

from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical195

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ENC = ROOT / "research/experiments/structural-lemmas-2026-10-02/checks"
BASE = ROOT / "research/experiments/parabola-cnf-deletion-distance-20261109/output/rc2-p2647-d1323-20261108T184724Z.cnf"
WARM = ROOT / "research/experiments/parabola-local-repair-20261109/output/walk-1000000-seed20261109/candidate.txt"
EDGES = ROOT / "research/experiments/parabola-hplus1-drat-20261109/input/verified_edges.txt.gz"
BASE_SHA = "0f09fc6efce1ba1b3df795eef24e4bb014fcfad836f31d4e6ba7e99b242ff0b3"
EDGES_GZ_SHA = "bb1c0201192863b560a8687b570cdbab0f0a7d51c40d71fcd4a03c0f9ccbdae0"
EDGES_TXT_SHA = "4e17fe105f191f781192466d0775a59d3c341b16b267ebe372ba279911f67a72"
D_FIXED = 1323

sys.path.insert(0, str(ENC))
from parabola_half_bound import clauses_for_pair


def base_clauses(p, d, edges):
    """The d=1323 stored CNF equals this, canonical clause order included."""
    h = (p-1)//2
    clauses = sorted(tuple(sorted(c, key=lambda lit: (abs(lit), lit)))
                     for c in clauses_for_pair(p, edges, d))
    assert len(clauses) == len(set(clauses)), f"duplicate base clause at d={d}"
    assert all(0 < abs(lit) <= h for c in clauses for lit in c), \
        f"base clause outside variable range at d={d}"
    return [list(c) for c in clauses]


def base_bytes(p, d, original):
    h = (p-1)//2
    return (f"p cnf {h} {len(original)}\n" + "".join(
        " ".join(map(str, c))+" 0\n" for c in original)).encode("ascii")


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
            # ternary.py sets both low and high positive when a pair is complete.
            # Only pair d may be complete, and its variables do not exist here;
            # for any other pair keep the hint one-hot (low wins).
            low, high = i in chosen, p-i in chosen
            if low and high:
                high = False
            states = (low, high, not low and not high)
            result.extend(v if state else -v for v, state in zip((i, h+i, 2*h+i), states))
    return result


def load_edges():
    raw = EDGES.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EDGES_GZ_SHA, "edge cache gz sha mismatch"
    text = gzip.decompress(raw)
    assert hashlib.sha256(text).hexdigest() == EDGES_TXT_SHA, "edge cache sha mismatch"
    header, *lines = text.decode("ascii").split("\n")
    edges = [tuple(map(int, line.split())) for line in lines if line.strip()]
    count, = map(int, header.split()[1:])
    assert len(edges) == count
    return edges


def write(path, value):
    path.write_text(json.dumps(value, indent=2)+"\n", encoding="utf-8", newline="\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=int, required=True)
    ap.add_argument("--d", type=int, default=D_FIXED)
    ap.add_argument("--budget", type=int, default=100000)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    p, h = 2647, 1323
    if not 3 <= args.target <= h+2 or args.budget <= 0 or not 1 <= args.d <= h:
        raise ValueError("invalid target, budget or d")
    args.output.mkdir(parents=True, exist_ok=False)
    edges = load_edges()
    original = base_clauses(p, args.d, edges)
    rebuilt = base_bytes(p, args.d, original)
    if args.d == D_FIXED:
        assert hashlib.sha256(rebuilt).hexdigest() == BASE_SHA
        assert rebuilt == BASE.read_bytes()
    clauses, empty_vars = encode(p, args.d, original)
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
    report = {"p": p, "d": args.d, "target": args.target, "empty_bound": h+2-args.target,
              "conflict_budget": args.budget, "variables": nv, "clauses": len(clauses),
              "base_clauses": len(original),
              "base_cnf_sha256": hashlib.sha256(rebuilt).hexdigest(),
              "base_cnf_source": "regenerated" if args.d != D_FIXED else "regenerated, equals stored file",
              "edge_cache_gz_sha256": EDGES_GZ_SHA, "edge_cache_sha256": EDGES_TXT_SHA,
              "encoded_cnf_sha256": hashlib.sha256(dimacs).hexdigest(),
              "warm_input_sha256": hashlib.sha256(warm_bytes).hexdigest(),
              "worker_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "python_sat": importlib.metadata.version("python-sat"), "solver": "Cadical195",
              "scope": "0 and complete pair d fixed; all other pairs low/high/empty. Solver UNSAT is unaudited and restricted to this d."}
    write(args.output/"init.json", report)
    print(f"READY d={args.d} target={args.target} clauses={len(clauses)} variables={nv}", flush=True)
    started = time.monotonic()
    with Cadical195(bootstrap_with=clauses) as solver:
        solver.set_phases(phases(p, args.d, warm[2:]))
        solver.conf_budget(args.budget)
        answer = solver.solve_limited()
        model = solver.get_model() if answer is True else None
        stats = solver.accum_stats()
    report.update(status="SAT" if answer is True else "SOLVER_UNSAT" if answer is False else "UNKNOWN",
                  solve_seconds=time.monotonic()-started, statistics=stats)
    if model is not None:
        positive = {v for v in model if v > 0}
        assert all(any((lit > 0) == (abs(lit) in positive) for lit in c) for c in clauses)
        result = parameters(p, args.d, positive)
        empties = [i for i in range(1, h+1) if i != args.d and 2*h+i in positive]
        assert len(result) >= args.target and len(result) == h+2-len(empties)
        assert {args.d, p-args.d} <= set(result)
        report.update(size=len(result), empty_pairs=empties, parameters=result,
                      direct_encoded_clause_violations=0, geometry="UNCHECKED")
        write(args.output/"model.json", {"signed_model": model})
        (args.output/"candidate.txt").write_text(f"{p} {len(result)}\n"+" ".join(map(str, result))+"\n", encoding="ascii", newline="\n")
    write(args.output/"result.json", report)
    print(json.dumps({k: report.get(k) for k in ("status", "solve_seconds", "size")}), flush=True)


if __name__ == "__main__":
    main()
