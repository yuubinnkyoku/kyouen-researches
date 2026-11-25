"""k=7 at q=7: the multiplicity scaling is wrong.

The assembly gives bad = 6,864,527,600 > C(50,7) = 99,884,400, hence a
NEGATIVE arc count.  So the scaling is wrong.

THE BUG.  The tuple loop fixes C = P^1(F_q) (ONE specific circle) and
enumerates T (4-subsets of C) and {x,y,z} (triples outside C).  So it
counts tuples with C FIXED.

To get all 7-sets, we must sum over ALL circles C, i.e. multiply by b.
But we must NOT multiply by C(s,4): the T's are already enumerated.

At q=5 the code used scale = b*C(s,4) and it worked.  Why?

Because at q=5 the tuple loop was over (C,T,{x,y,z}) with C fixed, T
enumerated (C(s,4) of them), and {x,y,z} enumerated.  Multiplying by b
gives all (C,T,xyz) tuples.  Multiplying ALSO by C(s,4) is wrong.

Let me recheck the q=5 code... In arc_k7_total.py the scale was
b*comb(s,4).  And it gave the right answer at q=5.  So either the q=5
answer was right by coincidence, or the tuple loop there was different.

Let me just test both scalings at q=5 and q=7 against the exhaustive count.

Run:  python arc_k7_scale.py --q 5
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter
from fractions import Fraction
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_field, build_inversive_plane  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[5])
    args = ap.parse_args()

    rows = []
    for q in args.q:
        F, sub = build_field(q)
        points, circles = build_inversive_plane(q)
        idx = {p: i for i, p in enumerate(points)}
        blocks = [tuple(sorted(idx[p] for p in c)) for c in circles]
        n = len(points)
        b = len(blocks)
        s = q + 1
        base = set(sub) | {None}
        ci = None
        for k, B in enumerate(blocks):
            if set(points[i] for i in B) == base:
                ci = k
                break
        B = blocks[ci]
        Bset = set(B)
        circ_of_triple = {}
        for k, BB in enumerate(blocks):
            for tri in itertools.combinations(BB, 3):
                circ_of_triple[tri] = k

        outside = [p for p in range(n) if p not in Bset]

        prof_tuples = Counter()
        for T in itertools.combinations(B, 4):
            Tset = set(T)
            for xyz in itertools.combinations(outside, 3):
                xyzset = set(xyz)
                W = circ_of_triple.get(tuple(sorted(xyz)))
                wT = len(Tset & set(blocks[W])) if W is not None else 0
                v = 0
                for kk in range(b):
                    if kk == ci:
                        continue
                    if len(Tset & set(blocks[kk])) != 2:
                        continue
                    if len(xyzset & set(blocks[kk])) == 2:
                        v += 1
                n4 = 1 + v + (1 if wT == 1 else 0)
                n5 = 1 if wT == 2 else 0
                prof = tuple([5] * n5 + [4] * n4)
                prof_tuples[prof] += 1

        # exhaustive
        circ_of_quad = {}
        for k, BB in enumerate(blocks):
            for quad in itertools.combinations(BB, 4):
                circ_of_quad[quad] = k
        ex = Counter()
        for S in itertools.combinations(range(n), 7):
            Sset = set(S)
            hits = {}
            for quad in itertools.combinations(S, 4):
                cj = circ_of_quad.get(quad)
                if cj is None:
                    continue
                hits[cj] = len(Sset & set(blocks[cj]))
            if not hits:
                ex[("ARC",)] += 1
                continue
            ex[tuple(sorted(hits.values(), reverse=True))] += 1

        # try scalings
        results = {}
        for name, scale in (("b", b), ("b*C(s,4)", b * comb(s, 4)),
                            ("1", 1)):
            bad = Fraction(0)
            for prof, cnt in prof_tuples.items():
                n4 = sum(1 for t in prof if t == 4)
                bad += Fraction(cnt, n4) * scale
            bad += b * comb(s, 6) * (n - s)
            results[name] = (str(bad), str(comb(n, 7) - bad))

        row = {"q": q, "n": n, "b": b, "s": s,
               "profiles": len(prof_tuples),
               "exhaustive_bad": sum(v for k, v in ex.items() if k != ("ARC",)),
               "exhaustive_arcs": ex.get(("ARC",), 0),
               "scalings": results}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  exhaustive: bad={row['exhaustive_bad']}, "
              f"arcs={row['exhaustive_arcs']}", flush=True)
        for name, (bd, ar) in results.items():
            print(f"  scale={name}: bad={bd}, arcs={ar}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
