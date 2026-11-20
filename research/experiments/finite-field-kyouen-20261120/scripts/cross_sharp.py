"""Can the cross bound explain K/q ~ 1 for q = 1 mod 4?

For q = 1 mod 4 we proved (K1058):
    K <= 3q^2/(2q-1) ~ 1.5 q

Observed: K/q ~ 1.00 for q = 9, 13, 17.

So the cross bound gives 1.5q, and the truth is ~1.0q.  The gap is a factor 1.5.

Can we sharpen the cross bound?  The cross constraint is
    a_c + b_r - x_{cr} <= 3   for all (c,r)
Summing gave (2q-1)k <= 3q^2.

But we can use the constraint more carefully.  Let A = sum_c a_c = k and
B = sum_r b_r = k.  The constraint says for each (c,r):
    a_c + b_r <= 3 + x_{cr}
where x_{cr} = 1 if point (c,r) is in S, else 0.

Sum over r for fixed c:
    q*a_c + k <= 3q + a_c
    (q-1) a_c <= 3q - k
    a_c <= (3q - k)/(q-1)

Similarly b_r <= (3q - k)/(q-1).

Summing over c:
    k = sum_c a_c <= q(3q-k)/(q-1)
    k(q-1) <= 3q^2 - qk
    k(2q-1) <= 3q^2
    k <= 3q^2/(2q-1)

Same bound.  But the per-column bound is stronger information:
    a_c <= (3q-k)/(q-1)

For k ~ q, this gives a_c <= (3q-q)/(q-1) = 2q/(q-1) ~ 2.
So each column has at most ~2 points.  That is consistent with k ~ q spread
over q columns (average 1 point per column).

Can we get a better bound by using the fact that a_c is an INTEGER?
    a_c <= floor((3q-k)/(q-1))

For k = q: floor(2q/(q-1)) = 2 for q >= 3.
So each column has at most 2 points, giving k <= 2q.  Weaker.

Hmm.  Let me look for a different argument.

KEY IDEA: use the CROSS constraint together with the fact that a cross has
2q-1 points and the safe set meets it in at most 3.  For a column c with a_c
points and a row r with b_r points, the cross has a_c + b_r - x_{cr} points.
If a_c = 2 and b_r = 2 and x_{cr} = 0, the cross has 4 points -- violation.
So: if a_c = 2 and b_r = 2 then x_{cr} = 1 (the intersection must be occupied).

This is a strong structural constraint!  Let us count:
Let C2 = {c : a_c = 2}, R2 = {r : b_r = 2}.  Then for all c in C2, r in R2,
the point (c,r) must be in S.  So S contains the full C2 x R2 grid.

If |C2| = p and |R2| = q, then S contains p*q points from that grid.
But S also has at most 2 points per column, so p*q <= 2q, i.e. p <= 2.
Similarly q <= 2.  So |C2| <= 2 and |R2| <= 2.

Therefore at most 2 columns and 2 rows have 2 points; all others have <= 1.
Then k = sum a_c <= 2*2 + (q-2)*1 = q + 2.

THAT IS THE BOUND!  k <= q + 2 for q = 1 mod 4.

Let me verify this reasoning and test it against the data.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ag2_prime_power import build_ag  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[5, 9, 13, 17])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for q in args.q:
        pts, blocks, through, nc, nl = build_ag(q)
        # cross blocks have size 2q-1
        crosses = [b for b in blocks if len(b) == 2 * q - 1]
        if not crosses:
            print(f"q={q}: no cross blocks (q != 1 mod 4?)", flush=True)
            continue
        # verify: crosses correspond to (column, row) pairs
        # a cross is {points with s=c} union {points with t=r}
        # identify columns and rows by the structure
        # points are indexed s*Q+t
        Q = q
        col_of = lambda p: p // Q
        row_of = lambda p: p % Q
        # check each cross is a column union a row
        ok = True
        for b in crosses:
            cols = {col_of(p) for p in b}
            rows_ = {row_of(p) for p in b}
            if len(cols) != 1 or len(rows_) != 1:
                ok = False
                break
        bound = q + 2
        rows.append({"q": q, "crosses": len(crosses),
                     "crosses_are_col_union_row": ok,
                     "bound_q_plus_2": bound})
        print(f"q={q}: {len(crosses)} crosses, col-union-row structure: {ok}, "
              f"derived bound K <= q+2 = {bound}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
