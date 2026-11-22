"""k=8 at q=9: verify the profile formula directly.

The assembly at q=9 gave arcs=120,087,360 but the exhaustive count is
1,062,720.  The gap is 119,024,640.

Since k=8 has NO single-circle profiles at q=5, the gap must come from
the profile formula or the multiplicity theorem.

Let me verify the profile formula at q=9 on a sample of (T, X) pairs.

Run:  python arc_k8_q9_check.py --q 9 --limit 2000
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
    ap.add_argument("--q", type=int, nargs="+", default=[9])
    ap.add_argument("--limit", type=int, default=2000)
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
        outside = [p for p in range(n) if p not in Bset]

        circ_of_triple = {}
        for k, BB in enumerate(blocks):
            for tri in itertools.combinations(BB, 3):
                circ_of_triple[tri] = k

        mismatch = Counter()
        checked = 0
        for T in itertools.combinations(B, 4):
            Tset = set(T)
            for X in itertools.combinations(outside, 4):
                Xset = set(X)
                Sset = Tset | Xset
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
                v2 = v3 = v4 = u3 = u4 = z4 = 0
                for kk in range(b):
                    if kk == ci:
                        continue
                    ct = len(Tset & set(blocks[kk]))
                    cx = len(Xset & set(blocks[kk]))
                    if ct == 2:
                        if cx == 2:
                            v2 += 1
                        elif cx == 3:
                            v3 += 1
                        elif cx == 4:
                            v4 += 1
                    elif ct == 1:
                        if cx == 3:
                            u3 += 1
                        elif cx == 4:
                            u4 += 1
                    elif ct == 0:
                        if cx == 4:
                            z4 += 1
                n4 = 1 + v2 + u3 + z4
                n5 = v3 + u4
                n6 = v4
                pred = tuple([6] * n6 + [5] * n5 + [4] * n4)
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
                            sorted(mismatch.items(), key=lambda x: -x[1])[:5]}}
        rows.append(row)
        print(f"q={q}: checked {checked}, mismatches {sum(mismatch.values())}",
              flush=True)
        for (a, p), v in sorted(mismatch.items(), key=lambda x: -x[1])[:5]:
            print(f"    actual {a} vs predicted {p}: {v}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
