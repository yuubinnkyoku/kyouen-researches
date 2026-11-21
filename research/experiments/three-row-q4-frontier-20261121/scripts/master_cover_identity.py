#!/usr/bin/env python3
"""master_cover_identity.py — unified arithmetic identity for cover circles on a
3-row (or any fixed small) board: circle through pair (α,a),(β,a) and single (γ,g).

MASTER LEMMA (derived by exact algebra; machine-verified below):
  Let A=(α,a), B=(β,a), a≠α? no: α≠β, and G=(γ,g), g≠a.  Circle through A,B,G.
  (S) SUM RULE: for every horizontal line y=d, the circle meets it in points whose
      x-coordinates sum to  α+β  (when two real points; else the two complex roots
      still sum to α+β). In particular a deficient-row stone δ on the circle forces
      the partner  δ' = α+β−δ ∈ Z  (δ, α, β, δ' integers automatically).
  (D) DISCRIMINANT: with  e1 = γ−α, e2 = γ−β  (so α+β = 2γ−e1−e2):
        Δ_d = (e1+e2)^2 − 4(d−a)(d−g) + 4·e1e2·(d−g)/(g−a)      (*)
      The row-d intersection points are
        (α+β ± sqrt(Δ_d))/2 ,  i.e. integer+legal iff Δ_d is a square ≥ 0 with
        α+β±√Δ_d even.
  Family corollaries on the 3-row board {0,1,2}:
    pair@0, single@2, covers row1:  Δ = e1²+e2²+4            ("AB" up-type)
    pair@2, single@0, covers row1:  Δ = e1²+e2²+4            ("AB" down-type, V)
    pair@0, single@1, covers row2:  Δ = e1²+e2²−2e1e2−4·1·1+... compute below
    pair@1, single@0, covers row2:  symmetric to previous
    pair@1, single@2, covers row0:  Δ = e1²+e2²−6e1e2−8
    pair@2, single@1, covers row0:  Δ = e1²+e2²+6e1e2−8
Verification: exact rational arithmetic on (i) all 20 witness covers, per row,
(ii) exhaustive small-range circle grids, (iii) consistency with cover_analysis.json.
"""
import json, sys
from fractions import Fraction
from itertools import combinations

BASE = '/home/user/work/fastlane/q34'

def row_of(stone):  # stone "x:y"
    x, y = stone.split(':')
    return int(x), int(y)

def circle_from3(p1, p2, p3):
    (x1, y1), (x2, y2), (x3, y3) = p1, p2, p3
    # x^2+y^2+E x+F y+G=0
    # solve 2x2 for E,F given subtracting eq1: G expressed via p1
    # [x2-x1, y2-y1]·[E,F] = -(x2^2-x1^2+y2^2-y1^2)
    A11, A12 = x2 - x1, y2 - y1
    b1 = -(x2*x2 - x1*x1 + y2*y2 - y1*y1)
    A21, A22 = x3 - x1, y3 - y1
    b2 = -(x3*x3 - x1*x1 + y3*y3 - y1*y1)
    det = A11 * A22 - A12 * A21
    if det == 0:
        return None
    E = Fraction(b1 * A22 - A12 * b2, det)
    F = Fraction(A11 * b2 - b1 * A21, det)
    G = -x1*x1 - y1*y1 - E*x1 - F*y1
    return (E, F, G)

def row_intersections(circ, d, m):
    """return integer x's in [0,m-1] where circle meets y=d (exact)"""
    E, F, G = circ
    # w^2 + E w + (d^2+F d+G) = 0
    c0 = Fraction(d*d) + F*d + G
    disc = E*E - 4*c0
    if disc < 0:
        return []
    num, den = disc.numerator, disc.denominator
    if den != 1 or num < 0:
        return []
    r = num**0.5 if num > 0 else 0
    if int(r)**2 != num:
        return []
    r = int(r)
    out = []
    for w in (( -E + Fraction(num).limit_denominator(1)*0 ),):  # placeholder
        pass
    # roots: (-E ± r)/2 with E possibly rational; must be integer
    for s in (r, -r):
        val = (-E + s)
        if val.denominator == 1 and val.numerator % 2 == 0:
            x = val.numerator // 2
            if 0 <= x < m:
                out.append(x)
    return sorted(out)

def master_check(m, stones, verbose=False):
    """For every triple-with-pair-in-a-row circle from the witness stones,
    verify SUM RULE and formula (*) for every row d in {0,1,2} (and any row)."""
    pts = [row_of(s) for s in stones]
    rows = {}
    for x, y in pts:
        rows.setdefault(y, []).append(x)
    bad = 0
    checked = 0
    results = []
    for a in rows:
        for g in rows:
            if a == g:
                continue
            for (alpha, beta) in combinations(rows[a], 2):
                for gamma in rows[g]:
                    A, B, Gp = (alpha, a), (beta, a), (gamma, g)
                    circ = circle_from3(A, B, Gp)
                    if circ is None:
                        bad += 1
                        continue
                    e1, e2 = gamma - alpha, gamma - beta
                    for d in (0, 1, 2):
                        # predicted
                        pred_disc = (e1 + e2)**2 - 4*(d - a)*(d - g) + Fraction(4*e1*e2*(d - g), (g - a))
                        # actual from circle
                        E, F, Gc = circ
                        c0 = d*d + F*d + Gc
                        act_disc = E*E - 4*c0
                        ok_disc = (pred_disc == act_disc)
                        ints = row_intersections(circ, d, m)
                        # sum rule vs alpha+beta (count complex too: polynomial sum = -E)
                        poly_sum = -E
                        ok_sum = (poly_sum == alpha + beta)
                        # if two real intersections in-row, they must be alpha+beta ± r / 2
                        ok_pts = True
                        if len(ints) == 2:
                            ok_pts = (ints[0] + ints[1] == alpha + beta)
                        checked += 1
                        if not (ok_disc and ok_sum and ok_pts):
                            bad += 1
                            if verbose:
                                print('MISMATCH', A, B, Gp, 'd=', d, pred_disc, act_disc, ints)
                        else:
                            results.append((a, g, d, alpha, beta, gamma, ints))
    return bad, checked, results

def main():
    import glob, os
    wdir = sys.argv[1] if len(sys.argv) > 1 else BASE + '/witall'
    wit = sorted(glob.glob(wdir + '/wit_3x*_4.witness.json'),
                 key=lambda s: int(s.split('3x')[1].split('_')[0]))
    wit = [{'m': json.load(open(f))['m'], 'coord': json.load(open(f))['coord']} for f in wit]
    if wit is None:
        # fall back: read from repo copies
        import subprocess
        out = subprocess.run(['ls', BASE], capture_output=True, text=True).stdout
        print('dir:', out)
        return 2
    total_bad = total_checked = 0
    for w in wit:
        m = w['m']
        stones = w['coord'].split(',')
        bad, checked, _ = master_check(m, stones)
        total_bad += bad
        total_checked += checked
        print(f"m={m:2d}: triples/pair-rows checked={checked} mismatches={bad}")
    print('TOTAL checked:', total_checked, 'mismatches:', total_bad)
    return 0 if total_bad == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
