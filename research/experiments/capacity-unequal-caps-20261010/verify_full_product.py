#!/usr/bin/env python3
"""Independent bottom-up DP on the entire labelled feasible box, not a root tree."""
import json
from itertools import product
from pathlib import Path


def main():
    cases = json.loads(Path(__file__).with_name('certificates.json').read_text())
    for case in cases:
        caps = case['caps']
        h, r = case['h'], case['r']
        safe = lambda x: sum(sorted(x, reverse=True)[:h]) <= r
        states = sorted((x for x in product(*(range(c + 1) for c in caps)) if safe(x)),
                        key=lambda x: -sum(x))
        values = {}
        for x in states:
            opts = set()
            for i in range(len(caps)):
                if x[i] >= caps[i]:
                    continue
                y = x[:i] + (x[i] + 1,) + x[i + 1:]
                if safe(y):
                    opts.add(values[y])
            mex = 0
            while mex in opts:
                mex += 1
            values[x] = mex
        root = tuple(case['root'])
        assert values[root] == case['root_grundy']
        for row in case['states']:
            assert values[tuple(row['x'])] == row['grundy']
        print('FULL_PRODUCT_PASS', case['name'], 'all_safe_states', len(states),
              'root', root, 'grundy', values[root])


if __name__ == '__main__':
    main()
