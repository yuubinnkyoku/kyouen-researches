"""k=7: the multiplicity reduces to counting CIRCLES, not triples.

KEY REDUCTION.  A triple {x,y,z} outside C determines W = the circle
through it.  Conversely, for a fixed circle W, the triples with
W(x,y,z) = W are exactly the 3-subsets of W \\ C (since x,y,z must be
outside C and on W).

So

    multiplicity of a type = sum over circles W of that type of C(s-a, 3)

where a = |W cap C|.

This turns the triple count into a CIRCLE count -- a much smaller and more
structured object (b = q(q^2+1) circles instead of C(n-s,3) triples).

Let me verify this reduction and then classify circles W by their type.

Run:  python arc_k7_circle_count.py --q 5
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

        # For each circle W != C, compute the (w,u)-distribution over T
        # induced by the triples on W.  But the distribution depends on the
        # triple, not just W.  So instead: for each W, and each triple on W,
        # the distribution.  Group by W's "type".
        #
        # Simpler check: verify multiplicity = sum over W of C(s-a,3) for
        # the triples that give each type.  Do it directly.
        type_by_triple = Counter()
        for xyz in itertools.combinations(outside, 3):
            W = None
            for cj, BB in enumerate(circles):
                if cj == ci:
                    continue
                if all(p in BB for p in xyz):
                    W = cj
                    break
            WcapC = Bset & set(circles[W]) if W is not None else set()
            invs = []
            for xy in itertools.combinations(xyz, 2):
                pairs = set()
                for cj in circ_through_pair.get(tuple(sorted(xy)), []):
                    if cj == ci:
                        continue
                    cap = Bset & set(circles[cj])
                    if len(cap) == 2:
                        pairs.add(tuple(sorted(cap)))
                invs.append(frozenset(pairs))
            dist = Counter()
            for T in itertools.combinations(B, 4):
                Tset = set(T)
                w = len(Tset & WcapC)
                u = set()
                for inv in invs:
                    for pr in inv:
                        if pr[0] in Tset and pr[1] in Tset:
                            u.add(pr)
                dist[(w, len(u))] += 1
            type_by_triple[tuple(sorted(dist.items()))] += 1

        # Now: for each circle W, count triples on it
        circle_triples = Counter()
        for cj, BB in enumerate(circles):
            if cj == ci:
                continue
            a = len(Bset & set(BB))
            circle_triples[a] += comb(s - a, 3)

        row = {"q": q, "n": n, "b": b, "s": s,
               "types": {str(k): v for k, v in
                         sorted(type_by_triple.items(), key=lambda x: -x[1])},
               "circle_triples_by_a": dict(sorted(circle_triples.items())),
               "total_triples": sum(type_by_triple.values()),
               "total_from_circles": sum(circle_triples.values()),
               "C(n-s,3)": comb(n - s, 3)}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  types (by distribution): {len(type_by_triple)}", flush=True)
        for k, v in sorted(type_by_triple.items(), key=lambda x: -x[1]):
            print(f"    {k}: {v}", flush=True)
        print(f"  circle triples by a=|W cap C|: "
              f"{dict(sorted(circle_triples.items()))}", flush=True)
        print(f"  total triples {sum(type_by_triple.values())} vs "
              f"from circles {sum(circle_triples.values())} vs "
              f"C(n-s,3) {comb(n-s,3)}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
