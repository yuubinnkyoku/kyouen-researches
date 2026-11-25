"""Single-CNF search for size h+1 sets of shape (b) at one prime.

Shape (b): no origin, one complete pair {d, p-d}, one element of every other
pair.  Encoding: each pair chooses BOTH / LOW / HIGH (no NONE), exactly one
BOTH; point t is selected iff side_t or BOTH(pair t) (auxiliary a_t); every
forbidden quadruple *not containing 0* contributes a clause over the a_t.

A model is turned into a set and checked against the full forbidden-edge list.

Usage: search_1104_shape_b.py <p> [budget]
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/experiments/parabola-equality-extension-2143-2500-20261107"))
from probe_driver import run_gen  # noqa: E402
from pysat.card import CardEnc, EncType  # noqa: E402
from pysat.solvers import Cadical195  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"


def main() -> int:
    p = int(sys.argv[1])
    h = (p - 1) // 2
    budget = int(sys.argv[2]) if len(sys.argv) > 2 else 20_000_000
    OUT.mkdir(exist_ok=True)
    edges = run_gen(str(Path(__import__("os").environ["TEMP"]) / "forbidden_edges.exe"), p)

    def v(pair, kind):
        base = 3 * pair - 3
        return base + {"B": 1, "L": 2, "H": 3}[kind]

    clauses = []
    for i in range(1, h + 1):
        B, L, H = v(i, "B"), v(i, "L"), v(i, "H")
        clauses.append([B, L, H])
        clauses.append([-B, -L])
        clauses.append([-B, -H])
        clauses.append([-L, -H])
    card = CardEnc.equals(lits=[v(i, "B") for i in range(1, h + 1)], bound=1,
                          top_id=3 * h, encoding=EncType.seqcounter)
    clauses.extend(card.clauses)
    aux = card.nv
    for t in range(1, p):
        pair = t if t <= h else p - t
        s = v(pair, "L" if t <= h else "H")
        b = v(pair, "B")
        a = aux + t
        clauses.append([-a, s, b])
        clauses.append([a, -s])
        clauses.append([a, -b])
    kept = dropped_trap = dropped_origin = 0
    for q in edges:
        pts = [t for t in q if t != 0]
        if len(pts) < len(q):
            dropped_origin += 1
            continue
        pairs = [t if t <= h else p - t for t in pts]
        if len(set(pairs)) < len(pairs):
            dropped_trap += 1
            continue
        clauses.append([-aux - t for t in pts])
        kept += 1
    nv = aux + p - 1
    print(f"p={p} h={h} edges={len(edges)} kept={kept} dropped_trap={dropped_trap} "
          f"dropped_origin={dropped_origin} vars={nv} clauses={len(clauses)}", flush=True)
    solver = Cadical195(bootstrap_with=clauses)
    solver.conf_budget(budget)
    t0 = time.time()
    res = solver.solve_limited()
    model = solver.get_model() if res else None
    solver.delete()
    print(f"shape(b): sat={res} secs={time.time()-t0:.1f}", flush=True)
    record = {"p": p, "h": h, "shape": "b", "vars": nv, "clauses": len(clauses),
              "kept_edges": kept, "sat": res, "unknown": res is None,
              "seconds": round(time.time() - t0, 1), "target_size": h + 1}
    if res:
        pos = {i for i in model if i > 0}
        chosen = set()
        for i in range(1, h + 1):
            if v(i, "B") in pos:
                chosen.update({i, p - i})
            elif v(i, "L") in pos:
                chosen.add(i)
            elif v(i, "H") in pos:
                chosen.add(p - i)
        chosen = sorted(chosen)
        safe = not any(set(e) <= set(chosen) for e in edges)
        record.update({"size": len(chosen), "safe_against_edges": safe, "points": chosen})
        print(f"size={len(chosen)} safe={safe}", flush=True)
    (OUT / f"shape_b_single_{p}.json").write_text(json.dumps(record, indent=2) + "\n",
                                                  encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
