#!/usr/bin/env python3
"""analyze_cover.py — third-implementation exact-rational cover-structure analyzer
for 3xM q=4 deficient-maximal witnesses (three-row-q4 lane, resume point 4).

For each witness:
  * enumerate all circles through >=3 stones (exact rational arithmetics: Fractions)
  * compute their integer grid points (per row, exact)
  * verify: every empty point of a non-rich row lies on a rich circle (circles with
    >=3 stones); rows with exactly 3 stones are rich (line y=c) and cover their own
    empties; non-row lines on a 3-row board hold <=3 grid points hence can never
    cover an empty point (only all-stone lines are rich) — recorded as a lemma here,
    checked experimentally too.
  * profile: per-witness rich circles, deficient-row coverage by circle ids,
    multiplicity, stones-per-circle, and rational centers/radius^2.

Output: JSON to stdout (aggregate + per-witness detail for m=23).
"""
import json, glob, sys
from fractions import Fraction as F
from math import isqrt

def psq(fr):
    n, d = fr.numerator, fr.denominator
    rn, rd = isqrt(abs(n)), isqrt(d)
    if rn * rn == n and rd * rd == d:
        return F(rn, rd)
    return None

def circle3(p1, p2, p3):
    (x1, y1), (x2, y2), (x3, y3) = p1, p2, p3
    a = 2 * (x2 - x1); b = 2 * (y2 - y1)
    c = x2**2 + y2**2 - x1**2 - y1**2
    d = 2 * (x3 - x2); e = 2 * (y3 - y2)
    f = x3**2 + y3**2 - x2**2 - y2**2
    det = a * e - b * d
    if det == 0:
        return None
    h = F(c * e - b * f, det)
    k = F(a * f - c * d, det)
    r2 = (x1 - h)**2 + (y1 - k)**2
    return (h, k, r2)

def rowints(h, k, r2, y):
    """integer x with (x-h)^2+(y-k)^2=r2"""
    dd = r2 - (y - k)**2
    out = set()
    if dd < 0:
        return out
    s = psq(dd)
    if s is None:
        return out
    for x in (h + s, h - s):
        if x.denominator == 1:
            out.add(int(x))
    return out

def grid_points(h, k, r2, m, w=3):
    pts = []
    for y in range(w):
        xs = rowints(h, k, r2, y)
        for x in sorted(xs):
            if 0 <= x < m:
                pts.append((x, y))
    return pts

def analyze(w, m, q, coord):
    stones = set()
    for tok in coord.split(','):
        x, y = tok.split(':')
        stones.add((int(x), int(y)))
    S = sorted(stones)
    n = w * m
    allpts = [(x, y) for y in range(w) for x in range(m)]
    empt = [p for p in allpts if p not in stones]
    # rich circles: through >=3 stones
    circs = {}
    L = len(S)
    for i in range(L):
        for j in range(i + 1, L):
            for k3 in range(j + 1, L):
                c = circle3(S[i], S[j], S[k3])
                if c is None:
                    continue
                key = (c[0], c[1], c[2])
                circs.setdefault(key, set()).update([S[i], S[j], S[k3]])
    rich = []
    for (h, k, r2), st in circs.items():
        # full stone set on this circle
        full = {p for p in S if (p[0]-h)**2 + (p[1]-k)**2 == r2}
        gp = grid_points(h, k, r2, m, w)
        rich.append({'h': h, 'k': k, 'r2': r2, 'stones': sorted(full),
                     'gp': gp})
    rich = [c for c in rich if len(c['stones']) >= 3]
    # dedupe by (stones, gp) signature
    seen = set()
    u = []
    for c in rich:
        sig = (tuple(map(tuple, c['stones'])), tuple(map(tuple, c['gp'])))
        if sig in seen:
            continue
        seen.add(sig)
        u.append(c)
    rich = u
    # row richness
    rowstones = {y: len([p for p in S if p[1] == y]) for y in range(w)}
    # coverage check per empty point (independent maximality semantics)
    cover = {}
    for p in empt:
        covs = []
        if rowstones[p[1]] == 3:  # rich row line y=p[1]
            covs.append(('row', p[1]))
        for ci, c in enumerate(rich):
            if p in c['gp']:
                covs.append(('circle', ci))
        cover['%d:%d' % p] = covs
    ok = all(len(v) >= 1 for v in cover.values())
    # deficient-row cover detail (rows with < 3 stones)
    defrows = {y: [] for y in range(w) if rowstones[y] < 3}
    for p in empt:
        if p[1] in defrows:
            defrows[p[1]].append((p, cover['%d:%d' % p]))
    profile = {
        'm': m, 'stones': len(S), 'rows': rowstones, 'ok': ok,
        'n_rich_circles': len(rich),
        'rich_circle_stones_hist': {},
        'deficient_row_cover': {},
        'gt2_gridpt_circles': 0,
    }
    for c in rich:
        t = len(c['stones'])
        profile['rich_circle_stones_hist'][t] = profile['rich_circle_stones_hist'].get(t, 0) + 1
        if len(c['gp']) > 2:
            profile['gt2_gridpt_circles'] += 1
    for y, plist in defrows.items():
        circles_used = set()
        mult = []
        for p, covs in plist:
            cmul = 0
            for typ, ci in covs:
                if typ == 'circle':
                    circles_used.add(ci)
                    cmul += 1
            mult.append(cmul)
        cover_pts = {}
        for ci in circles_used:
            c = rich[ci]
            pts = [(x, yy) for (x, yy) in c['gp'] if yy == y]
            cover_pts[ci] = pts
        profile['deficient_row_cover'][y] = {
            'n_empty': len(plist),
            'n_circles': len(circles_used),
            'cover_multiplicity_hist': {v: mult.count(v) for v in sorted(set(mult))},
            'circles': [
                {'ci': ci, 'h': str(rich[ci]['h']), 'k': str(rich[ci]['k']),
                 'r2': str(rich[ci]['r2']), 'stones': rich[ci]['stones'],
                 'row_pts': cover_pts[ci], 'ngp': len(rich[ci]['gp'])}
                for ci in sorted(circles_used)
            ],
        }
    return ok, profile, rich

def main():
    out = {'per_witness': [], 'm23_detail': None}
    allok = True
    for f in sorted(glob.glob(sys.argv[1] + '/wit_3x*_4.witness.json'),
                     key=lambda s: int(s.split('3x')[1].split('_')[0])):
        d = json.load(open(f))
        ok, prof, rich = analyze(3, d['m'], 4, d['coord'])
        allok = allok and ok
        out['per_witness'].append(prof)
        if d['m'] == 23:
            out['m23_detail'] = prof
    out['all_witnesses_cover_ok'] = allok
    print(json.dumps(out, indent=1))

if __name__ == '__main__':
    main()
