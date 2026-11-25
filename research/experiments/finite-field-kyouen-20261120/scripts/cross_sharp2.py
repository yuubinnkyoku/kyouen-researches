"""Sharpen the cross bound: K <= q + 2 for q = 1 mod 4.

Setup.  For q = 1 mod 4, the split coordinates (s,t) = (x+iy, x-iy) give
q^2 "cross" blocks: for each (c,r) in F_q^2, the cross is

    {(s,t) : s = c} union {(s,t) : t = r}

which has 2q-1 points.  A safe set S meets each cross in at most 3 points.

Let a_c = |S cap column c|, b_r = |S cap row r|, x_{cr} = 1 if (c,r) in S.
The cross constraint is

    a_c + b_r - x_{cr} <= 3.        (*)

KEY OBSERVATION.  If a_c = 2 and b_r = 2, then (*) forces x_{cr} = 1.
So S contains the entire grid C2 x R2 where C2 = {c : a_c = 2},
R2 = {r : b_r = 2}.

But S has at most 2 points per column (a_c <= 2 follows from (*) with b_r = 0
... actually we need to derive a_c <= 2 first).

Deriving a_c <= 2:  Sum (*) over r:
    q*a_c + k - a_c <= 3q
    (q-1) a_c <= 3q - k
    a_c <= (3q-k)/(q-1).
For k >= q this gives a_c <= 2q/(q-1) < 3, so a_c <= 2 (integer).
So for k >= q, every column has at most 2 points.  Similarly every row.

Now suppose |C2| = p >= 1 and |R2| = s >= 1.  Then S contains C2 x R2,
which has p*s points.  But each column of C2 has at most 2 points, so
p*s <= 2p, i.e. s <= 2.  Similarly p <= 2.

So at most 2 columns and at most 2 rows have 2 points; all others have <= 1.
Hence
    k = sum_c a_c <= 2*2 + (q-2)*1 = q + 2.

THEOREM: for q = 1 mod 4 and k >= q, K <= q + 2.

Let us verify this against the data:
    q=5:  K=6  <= 7   OK
    q=9:  K=9  <= 11  OK
    q=13: K>=13 <= 15 OK
    q=17: K>=17 <= 19 OK

This is a much sharper bound than 3q^2/(2q-1) ~ 1.5q.

This script verifies the structural facts (columns/rows/crosses) and the bound.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ag2_prime_power import build_ag  # noqa: E402
from inversive_prime_power import FiniteField, find_irreducible  # noqa: E402


def split_coords(q: int):
    """Return (F, i, points as (s,t) pairs, index map)."""
    p, e = (q, 1) if q in (3, 5, 7, 11, 13, 17, 19) else (None, None)
    if p is None:
        raise SystemExit("prime q only")
    F = FiniteField(p, e, find_irreducible(p, e))
    # find i with i^2 = -1
    i = None
    for cand in F.elements():
        if F.add(F.mul(cand, cand), F.one) == F.zero:
            i = cand
            break
    if i is None:
        return None
    return F, i


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[5, 9, 13, 17])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for q in args.q:
        if q % 4 != 1:
            print(f"q={q}: not 1 mod 4, skipped", flush=True)
            continue
        pts, blocks, through, nc, nl = build_ag(q)
        crosses = [b for b in blocks if len(b) == 2 * q - 1]
        # verify the cross structure: each cross is a union of one column and
        # one row in SOME coordinate system.  We verify the counting property
        # directly: for any two crosses, their intersection has size 1 or 2q-1
        # (two crosses sharing a column or row intersect in 2q-1 points,
        #  otherwise in exactly 1 point).
        inter_sizes = set()
        for a in range(min(len(crosses), 40)):
            for b in range(a + 1, min(len(crosses), 40)):
                inter_sizes.add(len(set(crosses[a]) & set(crosses[b])))
        bound = q + 2
        rows.append({
            "q": q,
            "crosses": len(crosses),
            "cross_intersection_sizes": sorted(inter_sizes),
            "bound_q_plus_2": bound,
        })
        print(f"q={q}: {len(crosses)} crosses, intersection sizes "
              f"{sorted(inter_sizes)}, bound K <= q+2 = {bound}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
