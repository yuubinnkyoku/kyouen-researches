"""Task 1 (part): verify board == PG(2,9), enumerate all conics, check
that every conic is a 10-arc and is maximal (no addable point).

Writes out/conics.txt (one 91-bit mask as decimal per line).
"""
import itertools
import time
from pathlib import Path

import pg

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BOARD = ROOT.parent / "output" / "board_pg2q9.txt"
OUT = ROOT / "out"


def parse_board():
    lines = BOARD.read_text().splitlines()
    n, m = map(int, lines[0].split())
    rows = []
    for ln in lines[1:]:
        vals = list(map(int, ln.split()))
        assert vals[0] == len(vals) - 1
        rows.append(tuple(vals[1:]))
    return n, m, rows


def det3(a, b, c, d, e, f):
    # symmetric matrix [[a,b,c],[b,d,e],[c,e,f]]
    return pg.ADD[
        pg.ADD[pg.MUL[a][pg.ADD[pg.MUL[d][f]][pg.NEG[pg.MUL[e][e]]]]
               ][pg.NEG[pg.MUL[b][pg.ADD[pg.MUL[b][f]][pg.NEG[pg.MUL[e][c]]]]]]
        ][pg.MUL[c][pg.ADD[pg.MUL[b][e]][pg.NEG[pg.MUL[d][c]]]]]


def main():
    t0 = time.time()
    n, m, rows = parse_board()
    board_masks = set()
    for r in rows:
        mask = 0
        for p in r:
            mask |= 1 << p
        board_masks.add(mask)
    print(f"board parsed: {n} points {m} lines")

    # board line family vs generated PG(2,9) line family
    gen = set(pg.LINES)
    print(f"generated lines: {len(gen)}; board lines: {len(board_masks)}; "
          f"EQUAL={gen == board_masks}")
    if gen != board_masks:
        raise SystemExit("board is not the coordinate PG(2,9) under this convention")

    # independent check: every 3-subset of board points lies on a board line
    # (plane axioms already checked in verify_board.py).  Check line sizes.
    assert all(mask.bit_count() == 10 for mask in board_masks)

    # monomials per point
    MONO = []
    for x, y, z in pg.COORDS:
        MONO.append((pg.MUL[x][x], pg.MUL[y][y], pg.MUL[z][z],
                     pg.MUL[x][y], pg.MUL[x][z], pg.MUL[y][z]))
    ZERO = 0
    TWO = pg.TWO

    conics = {}
    nform = 0
    ndet = 0
    t1 = time.time()
    for a in range(9):
        for b in range(9):
            for c in range(9):
                for d in range(9):
                    for e in range(9):
                        for f in range(9):
                            form = (a, b, c, d, e, f)
                            # first nonzero entry must be ONE for a unique
                            # projective representative
                            if a != 0:
                                if a != pg.ONE:
                                    continue
                            elif b != 0:
                                if b != pg.ONE:
                                    continue
                            elif c != 0:
                                if c != pg.ONE:
                                    continue
                            elif d != 0:
                                if d != pg.ONE:
                                    continue
                            elif e != 0:
                                if e != pg.ONE:
                                    continue
                            elif f != 0:
                                if f != pg.ONE:
                                    continue
                            else:
                                continue
                            nform += 1
                            if det3(a, b, c, d, e, f) == ZERO:
                                continue
                            ndet += 1
                            tb = pg.MUL[TWO][b]
                            tc = pg.MUL[TWO][c]
                            te = pg.MUL[TWO][e]
                            mask = 0
                            for p, (xx, yy, zz, xy, xz, yz) in enumerate(MONO):
                                s = pg.ADD[pg.MUL[a][xx]][pg.MUL[d][yy]]
                                s = pg.ADD[s][pg.MUL[f][zz]]
                                s = pg.ADD[s][pg.MUL[tb][xy]]
                                s = pg.ADD[s][pg.MUL[tc][xz]]
                                s = pg.ADD[s][pg.MUL[te][yz]]
                                if s == ZERO:
                                    mask |= 1 << p
                            conics.setdefault(mask, form)
    t2 = time.time()
    print(f"normalized projective forms: {nform}; nondegenerate: {ndet}; "
          f"distinct zero sets: {len(conics)}")
    print(f"form enumeration time: {t2 - t1:.1f}s")

    # checks on conics
    bad_size = [m for m in conics if m.bit_count() != 10]
    bad_cap = []
    not_max = []
    for mask in conics:
        pts = [p for p in range(91) if (mask >> p) & 1]
        # every line meets the conic in 0,1,2 points
        if any((lm & mask).bit_count() > 2 for lm in pg.LINES):
            bad_cap.append(mask)
            continue
        if pg.secant_union(pts) != pg.FULL:
            not_max.append(mask)
    print(f"conics with size != 10: {len(bad_size)}")
    print(f"conics with a 3-point line (not caps): {len(bad_cap)}")
    print(f"conics that are not maximal (addable point exists): {len(not_max)}")
    print(f"conic count == 58968: {len(conics) == 58968}")

    # incidence: each line meets a conic in 0/1/2 points: count secant/tangent
    # distribution across all conics (sanity)
    OUT.mkdir(exist_ok=True)
    with (OUT / "conics.txt").open("w") as fh:
        for mask in sorted(conics):
            fh.write(str(mask) + "\n")
    print("wrote out/conics.txt")
    print(f"total time {time.time() - t0:.1f}s")
    if len(conics) == 58968 and not bad_size and not bad_cap and not not_max:
        print("CONICS: PASS")
    else:
        print("CONICS: FAIL")


if __name__ == "__main__":
    main()
