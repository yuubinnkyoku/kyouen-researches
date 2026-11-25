#!/usr/bin/env python3
"""Exact occupied-mask bottom-up Grundy verification (Python 3, stdlib only)."""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

CASES = {
    'rank_le4_five_edges_9_nimber7': {
        'n': 9, 'edges': [[1, 3, 4], [1, 7], [3, 5, 7, 8], [2, 5, 7], [5, 6]],
        'expected': 7,
    },
    'rank4_five_edges_12': {
        'n': 12, 'expected': 6,
        'edges': [[1, 3, 4, 8], [3, 5, 9, 10], [0, 1, 9, 11],
                  [0, 2, 7, 8], [6, 7, 9, 11]],
    },
    'rank_le4_five_edges_8': {
        'n': 8, 'expected': 6,
        'edges': [[1, 4], [2, 5, 7], [0, 1, 5, 6], [6, 7], [1, 3, 6]],
    },
}


def solve(n, edges, expected):
    e_masks = [sum(1 << v for v in edge) for edge in edges]
    assert len(set(e_masks)) == len(e_masks)
    assert all(2 <= len(e) <= 4 for e in edges)
    assert all(not (a & b) == a for i, a in enumerate(e_masks)
               for j, b in enumerate(e_masks) if i != j)
    limit = 1 << n
    sg = [-1] * limit
    for mask in range(limit - 1, -1, -1):
        if any(mask & e == e for e in e_masks):
            continue
        children = set()
        for v in range(n):
            if not (mask >> v) & 1:
                val = sg[mask | (1 << v)]
                if val != -1:
                    children.add(val)
        value = 0
        while value in children:
            value += 1
        sg[mask] = value
    assert sg[0] == expected
    options = {str(v): sg[1 << v] for v in range(n)}
    assert set(options.values()) == set(range(expected))
    return {
        'n': n, 'edges': edges, 'root_grundy': sg[0],
        'first_move_grundy': options,
        'safe_position_count': sum(x >= 0 for x in sg),
        'grundy_distribution': {str(k): v for k, v in sorted(Counter(x for x in sg if x >= 0).items())},
        'sha256_sg_vector': sha256(','.join(map(str, sg)).encode()).hexdigest(),
    }, sg


def main():
    result = {}
    for key, case in CASES.items():
        info, _ = solve(**case)
        result[key] = info
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    path = Path(__file__).with_name('result.json')
    if path.exists():
        assert json.loads(path.read_text()) == result, 'result.json differs from verified computation'


if __name__ == '__main__':
    main()
