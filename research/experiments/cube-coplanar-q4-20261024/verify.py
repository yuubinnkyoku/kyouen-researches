#!/usr/bin/env python3
"""Complete 2x2x2, four-coplanar-forbidden game; independent XOR and determinant checks."""
from collections import Counter
from itertools import combinations
import json

P = [(i & 1, (i >> 1) & 1, (i >> 2) & 1) for i in range(8)]

def determinant4(ids):
    p = P[ids[0]]
    a, b, c = [[P[j][k] - p[k] for k in range(3)] for j in ids[1:]]
    return (a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))

def forbidden_xor(ids):
    # Of the 14 affine F_2 planes, the two parity tetrahedra are not
    # coplanar over R. All remaining 12 are rectangles in R^3.
    parity = {sum(1 << i for i in range(8) if i.bit_count() % 2 == r)
              for r in (0, 1)}
    mask = sum(1 << i for i in ids)
    return (ids[0] ^ ids[1] ^ ids[2] ^ ids[3]) == 0 and mask not in parity

def mex(values):
    value = 0
    while value in values:
        value += 1
    return value

def main():
    forbidden = []
    for ids in combinations(range(8), 4):
        direct = determinant4(ids) == 0
        xor_test = forbidden_xor(ids)
        assert direct == xor_test, ids
        if direct:
            forbidden.append(sum(1 << i for i in ids))
    assert len(forbidden) == 12
    safe = [not any((s & b) == b for b in forbidden) for s in range(256)]
    g, h = {}, {}
    for s in sorted((s for s in range(256) if safe[s]),
                    key=lambda x: x.bit_count(), reverse=True):
        children = [s | (1 << i) for i in range(8)
                    if not (s >> i) & 1 and safe[s | (1 << i)]]
        g[s] = mex({g[t] for t in children})
        h[s] = mex({h[t] for t in children}) if children else 1
    maximal = [s for s in g if not any(s | (1 << i) in g
                for i in range(8) if not (s >> i) & 1)]
    star = {sum(1 << j for j in (v, v ^ 1, v ^ 2, v ^ 4, v ^ 7))
            for v in range(8)}
    assert {s for s in g if s.bit_count() == 5} == star
    assert len(g) == 159 and len(maximal) == 32
    assert g[0] == h[0] == 0
    assert all(g[1 << i] == 2 for i in range(8))
    layers = {str(k): {
        'safe': sum(s.bit_count() == k for s in g),
        'normal': dict(sorted(Counter(g[s] for s in g if s.bit_count() == k).items())),
        'misere_aux': dict(sorted(Counter(h[s] for s in g if s.bit_count() == k).items())),
        'maximal': sum(s.bit_count() == k for s in maximal),
    } for k in range(6)}
    output = {
        'board': '2x2x2', 'rule': 'forbid four coplanar vertices, including degeneracies',
        'forbidden4': len(forbidden), 'safe_states': len(g),
        'maximal_sizes': dict(sorted(Counter(s.bit_count() for s in maximal).items())),
        'maximum_safe_size': 5, 'minimum_maximal_size': 4,
        'normal_empty_grundy': g[0], 'misere_empty_aux': h[0],
        'one_stone_grundy': sorted({g[1 << i] for i in range(8)}),
        'layers': layers,
        'swap_mismatches': sum(h[s] != (1 - g[s] if g[s] <= 1 else g[s]) for s in g),
        'five_stone_masks': sorted(star),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
