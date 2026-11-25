"""k=8 at q=9: measure the single-circle profiles efficiently.

A single-circle profile (j,) means exactly one circle carries >= 4 points
of S, and it carries j.

For k=8, j ranges 4..8.  The (4,) case is the "one 4-circle only" case.

EFFICIENT METHOD.  Instead of enumerating all 8-sets, enumerate over
(circle D, j-subset of D, (8-j)-subset of outside D) and test whether any
OTHER circle carries 4 of S.  This is what arc_k8_single.py does, but it
was too slow at q=9.

OPTIMISATION: for the "no other 4-circle" test, note that another circle
C' carrying 4 of S must carry 2 of the j points of D (since C' meets D in
<= 2 points) and 2 of the (8-j) outside points.  So we only need to check
pencil circles through pairs of the outside points.

Let me implement that.

Run:  python arc_k8_single_fast.py --q 9
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
import time
from collections import Counter
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_field, build_inversive_plane  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[9])
    args = ap.parse_args()

    rows = []
    for q in args.q:
        t0 = time.time()
        F, sub = build_field(q)
        points, circles = build_inversive_plane(q)
        idx = {p: i for i, p in enumerate(points)}
        blocks = [tuple(sorted(idx[p] for p in c)) for c in circles]
        n = len(points)
        b = len(blocks)
        s = q + 1

        circ_through_pair = {}
        for k, BB in enumerate(blocks):
            for pair in itertools.combinations(BB, 2):
                circ_through_pair.setdefault(pair, []).append(k)

        print(f"q={q}: n={n}, b={b}, s={s}, build {time.time()-t0:.1f}s",
              flush=True)

        single = Counter()
        t1 = time.time()
        for dk in range(b):
            D = blocks[dk]
            Dset = set(D)
            outD = [p for p in range(n) if p not in Dset]
            for j in range(4, 9):
                if j > len(D) or 8 - j > len(outD):
                    continue
                for Tj in itertools.combinations(D, j):
                    Tjset = set(Tj)
                    for Y in itertools.combinations(outD, 8 - j):
                        Yset = set(Y)
                        # another 4-circle needs 2 of Tj and 2 of Y
                        # (C' meets D in <= 2 points)
                        ok = True
                        if len(Y) >= 2:
                            for yp in itertools.combinations(Y, 2):
                                for ck in circ_through_pair.get(
                                        tuple(sorted(yp)), []):
                                    if ck == dk:
                                        continue
                                    if len(Tjset & set(blocks[ck])) == 2:
                                        ok = False
                                        break
                                if not ok:
                                    break
                        if ok:
                            single[j] += 1
        print(f"  enumeration {time.time()-t1:.1f}s", flush=True)

        row = {"q": q, "n": n, "b": b, "s": s,
               "single": dict(sorted(single.items())),
               "total": sum(single.values())}
        rows.append(row)
        print(f"  single-circle profiles: {dict(sorted(single.items()))}",
              flush=True)
        print(f"  total: {sum(single.values())}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
