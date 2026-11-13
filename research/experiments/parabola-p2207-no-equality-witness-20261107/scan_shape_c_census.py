"""Census: is the shape-(c) instance at size h+1 satisfiable for small primes?

Shape (c) is the class (x, c, e) = (1, 1, 1): 0, exactly one complete pair, one
empty pair, one element from each remaining pair.  It is the only class of size
h+1 that is satisfiable for p=2207 (witness of 1104 points, K0722) and it is
UNSAT for p=2647 (8.2 s).  This script decides the same instance for every odd
prime in a range, to see how special the UNSAT cases are.

Usage: scan_shape_c_census.py [--start 5] [--end 1001] [--budget 200000]
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
sys.path.insert(0, str(ROOT / "research/experiments/parabola-equality-extension-2143-2500-20261107"))
sys.path.insert(0, str(ROOT / "research/experiments/structural-lemmas-2026-10-02/checks"))
from edges_gen import run_edges  # noqa: E402
from quadratic_modular_barrier import prime  # noqa: E402
from search_1104_shape_c import build  # noqa: E402
from pysat.solvers import Cadical195  # noqa: E402

OUT = HERE / "output"


def save(path: Path, records: list[dict]) -> None:
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8", newline="\n")
    os.replace(tmp, path)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=int, default=5)
    ap.add_argument("--end", type=int, default=1001)
    ap.add_argument("--budget", type=int, default=200_000)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    out = Path(args.out) if args.out else OUT / f"shape_c_census_{args.start}_{args.end}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    gen = str(Path(os.environ["TEMP"]) / "forbidden_edges.exe")
    records: list[dict] = []
    counts = {"sat": 0, "unsat": 0, "unknown": 0}
    for p in range(args.start | 1, args.end + 1, 2):
        if not prime(p):
            continue
        h = (p - 1) // 2
        edges = run_edges(p)
        clauses, nv, kept, trapezoid = build(p, edges)
        solver = Cadical195(bootstrap_with=clauses)
        solver.conf_budget(args.budget)
        t0 = time.time()
        res = solver.solve_limited()
        solver.delete()
        secs = time.time() - t0
        key = "sat" if res else ("unknown" if res is None else "unsat")
        counts[key] += 1
        records.append({"p": p, "h": h, "size": h + 1, "shape": "c",
                        "vars": nv, "clauses": len(clauses), "kept_edges": kept,
                        "trapezoid_edges_dropped": trapezoid,
                        "edges": len(edges), "result": key,
                        "seconds": round(secs, 2)})
        print(f"p={p:5d} h+1={h+1:5d} edges={len(edges):6d} kept={kept:6d} "
              f"{key:7s} {secs:8.2f}s", flush=True)
        save(out, records)
    print(json.dumps(counts), flush=True)
    summary = out.with_name(out.stem + "_summary.json")
    summary.write_text(json.dumps({"start": args.start, "end": args.end,
                                   "budget": args.budget, "counts": counts,
                                   "unsat_primes": [r["p"] for r in records
                                                    if r["result"] == "unsat"],
                                   "unknown_primes": [r["p"] for r in records
                                                      if r["result"] == "unknown"]},
                                  indent=2) + "\n", encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
