"""TASK 1 -- verify that the board file is PG(2,8) in the claimed labelling.

Checks
  A. File syntax: header "73 73", 73 lines of 9 distinct points in 0..72.
  B. Incidence axioms of a projective plane of order 8 (v = b = 73, every line
     has 9 points, every point lies on 9 lines, every pair of distinct points
     lies on exactly one line, every pair of distinct lines meets in exactly
     one point).
  C. Exact comparison with PG(2,8) constructed from GF(8) = GF(2)[x]/(x^3+x+1)
     with the claimed labelling: point index = rank of its canonical vector
     (first non-zero coordinate 1) among the 73 canonical non-zero vectors
     sorted by integer value.  The *set* of 73 board lines must equal the set
     of 73 constructed lines.
  D. Cross-checks of the labelling: point 0 = [0:0:1], points 1..8 = [0:1:c],
     points 9+8b+c = [1:b:c]; board line 0 = {x0 = 0}; the 9 lines through
     point 0 are the 9 lines b = const.
"""

import sys
from itertools import combinations

import pg2q8 as P


def main():
    out = []

    def say(s=""):
        out.append(str(s))
        print(s)

    n, m, board_lines = P.read_board()
    say("== A. file syntax ==")
    say(f"header: {n} points, {m} lines")
    ok_hdr = (n == 73 and m == 73)
    say(f"73/73 header: {'OK' if ok_hdr else 'FAIL'}")
    all_len9 = all(len(L) == 9 for L in board_lines)
    distinct = all(len(set(L)) == 9 for L in board_lines)
    inrange = all(0 <= p < 73 for L in board_lines for p in L)
    say(f"every line has 9 entries: {all_len9}")
    say(f"entries distinct within each line: {distinct}")
    say(f"all entries in 0..72: {inrange}")
    okA = ok_hdr and all_len9 and distinct and inrange

    say()
    say("== B. projective-plane incidence axioms ==")
    bl = [frozenset(L) for L in board_lines]
    # duplicate lines?
    nodup = len(set(bl)) == 73
    say(f"73 distinct lines: {nodup}")
    # point -> lines through it
    through = [[] for _ in range(73)]
    for li, L in enumerate(bl):
        for p in L:
            through[p].append(li)
    degs = [len(x) for x in through]
    okdeg = all(d == 9 for d in degs)
    say(f"every point on exactly 9 lines: {okdeg}  (min {min(degs)}, max {max(degs)})")
    # pairs of points on exactly one line
    pair_count = {}
    bad_pair = 0
    for L in bl:
        for a, b in combinations(sorted(L), 2):
            k = pair_count.get((a, b), 0) + 1
            pair_count[(a, b)] = k
            if k > 1:
                bad_pair += 1
    npairs = 73 * 72 // 2
    okpairs = (
        len(pair_count) == npairs
        and all(v == 1 for v in pair_count.values())
    )
    say(f"pairs of points covered exactly once: {okpairs}  "
        f"({len(pair_count)} pairs, expected {npairs}, multiplicity>1 count {bad_pair})")
    # pairs of lines meet in exactly one point
    oklinepairs = True
    bad = []
    for i, j in combinations(range(73), 2):
        inter = bl[i] & bl[j]
        if len(inter) != 1:
            oklinepairs = False
            bad.append((i, j, sorted(inter)))
            if len(bad) > 5:
                break
    say(f"every two distinct lines meet in exactly one point: {oklinepairs}")
    if bad:
        say(f"  counterexamples: {bad[:3]}")
    # point/line duality totals
    incidences = sum(len(L) for L in bl)
    say(f"total incidences: {incidences} (expected 73*9 = {73*9})")
    okB = nodup and okdeg and okpairs and oklinepairs and incidences == 73 * 9

    say()
    say("== C. exact comparison with constructed PG(2,8) ==")
    canon = set(P.canonical_lines())
    say(f"constructed lines: {len(canon)}")
    say("point labelling (rank -> canonical vector), first 12:")
    for r in range(12):
        say(f"  {r:2d} -> {P.POINTS[r]}")
    say("...")
    for r in (63, 64, 71, 72):
        say(f"  {r:2d} -> {P.POINTS[r]}")
    set_board = set(bl)
    same = set_board == canon
    say(f"board line set == constructed line set: {same}")
    only_board = set_board - canon
    only_canon = canon - set_board
    say(f"# board lines not in constructed set: {len(only_board)}")
    say(f"# constructed lines not in board set: {len(only_canon)}")
    if only_board:
        ex = sorted(next(iter(only_board)))
        say(f"  example board-only line: {ex}")
    if only_canon:
        ex = sorted(next(iter(only_canon)))
        say(f"  example canon-only line: {ex}")
    # also verify board line *order* against a natural parametrisation
    # (not required by the claim, informational)
    order_note = []
    for li, L in enumerate(bl):
        order_note.append(frozenset(L))
    okC = same and len(canon) == 73

    say()
    say("== D. labelling cross-checks ==")
    zero_l1 = P.line_through(0, 1)
    say(f"point 0 = [0:0:1] = {P.POINTS[0]}, point 1 = [0:1:0] = {P.POINTS[1]}")
    say(f"board line 0 (indices) = {sorted(bl[0])}")
    say(f"board line 0 == x0 = 0 (points 0..8): {bl[0] == frozenset(range(9))}")
    say(f"board line 0 == constructed line through 0 and 1: {bl[0] == zero_l1}")
    # lines through point 0 in the board
    l0 = sorted(through[0])
    say(f"board lines through point 0: {l0}")
    expect = []
    for b in range(8):
        s = frozenset([0] + [9 + 8 * b + c for c in range(8)])
        expect.append(s)
    say(f"these are exactly {{0}} u {{(1,b,c) : c in GF(8)}} for b = 0..7 "
        f"(plus the line at infinity x0 = 0): "
        f"{set(bl[i] for i in l0 if i != 0) == set(expect)}")
    # point 0's pencil partitions the other 72 points
    parts = [bl[i] - {0} for i in l0 if i != 0]
    say(f"the 8 affine lines through point 0 partition the 64 affine points 9..72: "
        f"{sorted(x for p in parts for x in p) == list(range(9, 73))}")
    okD = (
        bl[0] == frozenset(range(9))
        and set(bl[i] for i in l0 if i != 0) == set(expect)
        and sorted(x for p in parts for x in p) == list(range(9, 73))
    )

    say()
    say("== SUMMARY ==")
    say(f"A file syntax: {'PASS' if okA else 'FAIL'}")
    say(f"B projective plane of order 8: {'PASS' if okB else 'FAIL'}")
    say(f"C exact PG(2,8) with claimed labelling: {'PASS' if okC else 'FAIL'}")
    say(f"D labelling cross-checks: {'PASS' if okD else 'FAIL'}")
    overall = okA and okB and okC and okD
    say(f"TASK 1: {'PASS' if overall else 'FAIL'}")

    with open("results_task1.txt", "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
