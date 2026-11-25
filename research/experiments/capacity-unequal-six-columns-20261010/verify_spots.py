#!/usr/bin/env python3
"""Independent labeled-state audits of selected high-capacity cases and g=5 witnesses."""
from verify_labeled import evaluate
from functools import lru_cache

CASES = [
    ((1, 1, 4, 4, 5, 5), 3, 12, (0, 1, 1, 2, 0, 1), 5),
    ((1, 4, 4, 4, 5, 5), 4, 16, (0, 1, 2, 4, 0, 1), 5),
    ((1, 2, 3, 4, 5, 7), 2, 8, None, None),
    ((1, 2, 3, 4, 5, 7), 3, 12, None, None),
    ((2, 3, 4, 5, 6, 7), 4, 16, None, None),
    ((3, 4, 5, 6, 7, 7), 5, 23, None, None),
    ((7, 7, 7, 7, 7, 7), 2, 9, None, None),
    ((7, 7, 7, 7, 7, 7), 3, 15, None, None),
    ((7, 7, 7, 7, 7, 7), 4, 19, None, None),
    ((7, 7, 7, 7, 7, 7), 5, 26, None, None),
]

def root_sg(c, h, r, root):
    @lru_cache(None)
    def sg(x):
        children = []
        for i in range(len(c)):
            if x[i] == c[i]:
                continue
            y = x[:i] + (x[i]+1,) + x[i+1:]
            if sum(sorted(y, reverse=True)[:h]) <= r:
                children.append(sg(y))
        g = 0
        while g in children:
            g += 1
        return g
    value = sg(root)
    return value, sg.cache_info().currsize

for c, h, r, root, expected in CASES:
    max_g, n, example = evaluate(c, h, r)
    assert max_g <= 5
    if root is not None:
        value, reachable = root_sg(c, h, r, root)
        assert value == expected == 5
        assert max_g >= value
        print(f'c={c} h={h} r={r}: max_g={max_g}, labeled_states={n}, witness_g={value}, reachable={reachable}')
    else:
        print(f'c={c} h={h} r={r}: max_g={max_g}, labeled_states={n}')
print('VERIFIED: 10 independent labeled-state cases')
