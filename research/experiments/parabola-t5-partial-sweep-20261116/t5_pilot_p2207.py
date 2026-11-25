"""W24/T5 pilot: partial 100k-budget d sweep on p=2207, class (1,1,3), size h-1.

Analogous to the p=2647 W21b setup (candidate-B class CNF + per-d assumption B_d).
Primary mode is fresh-each (brand-new Cadical195 per d) so the difficulty measured
is history-free and comparable across primes.  Output goes to a NEW path.
"""
from __future__ import annotations

import argparse, json, os, sys, threading, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = Path('/home/hatch/workspace/kyouen-omp/full/research/experiments/parabola-p2207-no-equality-witness-20261107')
sys.path.insert(0, str(SRC))
from search_shape_class import build  # noqa: E402
ROOT = SRC.parents[2]
sys.path.insert(0, str(ROOT / "research/experiments/parabola-equality-extension-2143-2500-20261107"))
from probe_driver import run_gen  # noqa: E402
from pysat.solvers import Cadical195  # noqa: E402

P, X, C, E = 2207, 1, 1, 3
H = (P - 1) // 2               # 1103
SIZE = H - 1                   # 1102
BUDGET = 100_000
WALL_LIMIT = 300.0

# tail (k=h-d small; k=0,6,7 bracket the p=2647 boundary k=6/7) + central spread
TAIL_KS = [0, 6, 7, 20, 44]
CENTRAL_DS = [276, 368, 551, 735, 827]
DS = [H - k for k in TAIL_KS] + CENTRAL_DS


def v(pair: int, kind: str) -> int:
    return 4 * pair - 4 + {"B": 1, "N": 2, "L": 3, "H": 4}[kind]


def decode(model, p: int, h: int, x: int) -> list[int]:
    pos = {i for i in model if i > 0}
    chosen = {0} if x else set()
    for i in range(1, h + 1):
        if v(i, "B") in pos:
            chosen.update({i, p - i})
        elif v(i, "L") in pos:
            chosen.add(i)
        elif v(i, "H") in pos:
            chosen.add(p - i)
    return sorted(chosen)


def solve_fresh(clauses, d, edge_sets) -> dict:
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
        rec = {"d": d, "k": H - d, "sat": res, "unknown": res is None,
               "seconds": round(dt, 3), "budget": BUDGET,
               "unit_conflict": unit_conflict,
               "conflicts": stats1["conflicts"] - stats0["conflicts"],
               "decisions": stats1["decisions"] - stats0["decisions"],
               "propagations": stats1["propagations"] - stats0["propagations"],
               "wall_timeout": res is None and dt >= WALL_LIMIT - 1.0}
        if res:
            chosen = decode(solver.get_model(), P, H, X)
            cs = frozenset(chosen)
            rec.update({"witness_size": len(chosen),
                        "safe_against_edges": not any(q <= cs for q in edge_sets),
                        "points": chosen})
        rec["total_seconds"] = round(time.time() - t0, 3)
        return rec
    finally:
        timer.cancel()
        solver.delete()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gen", default=None)
    ap.add_argument("--output", default=str(HERE / "output" / "t5-pilot-2207-1102.json"))
    args = ap.parse_args()
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    gen = args.gen or str(Path(os.environ["TEMP"]) / "forbidden_edges.exe")
    tb = time.time()
    edges = run_gen(gen, P)
    edge_sets = [frozenset(q) for q in edges]
    clauses, nv, kept = build(P, edges, X, C, E)
    print(f"p={P} h={H} size={SIZE} class=({X},{C},{E}) vars={nv} clauses={len(clauses)} "
          f"kept={kept} build={time.time()-tb:.1f}s", flush=True)

    doc = {"p": P, "h": H, "size": SIZE, "class": [X, C, E], "budget": BUDGET,
           "wall_limit": WALL_LIMIT, "mode": "fresh-each", "order": DS,
           "vars": nv, "clauses": len(clauses), "kept_edges": kept, "records": []}

    def flush():
        out_path.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8", newline="\n")

    flush()
    for d in DS:
        rec = solve_fresh(clauses, d, edge_sets)
        doc["records"].append(rec)
        flush()
        print(f"  fresh d={d} k={rec['k']} sat={rec['sat']} unk={rec['unknown']} "
              f"secs={rec['seconds']} conf={rec['conflicts']} up_conflict={rec['unit_conflict']} "
              f"timeout={rec['wall_timeout']}", flush=True)
        if rec["sat"]:
            print("*** SAT FOUND ***", flush=True)
    print(f"wrote {out_path} ({len(doc['records'])} records)", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
