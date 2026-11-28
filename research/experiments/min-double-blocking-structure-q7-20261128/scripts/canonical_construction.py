#!/usr/bin/env python3
"""General 2-fold blocking construction in AG(2,q) from a triangle.

Canonical triangle (all field ops from boards.field):
  l1: y = 0,  l2: x = 0,  l3: x + y = 1
  vertices v3 = l1^l2 = (0,0), v1 = l2^l3 = (0,1), v2 = l1^l3 = (1,0)
  anti-parallels D1: y = 1 (through v1 || l1), D2: x = 1,
                    D3: x + y = 0 (through v3 || l3).
  char 2: D1^D2^D3 = (1,1)  ->  C = triangle u {R}     size 3q-2
  odd char: R12 = D1^D2 = (1,1), R3 = (1,-1) on D3
            ->  C = triangle u {R12, R3}               size 3q-1
Every output set is verified against the full line list (each line >= 2).
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from boards import affine_plane, field

def construct(q):
    add, mul, neg, one = field(q)
    pts, lines = affine_plane(q)
    idx = {p: i for i, p in enumerate(pts)}
    def pt(x, y): return idx[(x, y)]
    l1 = set(pt(x, 0) for x in range(q))
    l2 = set(pt(0, y) for y in range(q))
    l3 = set(pt(x, add(1, neg(x))) for x in range(q))
    acc = one
    char = None
    for c in range(2, q + 2):
        acc = add(acc, one)
        if acc == 0:
            char = c
            break
    if char == 2:
        C = l1 | l2 | l3 | {pt(1, 1)}
    else:
        C = l1 | l2 | l3 | {pt(1, 1), pt(1, neg(1))}
    L = [set(l) for l in lines]
    cnts = [len(C & s) for s in L]
    return {'q': q, 'char': char, 'size': len(C),
            'expected': 3 * q - (2 if char == 2 else 1),
            'min_line_count': min(cnts),
            'all_lines_ge_2': min(cnts) >= 2,
            'C': sorted(C)}

if __name__ == '__main__':
    out = {}
    for q in [int(x) for x in sys.argv[1:]]:
        r = construct(q)
        out['ag2q%d' % q] = r
        print(json.dumps(r))
    if os.environ.get('SAVE'):
        json.dump(out, open(os.environ['SAVE'], 'w'), indent=1)
