"""CLOSED FORM FOR N_j: the second-circle count is a cross-ratio condition.

At q=7 the two PGL(2,q)-orbits on 4-subsets of P^1(F_q) have sizes 42 and
28, and their second-circle distributions are

    orbit 42:  (N0,N1,N2) = (284, 524, 53)
    orbit 28:  (N0,N1,N2) = (282, 528, 51)

The differences are tiny (2, -4, +2).  That suggests N_j is "almost
constant" and the orbit dependence is a small correction.

KEY IDEA.  Fix a circle C, a 4-subset T of C, and a pair {x,y} outside C.
The circles through x and y form a pencil of q+1 circles.  A circle C' in
that pencil meets C in 0, 1 or 2 points.  We want |T ∩ C'| = 2.

Since C' meets C in at most 2 points, |T ∩ C'| = 2 iff C' passes through
exactly 2 of the 4 points of T.  The pencil through x,y induces a
"projection" from C to the pencil: each point p of C determines the unique
circle through x, y, p.  So the pencil is parametrised by p in C, and

    |T ∩ C'| = #{p in T : C'(p) = C'}  -- i.e. how many points of T map to
    the same pencil element.

So the question becomes: for the map  phi: C -> pencil(x,y),  p |-> the
circle through x,y,p, how many fibres meet T in exactly 2 points?

phi is a bijection from C onto the pencil EXCEPT that the two points
C ∩ (line xy)... in the inversive plane, the pencil through x,y has q+1
circles and C has q+1 points, and phi is a bijection.  So each fibre has
exactly ONE point, and |T ∩ C'| = 1 always!

That contradicts the data (we see |T ∩ C'| = 2 sometimes).  The resolution:
C' can meet C in 2 points, and BOTH can be in T.  So phi is 2-to-1 on the
2 points of C ∩ C', not a bijection.

Let me just compute the exact structure numerically and fit a formula.

Run:  python arc_k6_Nj_formula.py --q 5 7
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from arc_on_quadric import build  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[5, 7])
    args = ap.parse_args()

    rows = []
    for q in args.q:
        F, ovoid, circles = build(q)
        n = len(ovoid)
        b = len(circles)
        circ_through_pair = {}
        for ci, B in enumerate(circles):
            for pair in itertools.combinations(B, 2):
                circ_through_pair.setdefault(pair, []).append(ci)

        ci = 0
        B = circles[ci]
        Bset = set(B)
        outside = [p for p in range(n) if p not in Bset]

        # For each T, record the full distribution AND the number of
        # circles C' meeting T in 0,1,2 points (summed over all xy)
        groups = Counter()
        for T in itertools.combinations(B, 4):
            Tset = set(T)
            d = Counter()
            meet = Counter()
            for xy in itertools.combinations(outside, 2):
                cnt = 0
                for cj in circ_through_pair.get(tuple(sorted(xy)), []):
                    if cj == ci:
                        continue
                    m = len(Tset & set(circles[cj]))
                    meet[m] += 1
                    if m == 2:
                        cnt += 1
                d[cnt] += 1
            groups[(tuple(sorted(d.items())), tuple(sorted(meet.items())))] += 1

        row = {"q": q, "n": n, "b": b,
               "groups": {str(k): v for k, v in groups.items()}}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}", flush=True)
        for (dist, meet), cnt in groups.items():
            print(f"  {cnt} subsets: dist={dict(dist)} meet={dict(meet)}",
                  flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
