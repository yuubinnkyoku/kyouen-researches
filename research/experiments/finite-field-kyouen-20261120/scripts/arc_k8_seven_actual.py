"""Measure the actual (7,) count at q=7.

(7,) = #8-sets with 7 points on one circle D + 1 outside, and NO other
4-circle.  The formula b*C(s,7)*(n-s) is an UPPER BOUND (it ignores the
"no other 4-circle" condition).

Run:  python arc_k8_seven_actual.py --q 7
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from math import comb
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

        circ_of_triple = {}
        for k, BB in enumerate(blocks):
            for tri in itertools.combinations(BB, 3):
                circ_of_triple[tri] = k

        D = blocks[0]
        Dset = set(D)
        outD = [p for p in range(n) if p not in Dset]

        ok = 0
        bad = 0
        for T7 in itertools.combinations(D, 7):
            T7set = set(T7)
            for y in outD:
                Sset = T7set | {y}
                found = False
                for quad in itertools.combinations(sorted(Sset), 4):
                    cj = circ_of_triple.get(tuple(sorted(quad[:3])))
                    if cj is None or cj == 0:
                        continue
                    if all(p in blocks[cj] for p in quad):
                        found = True
                        break
                if found:
                    bad += 1
                else:
                    ok += 1

        ub = comb(s, 7) * (n - s)
        row = {"q": q, "n": n, "b": b, "s": s,
               "ok_per_circle": ok, "bad_per_circle": bad,
               "upper_bound_per_circle": ub,
               "actual_7": b * ok,
               "formula_7": b * ub}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  per circle: ok={ok}, bad={bad}, total={ok+bad}", flush=True)
        print(f"  upper bound per circle = C(s,7)*(n-s) = {ub}", flush=True)
        print(f"  actual (7,) = b*{ok} = {b*ok}", flush=True)
        print(f"  formula (7,) = b*{ub} = {b*ub}", flush=True)
        print(f"  overcount = {b*ub - b*ok}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
