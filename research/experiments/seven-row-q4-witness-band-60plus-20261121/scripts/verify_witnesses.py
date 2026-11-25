#!/usr/bin/env python3
"""Independent exact verifier for 7-row q=4 deficient-maximal witnesses (width >= 60).
Generalized from the pinned verifier in seven-row-q4-width59-two-swap-20261115:
normalized integer line/circle equations, no floating point. System #2 of the two
independent integer arithmetic systems required by the lane declaration."""
import json, sys
from itertools import combinations
from math import gcd
from pathlib import Path

def norm_line(p, q):
    x1, y1 = p; x2, y2 = q
    a, b, c = y2 - y1, x1 - x2, x2 * y1 - x1 * y2
    g = gcd(gcd(abs(a), abs(b)), abs(c))
    if g: a, b, c = a // g, b // g, c // g
    if a < 0 or (a == 0 and b < 0): a, b, c = -a, -b, -c
    return a, b, c

def norm_circle(p, q, r):
    x1, y1 = p; x2, y2 = q; x3, y3 = r
    s1 = x1 * x1 + y1 * y1; s2 = x2 * x2 + y2 * y2; s3 = x3 * x3 + y3 * y3
    det = x1 * (y2 - y3) - y1 * (x2 - x3) + (x2 * y3 - x3 * y2)
    if det == 0: return None
    B = s1 * (y2 - y3) - y1 * (s2 - s3) + (s2 * y3 - s3 * y2)
    C = x1 * (s2 - s3) - s1 * (x2 - x3) + (x2 * s3 - x3 * s2)
    D = x1 * (y2 * s3 - y3 * s2) - y1 * (x2 * s3 - x3 * s2) + s1 * (x2 * y3 - x3 * y2)
    a, b, c, d = det, -B, -C, -D
    g = gcd(gcd(gcd(abs(a), abs(b)), abs(c)), abs(d))
    if g: a, b, c, d = a // g, b // g, c // g, d // g
    if a < 0: a, b, c, d = -a, -b, -c, -d
    return a, b, c, d

def on_line(co, p): a, b, c = co; x, y = p; return a * x + b * y + c == 0
def on_circle(co, p): a, b, c, d = co; x, y = p; return a * (x * x + y * y) + b * x + c * y + d == 0

def verify(width, stones):
    s = [tuple(p) for p in stones]
    assert len(s) == 20 and len(set(s)) == 20 and all(0 <= x < width and 0 <= y < 7 for x, y in s), 'board/shape'
    rows = [sum(y == r for x, y in s) for r in range(7)]
    assert sorted(rows) == [2, 3, 3, 3, 3, 3, 3], f'row counts {rows}'
    deficient = rows.index(2)
    lines = {norm_line(p, q) for p, q in combinations(s, 2)}
    lm = {c: [p for p in s if on_line(c, p)] for c in lines}
    circles = {c for tri in combinations(s, 3) if (c := norm_circle(*tri)) is not None}
    cm = {c: [p for p in s if on_circle(c, p)] for c in circles}
    ml = max(map(len, lm.values())); mc = max(map(len, cm.values()))
    assert ml <= 3 and mc <= 3, 'unsafe: 4 concyclic stones'
    occ = set(s); uncovered = []
    for x in range(width):
        p = (x, deficient)
        if p in occ: continue
        blocked = any(len(m) >= 3 and on_line(c, p) for c, m in lm.items()) or \
                  any(len(m) >= 3 and on_circle(c, p) for c, m in cm.items())
        if not blocked: uncovered.append(x)
    assert not uncovered, f'uncovered def-row cells {uncovered}'
    return {'width': width, 'stones': [list(p) for p in s], 'row_counts': rows, 'deficient_row': deficient,
            'safety': {'method': 'normalized integer line/circle equations', 'distinct_lines': len(lines), 'distinct_circles': len(circles), 'max_line_points': ml, 'max_circle_points': mc, 'safe': True},
            'maximality': {'deficient_row_empty_cells_all_blocked': True, 'uncovered_cells': []}}

def main():
    src = Path(sys.argv[1]); dst = Path(sys.argv[2])
    cases = json.loads(src.read_text())
    out = {'scope': 'exact finite witness verification of listed stones; no absence claims', 'verified_witnesses': []}
    for c in cases:
        v = verify(c['width'], c['stones'])
        v['tag'] = c.get('tag', f"w{c['width']}")
        out['verified_witnesses'].append(v)
    dst.write_text(json.dumps(out, indent=1) + '\n')
    print('OK', len(out['verified_witnesses']), 'witnesses verified, widths', sorted({c['width'] for c in cases}))

if __name__ == '__main__':
    main()
