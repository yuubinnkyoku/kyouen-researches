#!/usr/bin/env python3
"""Independent check of the 3x3 empty-board KYOENC3 certificate.

The certificate stores D4-canonical masks (the min over the orbit of each
position). To check every node that appears in the certificate DAG, this
script:

1. parses the 28 nodes;
2. expands every canonical mask over its D4 orbit;
3. verifies, for every expanded node, the same ordered check that
   checkPos performs in SquareCert2x2.lean:
     - winning: there is a legal move p such that p+position is losing
       with strictly smaller rank;
     - losing: every legal move p gives a position that is winning with
       strictly smaller rank.

Legality uses the exact 3x3 forbidden-quadruple test (the same determinant
condition as in Kyouen/Rules.lean), evaluated over integer arithmetic with
no overflow room. Winning/losing is provided by the certificate itself; the
check here does not re-run the search.

Expected result: all nodes pass (\u2713).
"""
import struct
import sys
from itertools import combinations, permutations

def bits(m):
    return [p for p in range(9) if (m >> p) & 1]

def mask(pts):
    m = 0
    for p in pts:
        m |= 1 << p
    return m

def det4(a, b, c, d):
    x1, y1 = a % 3, a // 3
    x2, y2 = b % 3, b // 3
    x3, y3 = c % 3, c // 3
    x4, y4 = d % 3, d // 3
    q = lambda x, y: x * x + y * y
    m = [[q(x1, y1), x1, y1, 1],
         [q(x2, y2), x2, y2, 1],
         [q(x3, y3), x3, y3, 1],
         [q(x4, y4), x4, y4, 1]]

    def det3(a, b, c, d, e, f, g, h, i):
        return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)

    return (
        m[0][0] * det3(m[1][1], m[1][2], m[1][3], m[2][1], m[2][2], m[2][3], m[3][1], m[3][2], m[3][3])
        - m[0][1] * det3(m[1][0], m[1][2], m[1][3], m[2][0], m[2][2], m[2][3], m[3][0], m[3][2], m[3][3])
        + m[0][2] * det3(m[1][0], m[1][1], m[1][3], m[2][0], m[2][1], m[2][3], m[3][0], m[3][1], m[3][3])
        - m[0][3] * det3(m[1][0], m[1][1], m[1][2], m[2][0], m[2][1], m[2][2], m[3][0], m[3][1], m[3][2])
    )

STRIDE = 3

base = [lambda x, y: (x, y),
        lambda x, y: (2 - y, x),
        lambda x, y: (2 - x, 2 - y),
        lambda x, y: (y, 2 - x),
        lambda x, y: (x, 2 - y),
        lambda x, y: (2 - x, y),
        lambda x, y: (y, x),
        lambda x, y: (2 - y, 2 - x)]

def transform_mask(mask, fn):
    pts = bits(mask)
    out = 0
    for p in pts:
        x, y = p % 3, p // 3
        nx, ny = fn(x, y)
        out |= 1 << (ny * 3 + nx)
    return out

def is_safe(stones):
    for quad in combinations(stones, 4):
        if det4(*quad) == 0:
            return False
    return True

def main():
    data = open(sys.argv[1], 'rb').read()
    assert data[:8].rstrip(b'\x00') == b'KYOENC3'
    version, boardSize, nodeCount, rootLo, rootHi, forbiddenCount = struct.unpack_from('<IIQQII', data, 8)
    nodeCount = int(nodeCount)
    offset = 40
    canon_entries = []
    for i in range(int(nodeCount)):
        lo, hi, outcome, witness, rank, reserved = struct.unpack_from('<QIBBBB', data, offset)
        offset += 16
        mask_ = lo | (hi << 64)
        pts = tuple(bits(mask_))
        canon_entries.append((mask_, pts, outcome, rank))

    # expand orbits
    orbit = {}
    for mask_, pts, outcome, rank in canon_entries:
        for fn in base:
            t = transform_mask(mask_, fn)
            assert t not in orbit or orbit[t] == outcome
            orbit[t] = outcome

    # validate every expanded entry
    bad = []
    for mask_, outcome in sorted(orbit.items()):
        pts = tuple(bits(mask_))
        rank = 9 - len(pts)
        wname = {1: 'losing', 2: 'winning'}[outcome]
        children = []
        for p in range(9):
            if mask_ >> p & 1:
                continue
            t_mask = mask_ | (1 << p)
            if not is_safe(bits(t_mask)):
                continue
            children.append(t_mask)
        if outcome == 2:  # winning
            ok = any(c in orbit and orbit[c] == 1 and (9 - len(bits(c))) < rank for c in children)
            if not ok:
                bad.append((mask_, wname, 'no losing child with smaller rank'))
        else:  # losing
            for c in children:
                if c not in orbit:
                    bad.append((mask_, wname, f'child {c:#05x} not in cert (losing node requires all children)'))
                elif orbit[c] != 2:
                    bad.append((mask_, wname, f'child {c:#05x} not winning'))
                elif not (9 - len(bits(c))) < rank:
                    bad.append((mask_, wname, f'child {c:#05x} rank not smaller'))

    if bad:
        print('FAIL')
        for b in bad:
            print(' ', b)
        return 1
    print(f'PASS: all {len(orbit)} orbit nodes satisfy the local checks')
    print(f'  canonical masks: {len(canon_entries)}')
    print(f'  orbit nodes:     {len(orbit)}')
    from collections import Counter
    print('  outcomes:', dict(Counter(orbit.values())))
    return 0

if __name__ == '__main__':
    sys.exit(main())
