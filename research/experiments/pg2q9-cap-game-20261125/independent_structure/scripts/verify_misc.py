"""Miscellaneous structural checks: conic incidences, frame stabilizer,
line-type distribution for a conic, and |PGL(3,9)| arithmetic.
"""
import itertools
from collections import Counter
from pathlib import Path

import pg

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / "out"


def bits(mask):
    while mask:
        b = mask & -mask
        yield b.bit_length() - 1
        mask ^= b


def main():
    conics = [int(ln) for ln in (OUT / "conics.txt").read_text().splitlines()]
    n = len(conics)
    print(f"conics: {n}")

    # incidence point-conic and pair-conic
    point_inc = Counter()
    pair_inc = Counter()
    for cm in conics:
        pts = list(bits(cm))
        for p in pts:
            point_inc[p] += 1
        for a, b in itertools.combinations(pts, 2):
            pair_inc[(a, b)] += 1
    vals = set(point_inc.values())
    print(f"point-conic incidences: points covered {len(point_inc)}/91, "
          f"counts {sorted(vals)} (expect 58968*10/91 = {n * 10 / 91})")
    vals2 = set(pair_inc.values())
    print(f"pair-conic incidences: pairs covered {len(pair_inc)}/4095, "
          f"counts {sorted(vals2)} (expect 58968*45/4095 = {n * 45 / 4095})")

    # line types for a conic
    C = conics[0]
    types = Counter()
    for lm in pg.LINES:
        types[(lm & C).bit_count()] += 1
    print(f"line intersection sizes with a conic: {dict(sorted(types.items()))} "
          f"(0=external,1=tangent,2=secant)")

    # frame stabilizer: a projectivity fixing e1,e2,e3 is diagonal; fixing
    # (1,1,1) forces the diagonal entries equal, i.e. a scalar matrix.
    # Enumerate diagonal matrices with equal entries and confirm they fix the
    # frame; enumerate diagonal matrices with unequal entries and confirm they
    # do not fix the frame (so the stabilizer is exactly the scalars).
    # Coordinates: field labels; frame (1,0,0),(0,1,0),(0,0,1),(1,1,1).
    INV = [None] * 9
    for x in range(1, 9):
        for y in range(1, 9):
            if pg.MUL[x][y] == pg.ONE:
                INV[x] = y

    def proj_eq(v, w):
        # v, w nonzero vectors equal up to a nonzero scalar (field labels)
        i = next(k for k, x in enumerate(v) if x != 0)
        s = pg.MUL[w[i]][INV[v[i]]]
        return all(pg.MUL[v[j]][s] == w[j] for j in range(3))

    def mat_apply(M, v):
        out = []
        for row in M:
            s = 0
            for x, y in zip(row, v):
                s = pg.ADD[s][pg.MUL[x][y]]
            out.append(s)
        return tuple(out)

    frame = [(pg.ONE, 0, 0), (0, pg.ONE, 0), (0, 0, pg.ONE), (pg.ONE, pg.ONE, pg.ONE)]
    scalars = []
    nonfix = 0
    for a in range(9):
        for b in range(9):
            for c in range(9):
                if a == 0 or b == 0 or c == 0:
                    continue
                M = [[a, 0, 0], [0, b, 0], [0, 0, c]]
                fixes = all(proj_eq(mat_apply(M, p), p) for p in frame[:3])
                fix4 = proj_eq(mat_apply(M, frame[3]), frame[3])
                if fixes and fix4:
                    scalars.append((a, b, c))
                elif fixes and not fix4:
                    nonfix += 1
    print(f"diagonal matrices fixing e1,e2,e3 projectively: scalars among them "
          f"{scalars}")
    print(f"diagonal matrices fixing e1,e2,e3 but not (1,1,1): {nonfix} "
          f"(all non-scalar; scalars are {scalars})")

    # |GL(3,9)| and |PGL(3,9)|
    gl = (9**3 - 1) * (9**3 - 9) * (9**3 - 9**2)
    pgl = gl // (9 - 1)
    print(f"|GL(3,9)| = {gl}")
    print(f"|PGL(3,9)| = {pgl}")
    print(f"ordered 4-arcs 91*90*81*64 = {91 * 90 * 81 * 64}")


if __name__ == "__main__":
    main()
