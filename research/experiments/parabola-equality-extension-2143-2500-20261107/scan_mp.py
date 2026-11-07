"""Multiprocess conflict-budget d-scan for one prime (no WSL, no GIL bound).

Each worker process rebuilds the forbidden-edge list from the shared file, builds
the CNF for its d, and solves with a CaDiCaL conflict budget.  The first SAT
model wins and the pool is terminated; unknown results are reported so a later
phase can retry them with a larger budget.
"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe_driver import run_gen  # noqa: E402
from parabola_half_bound import clauses_for_pair  # noqa: E402
from pysat.solvers import Cadical195  # noqa: E402


def _edges(path: str):
    with open(path, encoding="ascii") as f:
        return [tuple(map(int, line.split())) for line in f]


def _work(args):
    d, p, edges_path, budget = args
    edges = _edges(edges_path)
    clauses = clauses_for_pair(p, edges, d)
    solver = Cadical195(bootstrap_with=clauses)
    solver.conf_budget(budget)
    res = solver.solve_limited()
    model = solver.get_model() if res else None
    solver.delete()
    return d, res, model


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prime", type=int, required=True)
    ap.add_argument("--generator", required=True)
    ap.add_argument("--from-d", type=int, required=True)
    ap.add_argument("--to-d", type=int, default=1)
    ap.add_argument("--budget", type=int, default=200_000)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    p = args.prime
    h = (p - 1) // 2
    edges = run_gen(args.generator, p)
    edges_path = Path(tempfile.gettempdir()) / f"edges_{p}.txt"
    with edges_path.open("w", encoding="ascii") as f:
        for e in edges:
            f.write(" ".join(map(str, e)) + "\n")
    print(f"p={p} h={h} edges={len(edges)} range={args.from_d}..{args.to_d}", flush=True)

    tasks = [(d, p, str(edges_path), args.budget)
             for d in range(args.from_d, args.to_d - 1, -1)]
    unknown, done = [], 0
    t0 = time.time()
    with mp.Pool(processes=args.workers) as pool:
        for d, res, model in pool.imap_unordered(_work, tasks, chunksize=1):
            done += 1
            if res:
                upper = {i for i in model if i > 0}
                params = sorted([0, d, p - d] + [p - i if i in upper else i
                                                 for i in range(1, h + 1) if i != d])
                selected = set(params)
                safe = (len(params) == h + 2 and len(set(params)) == h + 2
                        and not any(set(e) <= selected for e in edges))
                rec = {"p": p, "attained": True, "double_pair": d,
                       "parameters": params, "size": len(params), "want": h + 2,
                       "safe_by_edges": safe, "forbidden_edges": len(edges),
                       "doubles_tried": [d], "unknown_timeouts": []}
                Path(args.out).write_text(json.dumps([rec], indent=2) + "\n",
                                          encoding="utf-8", newline="\n")
                print(f"SAT d={d} safe={safe} elapsed={time.time()-t0:.0f}s", flush=True)
                pool.terminate()
                return 0
            if res is None:
                unknown.append(d)
            if done % 25 == 0:
                print(f"progress {done}/{len(tasks)} unknown={len(unknown)} "
                      f"elapsed={time.time()-t0:.0f}s", flush=True)
    Path(args.out).write_text(json.dumps([{
        "p": p, "attained": False, "scanned": done, "budget": args.budget,
        "unknown": sorted(unknown), "status": "phase_done"}], indent=2) + "\n",
        encoding="utf-8", newline="\n")
    print(f"no SAT; unknown={len(unknown)} elapsed={time.time()-t0:.0f}s", flush=True)
    return 0


if __name__ == "__main__":
    mp.freeze_support()
    raise SystemExit(main())
