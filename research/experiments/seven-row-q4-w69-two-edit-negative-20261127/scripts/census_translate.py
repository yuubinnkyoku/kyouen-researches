#!/usr/bin/env python3
"""Fast D4-mirror x translation census for 7-row q=4 deficient-maximal witnesses.

For each published base (20 stones) and each of its 4 board symmetries,
compute once the set of deficient-row x-coordinates blocked by 3-stone
lines/circles, then scan integer x-shifts arithmetically to find the largest
board width W covered (all deficient-row cells [0,W) occupied or blocked),
with all stones inside [0,W). Safety and row-multiset are checked once per
base (translation/mirror invariant). Pure integer arithmetic.
"""
import json, sys
from itertools import combinations
from math import gcd, isqrt

def conc4(a, b, c, d):
    x1, y1 = a; x2, y2 = b; x3, y3 = c; x4, y4 = d
    ux, uy = x2-x1, y2-y1
    az = x2*x2+y2*y2 - x1*x1-y1*y1
    vx, vy = x3-x1, y3-y1
    vz = x3*x3+y3*y3 - x1*x1-y1*y1
    wx, wy = x4-x1, y4-y1
    wz = x4*x4+y4*y4 - x1*x1-y1*y1
    det = ux*(vy*wz - vz*wy) - uy*(vx*wz - vz*wx) + az*(vx*wy - vy*wx)
    return det == 0

def base_ok(stones):
    rows = [0]*7
    for _, y in stones: rows[y] += 1
    if sorted(rows) != [2,3,3,3,3,3,3]: return None
    s = list(stones)
    for quad in combinations(range(20), 4):
        if conc4(s[quad[0]], s[quad[1]], s[quad[2]], s[quad[3]]):
            return None
    return rows.index(2)

def blocked_row_cells(stones, y0):
    """x-coordinates of points on row y0 lying on some 3-stone line or circle."""
    blocked = set()
    s = list(stones)
    for tri in combinations(range(20), 3):
        p, q, r = s[tri[0]], s[tri[1]], s[tri[2]]
        x1, y1 = p; x2, y2 = q; x3, y3 = r
        d2 = x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2)
        if d2 == 0:
            # line p,q,r: primitive direction
            dx, dy = x2-x1, y2-y1
            g = gcd(abs(dx), abs(dy)); dx //= g; dy //= g
            if dy == 0:
                continue  # horizontal line never meets other rows' cells
            t_num = y0 - y1
            if t_num % dy == 0:
                t = t_num // dy
                blocked.add(x1 + t*dx)
        else:
            # circumcircle: a(x^2+y^2)+bx+cy+d=0 with integer a,b,c,d
            s1 = x1*x1+y1*y1; s2 = x2*x2+y2*y2; s3 = x3*x3+y3*y3
            det = x1*(y2-y3) - y1*(x2-x3) + (x2*y3 - x3*y2)
            B = s1*(y2-y3) - y1*(s2-s3) + (s2*y3 - s3*y2)
            C = x1*(s2-s3) - s1*(x2-x3) + (x2*s3 - x3*s2)
            D = x1*(y2*s3 - y3*s2) - y1*(x2*s3 - x3*s2) + s1*(x2*y3 - x3*y2)
            a, b, c, d = det, -B, -C, -D
            g = gcd(gcd(gcd(abs(a), abs(b)), abs(c)), abs(d))
            if g: a, b, c, d = a//g, b//g, c//g, d//g
            if a < 0: a, b, c, d = -a, -b, -c, -d
            # row y0: a*x^2 + b*x + (a*y0^2 + c*y0 + d) = 0
            q0 = a*y0*y0 + c*y0 + d
            disc = b*b - 4*a*q0
            if disc < 0: continue
            sq = isqrt(disc)
            if sq*sq != disc: continue
            for num in (-b + sq, -b - sq):
                if num % (2*a) == 0:
                    blocked.add(num // (2*a))
    return blocked

def main():
    bases = json.load(open(sys.argv[1]))
    target = int(sys.argv[2]) if len(sys.argv) > 2 else 69
    hits = []
    best_overall = []
    for b in bases:
        stones = [tuple(p) for p in b['stones']]
        y0 = base_ok(stones)
        if y0 is None:
            continue  # e.g. non-deficient anchor shapes; census only concerns valid bases
        mx = max(x for x, _ in stones)
        for name, img in [
            ('id', stones),
            ('V', [(mx - x, y) for x, y in stones]),
            ('H', [(x, 6 - y) for x, y in stones]),
            ('HV', [(mx - x, 6 - y) for x, y in stones]),
        ]:
            y0i = y0 if 'H' not in name else 6 - y0
            mxi = max(x for x, _ in img)
            occ_x = {x for x, y in img if y == y0i}
            bl = blocked_row_cells(img, y0i)
            best = 0; bestdx = 0
            for dx in range(0, 200):
                occ = {x + dx for x in occ_x}
                bls = {x + dx for x in bl}
                W = 0
                while (W in occ) or (W in bls):
                    W += 1
                    if W > 400: break
                if mxi + dx < W and W > best:
                    best = W; bestdx = dx
            best_overall.append((best, b['tag'], name, bestdx))
            if best >= target:
                shifted = sorted([((x + bestdx), y) for x, y in img])
                hits.append({'tag': b['tag'], 'image': name, 'dx': bestdx,
                             'width': best, 'stones': [[x, y] for x, y in shifted]})
                print('HIT', b['tag'], name, 'dx', bestdx, 'width', best, flush=True)
    best_overall.sort(reverse=True)
    print('TOP widths (width, tag, image, dx):', best_overall[:10])
    print('bases', len(bases), 'hits>=', target, ':', len(hits))
    if hits:
        json.dump(hits, open(sys.argv[3], 'w'), indent=1)
        print('hits written to', sys.argv[3])

if __name__ == '__main__':
    main()
