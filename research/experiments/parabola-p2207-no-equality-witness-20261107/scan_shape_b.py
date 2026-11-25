"""Decide whether Q_2207 has a safe set of size h+1 = 1104.

Sizes h+1 have exactly two shapes:
  (a) 0 plus one element of every pair, no complete pair;
  (b) no 0, one complete pair {d, p-d} plus one element of every other pair.

Shape (a) is the CNF ``clauses_for_pair(p, edges, 0)`` (double = 0 means no pair
is fixed).  Shape (b) is ``clauses_for_pair(p, edges_without_origin, d)`` for
each d.  A SAT model is turned into a set and checked against the full
forbidden-edge list, so a reported witness is a genuine safe set.
"""
from __future__ import annotations

import json
import multiprocessing as mp
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/experiments/structural-lemmas-2026-10-02/checks"))
sys.path.insert(0, str(ROOT / "research/experiments/parabola-equality-extension-2143-2500-20261107"))
from parabola_half_bound import clauses_for_pair  # noqa: E402
from probe_driver import run_gen  # noqa: E402
from pysat.solvers import Cadical195  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"


def read_edges(path: str):
    with open(path, encoding="ascii") as f:
        return [tuple(map(int, line.split())) for line in f]


def solve(clauses, budget: int):
    solver = Cadical195(bootstrap_with=list(clauses))
    solver.conf_budget(budget)
    res = solver.solve_limited()
    model = solver.get_model() if res else None
    solver.delete()
    return res, model


def work(args):
    p, path, d, budget = args
    edges = read_edges(path)
    clauses = list(clauses_for_pair(p, edges, d))
    res, model = solve(clauses, budget)
    return d, res, model


def main() -> int:
    p = int(sys.argv[1]) if len(sys.argv) > 1 else 2207
    h = (p - 1) // 2
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    budget = int(sys.argv[3]) if len(sys.argv) > 3 else 2_000_000
    OUT.mkdir(exist_ok=True)
    edges = run_gen(str(Path(os.environ["TEMP"]) / "forbidden_edges.exe"), p)
    all_path = OUT / f"edges_all_{p}.txt"
    no0_path = OUT / f"edges_no0_{p}.txt"
    all_path.write_text("".join(" ".join(map(str, e)) + "\n" for e in edges), encoding="ascii")
    no_origin = [e for e in edges if 0 not in e]
    no0_path.write_text("".join(" ".join(map(str, e)) + "\n" for e in no_origin), encoding="ascii")
    print(f"p={p} h={h} edges={len(edges)} no_origin={len(no_origin)}", flush=True)

    record = {"p": p, "h": h, "target_size": h + 1,
              "edges_all": len(edges), "edges_no_origin": len(no_origin)}

    # shape (a): 0 plus one of each pair, no complete pair
    t0 = time.time()
    clauses_a = list(clauses_for_pair(p, edges, 0))
    res_a, model_a = solve(clauses_a, budget)
    record["shape_a"] = {"sat": bool(res_a), "unknown": res_a is None,
                         "clauses": len(clauses_a), "seconds": round(time.time() - t0, 1)}
    print(f"shape(a): sat={res_a} clauses={len(clauses_a)} ({time.time()-t0:.1f}s)", flush=True)
    if res_a:
        pos = {i for i in model_a if i > 0}
        chosen = sorted({0} | {i if i in pos else p - i for i in range(1, h + 1)})
        safe = not any(set(e) <= set(chosen) for e in edges)
        record["witness"] = {"shape": "a", "size": len(chosen), "points": chosen,
                             "safe_against_edges": safe}
        (OUT / f"shape_a_{p}.json").write_text(json.dumps(record, indent=2) + "\n",
                                              encoding="utf-8", newline="\n")
        return 0

    # shape (b): no 0, one complete pair d plus one of each other pair
    lo = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    hi = int(sys.argv[5]) if len(sys.argv) > 5 else h
    tasks = [(p, str(no0_path), d, budget) for d in range(lo, hi + 1)]
    found, unknown, done = None, [], 0
    t1 = time.time()
    with mp.Pool(processes=workers) as pool:
        for d, res, model in pool.imap_unordered(work, tasks, chunksize=1):
            done += 1
            if res:
                found = (d, model)
                pool.terminate()
                break
            if res is None:
                unknown.append(d)
            if done % 50 == 0:
                print(f"progress {done}/{h} unknown={len(unknown)} elapsed={time.time()-t1:.0f}s",
                      flush=True)
    record["shape_b"] = {"d_range": [lo, hi], "done": done, "unknown": sorted(unknown),
                         "seconds": round(time.time() - t1, 1), "sat_d": found[0] if found else None}
    print(f"shape(b): done={done} found={bool(found)} unknown={len(unknown)} "
          f"({time.time()-t1:.0f}s)", flush=True)
    if found:
        d, model = found
        pos = {i for i in model if i > 0}
        chosen = sorted({d, p - d} | {i if i in pos else p - i
                                      for i in range(1, h + 1) if i != d})
        safe = not any(set(e) <= set(chosen) for e in edges)
        record["witness"] = {"shape": "b", "d": d, "size": len(chosen),
                             "points": chosen, "safe_against_edges": safe}
        print(f"witness shape=b d={d} size={len(chosen)} safe={safe}", flush=True)
    (OUT / f"shape_b_{p}.json").write_text(json.dumps(record, indent=2) + "\n",
                                           encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    mp.freeze_support()
    raise SystemExit(main())
