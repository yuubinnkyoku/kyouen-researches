#!/usr/bin/env python3
"""Two-edit surgery of the (7,6) m=31 witness on the 7x32 board, targeting the
unique uncovered cell T=(31,3). Port of surgery_m31.py (same algorithm, seed
swapped to the m=31 surgery witness).

Complete enumeration of final states S' = seed - R + A with |R| <= 2, |A| <= 2,
final size <= 34 (a <= r; size 35 would force all rows full = non-deficient and
size 36+ needs a 6-stone row = unsafe), A disjoint from seed minus R, in-board, and
T occupied or blocked in S'.

Unified curve bookkeeping: every curve carries st_on (seed stones) and ALL
board cells on it (full). For any final state:
  |C ∩ S'| = |st_on minus R| + |A ∩ full|
which is correct even when an addition lands on a removed stone's own cell
(relocation). Safety: some curve with |C ∩ S'| >= 6. Blocking of cell e
(e not in S'): some curve C through e with |C ∩ S'| >= 5.

Blocking-curve case split for T (complete; c = |st_on| for seed curves C ∋ T):
  T occupied                                            [occ]
  c=4, t=0: >=1 addition on C (2nd addition anywhere)   [need=1]
  c=4, t=1: both additions on C                         [need=2]
  c=3, t=0: both additions on C                          [need=2]
  c=5 curves through T do not exist (T uncovered in the seed); c-t<=2 needs
  >=3 additions - impossible. Removals never create blocking curves.

Exact Fraction arithmetic; no repo code; self-tests included.
"""
import json, itertools, time
from math import gcd
from fractions import Fraction

W, M, Q = 32, 32, 6
BX, BY = 32, 7        # x in 0..31, y in 0..6
T = (31, 3)
SEED_REL = "../../seven-row-q6-m31-frontier-20261115/output/m31.witness.stones.json"

def circum(a, b, c):
    ax, ay = a; bx, by = b; cx, cy = c
    d = 2*(ax*(by-cy) + bx*(cy-ay) + cx*(ay-by))
    if d == 0: return None
    a2, b2, c2 = ax*ax+ay*ay, bx*bx+by*by, cx*cx+cy*cy
    return (Fraction(a2*(by-cy) + b2*(cy-ay) + c2*(ay-by), d),
            Fraction(a2*(cx-bx) + b2*(ax-cx) + c2*(bx-ax), d))

def selftest():
    u = circum((0,0), (1,0), (0,1))
    assert u == (Fraction(1,2), Fraction(1,2)), u
    u2 = circum((0,2), (13,2), (12,3))
    assert u2 == (Fraction(13,2), Fraction(-7,2)), u2
    print("selftest PASS")

def build_curves(stones):
    S = set(stones)
    curves = {}
    n = len(stones)
    for i, j in itertools.combinations(range(n), 2):
        a, b = stones[i], stones[j]
        A, B = b[1]-a[1], a[0]-b[0]
        C = -(A*a[0] + B*a[1])
        if A < 0 or (A == 0 and B < 0): A, B, C = -A, -B, -C
        g = gcd(gcd(abs(A), abs(B)), abs(C)) or 1
        curves[("L", A//g, B//g, C//g)] = None
    for i, j, k in itertools.combinations(range(n), 3):
        a, b, c = stones[i], stones[j], stones[k]
        if (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0]) == 0: continue
        u = circum(a, b, c)
        if u is None: continue
        r2 = (Fraction(a[0])-u[0])**2 + (Fraction(a[1])-u[1])**2
        curves[("C", u[0], u[1], r2)] = None
    out = []
    for key in curves:
        st_on = set(); full = []
        for x in range(BX):
            for y in range(BY):
                if key[0] == "L":
                    on = key[1]*x + key[2]*y + key[3] == 0
                else:
                    _, ux, uy, r2 = key
                    on = (Fraction(x)-ux)**2 + (Fraction(y)-uy)**2 == r2
                if on:
                    full.append((x, y))
                    if (x, y) in S: st_on.add((x, y))
        if len(st_on) >= 3:
            out.append((key, frozenset(st_on), frozenset(full)))
    return out

def main():
    t0 = time.time()
    selftest()
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    seed = [tuple(p) for p in json.load(open(os.path.join(here, SEED_REL)))]
    S = set(seed)
    assert len(S) == 34 and T not in S
    curves = build_curves(seed)
    by_c = {}
    for key, st_on, full in curves:
        by_c.setdefault(len(st_on), []).append((key, st_on, full))
    for c in sorted(by_c): print(f"curves c={c}: {len(by_c[c])}")
    assert max(by_c) <= Q - 1, "seed unsafe"
    board = [(x, y) for x in range(BX) for y in range(BY)]
    empty = [p for p in board if p not in S]
    assert T in empty and len(empty) == 224 - 34

    # T-curve census
    tc4 = [(k, s, f) for (k, s, f) in by_c.get(4, []) if T in f]
    tc3 = [(k, s, f) for (k, s, f) in by_c.get(3, []) if T in f]
    print(f"T-curve census: c4={len(tc4)} c3={len(tc3)}")
    for k, s, f in tc4:
        print("  c4 curve:", sorted(s), "empty_on:", len(f) - 4 - (1 if T in f else 0))

    # tables: curves through each cell (c>=4 for safety; c>=3 for blocking)
    tab4 = {}; tab3 = {}; block5 = {}
    for c in (3, 4, 5):
        for key, st_on, full in by_c.get(c, []):
            for p in full:
                if c >= 4: tab4.setdefault(p, []).append((st_on, full))
                tab3.setdefault(p, []).append((st_on, full))
                if c == 5: block5.setdefault(p, []).append(st_on)

    # candidate enumeration
    cands = set()
    Rsets = [(frozenset(p), len(p)) for p in
             [()] + [(a,) for a in seed] + list(itertools.combinations(seed, 2))]
    def add(R, A):
        A = frozenset(A)
        if len(A) > 2 or len(A & (S - set(R))): return
        if 34 - len(R) + len(A) > 34: return
        cands.add((R, A))
    for R, r in Rsets:
        if r == 0: continue
        add(R, [T])
        if r == 2:
            for w in empty:
                if w != T: add(R, [T, w])
    for clist in (tc4, tc3):
        for key, st_on, full in clist:
            c = len(st_on)
            ec = [z for z in full if z not in st_on and z != T]
            for R, r in Rsets:
                if r == 0: continue
                t = len(set(R) & set(st_on))
                need = 5 - (c - t)
                if need <= 0 or need > 2: continue
                if need == 1:
                    for z in ec: add(R, [z])
                    if r == 2:
                        for z in ec:
                            for w in empty:
                                if w != z: add(R, [z, w])
                else:
                    if r == 2:
                        for z1, z2 in itertools.combinations(ec, 2):
                            add(R, [z1, z2])
    print(f"unique candidates: {len(cands)}  [{time.time()-t0:.0f}s]")

    def cnt_on(st_on, full, R, A):
        return len(st_on - set(R)) + len(A & full)

    def safe_and_max(R, A):
        Rs = set(R)
        # safety: only curves through an addition can reach 6
        for z in A:
            for st_on, full in tab4.get(z, ()):
                if cnt_on(st_on, full, Rs, A) >= 6: return None
        Sp = (S - Rs) | set(A)
        # maximality over all board cells not in S'
        for e in board:
            if e in Sp: continue
            blocked = False
            for st_on in block5.get(e, ()):
                if not (st_on & Rs): blocked = True; break
            if blocked: continue
            for st_on, full in tab3.get(e, ()):
                if cnt_on(st_on, full, Rs, A) >= 5: blocked = True; break
            if not blocked: return None
        return Sp

    witnesses = []; safe = 0; n = 0
    for R, A in cands:
        n += 1
        Sp = safe_and_max(R, A)
        if Sp is None: continue
        safe += 1
        witnesses.append({"R": sorted(map(list, R)), "A": sorted(map(list, A)),
                          "stones": sorted(map(list, Sp))})
        print("WITNESS R=", sorted(map(list, R)), "A=", sorted(map(list, A)))
    print(f"checked={n} safe={safe} witnesses={len(witnesses)} [{time.time()-t0:.0f}s]")
    out = {"seed": sorted(map(list, seed)), "target": list(T), "board": [BX, BY], "q": Q,
           "tcurve_census": {"c4": len(tc4), "c3": len(tc3)},
           "candidates": n, "safe": safe, "witnesses": witnesses}
    op = os.path.join(os.path.dirname(here), "output", "surgery-m32.json")
    json.dump(out, open(op, "w"), indent=1)
    print("wrote", op)

if __name__ == "__main__":
    main()
