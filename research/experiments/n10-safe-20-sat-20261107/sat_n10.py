"""SAT search for a safe 20-point set on the 10x10 grid (K0141).

Variables 1..100 are the grid points; a forbidden quadruple contributes the
clause (not a or not b or not c or not d); a sequential-counter cardinality
constraint asks for at least 20 selected points.  Any model is re-checked with
an independent 4x4 determinant, so a reported witness is a genuine safe set.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from itertools import combinations
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical195, Glucose4, Minisat22

HERE = Path(__file__).resolve().parent
V = 100


def det4(q) -> int:
    pts = [(p % 10, p // 10) for p in q]
    x, y = pts[0]
    rows = [(a - x, b - y, (a - x) ** 2 + (b - y) ** 2) for a, b in pts[1:]]
    (a1, b1, c1), (a2, b2, c2), (a3, b3, c3) = rows
    return (a1 * (b2 * c3 - c2 * b3)
            - b1 * (a2 * c3 - c2 * a3)
            + c1 * (a2 * b3 - b2 * a3))


def verify(points: list[int]) -> bool:
    for q in combinations(points, 4):
        if det4(q) == 0:
            return False
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--atleast", type=int, default=20)
    ap.add_argument("--budget", type=int, default=50_000_000)
    ap.add_argument("--solver", default="cadical")
    ap.add_argument("--out", default=str(HERE / "output" / "n10_safe20_result.json"))
    args = ap.parse_args()

    quads = [tuple(map(int, line.split()))
             for line in (HERE / "output_quads.txt").read_text().splitlines()]
    clauses = [[-(p + 1) for p in q] for q in quads]
    card = CardEnc.atleast(lits=list(range(1, V + 1)), bound=args.atleast,
                           top_id=V, encoding=EncType.seqcounter)
    clauses.extend(card.clauses)
    print(f"quads={len(quads)} clauses={len(clauses)} vars={card.nv} "
          f"atleast={args.atleast}", flush=True)

    if args.solver == "cadical":
        solver = Cadical195(bootstrap_with=clauses)
        solver.conf_budget(args.budget)
    elif args.solver == "glucose":
        solver = Glucose4(bootstrap_with=clauses)
    else:
        solver = Minisat22(bootstrap_with=clauses)
    t0 = time.time()
    res = solver.solve_limited()
    dt = time.time() - t0
    model = solver.get_model() if res else None
    solver.delete()
    print(f"solver={args.solver} result={res} secs={dt:.1f}", flush=True)
    record = {"atleast": args.atleast, "solver": args.solver, "budget": args.budget,
              "result": res, "seconds": round(dt, 1), "quads": len(quads),
              "clauses": len(clauses)}
    if res:
        chosen = [i - 1 for i in model if 0 < i <= V]
        record.update({"size": len(chosen), "points": sorted(chosen),
                       "safe_exact": verify(chosen)})
        print("size", len(chosen), "safe", record["safe_exact"], flush=True)
        if record["safe_exact"]:
            Path(args.out).write_text(json.dumps(record, indent=2) + "\n",
                                      encoding="utf-8", newline="\n")
            return 0
    Path(args.out).write_text(json.dumps(record, indent=2) + "\n",
                              encoding="utf-8", newline="\n")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
