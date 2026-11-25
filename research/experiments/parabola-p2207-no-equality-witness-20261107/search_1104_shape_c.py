"""Unified SAT search for h+1 point sets in Q_p (all shapes).

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

Usage:
  search_1104_shape_c.py <p> [budget]
  search_1104_shape_c.py <p> --write-cnf <path>     # dump DIMACS, do not solve
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
KINDS = {"B": 1, "N": 2, "L": 3, "H": 4}


def build(p: int, edges):
    """Shape (c) at size h+1: exactly one BOTH and exactly one NONE pair.

    Returns (clauses, nv, kept_edges, dropped_trapezoid_edges).
    """

    def v(pair, kind):
        return 4 * pair - 4 + KINDS[kind]

    h = (p - 1) // 2
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

    # auxiliary a_t: point t is selected  <=>  side_t or BOTH(pair(t))
    aux = card_n.nv
    for t in range(1, p):
        pair = t if t <= h else p - t
        s = v(pair, "L" if t <= h else "H")
        b = v(pair, "B")
        a = aux + t
        clauses.append([-a, s, b])
        clauses.append([a, -s])
        clauses.append([a, -b])
    trapezoid = 0
    kept = 0
    for q in edges:
        pts = [t for t in q if t != 0]
        pairs = [t if t <= h else p - t for t in pts]
        if len(set(pairs)) < len(pairs):
            # contains a complete pair: implied by the exactly-one-BOTH constraint
            trapezoid += 1
            continue
        clauses.append([-aux - t for t in pts])
        kept += 1
    return clauses, aux + p - 1, kept, trapezoid


def main() -> int:
    p = int(sys.argv[1]) if len(sys.argv) > 1 else 2207
    if "--write-cnf" in sys.argv:
        target = Path(sys.argv[sys.argv.index("--write-cnf") + 1])
        budget = None
    else:
        target = None
        budget = int(sys.argv[2]) if len(sys.argv) > 2 else 20_000_000
    h = (p - 1) // 2
    OUT.mkdir(exist_ok=True)
    edges = run_gen(str(Path(__import__("os").environ["TEMP"]) / "forbidden_edges.exe"), p)
    print(f"p={p} h={h} edges={len(edges)}", flush=True)
    clauses, nv, kept, trapezoid = build(p, edges)
    print(f"trapezoid clauses dropped: {trapezoid} kept={kept}", flush=True)
    print(f"vars={nv} clauses={len(clauses)}", flush=True)

    if target is not None:
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("w", encoding="ascii", newline="\n") as f:
            f.write(f"p cnf {nv} {len(clauses)}\n")
            for c in clauses:
                f.write(" ".join(map(str, c)) + " 0\n")
        print(f"wrote {target} ({target.stat().st_size} bytes)", flush=True)
        return 0

    solver = Cadical195(bootstrap_with=clauses)
    solver.conf_budget(budget)
    t0 = time.time()
    res = solver.solve_limited()
    model = solver.get_model() if res else None
    solver.delete()
    secs = time.time() - t0
    print(f"shape(c): sat={res} secs={secs:.1f}", flush=True)
    record = {"p": p, "h": h, "target_size": h + 1, "shape": "c",
              "vars": nv, "clauses": len(clauses), "kept_edges": kept,
              "trapezoid_edges_dropped": trapezoid, "budget": budget,
              "sat": bool(res), "unknown": res is None, "seconds": round(secs, 1)}
    if res:
        def v(pair, kind):
            return 4 * pair - 4 + KINDS[kind]

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
