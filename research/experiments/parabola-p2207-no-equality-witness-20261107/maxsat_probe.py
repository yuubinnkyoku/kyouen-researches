"""How far is the parabola equality CNF from satisfiable?  (max-sat probe)

For a fixed d the equality CNF is UNSAT; here we ask for the minimum number of
violated edge clauses, i.e. whether a near-witness exists.  Each clause gets a
relaxation variable r_c (satisfied or r_c true) and an at-most-k cardinality
constraint over all r_c.  If the instance with k=1 is SAT, then removing the
points of the single violated quadruple yields a safe set of size h+1, i.e. a
lower bound A(p) >= h+1.

Usage: maxsat_probe.py <p> <d> [k]
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/experiments/structural-lemmas-2026-10-02/checks"))
sys.path.insert(0, str(ROOT / "research/experiments/parabola-equality-extension-2143-2500-20261107"))
from parabola_half_bound import clauses_for_pair  # noqa: E402
from probe_driver import run_gen  # noqa: E402
from pysat.card import CardEnc, EncType  # noqa: E402
from pysat.solvers import Cadical195  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"


def main() -> int:
    p = int(sys.argv[1])
    d = int(sys.argv[2])
    k = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    h = (p - 1) // 2
    budget = int(sys.argv[4]) if len(sys.argv) > 4 else 50_000_000
    OUT.mkdir(exist_ok=True)
    edges = run_gen(str(Path(__import__("os").environ["TEMP"]) / "forbidden_edges.exe"), p)
    base = list(clauses_for_pair(p, edges, d))
    top = h
    relax = []
    clauses = []
    for c in base:
        top += 1
        clauses.append(list(c) + [top])
        relax.append(top)
    card = CardEnc.atmost(lits=relax, bound=k, top_id=top, encoding=EncType.seqcounter)
    clauses.extend(card.clauses)
    print(f"p={p} d={d} base={len(base)} relax={len(relax)} k={k} vars={card.nv} "
          f"clauses={len(clauses)}", flush=True)
    solver = Cadical195(bootstrap_with=clauses)
    solver.conf_budget(budget)
    t0 = time.time()
    res = solver.solve_limited()
    dt = time.time() - t0
    model = solver.get_model() if res else None
    solver.delete()
    print(f"sat={res} secs={dt:.1f}", flush=True)
    record = {"p": p, "h": h, "d": d, "k": k, "base_clauses": len(base),
              "vars": card.nv, "clauses": len(clauses), "sat": res,
              "unknown": res is None, "seconds": round(dt, 1)}
    if res:
        pos = {i for i in model if i > 0}
        violated = [c for c in base if not any(
            (lit > 0) == (lit in pos) for lit in c)]
        chosen = {0}
        upper = {i for i in pos if i <= h}
        for i in range(1, h + 1):
            if i == d:
                chosen.update({d, p - d})
            else:
                chosen.add(i if i in upper else p - i)
        safe_set = set(chosen)
        removed = []
        for c in violated:
            for lit in c:
                pt = lit if lit > 0 else p - lit
                if pt in safe_set:
                    safe_set.discard(pt)
                    removed.append(pt)
                    break
        safe = not any(set(e) <= safe_set for e in edges)
        record.update({"violated_clauses": len(violated),
                       "violated": [list(c) for c in violated],
                       "removed_points": removed, "size_after": len(safe_set),
                       "safe_after_removal": safe})
        print(f"violated={len(violated)} size_after={len(safe_set)} safe={safe}", flush=True)
        if safe:
            (OUT / f"near_witness_{p}_{d}.json").write_text(
                json.dumps({**record, "points": sorted(safe_set)}, indent=2) + "\n",
                encoding="utf-8", newline="\n")
            return 0
    (OUT / f"maxsat_probe_{p}_{d}.json").write_text(json.dumps(record, indent=2) + "\n",
                                                    encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
