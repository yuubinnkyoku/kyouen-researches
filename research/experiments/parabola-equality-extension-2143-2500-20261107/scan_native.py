"""Native Cadical195 d-scan using conflict budgets (no timers, no WSL).

``pysat``'s CaDiCaL wrapper does not support ``interrupt``, but it supports
``conf_budget``: ``solve_limited`` then returns True (model), False (UNSAT) or
None (budget exhausted).  That makes the scan deterministic and robust: easy
UNSAT instances are refuted, SAT instances are found, and hard ones are
reported as budget-unknown for a later, larger phase.

Phases are separate invocations with ``--budget`` (conflicts) and
``--skip-file`` (d values already decided UNSAT by an earlier phase).
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe_driver import run_gen  # noqa: E402
from parabola_half_bound import clauses_for_pair  # noqa: E402
from pysat.solvers import Cadical195  # noqa: E402


def solve(clauses: list[list[int]], conflicts: int):
    solver = Cadical195(bootstrap_with=clauses)
    solver.conf_budget(conflicts)
    ok = solver.solve_limited()
    model = solver.get_model() if ok else None
    solver.delete()
    return ok, model


def witness(p: int, d: int, model: list[int], edges, h: int):
    upper = {i for i in model if i > 0}
    params = sorted([0, d, p - d] + [p - i if i in upper else i
                                     for i in range(1, h + 1) if i != d])
    selected = set(params)
    safe = (len(params) == h + 2 and len(set(params)) == h + 2
            and not any(set(e) <= selected for e in edges))
    return {"p": p, "attained": True, "double_pair": d, "parameters": params,
            "size": len(params), "want": h + 2, "safe_by_edges": safe,
            "forbidden_edges": len(edges), "doubles_tried": [d]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prime", type=int, required=True)
    ap.add_argument("--generator", required=True)
    ap.add_argument("--from-d", type=int, required=True)
    ap.add_argument("--to-d", type=int, default=1)
    ap.add_argument("--budget", type=int, default=100_000, help="conflict budget")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--skip-file", default=None, help="JSON list of d already decided UNSAT")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    p = args.prime
    h = (p - 1) // 2
    edges = run_gen(args.generator, p)
    skip = set(json.loads(Path(args.skip_file).read_text())) if args.skip_file else set()
    todo = [d for d in range(args.from_d, args.to_d - 1, -1) if d not in skip]
    print(f"p={p} h={h} edges={len(edges)} todo={len(todo)} budget={args.budget}", flush=True)

    def job(d: int):
        clauses = clauses_for_pair(p, edges, d)
        t0 = time.time()
        ok, model = solve(clauses, args.budget)
        return d, ok, model, time.time() - t0

    unknown, done = [], 0
    t_start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = {ex.submit(job, d): d for d in todo}
        for fut in concurrent.futures.as_completed(futures):
            d, ok, model, dt = fut.result()
            done += 1
            if ok:
                rec = witness(p, d, model, edges, h)
                Path(args.out).write_text(json.dumps([rec], indent=2) + "\n",
                                          encoding="utf-8", newline="\n")
                print(f"SAT d={d} safe={rec['safe_by_edges']} secs={dt:.2f}", flush=True)
                return 0
            if ok is None:
                unknown.append(d)
            if done % 20 == 0:
                print(f"progress done={done}/{len(todo)} unknown={len(unknown)} "
                      f"elapsed={time.time()-t_start:.0f}s", flush=True)
    Path(args.out).write_text(json.dumps([{
        "p": p, "attained": False, "scanned": done, "budget": args.budget,
        "unknown": sorted(unknown), "status": "phase_done"}], indent=2) + "\n",
        encoding="utf-8", newline="\n")
    print(f"phase done: no SAT; unknown={len(unknown)} elapsed={time.time()-t_start:.0f}s", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
