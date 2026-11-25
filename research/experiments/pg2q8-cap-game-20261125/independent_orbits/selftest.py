"""Self-tests for pg8core: field, geometry, and the Schreier-Sims implementation.

Every test here is independent of the board file except the explicit board
comparison.  Run:  python selftest.py
"""

import sys
import time

import random

import pg8core as G

FAIL = []


def check(cond, msg):
    print(("  ok   " if cond else "  FAIL ") + msg)
    if not cond:
        FAIL.append(msg)


def sec(t):
    return "%.2fs" % (time.time() - t)


print("== GF(8) ==")
t = time.time()
bad = G.check_field()
check(not bad, "field axioms (comm/assoc/distrib/inverse, x primitive, x^3+x+1 irred.): %r" % (bad[:3],))
print("  mul table row 2:", [G.gf_mul(2, b) for b in range(8)])
print("  inverses 1..7:", [G.gf_inv(a) for a in range(1, 8)])
print("  " + sec(t))

print("== points ==")
t = time.time()
check(len(G.PTS) == 73, "73 points")
check(G.PTS[0] == (0, 0, 1), "point 0 = (0,0,1)")
check(G.PTS[1] == (0, 1, 0) and G.PTS[8] == (0, 1, 7), "points 1..8 = (0,1,c)")
check(G.PTS[9] == (1, 0, 0) and G.PTS[16] == (1, 0, 7), "points 9..16 = (1,0,c)")
check(G.PTS[17] == (1, 1, 0) and G.PTS[72] == (1, 7, 7), "points 17..72 = (1,b,c)")
check(len(set(G.PTS)) == 73, "points distinct")
check(all(G.PTS[i][0] == 1 or (G.PTS[i][0] == 0 and (G.PTS[i][1] == 1 or (G.PTS[i][1] == 0 and G.PTS[i][2] == 1))) for i in range(73)),
      "all canonical (first nonzero coord = 1)")
print("  " + sec(t))

print("== lines (independent construction from the field) ==")
t = time.time()
LINES = G.build_lines()
check(len(LINES) == 73, "73 lines, got %d" % len(LINES))
check(all(len(L) == 9 for L in LINES), "each line has 9 points")
pairs = set()
okpairs = True
for L in LINES:
    pts = sorted(L)
    for a in range(len(pts)):
        for b in range(a + 1, len(pts)):
            if (pts[a], pts[b]) in pairs:
                okpairs = False
            pairs.add((pts[a], pts[b]))
check(okpairs, "no pair of points lies on two lines")
check(len(pairs) == 73 * 72 // 2, "all 2628 pairs covered, got %d" % len(pairs))
# every line has 9 points; check intersections of two lines are 0 or 1 points
okint = True
LL = list(LINES)
for i in range(73):
    for j in range(i + 1, 73):
        if len(LL[i] & LL[j]) > 1:
            okint = False
check(okint, "two distinct lines meet in at most one point")
print("  " + sec(t))

print("== board file agrees with the construction ==")
t = time.time()
N, B, BOARD = G.read_board("../output/board_pg2q8.txt")
check(N == 73 and B == 73, "board header 73 73")
check(len(BOARD) == 73 and all(len(L) == 9 for L in BOARD), "73 board lines of size 9")
check(set(BOARD) == set(LINES), "board line set == independently constructed line set")
check(sorted(sorted(L) for L in BOARD) == sorted(sorted(L) for L in LINES), "same multiset of lines")
print("  " + sec(t))

print("== Schreier-Sims on known groups ==")


def closure_order(gens, n):
    """Brute-force order of <gens> by BFS over permutations (small groups only)."""
    return G.closure_order(gens, n)


def cyc(n, k):
    p = list(range(n))
    for i in range(k):
        p[i] = (i + 1) % k
    return tuple(p)


def onpoints(n, mapping):
    p = list(range(n))
    for a, b in mapping.items():
        p[a] = b
    return tuple(p)


# cyclic
t = time.time()
B5 = G.bsgs_order([cyc(73, 5)], 73)
check(B5.order() == 5 and B5.verify() == 0, "C5 on 73 pts -> order 5 (%d, fails %d)" % (B5.order(), B5.verify()))
# C7 x C11 commuting, disjoint supports
c11 = list(range(73))
for i in range(11):
    c11[7 + i] = 7 + (i + 1) % 11
c11 = tuple(c11)
check(closure_order([cyc(73, 7), c11], 73) == 77, "brute-force closure C7xC11 = 77")
B = G.bsgs_order([cyc(73, 7), c11], 73)
check(B.order() == 77 and B.verify() == 0, "C7 x C11 -> 77 (%d)" % B.order())
# S7 on 7 points (embedded)
s7a = onpoints(73, {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 0})
s7b = onpoints(73, {0: 1, 1: 0})
B = G.bsgs_order([s7a, s7b], 73)
check(B.order() == 5040 and B.verify() == 0, "S7 -> 5040 (%d)" % B.order())
check(closure_order([s7a, s7b], 73) == 5040, "brute-force closure S7 = 5040")
# A5 on 5 points
a5a = onpoints(73, {0: 1, 1: 2, 2: 3, 3: 4, 4: 0})
a5b = onpoints(73, {0: 2, 2: 1, 1: 0})
B = G.bsgs_order([a5a, a5b], 73)
check(B.order() == 60 and B.verify() == 0, "A5 -> 60 (%d)" % B.order())
check(closure_order([a5a, a5b], 73) == 60, "brute-force closure A5 = 60")
print("  " + sec(t))

print("== PGL(2,8) on PG(1,8) = 9 points -> order 504 ==")
t = time.time()


def pgl28():
    # points: {0,1,...,7} U {inf=8}
    inf = 8

    def mobius(a, b, c, d):
        # x -> (a x + b)/(c x + d)
        p = [0] * 9
        for x in range(9):
            if x == inf:
                num, den = a, c
            else:
                num = G.gf_add(G.gf_mul(a, x), b)
                den = G.gf_add(G.gf_mul(c, x), d)
            if den == 0:
                p[x] = inf
            elif num == 0:
                p[x] = 0
            else:
                p[x] = G.gf_mul(num, G.gf_inv(den))
        return tuple(p)

    t1 = mobius(1, 1, 0, 1)   # x -> x+1
    t2 = mobius(2, 0, 0, 1)   # x -> 2x
    t3 = mobius(0, 1, 1, 0)   # x -> 1/x
    return t1, t2, t3


g1, g2, g3 = pgl28()
print("  generator orders:", G.porder(g1), G.porder(g2), G.porder(g3))
Bp = G.bsgs_order([g1, g2, g3], 9)
check(Bp.order() == 504 and Bp.verify() == 0, "|PGL(2,8)| = 504 (%d)" % Bp.order())
check(closure_order([g1, g2, g3], 9) == 504, "brute-force closure PGL(2,8) = 504")
Bq = G.bsgs_order([g1, g2], 9)
check(Bq.order() == 56 and Bq.verify() == 0,
      "Borel <x->x+1, x->2x> has order 56 = q(q-1) (%d)" % Bq.order())
check(closure_order([g1, g2], 9) == 56, "brute-force closure Borel = 56")
print("  " + sec(t))

print("== PGL(3,8) subgroup structure ==")
t = time.time()
trans = []
for i in range(3):
    for j in range(3):
        if i == j:
            continue
        for c in (1, 2):
            trans.append(G.perm_from_matrix(G.transvection(i, j, c)))
check(len(trans) == 12, "12 transvection generators (E_ij(1), E_ij(w))")
d = G.perm_from_matrix(G.diagonal(2, 1, 1))
sw = G.perm_from_matrix(G.coord_swap())
print("  diag(w,1,1) order:", G.porder(d), " swap order:", G.porder(sw))
Bsl = G.bsgs_order(trans, 73)
print("  transvection-only chain:", Bsl.report())
check(Bsl.order() == 16482816 and Bsl.verify() == 0,
      "|<transvections>| = |SL(3,8)| = |PSL(3,8)| = 16482816 (%d)" % Bsl.order())
Ball = G.bsgs_order(trans + [d], 73)
print("  +diag chain:", Ball.report())
check(Ball.order() == 16482816 and Ball.verify() == 0,
      "|<transvections, diag(w,1,1)>| = 16482816 (%d)" % Ball.order())
Ball2 = G.bsgs_order(trans + [d, sw], 73)
print("  +diag+swap chain:", Ball2.report())
check(Ball2.order() == 16482816 and Ball2.verify() == 0,
      "|<transvections, diag, swap>| = 16482816 (%d)" % Ball2.order())
# Lagrange consistency with the geometric chain 73*72*64*49
check(73 * 72 * 64 * 49 == 16482816, "73*72*64*49 = 16482816")
print("  " + sec(t))

print("== randomized validation of Schreier-Sims vs brute-force closure ==")
t = time.time()
rng = random.Random(20261126)
tested = bad = 0
for _ in range(120):
    npt = rng.choice([5, 6, 7, 8])
    gs = []
    for _ in range(rng.choice([2, 3])):
        q = list(range(npt))
        rng.shuffle(q)
        gs.append(tuple(q))
    try:
        c = G.closure_order(gs, npt)
    except RuntimeError:
        continue
    tested += 1
    Bt = G.bsgs_order(gs, npt)
    if Bt.order() != c or Bt.verify() != 0:
        bad += 1
        print("   MISMATCH n=%d closure=%d bsgs=%d verify=%d" % (npt, c, Bt.order(), Bt.verify()))
check(tested >= 100 and bad == 0,
      "%d random groups: BSGS order == brute-force closure order (%d mismatches)" % (tested, bad))
print("  " + sec(t))

print()
if FAIL:
    print("SELFTEST FAILURES: %d" % len(FAIL))
    for f in FAIL:
        print("   -", f)
    sys.exit(1)
print("ALL SELFTESTS PASSED")
