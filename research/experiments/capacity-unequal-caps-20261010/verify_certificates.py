#!/usr/bin/env python3
"""Verify a complete finite game-tree Grundy certificate without solving by recursion."""
import json
from pathlib import Path


def check(case):
    caps = tuple(case['caps'])
    h, r = case['h'], case['r']
    root = tuple(case['root'])
    rows = {tuple(row['x']): row for row in case['states']}
    assert len(rows) == len(case['states'])
    assert root in rows
    assert case['slack'] == r - sum(sorted(root, reverse=True)[:h])
    assert all(0 <= x <= cap for row in rows.values() for x, cap in zip(row['x'], caps))
    assert all(sum(sorted(row['x'], reverse=True)[:h]) <= r for row in rows.values())
    # Independent legal-child reconstruction, not trusting the certificate's edges.
    def successors(x):
        ans = []
        for i, cap in enumerate(caps):
            if x[i] >= cap:
                continue
            y = list(x)
            y[i] += 1
            if sum(sorted(y, reverse=True)[:h]) <= r:
                ans.append(tuple(y))
        return set(ans)
    seen = {root}
    pending = [root]
    while pending:
        x = pending.pop()
        actual = successors(x)
        listed = {tuple(y) for y in rows[x]['children']}
        assert actual == listed, (case['name'], x, actual ^ listed)
        for y in actual:
            assert y in rows, (case['name'], 'missing state', y)
            if y not in seen:
                seen.add(y)
                pending.append(y)
    assert seen == set(rows), 'certificate contains unreachable states'
    for x, row in rows.items():
        child_values = {rows[y]['grundy'] for y in successors(x)}
        mex = next(k for k in range(len(child_values) + 1) if k not in child_values)
        assert mex == row['grundy'], (case['name'], x, mex, row['grundy'])
    assert rows[root]['grundy'] == case['root_grundy']
    assert case['slack'] % 2 == 0 and case['root_grundy'] in (2, 3)
    print('VERIFIED', case['name'], 'reachable_states', len(rows),
          'root_grundy', case['root_grundy'], 'root_slack', case['slack'])


def main():
    path = Path(__file__).with_name('certificates.json')
    for case in json.loads(path.read_text()):
        check(case)


if __name__ == '__main__':
    main()
