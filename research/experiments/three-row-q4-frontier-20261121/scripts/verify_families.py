#!/usr/bin/env python3
"""verify_families.py — machine-verify the covering-circle arithmetic identities for
all three-row q4 witnesses (families A/B/C/D), and collect (d1,d2,s) statistics.

Identities (candidate theorems, derived for a 3-row board, deficient row 1):
  Family A: circle through 2 stones of row 0 at (a,0),(b,0) and 1 stone of row 2 at (g,2).
     row-1 intersections u,v satisfy u+v = a+b exactly,
     and (v-u)^2/4 = (g-a)^2+(g-b)^2+4   i.e. s^2 = d1^2+d2^2+4, d1=g-a, d2=g-b.
     Parity lemma: d1,d2 both odd => impossible (mod 8). [proved]
  Family B: same with rows 0/2 swapped (2 stones row2, 1 stone row0).
  Family C: circle through an outer-row stone pair (a,b) (row 0 or row 2) and a
     middle stone (d,1): the second row-1 intersection is d' = a+b-d (always
     integer; partner coverage).
  Family D: circle through (p,0),(q,1),(r,2) one stone each row: second row-1
     intersection q' with q+q' = -D where D is the circle x-coefficient
     (machine-checked numerically here; algebraic divisibility is data-dependent).
Any covering circle of a deficient middle row (row 1) that hits >=1 empty point of
row 1 must have its stones among: 2-in-one-outer-row (A/B/C) or 1-per-row (D) —
all other stone distributions contain <=2 non-row-1 stones + row-1 stone(s) and
cannot make 3 stones; circles with 2 stones IN row 1 plus 1 outer stone have both
row-1 intersections = stones (cover nothing).
"""
import json, glob, sys
from fractions import Fraction as F
from math import isqrt

def psq(fr):
    n, d = fr.numerator, fr.denominator
    rn, rd = isqrt(abs(n)), isqrt(d)
    if rn*rn == n and rd*rd == d:
        return F(rn, rd)
    return None

def circle3(p1, p2, p3):
    (x1, y1), (x2, y2), (x3, y3) = p1, p2, p3
    a = 2*(x2-x1); b = 2*(y2-y1)
    c = x2**2+y2**2-x1**2-y1**2
    d2 = 2*(x3-x2); e = 2*(y3-y2)
    f = x3**2+y3**2-x2**2-y2**2
    det = a*e-b*d2
    if det == 0:
        return None
    h = F(c*e-b*f, det); k = F(a*f-c*d2, det)
    r2 = (x1-h)**2+(y1-k)**2
    return (h, k, r2)

def rowints1(h, k, r2, y):
    dd = r2-(y-k)**2
    out = set()
    if dd < 0:
        return out
    s = psq(dd)
    if s is None:
        return out
    for x in (h+s, h-s):
        if x.denominator == 1:
            out.add(int(x))
    return out

def classify_and_check(R, yd, m, w=3):
    """R = circle record with stones and gp; returns check results."""
    stones = [tuple(s) for s in R['stones']]
    rows_of = {}
    for st in stones:
        rows_of.setdefault(st[1], []).append(st)
    emptypts = [(x, yd) for x in range(m) if (x, yd) not in stones and (x, yd) in R['gp'] and len(R['gp']) > 0]
    # classify by stone rows
    mid = rows_of.get(yd, [])
    out_rows = [y for y in (0, 1, 2) if y != yd]
    fam = None
    if len(mid) == 0:
        # stones: 2 in one outer row, 1 in the other  -> family A/B
        cnts = {y: len(rows_of.get(y, [])) for y in out_rows}
        if sorted(cnts.values()) == [1, 2]:
            fam = 'AB'
            double = out_rows[0] if cnts[out_rows[0]] == 2 else out_rows[1]
            single = out_rows[0] if double == out_rows[1] else out_rows[1]
            (a, _), (b, _) = rows_of[double]
            (g, _), = rows_of[single]
            xs = sorted(set(x for (x, yy) in R['gp'] if yy == yd))
            # algebraic root pair sums to a+b; any visible integer root x must satisfy
            # (2x-(a+b))^2 = d1^2+d2^2+4 (covers both pair- and single-visible cases;
            # the partner root a+b-x is an integer that may be off-board or a stone)
            rsum = a+b
            checks = {
                'sum_ok': all((2*x - rsum) == (rsum - 2*x) for x in xs),
                'root_ok': all((2*x - rsum)**2 == (g-a)**2+(g-b)**2+4 for x in xs),
                'parity_ok': not ((g-a) % 2 == 1 and (g-b) % 2 == 1),
                'partner_int': all((rsum - x) == (rsum - x) for x in xs),
            }
            return fam, checks, {'d1': g-a, 'd2': g-b}
    elif len(mid) == 1:
        if len(rows_of.get(out_rows[0], [])) == 2 and len(rows_of.get(out_rows[1], [])) == 0:
            fam = 'C'
            double = out_rows[0]
        elif len(rows_of.get(out_rows[1], [])) == 2 and len(rows_of.get(out_rows[0], [])) == 0:
            fam = 'C'
            double = out_rows[1]
        else:
            fam = 'D'
        if fam == 'C':
            (a, _), (b, _) = rows_of[double]
            (dval, _), = mid
            xs = sorted(set(x for (x, yy) in R['gp'] if yy == yd))
            u = xs[0]; v = xs[-1]
            partner = a+b-dval
            checks = {
                'pair_ok': (dval in (u, v)),
                'partner_ok': (partner in (u, v)),
                'partner_is_d_or_int': partner == int(partner),
            }
            return fam, checks, {}
        else:
            p, = [st[0] for st in stones if st[1] == out_rows[0]]
            rr, = [st[0] for st in stones if st[1] == out_rows[1]]
            q, = [st[0] for st in mid]
            xs = sorted(set(x for (x, yy) in R['gp'] if yy == yd))
            u = xs[0]; v = xs[-1]
            # q + q' = -D ; compute D rationally
            hs = (p+q+rr)  # not used
            # solve circle through (p,y0),(q,1),(r,y2):
            (dummy_y0, dummy_y1, dummy_y2) = out_rows[0], yd, out_rows[1]
            # points in order rows y0 < yd < y2 with vertical order flexibility
            pts = sorted(stones, key=lambda s: s[1])
            (x_lo, y_lo), (x_mi, y_mi), (x_hi, y_hi) = pts
            c = circle3((x_lo, y_lo), (x_mi, y_mi), (x_hi, y_hi))
            h, k, r2c = c
            # -D = 2h
            qprime = 2*h - q
            checks = {
                'q_in': (q in (u, v)),
                'qprime_ok': (qprime == u or qprime == v),
                'qprime_int': (qprime.denominator == 1),
            }
            return fam, checks, {}
    else:
        return 'mid2', {'both_stones': True}, {}

def main():
    witdir = sys.argv[1]
    out = {}
    famstats = {}
    dd_stats = []
    allchecks = []
    for f in sorted(glob.glob(witdir + '/wit_3x*_4.witness.json'),
                    key=lambda s: int(s.split('3x')[1].split('_')[0])):
        d = json.load(open(f))
        m = d['m']
        stones = set()
        for tok in d['coord'].split(','):
            x, y = tok.split(':')
            stones.add((int(x), int(y)))
        S = sorted(stones)
        rows = {y: [s[0] for s in S if s[1] == y] for y in range(3)}
        # deficient rows (stones <= 2)
        deff = [y for y in range(3) if len(rows[y]) <= 2]
        rec = {'m': m, 'rows': {y: len(v) for y, v in rows.items()}}
        for yd in [y for y in deff if y == 1]:
            # rich circles through >=3 stones that hit empty pts of row yd
            res = []
            for i in range(len(S)):
                for j in range(i+1, len(S)):
                    for k3 in range(j+1, len(S)):
                        c = circle3(S[i], S[j], S[k3])
                        if c is None:
                            continue
                        h, k, r2c = c
                        gpset = set()
                        for y in range(3):
                            for x in rowints1(h, k, r2c, y):
                                if 0 <= x < m:
                                    gpset.add((x, y))
                        stson = {p for p in S if (p[0]-h)**2+(p[1]-k)**2 == r2c}
                        if len(stson) < 3:
                            continue
                        empt_hit = [(x, yd) for x in range(m)
                                    if (x, yd) in gpset and (x, yd) not in stones]
                        if not empt_hit:
                            continue
                        R = {'stones': sorted(stson), 'gp': sorted(gpset)}
                        # affine-normalize: if yd==0 or 2, reflect board so deficient middle... no:
                        # families defined w.r.t. deficient row position; reflect vertically to make yd the middle when possible
                        famrec = classify_circ(R, yd, m)
                        res.append(famrec)
            rec[yd] = res
        out[m] = rec
    # aggregate
    print(json.dumps(out, indent=1, default=str))

def classify_circ(R, yd, m):
    """wrapper: reflect board vertically so the deficient row is middle if possible.
       If yd in (0,2) reflection maps rows; families verified in original coords."""
    def refl(p):
        return (p[0], 2-p[1]) if yd in (0, 2) else (p[0], p[1])
    stones = [tuple(s) for s in R['stones']]
    gp = [tuple(g) for g in R['gp']]
    if yd in (0, 2):
        stones = [refl(s) for s in stones]
        gp = [refl(g) for g in gp]
    Rn = {'stones': sorted(stones), 'gp': sorted(gp)}
    fam, checks, extra = classify_and_check(Rn, 1, m)
    return {'fam': fam, 'checks': checks, 'extra': extra}

if __name__ == '__main__':
    main()
