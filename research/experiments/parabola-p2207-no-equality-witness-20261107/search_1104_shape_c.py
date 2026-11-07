"""Unified SAT search for h+1 = 1104 point sets in Q_2207 (all shapes).

For size h+1 the counting x + c - e = 1 (x = contains 0, c = complete pairs,
e = empty pairs) leaves three shapes:
  (a) x=1, c=0, e=0   (0 plus one element of every pair),
  (b) x=0, c=1, e=0   (one complete pair, no 0),
  (c) x=1, c=1, e=1   (0, one complete pair, one pair omitted).
The two earlier scans covered (a) and (b); this script covers (c) with a single
encoding: each pair chooses one of {BOTH, NONE, LOW, HIGH} with exactly one BOTH
and exactly one NONE, and every forbidden quadruple contributes a clause that
forbids all its points being selected.

A model is turned into a set and checked against the full forbidden-edge list,
so a reported witness is a genuine safe set.
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
    p = int(sys.argv[1]) if len(sys.argv) > 1 else 2207
    h = (p - 1) // 2
    budget = int(sys.argv[2]) if len(sys.argv) > 2 else 20_000_000
    OUT.mkdir(exist_ok=True)
    edges = run_gen(str(Path(__import__("os").environ["TEMP"]) / "forbidden_edges.exe"), p)
    print(f"p={p} h={h} edges={len(edges)}", flush=True)

    # variable layout: pair i (1..h) -> B=4i-3, N=4i-2, L=4i-1, H=4i
    def v(pair, kind):
        base = 4 * pair - 4
        return base + {"B": 1, "N": 2, "L": 3, "H": 4}[kind]

    def side_var(point):
        pair = point if point <= h else p - point
        return v(pair, "L" if point <= h else "H"), v(pair, "B")

    clauses = []
    for i in range(1, h + 1):
        B, N, L, H = v(i, "B"), v(i, "N"), v(i, "L"), v(i, "H")
        clauses.append([B, N, L, H])
        for a, b in ((B, N), (B, L), (B, H), (N, L), (N, H), (L, H)):
            clauses.append([-a, -b])
    top = 4 * h
    both = [v(i, "B") for i in range(1, h + 1)]
    none = [v(i, "N") for i in range(1, h + 1)]
    card_b = CardEnc.equals(lits=both, bound=1, top_id=top, encoding=EncType.seqcounter)
    card_n = CardEnc.equals(lits=none, bound=1, top_id=card_b.nv, encoding=EncType.seqcounter)
    clauses.extend(card_b.clauses)
    clauses.extend(card_n.clauses)
    nv = card_n.nv

    # auxiliary a_t: point t is selected  <=>  side_t or BOTH(pair(t))
    aux = nv
    for t in range(1, p):
        pair = t if t <= h else p - t
        s = v(pair, "L" if t <= h else "H")
        b = v(pair, "B")
        a = aux + t
        clauses.append([-a, s, b])
        clauses.append([a, -s])
        clauses.append([a, -b])
    trapezoid = 0
    for q in edges:
        pts = [t for t in q if t != 0]
        pairs = [t if t <= h else p - t for t in pts]
        if len(set(pairs)) < len(pairs):
            # contains a complete pair: implied by the exactly-one-BOTH constraint
            trapezoid += 1
            continue
        clauses.append([-aux - t for t in pts])
    print(f"trapezoid clauses dropped: {trapezoid}", flush=True)
    nv = aux + p - 1
    print(f"vars={nv} clauses={len(clauses)}", flush=True)

    solver = Cadical195(bootstrap_with=clauses)
    solver.conf_budget(budget)
    t0 = time.time()
    res = solver.solve_limited()
    model = solver.get_model() if res else None
    solver.delete()
    print(f"shape(c): sat={res} secs={time.time()-t0:.1f}", flush=True)
    record = {"p": p, "h": h, "target_size": h + 1, "shape": "c",
              "vars": nv, "clauses": len(clauses), "sat": bool(res),
              "unknown": res is None, "seconds": round(time.time() - t0, 1)}
    if res:
        pos = {i for i in model if i > 0}
        chosen = {0}
        for i in range(1, h + 1):
            if v(i, "B") in pos:
                chosen.update({i, p - i})
            elif v(i, "L") in pos:
                chosen.add(i)
            elif v(i, "H") in pos:
                chosen.add(p - i)
        chosen = sorted(chosen)
        safe = not any(set(e) <= set(chosen) for e in edges)
        complete = [i for i in range(1, h + 1) if v(i, "B") in pos]
        empty = [i for i in range(1, h + 1) if v(i, "N") in pos]
        record.update({"size": len(chosen), "safe_against_edges": safe,
                       "complete": complete, "empty": empty, "points": chosen})
        print(f"size={len(chosen)} safe={safe} complete={complete} empty={empty}", flush=True)
    (OUT / f"shape_c_{p}.json").write_text(json.dumps(record, indent=2) + "\n",
                                           encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
