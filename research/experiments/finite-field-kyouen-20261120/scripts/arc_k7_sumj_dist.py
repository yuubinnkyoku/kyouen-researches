"""k=7: the (2,2) circle count in closed form.

From the previous result, sum_j = #(2,2) + 3*[W present], and the (2,2)
circles are the circles through exactly 2 of {x,y,z} meeting T in 2 points.

For a FIXED pair {x,y}, the number of circles through x,y meeting T in 2
points is j({x,y}) -- the k=6 quantity.  Summing over the three pairs gives

    j1 + j2 + j3 = #(2,2) + 3*[W present]

because W is counted in all three j's but appears once as a (3,2) circle.

So #(2,2) = j1 + j2 + j3 - 3*[W present] = sum_j - 3[w=2] = u.

That is exactly the u we already have!  So the (2,2) count is u, and there
is nothing new to close -- the chain is:

    profile <- (w,u) <- (case,w,sum_j) <- (2,2) count = u

which is circular.  The genuinely open quantity is the DISTRIBUTION of u,
i.e. the joint law of (j1,j2,j3).

Let me instead attack the distribution of j1+j2+j3 directly, using the fact
that each j is a k=6 quantity with a known marginal.

KEY IDEA.  For a fixed pair {x,y}, j({x,y}) is determined by the involution
iota(x,y) and T.  The three involutions are related (disjoint or one
common pair).  So:

  Case A: the three involutions are disjoint, so the three j's count
      DISJOINT sets of pairs.  Hence sum_j = |union| and the j's are
      "independent given the involutions".

  Case B: they share one pair, so sum_j = |union| + 2*[common pair in T].

Let me measure the distribution of sum_j in Case A and see whether it
factors.

Run:  python arc_k7_sumj_dist.py --q 5
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
    ap.add_argument("--q", type=int, nargs="+", default=[5])
    args = ap.parse_args()

    rows = []
    for q in args.q:
        F, ovoid, circles = build(q)
        n = len(ovoid)
        b = len(circles)
        s = q + 1
        circ_through_pair = {}
        for ci, B in enumerate(circles):
            for pair in itertools.combinations(B, 2):
                circ_through_pair.setdefault(pair, []).append(ci)

        ci = 0
        B = circles[ci]
        Bset = set(B)
        outside = [p for p in range(n) if p not in Bset]
        T = tuple(B[:4])
        Tset = set(T)

        # Case A: distribution of (n2-triple, sum_j)
        joint = Counter()
        for xyz in itertools.combinations(outside, 3):
            invs = []
            js = []
            n2s = []
            for xy in itertools.combinations(xyz, 2):
                pairs = set()
                j = 0
                for cj in circ_through_pair.get(tuple(sorted(xy)), []):
                    if cj == ci:
                        continue
                    cap = Bset & set(circles[cj])
                    if len(cap) == 2:
                        pairs.add(tuple(sorted(cap)))
                        if len(Tset & set(circles[cj])) == 2:
                            j += 1
                invs.append(frozenset(pairs))
                js.append(j)
                n2s.append(len(pairs))
            common = (len(invs[0] & invs[1]), len(invs[0] & invs[2]),
                      len(invs[1] & invs[2]))
            case = "B" if common == (1, 1, 1) else "A"
            joint[(case, tuple(sorted(n2s)), sum(js))] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "joint": {str(k): v for k, v in
                         sorted(joint.items(), key=lambda x: -x[1])}}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  (case, n2-triple, sum_j) -> count", flush=True)
        for k, v in sorted(joint.items(), key=lambda x: -x[1]):
            print(f"    {k}: {v}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
