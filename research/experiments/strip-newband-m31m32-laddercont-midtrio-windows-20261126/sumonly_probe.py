#!/usr/bin/env python3
"""sumonly_probe.py — post-recovery sum-only value witness probe
(analysis-time engine diagnostic; candidate law L8, NOT a registered row
sweep and NOT part of the frozen kit-8 output).

The pre-reset session ran wider probes whose artifacts were lost in the
sandbox reset; this is the FRESH reduced-domain re-probe whose printed
counts are the citable ones. Two probes:

R1 (in-sweep families, the rich collision territory): for m in
[mlo..mhi] from argv, z in {25..66}, R=z+m+1 (the published row
convention), sweep m <= S <= min(m+38, z+2), shapes = x0 family
(parts(S,m,3) with X[0]==m, arity <= 3). A multi-shape sum-family is a
fixed (m,z,R,S) with >= 2 in-sweep shapes; L8 violation = the canonical
engine value disagreeing within the family.

R2 (off-convention-R trios, run with mlo=mhi=0): the measured mid-ladder
slices m in {13,15,17,19,20} at their mid-slice z, trio {m,m,m} (S=3m)
vs the same-S registered birth seat, under R offsets -3..+3 around the
row convention (excluding 0): check trio value == seat value.

Usage: sumonly_probe.py <mlo> <mhi>     (R1 chunk)
       sumonly_probe.py 0 0             (R2)
No universal claim; K0832 remains the only PROVED statement; the
standard 11x11 cell remains UNKNOWN; no K slot; no residual verdict.
"""
import json
import sys

sys.setrecursionlimit(100000)
from engine_block import H_canonical as H


def parts(s, lo, arity):
    out = []

    def rec(rem, k, cur):
        if rem == 0:
            if 1 <= len(cur) <= arity:
                out.append(tuple(cur))
            return
        if k == arity:
            return
        for t in range(lo, rem + 1):
            if cur and t < cur[-1]:
                continue
            cur.append(t)
            rec(rem - t, k + 1, cur)
            cur.pop()

    rec(s, 0, [])
    return out


def x0_shapes(m, S):
    return [X for X in parts(S, m, 3) if X and X[0] == m]


def r1(mlo, mhi):
    pos = fam = agree = bad = 0
    for m in range(mlo, mhi + 1):
        for z in range(25, 67):
            R = z + m + 1
            smax = min(m + 38, z + 2)
            by_sum = {}
            H.cache_clear()
            for S in range(m, smax + 1):
                for X in x0_shapes(m, S):
                    pos += 1
                    by_sum.setdefault(S, []).append((X, H(R, X, z)))
            for S, lst in by_sum.items():
                if len(lst) >= 2:
                    fam += 1
                    if len(set(v for _, v in lst)) == 1:
                        agree += 1
                    else:
                        bad += 1
                        print('L8-VIOLATION R1', m, z, R, S, lst)
    return {'probe': 'R1', 'm_range': [mlo, mhi], 'z_range': [25, 66],
            'positions': pos, 'sum_families': fam, 'families_agree': agree,
            'violations': bad}


MID_SLICE = {13: (37, 39), 15: (43, 45), 17: (49, 51), 19: (55, 57),
             20: (58, 60)}


def r2():
    chk = bad = 0
    rows = []
    for m, (z, S) in sorted(MID_SLICE.items()):
        seat = tuple(sorted((m, S - m), reverse=True))
        for off in (-3, -2, -1, 1, 2, 3):
            R = z + m + 1 + off
            H.cache_clear()
            vt = H(R, (m, m, m), z)
            vs = H(R, seat, z)
            ok = (vt == vs)
            chk += 1
            bad += (0 if ok else 1)
            rows.append({'m': m, 'z': z, 'S': S, 'R': R, 'R_offset': off,
                         'trio_value': vt, 'seat_value': vs, 'agree': ok})
            if not ok:
                print('L8-VIOLATION R2', m, z, R, vt, vs)
    return {'probe': 'R2', 'checks': chk, 'violations': bad, 'rows': rows}


def main():
    mlo, mhi = int(sys.argv[1]), int(sys.argv[2])
    if mlo == 0:
        print(json.dumps({'result': 'SUMONLY-R2', 'probe': r2()},
                         sort_keys=True, separators=(',', ':')))
    else:
        print(json.dumps({'result': 'SUMONLY-R1', 'probe': r1(mlo, mhi)},
                         sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
)
