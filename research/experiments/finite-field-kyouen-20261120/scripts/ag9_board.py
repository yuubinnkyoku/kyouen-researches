"""AG(2,9) in *split* coordinates, and a cross-check against build_ag(9).

F_9 = F_3[i]/(i^2 + 1)  (i^2 = -1 = 2 mod 3).  The invertible F_9-linear map

    (x, y) |-> (s, t) = (x + i y, x - i y)

sends x^2 + y^2 to s*t, because (x+iy)(x-iy) = x^2 - i^2 y^2 = x^2 + y^2.
Hence every "circle" x^2 + y^2 + D x + E y + F = 0 becomes

    s*t + a*s + b*t + c = 0

for suitable a, b, c in F_9.  So the 819 blocks of AG(2,9) are exactly

  * 90 lines  a*s + b*t = c   (10 directions x 9 offsets), 9 points each,
  * 729 conics s*t + a*s + b*t + c = 0, of which
      - 648 are non-degenerate (a*b != c), 8 points each,
      - 81 are degenerate: (s+a)(t+b) = 0, i.e. a column plus a row
        ("cross"), 17 points each.

This is the key structural fact used by the search: the 81 crosses are blocks,
so a safe set meets every column and every row in at most 2 points.

The script verifies the description against the independent builder
`ag2_prime_power.build_ag(9)`.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ag2_prime_power import build_ag  # noqa: E402
from inversive_prime_power import FiniteField, find_irreducible  # noqa: E402

# ---------------------------------------------------------------- F_9
# element = a + 3*b  <->  a + b*i,  i^2 = -1 = 2 (mod 3)


def f9add(x: int, y: int) -> int:
    return ((x % 3 + y % 3) % 3) + 3 * ((x // 3 + y // 3) % 3)


def f9mul(x: int, y: int) -> int:
    a1, b1, a2, b2 = x % 3, x // 3, y % 3, y // 3
    re = (a1 * a2 - b1 * b2) % 3
    im = (a1 * b2 + b1 * a2) % 3
    return re + 3 * im


def f9neg(x: int) -> int:
    return (-x % 3) + 3 * (-(x // 3) % 3)


def build_split_board():
    """Return (blocks, kinds) for AG(2,9) in (s,t) coordinates.

    point index = s*9 + t.  kinds[i] is 'line', 'conic' or 'cross'.
    """
    blocks = []
    kinds = []

    # lines: directions of PG(1,9) are (1,b) for b in F_9, plus (0,1)
    dirs = [(1, b) for b in range(9)] + [(0, 1)]
    assert len(dirs) == 10
    for a, b in dirs:
        for c in range(9):
            blk = [s * 9 + t for s in range(9) for t in range(9)
                   if f9add(f9mul(a, s), f9mul(b, t)) == c]
            blocks.append(blk)
            kinds.append("line")

    # conics s*t + a*s + b*t + c = 0
    for a in range(9):
        for b in range(9):
            for c in range(9):
                blk = [s * 9 + t for s in range(9) for t in range(9)
                       if f9add(f9add(f9mul(s, t), f9mul(a, s)),
                                f9add(f9mul(b, t), c)) == 0]
                blocks.append(blk)
                kinds.append("cross" if f9mul(a, b) == c else "conic")
    return blocks, kinds


def main() -> None:
    blocks, kinds = build_split_board()
    print(f"split board: {len(blocks)} blocks")
    from collections import Counter
    print("  kinds:", Counter(kinds))
    print("  sizes:", Counter(len(b) for b in blocks))
    # distinctness
    fs = {frozenset(b) for b in blocks}
    print(f"  distinct point sets: {len(fs)}")
    inc = Counter()
    for b in blocks:
        for p in b:
            inc[p] += 1
    print(f"  incidences per point: {set(inc.values())} (81 points: {len(inc)})")

    # ---- cross-check against build_ag(9) -------------------------------
    pts, blocks2, through2, nc, nl = build_ag(9)
    print(f"build_ag(9): {len(blocks2)} blocks (circles={nc}, lines={nl})")
    print("  sizes:", Counter(len(b) for b in blocks2))

    # map build_ag point index -> (s,t) index
    F = FiniteField(3, 2, find_irreducible(3, 2))
    print(f"  irreducible poly used by build_ag: {F.f}")
    # find i with i^2 = -1
    minus1 = F.neg(F.one)
    ii = None
    for e in F.elements():
        if F.mul(e, e) == minus1:
            ii = e
            break
    assert ii is not None, "no square root of -1"
    print(f"  sqrt(-1) = {ii}")

    def to_st(pt):
        x, y = pt
        s = F.add(x, F.mul(ii, y))
        t = F.sub(x, F.mul(ii, y))
        return (s[0] + 3 * s[1]) * 9 + (t[0] + 3 * t[1])

    perm = [to_st(pt) for pt in pts]
    assert sorted(perm) == list(range(81)), "coordinate map is not a bijection"

    set_a = {frozenset(perm[i] for i in b) for b in blocks2}
    set_b = {frozenset(b) for b in blocks}
    print(f"  build_ag block sets: {len(set_a)}, split block sets: {len(set_b)}")
    print(f"  IDENTICAL: {set_a == set_b}")
    if set_a != set_b:
        print(f"  only in build_ag: {len(set_a - set_b)}")
        print(f"  only in split:    {len(set_b - set_a)}")
        for b in list(set_a - set_b)[:3]:
            print("   A:", sorted(b))
        for b in list(set_b - set_a)[:3]:
            print("   B:", sorted(b))
        raise SystemExit(1)

    # ---- the cross / row-column structure ------------------------------
    crosses = [b for b, k in zip(blocks, kinds) if k == "cross"]
    print(f"\ncrosses: {len(crosses)}")
    # each cross is (full column s0) union (full row t0), 9+9-1 = 17 points
    from collections import Counter as C
    cols: C = C()
    rows: C = C()
    for b in crosses:
        cs = C(p // 9 for p in b)
        ct = C(p % 9 for p in b)
        s_full = [s for s, k in cs.items() if k == 9]
        t_full = [t for t, k in ct.items() if k == 9]
        assert len(s_full) == 1 and len(t_full) == 1, "cross is not col+row"
        assert len(b) == 17, "cross size"
        cols[s_full[0]] += 1
        rows[t_full[0]] += 1
    print(f"  columns seen: {len(cols)} (each in {set(cols.values())} crosses)")
    print(f"  rows seen:    {len(rows)} (each in {set(rows.values())} crosses)")
    print("\nOK: split description matches build_ag(9) exactly.")


if __name__ == "__main__":
    main()
