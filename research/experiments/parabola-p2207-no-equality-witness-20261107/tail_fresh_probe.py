"""W17: is the "instant UNSAT" tail (d=1279..1316) a property of d itself?

The W7 ascending sweep (search_shape_class_assump.py) solved d=1..1323 inside ONE
Cadical195 instance.  From d=1279 to 1316 (38 consecutive values) every query was
UNSAT in 0.006..4.3 s, while d<=1278 was UNKNOWN at ~44 s/query.  Learning from
1,278 earlier queries may or may not be responsible; a single ascending run cannot
separate "d is intrinsically easy" from "the accumulated clause DB makes it easy".

This probe fixes the encoding (search_shape_class.build, class (1,1,3), p=2647,
size=1322) and the solver/budget (Cadical195, 100k conflicts, assumption B_d) and
removes the history: every d is solved in a BRAND-NEW instance with an empty
clause DB.  That is the strongest separation available within this
encoding+solver, exactly as in W11's fresh-each mode.

Extra per-record diagnostics (no extra solving):
  unit_conflict  -- did propagate(assumptions=[B_d]) already fail (pure UP)?
  conflicts/decisions/propagations -- Cadical statistics spent on this d alone.
These tell whether a fresh fast-UNSAT is a deep proof or a shallow propagation.

Output: output/w17-tail-fresh.json (own file; the sweep JSON is never written).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from search_shape_class import build  # noqa: E402

ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "research/experiments/parabola-equality-extension-2143-2500-20261107"))
from probe_driver import run_gen  # noqa: E402
from pysat.solvers import Cadical195  # noqa: E402

P, SIZE, X, C, E = 2647, 1322, 1, 1, 3
BUDGET = 100_000
WALL_LIMIT = 300.0

# tail interior + boundary + two controls outside the tail
DS = [1280, 1290, 1300, 1310, 1316, 1317, 1322, 1200]


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


def solve_fresh(clauses, d, p, h, x, edge_sets) -> dict:
    """Brand-new Cadical195 (empty history) for this single d."""
    t0 = time.time()
    solver = Cadical195(bootstrap_with=clauses)
    timer = threading.Timer(WALL_LIMIT, solver.interrupt)
    timer.daemon = True
    timer.start()
    try:
        up = solver.propagate(assumptions=[v(d, "B")])
        unit_conflict = up[0] is False
        stats0 = solver.accum_stats()
        solver.conf_budget(BUDGET)
        t1 = time.time()
        res = solver.solve_limited(assumptions=[v(d, "B")])
        dt = time.time() - t1
        stats1 = solver.accum_stats()
        rec = {
            "d": d,
            "sat": res,
            "unknown": res is None,
            "seconds": round(dt, 3),
            "budget": BUDGET,
            "unit_conflict": unit_conflict,
            "conflicts": stats1["conflicts"] - stats0["conflicts"],
            "decisions": stats1["decisions"] - stats0["decisions"],
            "propagations": stats1["propagations"] - stats0["propagations"],
            "wall_timeout": res is None and dt >= WALL_LIMIT - 1.0,
        }
        if res:
            chosen = decode(solver.get_model(), p, h, x)
            cs = frozenset(chosen)
            safe = not any(q <= cs for q in edge_sets)
            rec.update({"witness_size": len(chosen),
                        "safe_against_edges": safe, "points": chosen})
        rec["total_seconds"] = round(time.time() - t0, 3)
        return rec
    finally:
        timer.cancel()
        solver.delete()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gen", default=None,
                    help="path to forbidden_edges.exe (default: $TEMP/forbidden_edges.exe)")
    ap.add_argument("--output", default=str(HERE / "output" / "w17-tail-fresh.json"))
    args = ap.parse_args()

    h = (P - 1) // 2
    gen = args.gen or str(Path(os.environ["TEMP"]) / "forbidden_edges.exe")
    t_build = time.time()
    edges = run_gen(gen, P)
    edge_sets = [frozenset(q) for q in edges]
    clauses, nv, kept = build(P, edges, X, C, E)
    print(f"class vars={nv} clauses={len(clauses)} kept_edges={kept} "
          f"build={time.time() - t_build:.1f}s", flush=True)

    out_path = Path(args.output)
    doc = {"p": P, "h": h, "size": SIZE, "class": [X, C, E], "budget": BUDGET,
           "wall_limit": WALL_LIMIT, "mode": "fresh-each",
           "order": DS, "vars": nv, "clauses": len(clauses),
           "kept_edges": kept, "records": []}

    def flush() -> None:
        out_path.write_text(json.dumps(doc, indent=1) + "\n",
                            encoding="utf-8", newline="\n")

    flush()
    for d in DS:
        rec = solve_fresh(clauses, d, P, h, X, edge_sets)
        doc["records"].append(rec)
        flush()
        print(f"  fresh d={d} sat={rec['sat']} unknown={rec['unknown']} "
              f"secs={rec['seconds']} conf={rec['conflicts']} "
              f"dec={rec['decisions']} up_conflict={rec['unit_conflict']} "
              f"timeout={rec['wall_timeout']}", flush=True)
        if rec["sat"]:
            print("*** SAT FOUND ***", flush=True)

    print(f"wrote {out_path} ({len(doc['records'])} records)", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
