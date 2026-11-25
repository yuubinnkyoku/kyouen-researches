"""Census of the equality question with ONE CNF per prime.

For size ``h+2`` the counting ``x + c - e = 2`` forces the single class
``(x, c, e) = (1, 1, 0)``: the origin, exactly one complete pair and one element
of every other pair.  So "does A(p) reach the general upper bound (p+3)/2?" is a
single SAT question per prime, not ``h`` of them -- that is the expensive part of
the per-``d`` scan.

Empirically the UNSAT side (an exception) is *fast* (p=2207: 19.9 s,
p=3719: 2.0 s, p=3727: seconds), while the SAT side can be slow because the
instance sits near the random 4-SAT threshold with a small witness density.
Hence this census is a filter:

  UNSAT within the budget  -> exception, worth certifying with
                              ``certify_equality_failure.py``
  SAT                      -> a witness of size h+2 (bound attained)
  unknown                  -> inconclusive; retry with a larger budget

Usage: census_h2_single_cnf.py --start 3501 --end 3900 [--budget 2000000]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "research/experiments/structural-lemmas-2026-10-02/checks"))
from edges_gen import run_edges  # noqa: E402
from quadratic_modular_barrier import prime  # noqa: E402
from search_shape_class import build  # noqa: E402
from pysat.solvers import Cadical195  # noqa: E402

OUT = HERE / "output"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=int, required=True)
    ap.add_argument("--end", type=int, required=True)
    ap.add_argument("--budget", type=int, default=2_000_000)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    out = Path(args.out) if args.out else OUT / f"h2_census_{args.start}_{args.end}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    records: list[dict] = []
    counts = {"sat": 0, "unsat": 0, "unknown": 0}
    for p in range(args.start | 1, args.end + 1, 2):
        if not prime(p):
            continue
        h = (p - 1) // 2
        edges = run_edges(p)
        clauses, nv, kept = build(p, edges, 1, 1, 0)
        solver = Cadical195(bootstrap_with=clauses)
        solver.conf_budget(args.budget)
        t0 = time.time()
        res = solver.solve_limited()
        model = solver.get_model() if res else None
        solver.delete()
        secs = time.time() - t0
        key = "sat" if res else ("unknown" if res is None else "unsat")
        counts[key] += 1
        rec = {"p": p, "h": h, "size": h + 2, "class": [1, 1, 0],
               "vars": nv, "clauses": len(clauses), "kept_edges": kept,
               "edges": len(edges), "result": key, "seconds": round(secs, 1)}
        if res:
            pos = {i for i in model if i > 0}
            chosen = {0}
            for i in range(1, h + 1):
                if 4 * i - 3 in pos:
                    chosen.update({i, p - i})
                elif 4 * i - 1 in pos:
                    chosen.add(i)
                elif 4 * i in pos:
                    chosen.add(p - i)
            chosen = sorted(chosen)
            rec["witness_size"] = len(chosen)
            rec["safe"] = not any(set(q) <= set(chosen) for q in edges)
            rec["complete"] = [i for i in range(1, h + 1) if 4 * i - 3 in pos]
            if rec["safe"]:
                rec["points"] = chosen
        records.append(rec)
        tmp = out.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8", newline="\n")
        os.replace(tmp, out)
        print(f"p={p:5d} h+2={h+2:5d} edges={len(edges):7d} kept={kept:6d} "
              f"{key:7s} {secs:8.1f}s", flush=True)
    print(json.dumps(counts), flush=True)
    summary = out.with_name(out.stem + "_summary.json")
    summary.write_text(json.dumps({
        "start": args.start, "end": args.end, "budget": args.budget, "counts": counts,
        "unsat_primes": [r["p"] for r in records if r["result"] == "unsat"],
        "unknown_primes": [r["p"] for r in records if r["result"] == "unknown"],
    }, indent=2) + "\n", encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
