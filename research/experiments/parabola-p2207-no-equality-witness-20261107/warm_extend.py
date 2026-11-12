"""Step a greedy safe set upward one point at a time with warm-started SAT.

Each step asks for size `s+1`.  For size `s+1` the earlier count `x+c-e = s+1-h`
fixes the class once the shape family is chosen; the walker's sets are always
`(1,1,e)`, so the next target is class (1, 1, e-1) as long as the solver keeps
that family.  The current best set is supplied as solver phases, so CaDiCaL
searches around it instead of from scratch.

A SAT answer is audited (edge containment + independent integer verifier) before
it replaces the incumbent.

Usage: warm_extend.py --p 2531 --witness witness.json [--steps 5] [--budget 2000000]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "research/experiments/parabola-equality-extension-2143-2500-20261107"))
from probe_driver import run_gen  # noqa: E402
from pysat.card import CardEnc, EncType  # noqa: E402
from pysat.solvers import Cadical195  # noqa: E402

KINDS = {"B": 1, "N": 2, "L": 3, "H": 4}


def build(p: int, edges, x: int, c: int, e: int):
    h = (p - 1) // 2

    def v(pair, kind):
        return 4 * pair - 4 + KINDS[kind]

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
    top = max(top, card_b.nv)
    card_n = CardEnc.equals(lits=none, bound=e, top_id=top, encoding=EncType.seqcounter)
    clauses.extend(card_n.clauses)
    aux = max(top, card_n.nv)
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
        pts = [t for t in q if t != 0]
        pairs = [t if t <= h else p - t for t in pts]
        if len(set(pairs)) < len(pairs):
            continue
        clauses.append([-aux - t for t in pts])
        kept += 1
    return clauses, aux + p - 1, kept


def classify(points, p):
    h = (p - 1) // 2
    s = set(points)
    x = 1 if 0 in s else 0
    c = sum(1 for t in range(1, h + 1) if t in s and p - t in s)
    e = sum(1 for t in range(1, h + 1) if t not in s and p - t not in s)
    return x, c, e


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, required=True)
    ap.add_argument("--witness", required=True)
    ap.add_argument("--steps", type=int, default=5)
    ap.add_argument("--budget", type=int, default=2_000_000)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    p = args.p
    h = (p - 1) // 2
    data = json.loads(Path(args.witness).read_text(encoding="utf-8"))
    if data["p"] != p:
        raise SystemExit("prime mismatch")
    points = sorted(data["points"])
    edges = run_gen(str(Path(__import__("os").environ["TEMP"]) / "forbidden_edges.exe"), p)
    out = Path(args.out) if args.out else Path(args.witness).with_name(
        Path(args.witness).stem + "_extended.json")
    trail = []
    for _ in range(args.steps):
        x, c, e = classify(points, p)
        size = x + c + h - e
        target = size + 1
        # keep the (x, c) family, drop one empty pair
        e_new = x + c + h - target
        if e_new < 0 or not (0 <= x <= 1) or not (0 <= c <= 1):
            print("target leaves the (x,c) family", flush=True)
            break
        clauses, nv, kept = build(p, edges, x, c, e_new)
        solver = Cadical195(bootstrap_with=clauses)
        chosen = set(points)
        phases = []
        for i in range(1, h + 1):
            lo, hi = i in chosen, p - i in chosen
            state = "B" if lo and hi else "N" if not lo and not hi else "L" if lo else "H"
            for kind in ("B", "N", "L", "H"):
                lit = 4 * i - 4 + KINDS[kind]
                phases.append(lit if kind == state else -lit)
        solver.set_phases(phases)
        solver.conf_budget(args.budget)
        res = solver.solve_limited()
        model = solver.get_model() if res else None
        solver.delete()
        print(f"size={size} -> target={target} class=({x},{c},{e_new}) "
              f"clauses={len(clauses)} sat={res}", flush=True)
        if not res:
            trail.append({"target": target, "class": [x, c, e_new], "sat": res})
            break
        pos = {i for i in model if i > 0}
        got = {0} if x else set()
        for i in range(1, h + 1):
            if 4 * i - 3 in pos:
                got.update({i, p - i})
            elif 4 * i - 1 in pos:
                got.add(i)
            elif 4 * i in pos:
                got.add(p - i)
        got = sorted(got)
        safe = not any(set(q) <= set(got) for q in edges)
        print(f"  witness {len(got)} safe={safe}", flush=True)
        if not safe:
            raise SystemExit("unsafe model")
        points = got
        trail.append({"target": target, "class": [x, c, e_new], "sat": True,
                      "size": len(got)})
        payload = {"p": p, "size": len(got), "seed": None, "rounds": None, "ruin": None,
                   "source": "warm_extend.py", "points": got}
        out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline="\n")
    (out.with_suffix(".trail.json")).write_text(json.dumps(trail, indent=2) + "\n",
                                                encoding="utf-8", newline="\n")
    print(f"final size {len(points)} -> {out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
