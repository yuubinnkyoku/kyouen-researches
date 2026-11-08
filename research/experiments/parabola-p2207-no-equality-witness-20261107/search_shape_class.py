"""Single-CNF search for safe sets of a prescribed size class (x, c, e).

For size s the counting ``x + c + h - e = s`` (x = contains 0, c = complete
pairs, e = empty pairs) fixes the possible classes.  Each class is encoded with
4-valued pair variables {BOTH, NONE, LOW, HIGH}:

  exactly-one per pair, exactly ``c`` BOTH, exactly ``e`` NONE,
  point t selected  <=>  side_t or BOTH(pair t)      (auxiliary a_t),
  every forbidden quadruple not containing 0 (or containing it when x=0 is
  excluded) contributes  -a_t1 v ... v -a_tk.

Trapezoid edges (two complete pairs) are redundant because c <= 1.

Usage: search_shape_class.py <p> --size <s> [--x 0|1] [--c C] [--e E] [--budget N]
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
from pysat.card import CardEnc, EncType  # noqa: E402
from pysat.solvers import Cadical195  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"


def build(p: int, edges, x: int, c: int, e: int):
    h = (p - 1) // 2

    def v(pair, kind):
        base = 4 * pair - 4
        return base + {"B": 1, "N": 2, "L": 3, "H": 4}[kind]

    clauses = []
    for i in range(1, h + 1):
        B, N, L, H = v(i, "B"), v(i, "N"), v(i, "L"), v(i, "H")
        clauses.append([B, N, L, H])
        for a, b in ((B, N), (B, L), (B, H), (N, L), (N, H), (L, H)):
            clauses.append([-a, -b])
    top = 4 * h
    both = [v(i, "B") for i in range(1, h + 1)]
    none = [v(i, "N") for i in range(1, h + 1)]
    card_b = CardEnc.equals(lits=both, bound=c, top_id=top, encoding=EncType.seqcounter)
    clauses.extend(card_b.clauses)
    card_n = CardEnc.equals(lits=none, bound=e, top_id=card_b.nv, encoding=EncType.seqcounter)
    clauses.extend(card_n.clauses)
    aux = card_n.nv
    for t in range(1, p):
        pair = t if t <= h else p - t
        s = v(pair, "L" if t <= h else "H")
        b = v(pair, "B")
        a = aux + t
        clauses.append([-a, s, b])
        clauses.append([a, -s])
        clauses.append([a, -b])
    kept = 0
    for q in edges:
        if 0 in q and x == 0:
            continue
        pts = [t for t in q if t != 0]
        pairs = [t if t <= h else p - t for t in pts]
        if len(set(pairs)) < len(pairs):
            continue
        clauses.append([-aux - t for t in pts])
        kept += 1
    nv = aux + p - 1
    return clauses, nv, kept


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, required=True)
    ap.add_argument("--size", type=int, required=True)
    ap.add_argument("--x", type=int, default=None)
    ap.add_argument("--c", type=int, default=None)
    ap.add_argument("--e", type=int, default=None)
    ap.add_argument("--budget", type=int, default=20_000_000)
    args = ap.parse_args()
    p, h = args.p, (args.p - 1) // 2
    # enumerate classes with x + c + h - e = size
    classes = []
    for x in (0, 1):
        for c in range(0, 2):
            e = x + c + h - args.size
            if e < 0 or e > h - c:
                continue
            if args.x is not None and x != args.x:
                continue
            if args.c is not None and c != args.c:
                continue
            if args.e is not None and e != args.e:
                continue
            classes.append((x, c, e))
    if not classes:
        print("no admissible class", flush=True)
        return 1
    OUT.mkdir(exist_ok=True)
    edges = run_gen(str(Path(__import__("os").environ["TEMP"]) / "forbidden_edges.exe"), p)
    results = []
    for (x, c, e) in classes:
        clauses, nv, kept = build(p, edges, x, c, e)
        solver = Cadical195(bootstrap_with=clauses)
        solver.conf_budget(args.budget)
        t0 = time.time()
        res = solver.solve_limited()
        model = solver.get_model() if res else None
        solver.delete()
        dt = time.time() - t0
        rec = {"p": p, "h": h, "size": args.size, "class": [x, c, e],
               "vars": nv, "clauses": len(clauses), "kept_edges": kept,
               "sat": res, "unknown": res is None, "seconds": round(dt, 1)}
        print(f"p={p} size={args.size} class(x={x},c={c},e={e}) sat={res} "
              f"clauses={len(clauses)} secs={dt:.1f}", flush=True)
        if res:
            pos = {i for i in model if i > 0}
            chosen = {0} if x else set()

            def vv(pair, kind):
                return 4 * pair - 4 + {"B": 1, "N": 2, "L": 3, "H": 4}[kind]

            for i in range(1, h + 1):
                if vv(i, "B") in pos:
                    chosen.update({i, p - i})
                elif vv(i, "L") in pos:
                    chosen.add(i)
                elif vv(i, "H") in pos:
                    chosen.add(p - i)
            chosen = sorted(chosen)
            safe = not any(set(q) <= set(chosen) for q in edges)
            rec.update({"witness_size": len(chosen), "safe_against_edges": safe,
                        "points": chosen})
            print(f"  witness size={len(chosen)} safe={safe}", flush=True)
            if safe:
                (OUT / f"shape_class_witness_{p}_{args.size}.json").write_text(
                    json.dumps(rec, indent=2) + "\n", encoding="utf-8", newline="\n")
        results.append(rec)
    (OUT / f"shape_class_{p}_{args.size}.json").write_text(
        json.dumps(results, indent=2) + "\n", encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
