"""Scan all d for a one-violation near-witness (k=1 max-sat probes).

If for some d a single edge clause can be violated, deleting one point of that
quadruple yields a safe set of size h+1 = 1104, i.e. a verified lower bound.
This is an independent route to the shape-(c) question (which the single-CNF
encoding could not settle).

Usage: scan_maxsat_k1.py <p> [workers] [budget]
"""
from __future__ import annotations

import json
import multiprocessing as mp
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/experiments/structural-lemmas-2026-10-02/checks"))
sys.path.insert(0, str(ROOT / "research/experiments/parabola-equality-extension-2143-2500-20261107"))
from parabola_half_bound import clauses_for_pair  # noqa: E402
from probe_driver import run_gen  # noqa: E402
from pysat.card import CardEnc, EncType  # noqa: E402
from pysat.solvers import Cadical195  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
TMP = Path(tempfile.gettempdir()) / "p2207_drat"


def work(args):
    p, d, budget, edges_path = args
    with open(edges_path, encoding="ascii") as f:
        edges = [tuple(map(int, line.split())) for line in f]
    h = (p - 1) // 2
    base = list(clauses_for_pair(p, edges, d))
    top = h
    relax = []
    clauses = []
    for c in base:
        top += 1
        clauses.append(list(c) + [top])
        relax.append(top)
    card = CardEnc.atmost(lits=relax, bound=1, top_id=top, encoding=EncType.seqcounter)
    clauses.extend(card.clauses)
    solver = Cadical195(bootstrap_with=clauses)
    solver.conf_budget(budget)
    res = solver.solve_limited()
    model = solver.get_model() if res else None
    solver.delete()
    return d, res, model


def main() -> int:
    p = int(sys.argv[1]) if len(sys.argv) > 1 else 2207
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    budget = int(sys.argv[3]) if len(sys.argv) > 3 else 2_000_000
    h = (p - 1) // 2
    OUT.mkdir(exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    edges_path = TMP / f"edges_{p}.txt"
    if not edges_path.exists():
        edges = run_gen(str(Path(__import__("os").environ["TEMP"]) / "forbidden_edges.exe"), p)
        edges_path.write_text("".join(" ".join(map(str, e)) + "\n" for e in edges),
                              encoding="ascii")
    with edges_path.open(encoding="ascii") as f:
        edges = [tuple(map(int, line.split())) for line in f]
    print(f"p={p} h={h} edges={len(edges)} tasks={h}", flush=True)
    tasks = [(p, d, budget, str(edges_path)) for d in range(1, h + 1)]
    t0 = time.time()
    done, sat_d = 0, None
    with mp.Pool(processes=workers) as pool:
        for d, res, model in pool.imap_unordered(work, tasks, chunksize=1):
            done += 1
            if res:
                sat_d = d
                pos = {i for i in model if i > 0}
                upper = {i for i in pos if i <= h}
                chosen = {0}
                for i in range(1, h + 1):
                    if i == d:
                        chosen.update({d, p - d})
                    else:
                        chosen.add(i if i in upper else p - i)
                removed = []
                safe_set = set(chosen)
                for c in list(clauses_for_pair(p, edges, d)):
                    if not any((lit > 0) == (lit in pos) for lit in c):
                        for lit in c:
                            pt = lit if lit > 0 else p - lit
                            if pt in safe_set:
                                safe_set.discard(pt)
                                removed.append(pt)
                                break
                safe = not any(set(e) <= safe_set for e in edges)
                rec = {"p": p, "d": d, "removed": removed, "size": len(safe_set),
                       "safe_against_edges": safe, "points": sorted(safe_set)}
                print(f"SAT d={d} size={len(safe_set)} safe={safe}", flush=True)
                (OUT / f"maxsat_k1_witness_{p}.json").write_text(
                    json.dumps(rec, indent=2) + "\n", encoding="utf-8", newline="\n")
                pool.terminate()
                break
            if done % 50 == 0:
                print(f"progress {done}/{h} elapsed={time.time()-t0:.0f}s", flush=True)
    print(f"done={done} sat_d={sat_d} elapsed={time.time()-t0:.0f}s", flush=True)
    (OUT / f"maxsat_k1_scan_{p}.json").write_text(
        json.dumps({"p": p, "done": done, "sat_d": sat_d,
                    "seconds": round(time.time() - t0, 1)}, indent=2) + "\n",
        encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    mp.freeze_support()
    raise SystemExit(main())
