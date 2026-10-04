#!/usr/bin/env python3
"""Full-state odd-r SG formula: labeled mex and shared canonical cross-check.

Parameters below also include small abstract pair-cap games outside q>2w.
Only the proved geometric reduction is used to transfer results to the prism.
"""
from functools import lru_cache
from itertools import combinations_with_replacement, product
import json
from pathlib import Path

from verify import occupancy_game

if not __debug__:
    raise SystemExit('Assertions must remain enabled; do not use python -O.')


def mex(values):
    result = 0
    while result in values:
        result += 1
    return result


def odd_r_formula(x, r):
    """For odd w>=3, odd r>=1, pair-safe x and m>=r."""
    if not len(x) % 2 or len(x) < 3 or not r % 2:
        raise ValueError('odd w>=3 and odd r are required')
    k = r // 2
    a = max(x)
    if a <= k:
        return (k + 1 - sum(x)) % 2
    dominant = x.index(a)
    gaps = [r - a - count for i, count in enumerate(x) if i != dominant]
    if min(gaps) < 0:
        raise ValueError('unsafe occupancy')
    return 2 * (min(gaps) % 2) + sum(gaps) % 2


def labeled_pair_audit(w, r):
    """Traverse every reachable labeled state without sorting or quotienting.

    Every pair-safe vector is reachable from zero: its subsets are pair-safe.
    Formula checks therefore cover the complete finite state space.
    """
    histogram = {}

    @lru_cache(None)
    def grundy(x):
        values = set()
        for i in range(w):
            if all(x[i] + 1 + x[j] <= r for j in range(w) if i != j):
                y = x[:i] + (x[i] + 1,) + x[i+1:]
                values.add(grundy(y))
        value = mex(values)
        if r % 2:
            assert value == odd_r_formula(x, r), (w, r, x, value)
        # The high-region reduction also holds for even r.
        a = max(x)
        if 2 * a > r:
            dominant = x.index(a)
            gaps = [r-a-x[j] for j in range(w) if j != dominant]
            assert value == 2*(min(gaps) % 2) + sum(gaps) % 2
        histogram[value] = histogram.get(value, 0) + 1
        return value

    root = grundy((0,) * w)
    expected = 1 if r % 4 == 1 else 0
    assert root == expected, (w, r, root)
    return dict(w=w, r=r, m=r, root_grundy=root,
                full_labeled_safe_states=grundy.cache_info().currsize,
                grundy_histogram=dict(sorted(histogram.items())),
                odd_r_full_formula_checked=bool(r % 2),
                high_region_formula_checked=True)


def gap_audit(n, maximum):
    @lru_cache(None)
    def grundy(y):
        values = {grundy(y[:i] + (v-1,) + y[i+1:])
                  for i, v in enumerate(y) if v}
        if min(y):
            values.add(grundy(tuple(v-1 for v in y)))
        value = mex(values)
        assert value == 2*(min(y) % 2) + sum(y) % 2, (n, y, value)
        return value

    for y in product(range(maximum+1), repeat=n):
        grundy(y)
    return dict(n=n, max_gap=maximum,
                full_labeled_states=grundy.cache_info().currsize)


def canonical_audit(w, r):
    grundy = occupancy_game(w, r, r)
    count = 0
    for asc in combinations_with_replacement(range(r+1), w):
        x = tuple(reversed(asc))
        if x[0] + x[1] > r:
            continue
        if r % 2:
            assert grundy(x) == odd_r_formula(x, r), (w, r, x)
        count += 1
    root = grundy((0,) * w)
    assert root == (1 if r % 4 == 1 else 0)
    return dict(w=w, r=r, m=r, root_grundy=root,
                full_canonical_safe_states=count,
                odd_r_full_formula_checked=bool(r % 2))


def main():
    result = dict(
        scope='Odd-column abstract pair-cap game, m>=r; prism transfer requires q=r+1>2w.',
        universal_evidence='Mathematical mex proof and explicit parity-pair response; finite audits only check implementations.',
        labeled_pair_audits=[labeled_pair_audit(w, r)
                             for w, high in [(3, 17), (5, 13), (7, 9)]
                             for r in range(1, high+1)],
        independent_gap_audits=[gap_audit(2, 12), gap_audit(4, 6), gap_audit(6, 4)],
        shared_canonical_audits=[canonical_audit(w, r)
                                for w in [7, 9] for r in [2*w, 2*w+1, 2*w+2]],
    )
    target = Path(__file__).with_name('odd-root-output.json')
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print('Odd-r complete SG formula and all-r odd-w root rule verified:',
          sum(row['full_labeled_safe_states'] for row in result['labeled_pair_audits']),
          'labeled pair-safe states;',
          sum(row['full_labeled_states'] for row in result['independent_gap_audits']),
          'labeled gap states;',
          sum(row['full_canonical_safe_states'] for row in result['shared_canonical_audits']),
          'canonical states.')


if __name__ == '__main__':
    main()
