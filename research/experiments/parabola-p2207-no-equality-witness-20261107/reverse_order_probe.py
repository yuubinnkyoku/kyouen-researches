"""W11 H4 probe: does the easy-UNSAT set depend on shared learned clauses?

Re-solves selected d of the shape class (p=2647, size=1322, x=1,c=1,e=3) with the
SAME encoding (search_shape_class.build) and the SAME solver/budget
(Cadical195, 100k conflicts, assumption B_d) as the W7 ascending sweep.

Two modes:
  shared-reverse (default, task spec): ONE fresh Cadical195 instance, d solved in
      DESCENDING order [1322, 1000, 851, 500, 478, 300, 100, 1]. Easy-UNSAT d
      values are solved AFTER the hard ones, so ascending-accumulated clauses
      cannot help them; remaining learning is only descending-order history.
  fresh-each: a brand-new Cadical195 per d (zero prior history). Strongest
      available independence check for the easy-UNSAT values.

Output: output/w11-artifact-reverse.json (own file; sweep JSON never touched).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from search_shape_class import build  # noqa: E402

ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "research/experiments/parabola-equality-extension-2143-2500-20261107"))
from probe_driver import run_gen  # noqa: E402
from pysat.solvers import Cadical195  # noqa: E402

DS = [1322, 1000, 851, 500, 478, 300, 100, 1]
FRESH_DS = [851, 478, 300, 1]

P, SIZE, X, C, E = 2647, 1322, 1, 1, 3
BUDGET = 100_000


def v(pair: int, kind: str) -> int:
    return 4 * pair - 4 + {"B": 1, "N": 2, "L": 3, "H": 4}[kind]


def decode(model, p: int, h: int, x: int) -> list[int]:
    pos = {i for i in model if i > 0}
    chosen = {0} if x else set()
    for t in range(1, p):
        pair = t if t <= h else p - t
        lit = 4 * pair - 4 + (1 if t <= h else 4)
        if lit in pos:
            chosen.add(t)
    return sorted(chosen)


def solve_one(solver, d, p, h, x, edge_sets) -> dict:
    solver.conf_budget(BUDGET)
    t0 = time.time()
    res = solver.solve_limited(assumptions=[v(d, "B")])
    dt = time.time() - t0
    rec = {"d": d, "sat": res, "unknown": res is None,
           "seconds": round(dt, 3), "budget": BUDGET}
    if res:
        chosen = decode(solver.get_model(), p, h, x)
        cs = frozenset(chosen)
        safe = not any(q <= cs for q in edge_sets)
        rec.update({"witness_size": len(chosen),
                    "safe_against_edges": safe, "points": chosen})
    return rec


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["shared-reverse", "fresh-each"],
                    default="shared-reverse")
    ap.add_argument("--gen", default=None,
                    help="path to forbidden_edges.exe (default: $TEMP/forbidden_edges.exe)")
    ap.add_argument("--output", default=str(HERE / "output" / "w11-artifact-reverse.json"))
    args = ap.parse_args()

    h = (P - 1) // 2
    gen = args.gen or str(Path(os.environ["TEMP"]) / "forbidden_edges.exe")
    t_build = time.time()
    edges = run_gen(gen, P)
    edge_sets = [frozenset(q) for q in edges]
    clauses, nv, kept = build(P, edges, X, C, E)
    print(f"class vars={nv} clauses={len(clauses)} kept_edges={kept} "
          f"build={time.time() - t_build:.1f}s", flush=True)

    ds = DS if args.mode == "shared-reverse" else FRESH_DS
    out_path = Path(args.output)
    doc = {"p": P, "h": h, "size": SIZE, "class": [X, C, E], "budget": BUDGET,
           "mode": args.mode, "order": ds, "vars": nv, "clauses": len(clauses),
           "kept_edges": kept, "records": []}

    def flush() -> None:
        out_path.write_text(json.dumps(doc, indent=1) + "\n",
                            encoding="utf-8", newline="\n")

    flush()
    if args.mode == "shared-reverse":
        solver = Cadical195(bootstrap_with=clauses)
        try:
            for d in ds:
                rec = solve_one(solver, d, P, h, X, edge_sets)
                doc["records"].append(rec)
                flush()
                print(f"  d={d} sat={rec['sat']} unknown={rec['unknown']} "
                      f"secs={rec['seconds']}", flush=True)
                if rec["sat"]:
                    print("*** SAT FOUND ***", flush=True)
        finally:
            solver.delete()
    else:
        for d in ds:
            solver = Cadical195(bootstrap_with=clauses)
            try:
                rec = solve_one(solver, d, P, h, X, edge_sets)
            finally:
                solver.delete()
            doc["records"].append(rec)
            flush()
            print(f"  fresh d={d} sat={rec['sat']} unknown={rec['unknown']} "
                  f"secs={rec['seconds']}", flush=True)
            if rec["sat"]:
                print("*** SAT FOUND ***", flush=True)

    print(f"wrote {out_path} ({len(doc['records'])} records)", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
