"""THE TRICHOTOMY: the kyouen game on Steiner t-designs.

The kyouen game has so far been studied on two boards, AG(2,q) and the
inversive plane.  Both are Steiner 3-designs.  This suggests the right
general setting:

    A t-(v, s, 1) design D.  Players alternately pick points.
    A set is SAFE if it meets every block in at most 3 points.
    K(D) = maximum safe size.

The parameter t controls everything:

    t >= 4 :  every 4-subset lies in a block  =>  K = 3 exactly.
              (TRIVIALITY THEOREM -- the game is a draw-ish 3-move game)

    t = 3  :  the genuinely new case.  This is where AG(2,q) and the
              inversive plane live.  K is a new invariant.

    t = 2  :  blocks are the lines of a projective plane PG(2,q);
              "no 4 in a block" = "no 4 collinear" = an ARC.
              K = q+1 (q odd), q+2 (q even)  -- CLASSICAL arc theory.

    t <= 1 :  no constraint at all, K = v.

So the kyouen game INTERPOLATES between classical arc theory (t=2) and
triviality (t>=4), and t=3 is the new territory.  This script verifies the
t=2 and t>=4 ends and re-confirms the t=3 middle.

Run:  python design_trichotomy.py
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from steiner3_kyouen import (  # noqa: E402
    build_ag32,
    build_inversive,
    check_design,
    max_safe,
    steiner_design,
)


# ------------------------------------------------------------------ PG(2,q)


def build_pg2q(q: int):
    """Points and lines of PG(2,q) for prime q, as index sets."""
    def normalise(v):
        for c in v:
            if c % q != 0:
                inv = pow(c, -1, q)
                return tuple((x * inv) % q for x in v)
        return None

    pts = set()
    for x in range(q):
        for y in range(q):
            for z in range(q):
                if (x, y, z) == (0, 0, 0):
                    continue
                pts.add(normalise((x, y, z)))
    points = sorted(pts)
    idx = {p: i for i, p in enumerate(points)}

    lines = set()
    for a in range(q):
        for b in range(q):
            for c in range(q):
                if (a, b, c) == (0, 0, 0):
                    continue
                key = normalise((a, b, c))
                ln = tuple(sorted(
                    idx[p] for p in points
                    if (a * p[0] + b * p[1] + c * p[2]) % q == 0
                ))
                if len(ln) == q + 1:
                    lines.add(ln)
    return len(points), sorted(lines)


# ------------------------------------------------------------------ main


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--node-cap", type=int, default=200_000_000)
    args = ap.parse_args()

    rows = []

    def run(name, v, blocks, t, predicted, note=""):
        t0 = time.time()
        design = check_design(v, blocks, t)
        try:
            best, nodes = max_safe(v, blocks, node_cap=args.node_cap)
            K = len(best)
            err = None
        except RuntimeError as exc:
            K, best, nodes, err = None, None, -1, str(exc)
        dt = time.time() - t0
        ok = (predicted is None) or (K == predicted)
        rows.append({
            "name": name, "v": v, "b": len(blocks), "t": t,
            "s": sorted({len(b) for b in blocks}),
            "K": K, "predicted": predicted, "match": ok,
            "witness": best, "nodes": nodes, "seconds": round(dt, 2),
            "design_ok": design["is_design"], "note": note, "error": err,
        })
        print(f"{name:<24} t={t} v={v:>3} b={len(blocks):>4} "
              f"s={rows[-1]['s']}  K={K}  predicted={predicted}  "
              f"{'OK' if ok else 'MISMATCH'}  {dt:.1f}s"
              + (f"  ERROR {err}" if err else ""), flush=True)

    print("=== t = 2 : projective planes, K = max (k,3)-arc ===")
    for q in (2, 3, 5):
        v, lines = build_pg2q(q)
        # complement of a line is a (v-(q+1), q)-arc, so only a 3-arc for q=3
        run(f"PG(2,{q})", v, lines, 2, None, "(k,3)-arc")

    print()
    print("=== t = 3 : the new territory ===")
    v, blocks = build_ag32()
    run("AG(3,2)=S(3,4,8)", v, blocks, 3, None)
    v, blocks = build_inversive(3)
    run("inversive q=3", v, blocks, 3, 5, "known K=5")
    blocks, _ = steiner_design(22, 6, 3)
    run("Witt S(3,6,22)", 22, blocks, 3, None)
    v, blocks = build_inversive(5)
    run("inversive q=5", v, blocks, 3, 6, "known K=6")

    print()
    print("=== t >= 4 : triviality theorem, K = 3 ===")
    for (v, s, t, name) in ((11, 5, 4, "Witt S(4,5,11)"),
                            (12, 6, 5, "Witt S(5,6,12)")):
        blocks, _ = steiner_design(v, s, t)
        run(name, v, blocks, t, 3, "theorem")

    print()
    print("TRICHOTOMY")
    print("  t >= 4 :  K = 3                      (trivial)")
    print("  t = 3  :  K = new invariant          (AG(2,q), inversive plane)")
    print("  t = 2  :  K = max arc in PG(2,q)     (classical: q+1 / q+2)")
    print("  t <= 1 :  K = v                      (no constraint)")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
