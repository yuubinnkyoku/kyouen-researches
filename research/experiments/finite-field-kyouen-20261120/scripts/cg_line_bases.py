"""Print the lines of a char-2 pencil member in a canonical basis form.

For Q = s(X0X3+X1X2) + r0(X0X1+X2^2) + r1(X1^2+X2X3) over q = 2^m, enumerate the
lines on Q and print each as a normalised pair (u, v) of spanning points, so the
dependence on (s, r0, r1) becomes visible.

Run:  python cg_line_bases.py --q 8 --member 1,1,0
"""

from __future__ import annotations

import argparse
import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_prime_power import FiniteField, factorize, find_irreducible  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, required=True)
    ap.add_argument("--member", type=str, required=True, help="s,r0,r1 as field element indices")
    args = ap.parse_args()
    q = args.q
    p, m = factorize(q)[0]
    assert p == 2
    F = FiniteField(p, m, find_irreducible(p, m))
    elems = list(F.elements())
    one = F.pow(elems[0], 0)
    zero = F.sub(one, one)
    mul, add = F.mul, F.add
    s_idx, r0_idx, r1_idx = (int(x) for x in args.member.split(","))
    s, r0, r1 = elems[s_idx], elems[r0_idx], elems[r1_idx]

    def normalise(v):
        if all(F.is_zero(x) for x in v):
            return None
        inv = None
        for x in v:
            if not F.is_zero(x):
                inv = F.div(one, x)
                break
        return tuple(mul(inv, x) for x in v)

    seen = set()
    pts = []
    for v in itertools.product(elems, repeat=4):
        nv = normalise(v)
        if nv is None or nv in seen:
            continue
        seen.add(nv)
        pts.append(nv)
    index = {v: i for i, v in enumerate(pts)}

    def Q(pt):
        x0, x1, x2, x3 = pt
        acc = mul(s, add(mul(x0, x3), mul(x1, x2)))
        acc = add(acc, mul(r0, add(mul(x0, x1), mul(x2, x2))))
        acc = add(acc, mul(r1, add(mul(x1, x1), mul(x2, x3))))
        return acc

    lines = set()
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            lp = set()
            for lam in elems:
                lp.add(normalise(tuple(add(pts[i][k], mul(lam, pts[j][k])) for k in range(4))))
            lp.add(pts[j])
            if len(lp) == q + 1 and all(Q(pt) is not None and F.is_zero(Q(pt)) for pt in lp):
                # canonical description: the "smallest" pair of a basis
                idxs = sorted(index[pt] for pt in lp)
                lines.add(tuple(idxs))
    print(f"q={q} member (s,r0,r1) = ({s_idx},{r0_idx},{r1_idx}): {len(lines)} lines on Q")
    for ln in sorted(lines):
        u = pts[ln[0]]
        # pick v as the lexicographically smallest point of the line independent of u
        v = None
        for i in ln[1:]:
            cand = pts[i]
            if not all(F.is_zero(cand[k]) for k in range(4)) and cand != u:
                v = cand
                break
        print("   u =", u, " v =", v)


if __name__ == "__main__":
    main()
