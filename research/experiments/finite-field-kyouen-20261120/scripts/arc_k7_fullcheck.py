"""k=7: the CORRECT assembly, enumerating over all circles C.

The previous bug: the tuple loop fixed C = P^1(F_q), so only 7-sets whose
4-circle is that specific C appeared, and the multiplicity division was
invalid.

THE FIX.  Enumerate over ALL circles C (b of them), all 4-subsets T of C,
and all triples {x,y,z} outside C.  Then each 7-set S with profile P is
counted exactly #4-circles(P) times (once per (4-circle, 4-subset) pair),
so dividing by #4-circles(P) is correct.

But that is b * C(s,4) * C(n-s,3) tuples = 130*15*1140 = 2,223,000 at q=5
and 350*70*11480 = 281,260,000 at q=7.  Too many to enumerate directly.

KEY OPTIMISATION.  The profile depends only on the ISOMORPHISM CLASS of
the configuration (C, T, {x,y,z}).  By 3-transitivity we can fix C and T
up to the stabiliser, but the {x,y,z} still vary.

SIMPLER: use the fact that the count of 7-sets with profile P equals

    (1/#4(P)) * sum over circles C of #{T, xyz giving profile P}

and by symmetry over C this is

    (1/#4(P)) * b * #{T, xyz for the FIXED C giving profile P}

Wait -- that IS what the previous code did with scale=b.  And it gave
1,414,000 arcs at q=7 where the truth is 0.

So the issue is the DIVISION.  Let me check: for the fixed C, a 7-set S
whose 4-circles include C is counted once (T = C cap S is determined).
A 7-set S whose 4-circles do NOT include C is not counted at all.

So sum over C of (count for that C) = sum over S of (#4-circles of S).
Dividing by #4-circles(P) gives the number of S with profile P.  That IS
correct.

Then why 1,414,000 vs 0?

Let me check whether the profile formula is right for ALL (T,xyz), not
just the sampled ones.  The earlier check sampled 11,480 of 803,600.

Run:  python arc_k7_fullcheck.py --q 7
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_field, build_inversive_plane  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[7])
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

        mismatch = Counter()
        checked = 0
        for T in itertools.combinations(B, 4):
            Tset = set(T)
            for xyz in itertools.combinations(outside, 3):
                xyzset = set(xyz)
                Sset = Tset | xyzset
                # actual profile
                hits = {}
                for quad in itertools.combinations(sorted(Sset), 4):
                    cj = circ_of_triple.get(tuple(sorted(quad[:3])))
                    if cj is None:
                        continue
                    if all(p in blocks[cj] for p in quad):
                        hits[cj] = len(Sset & set(blocks[cj]))
                actual = tuple(sorted(hits.values(), reverse=True))
                # formula
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
                pred = tuple([5] * n5 + [4] * n4)
                checked += 1
                if actual != pred:
                    mismatch[(actual, pred)] += 1

        row = {"q": q, "checked": checked,
               "mismatches": sum(mismatch.values()),
               "examples": {str(k): v for k, v in
                            sorted(mismatch.items(), key=lambda x: -x[1])[:5]}}
        rows.append(row)
        print(f"q={q}: FULL check {checked} (T,xyz) pairs", flush=True)
        print(f"  mismatches: {sum(mismatch.values())}", flush=True)
        for (a, p), v in sorted(mismatch.items(), key=lambda x: -x[1])[:5]:
            print(f"    actual {a} vs predicted {p}: {v}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
