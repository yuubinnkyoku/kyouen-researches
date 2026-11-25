"""Screen candidates with the single size-h+2 CNF (one solve per prime).

For each prime p the class (x,c,e) = (1,1,0) encodes "the origin, one complete
pair and one element of every other pair", i.e. the equality sets.  UNSAT means
the equality fails; SAT yields a witness that is checked against the edge list.

Usage: screen_equality_single.py --ps 2539,2543 --budget 2000000
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/experiments/parabola-equality-extension-2143-2500-20261107"))
from probe_driver import run_gen  # noqa: E402
from search_shape_class import build  # noqa: E402
from pysat.solvers import Cadical195  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ps", required=True)
    ap.add_argument("--budget", type=int, default=2_000_000)
    ap.add_argument("--out", default="equality_single_screen.json")
    args = ap.parse_args()
    ps = [int(x) for x in args.ps.split(",") if x.strip()]
    OUT.mkdir(exist_ok=True)
    path = OUT / args.out
    results = []
    if path.exists():
        results = json.loads(path.read_text(encoding="utf-8"))
    done = {r["p"] for r in results}
    for p in ps:
        if p in done:
            print(f"p={p} already screened", flush=True)
            continue
        h = (p - 1) // 2
        size = h + 2
        t0 = time.time()
        edges = run_gen(str(Path(__import__("os").environ["TEMP"]) / "forbidden_edges.exe"), p)
        clauses, nv, kept = build(p, edges, 1, 1, 0)
        solver = Cadical195(bootstrap_with=clauses)
        solver.conf_budget(args.budget)
        res = solver.solve_limited()
        model = solver.get_model() if res else None
        solver.delete()
        rec = {"p": p, "h": h, "size": size, "vars": nv, "clauses": len(clauses),
               "sat": res, "unknown": res is None, "seconds": round(time.time() - t0, 1)}
        if res:
            pos = {i for i in model if i > 0}
            chosen = {0}
            for i in range(1, h + 1):
                B, N, L, H = 4 * i - 3, 4 * i - 2, 4 * i - 1, 4 * i
                if B in pos:
                    chosen.update({i, p - i})
                elif L in pos:
                    chosen.add(i)
                elif H in pos:
                    chosen.add(p - i)
            chosen = sorted(chosen)
            safe = not any(set(q) <= set(chosen) for q in edges)
            rec.update({"witness_size": len(chosen), "safe": safe, "points": chosen})
            print(f"p={p} SAT size={len(chosen)} safe={safe} ({rec['seconds']}s)", flush=True)
        else:
            print(f"p={p} res={res} ({rec['seconds']}s)", flush=True)
        results.append(rec)
        path.write_text(json.dumps(results, indent=1) + "\n", encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
