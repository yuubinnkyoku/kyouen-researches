"""Task 1 (main): prove/compute exhaustively that every 5-cap lies on a conic.

Method (no unverified uniqueness assumption):
  * list all conics (out/conics.txt), each a 10-arc;
  * for every 4-arc Q (4 points, no 3 collinear), collect
        U(Q) = union of (C \\ Q) over all conics C containing Q;
  * every point of U(Q) is addable to Q (a conic has no 3 collinear);
  * the addable set E(Q) has |E(Q)| = 42 for every 4-arc;
  * if U(Q) == E(Q) for every Q, then every 5-cap Q+{p} is contained in a
    conic through Q, hence is a conic 5-subset.
  * count: #5-caps = sum_Q |E(Q)| / 5 (each 5-cap has five 4-subsets),
    and compare with 58968 * C(10,5).

Also independently counts the 4-arcs by brute-force enumeration of all
C(91,4) 4-subsets.
"""
import itertools
import time
from pathlib import Path

import pg

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / "out"
SHIFT = 91
COUNT_ONE = 1 << SHIFT
LOWMASK = (1 << SHIFT) - 1


def load_conics():
    masks = []
    for ln in (OUT / "conics.txt").read_text().splitlines():
        m = int(ln)
        assert m.bit_count() == 10
        masks.append(m)
    return masks


def pack4(p0, p1, p2, p3):
    return p0 | (p1 << 7) | (p2 << 14) | (p3 << 21)


def unpack(code):
    return (code & 127, (code >> 7) & 127, (code >> 14) & 127, (code >> 21) & 127)


def main():
    t0 = time.time()
    conics = load_conics()
    print(f"loaded {len(conics)} conics")

    # independent brute-force count of 4-arcs
    t = time.time()
    n4 = 0
    for comb in itertools.combinations(range(91), 4):
        a, b, c, d = comb
        if (pg.PAIR_LINE[(a, b)] == pg.PAIR_LINE[(a, c)] or
                pg.PAIR_LINE[(a, b)] == pg.PAIR_LINE[(a, d)] or
                pg.PAIR_LINE[(a, c)] == pg.PAIR_LINE[(a, d)] or
                pg.PAIR_LINE[(b, c)] == pg.PAIR_LINE[(b, d)] or
                pg.PAIR_LINE[(b, c)] == pg.PAIR_LINE[(c, d)] or
                pg.PAIR_LINE[(a, c)] == pg.PAIR_LINE[(b, c)]):
            continue
        n4 += 1
    print(f"brute-force 4-arc count: {n4} ({time.time() - t:.1f}s)")
    print(f"ordered 4-arcs by formula 91*90*81*64: {91 * 90 * 81 * 64}; "
          f"/24 = {91 * 90 * 81 * 64 // 24}")

    # accumulate conic incidences over 4-subsets
    t = time.time()
    d = {}
    get = d.get
    for cm in conics:
        pts = [p for p in range(91) if (cm >> p) & 1]
        for comb in itertools.combinations(pts, 4):
            code = pack4(*comb)
            qmask = (1 << comb[0]) | (1 << comb[1]) | (1 << comb[2]) | (1 << comb[3])
            extra = cm & ~qmask
            v = get(code)
            if v is None:
                d[code] = COUNT_ONE | extra
            else:
                d[code] = (v | extra) + COUNT_ONE
    print(f"4-arc incidence table: {len(d)} keys ({time.time() - t:.1f}s)")
    print(f"incidence table equals brute-force 4-arc count: {len(d) == n4}")
    print(f"total conic/4-arc incidences: {len(conics) * 210}")

    # verify every 4-arc: 7 conics, extra points cover the addable set
    t = time.time()
    bad = 0
    bad_count = 0
    bad_extra = 0
    total_addable = 0
    examples = []
    FULL = pg.FULL
    for code, v in d.items():
        cnt = v >> SHIFT
        union = v & LOWMASK
        if cnt != 7:
            bad_count += 1
            if len(examples) < 5:
                examples.append(("count", unpack(code), cnt))
        pts = unpack(code)
        sec = 0
        for a, b in itertools.combinations(pts, 2):
            sec |= pg.LINES[pg.PAIR_LINE[(a, b)]]
        E = FULL & ~sec
        if E.bit_count() != 42:
            bad += 1
            if len(examples) < 5:
                examples.append(("Esize", pts, E.bit_count()))
        total_addable += E.bit_count()
        if E != union:
            bad_extra += 1
            if len(examples) < 5:
                examples.append(("coverage", pts, (E ^ union).bit_count()))
    print(f"bad |E|: {bad}; bad conic-count: {bad_count}; bad coverage: {bad_extra} "
          f"({time.time() - t:.1f}s)")
    print("examples:", examples)
    print(f"sum |E(Q)| = {total_addable}")
    print(f"#5-caps = sum/5 = {total_addable // 5}")
    print(f"58968*C(10,5) = {58968 * 252}")
    print(f"5-cap count matches conic-subset count: {total_addable // 5 == 58968 * 252}")

    ok = (len(d) == n4 and bad == 0 and bad_count == 0 and bad_extra == 0
          and total_addable // 5 == 58968 * 252)
    print("EVERY_5CAP_CONIC:", "PASS" if ok else "FAIL")
    print(f"total time {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
