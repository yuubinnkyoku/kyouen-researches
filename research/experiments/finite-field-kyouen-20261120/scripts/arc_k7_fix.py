"""k=7: the CORRECT profile formula.

The bug: u counts circles with |C' cap T| = 2 but a 4-circle also needs
|C' cap {x,y,z}| = 2.

THE FIX.  Define

    v = #{C' != C : |C' cap T| = 2 AND |C' cap {x,y,z}| = 2}

Then the profile is

    #4-circles = 1 + v + [w = 1]
    #5-circles = [w = 2]

and u >= v (u is the count with only the first condition).

Let me verify this corrected formula at q=5 AND q=7.

Run:  python arc_k7_fix.py --q 5 7
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
    ap.add_argument("--q", type=int, nargs="+", default=[5, 7])
    ap.add_argument("--limit", type=int, default=20000)
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

        circ_through_pair = {}
        for k, BB in enumerate(blocks):
            for pair in itertools.combinations(BB, 2):
                circ_through_pair.setdefault(pair, []).append(k)
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
                Sset = Tset | set(xyz)
                # actual profile
                hits = {}
                for quad in itertools.combinations(sorted(Sset), 4):
                    cj = circ_of_triple.get(tuple(sorted(quad[:3])))
                    if cj is None:
                        continue
                    if all(p in blocks[cj] for p in quad):
                        hits[cj] = len(Sset & set(blocks[cj]))
                actual = tuple(sorted(hits.values(), reverse=True))
                # corrected formula: v counts BOTH conditions
                W = circ_of_triple.get(tuple(sorted(xyz)))
                WcapC = Bset & set(blocks[W]) if W is not None else set()
                w = len(WcapC)
                v = 0
                for kk in range(b):
                    if kk == ci:
                        continue
                    capT = len(Tset & set(blocks[kk]))
                    if capT != 2:
                        continue
                    capX = len(set(xyz) & set(blocks[kk]))
                    if capX == 2:
                        v += 1
                n4 = 1 + v + (1 if w == 1 else 0)
                n5 = 1 if w == 2 else 0
                pred = tuple([5] * n5 + [4] * n4)
                checked += 1
                if actual != pred:
                    mismatch[(actual, pred)] += 1
                if checked >= args.limit:
                    break
            if checked >= args.limit:
                break

        row = {"q": q, "checked": checked,
               "mismatches": sum(mismatch.values()),
               "examples": {str(k): v for k, v in
                            sorted(mismatch.items(), key=lambda x: -x[1])[:3]}}
        rows.append(row)
        print(f"q={q}: checked {checked}, mismatches {sum(mismatch.values())}",
              flush=True)
        for (a, p), v in sorted(mismatch.items(), key=lambda x: -x[1])[:3]:
            print(f"    actual {a} vs predicted {p}: {v}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
