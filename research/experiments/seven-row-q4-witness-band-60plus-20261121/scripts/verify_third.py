#!/usr/bin/env python3
"""Third independent verification system: pure brute force with direct 4x4
determinants |x y x^2+y^2 1| over all quadruples (safety) and all triples
(cell blocking). Independent of both the JS enumerator and the normalized
line/circle equation verifier. Exact integers only."""
import json, sys
from itertools import combinations
from pathlib import Path

def det4(r1, r2, r3, r4):
    m = [list(r1), list(r2), list(r3), list(r4)]
    det = 0
    for c1 in range(4):
        for c2 in range(4):
            if c2 == c1: continue
            for c3 in range(4):
                if c3 in (c1, c2): continue
                c4 = 6 - c1 - c2 - c3
                perm = (c1, c2, c3, c4)
                inv = sum(1 for a in range(4) for b in range(a + 1, 4) if perm[a] > perm[b])
                sgn = -1 if inv % 2 else 1
                prod = m[0][c1] * m[1][c2] * m[2][c3] * m[3][c4]
                det += sgn * prod
    return det

def check(width, stones):
    s = [tuple(p) for p in stones]
    assert len(s) == 20 and len(set(s)) == 20
    rows = [sum(y == r for x, y in s) for r in range(7)]
    assert sorted(rows) == [2, 3, 3, 3, 3, 3, 3]
    def row(p): x, y = p; return [x, y, x * x + y * y, 1]
    for quad in combinations(s, 4):
        assert det4(row(quad[0]), row(quad[1]), row(quad[2]), row(quad[3])) != 0, f'unsafe quad {quad}'
    deficient = rows.index(2); occ = set(s); uncovered = []
    for x in range(width):
        p = (x, deficient)
        if p in occ: continue
        blocked = any(det4(row(p), row(t[0]), row(t[1]), row(t[2])) == 0 for t in combinations(s, 3))
        if not blocked: uncovered.append(x)
    assert not uncovered, f'uncovered {uncovered}'
    return True

def main():
    cases = json.loads(Path(sys.argv[1]).read_text())
    ok = 0
    for c in cases:
        check(c['width'], c['stones'])
        ok += 1
    print('THIRD SYSTEM OK:', ok, 'witnesses, widths', sorted({c['width'] for c in cases}))

if __name__ == '__main__':
    main()
