#!/usr/bin/env python3
"""All lengths, even capacity, odd columns: independent complete mex audits.

The unbounded claim rests on even-capacity-proof.md; these are finite audits.
The formula applies to pair-safe states with any common column length m>=1.
Transfer to the geometric prism additionally requires q=r+1>2w.
"""
from collections import Counter
from functools import lru_cache
from itertools import combinations_with_replacement
import json
from math import factorial
from pathlib import Path
import sys

if not __debug__:
    raise SystemExit('Assertions must remain enabled; do not use python -O.')

SOURCE = Path(__file__).resolve().parents[1] / 'prism-hyperplane-2026-10-05'
sys.path.insert(0, str(SOURCE))
from verify import occupancy_game


def formula(x, r, m):
    if len(x) < 3 or not len(x) % 2 or r < 2 or r % 2 or m < 1:
        raise ValueError('odd w>=3, even r>=2, and m>=1 are required')
    if min(x) < 0 or max(x) > m:
        raise ValueError('invalid column count')
    ordered = sorted(x, reverse=True)
    a, b = ordered[:2]
    if a + b > r:
        raise ValueError('unsafe pair capacity')
    if b < r-m:
        return (sum(x)+m) % 2
    return 2 * ((a-b) % 2) + (sum(x)-a) % 2


def labeled_game(w, r, m, audit=False):
    """Direct labeled recurrence: no sorting and no state identification."""
    @lru_cache(None)
    def grundy(x):
        values = set()
        for i, count in enumerate(x):
            if count == m:
                continue
            if any(count+1+x[j] > r for j in range(w) if j != i):
                continue
            child = x[:i] + (count+1,) + x[i+1:]
            values.add(grundy(child))
        result = 0
        while result in values:
            result += 1
        if audit:
            assert result == formula(x, r, m), (w, r, m, x, result)
        return result
    return grundy


def labeled_audit(w, r, m):
    grundy = labeled_game(w, r, m, audit=True)
    root = grundy((0,) * w)
    # All safe labeled vectors are reachable by adding their entries in any order.
    histogram = Counter()
    safe_count = 0
    for ordered in combinations_with_replacement(range(m+1), w):
        if ordered[-1] + ordered[-2] > r:
            continue
        # Every distinct labeling has equal Grundy but is visited independently.
        multiplicities = Counter(ordered)
        labels = factorial(w)
        for amount in multiplicities.values():
            labels //= factorial(amount)
        safe_count += labels
        expected = formula(ordered, r, m)
        value = grundy(ordered)
        assert value == expected, (w, r, ordered, value, expected)
        histogram[value] += labels
    # The recurrence asserts at each new labeled state; counts independently
    # establish that the root traversal included every safe labeling.
    assert safe_count == grundy.cache_info().currsize
    assert root == (m % 2 if m < r else 0)
    if m >= r and r >= 4:
        assert grundy((2, 1) + (0,) * (w-2)) == 3
    return dict(w=w, r=r, m=m, root_grundy=root,
                full_labeled_safe_states=safe_count,
                grundy_histogram=dict(sorted(histogram.items())))


def canonical_audit(w, r, m):
    grundy = occupancy_game(w, m, r)
    count = 0
    histogram = Counter()
    for b in range(min(m, r//2)+1):
        for others in combinations_with_replacement(range(b+1), w-2):
            for a in range(b, min(m, r-b)+1):
                x = (a, b) + tuple(reversed(others))
                value = grundy(x)
                assert value == formula(x, r, m), (w, r, m, x, value)
                histogram[value] += 1
                count += 1
    return dict(w=w, r=r, m=m, full_canonical_safe_states=count,
                grundy_histogram=dict(sorted(histogram.items())))


def scope_counterexamples():
    examples = []
    for scope, w, r, m, x in [
        ('even column count', 4, 6, 6, (1, 0, 0, 0)),
        ('odd capacity', 3, 5, 5, (0, 0, 0)),
    ]:
        grundy = labeled_game(w, r, m)
        value = grundy(x)
        a, b = sorted(x, reverse=True)[:2]
        unsupported = 2*((a-b) % 2)+(sum(x)-a) % 2
        assert value != unsupported, (scope, x, value)
        try:
            formula(x, r, m)
        except ValueError:
            pass
        else:
            raise AssertionError('scope guard failed')
        examples.append(dict(violated_scope=scope, w=w, r=r, m=m,
                             x=x, exact_grundy=value,
                             unsupported_formula=unsupported))
    # The old long-board formula is demonstrably wrong on a short board;
    # the new finite-length branch fixes this instance exactly.
    x = (2, 1, 1)
    actual = labeled_game(3, 4, 2)(x)
    assert actual == formula(x, 4, 2) == 0
    assert 2*((x[0]-x[1]) % 2)+(sum(x)-x[0]) % 2 == 2
    return dict(unsupported_scope_counterexamples=examples,
                cap_correction_example=dict(w=3, r=4, m=2, x=x,
                                            exact_grundy=actual,
                                            old_long_formula=2))


def main():
    result = dict(
        scope='Odd w>=3, even r>=2, all m>=1; geometric transfer requires q=r+1>2w.',
        universal_evidence='Complete mathematical mex proof in even-capacity-proof.md.',
        labeled_long_audits=[labeled_audit(w, r, r)
                        for w, high in [(3, 20), (5, 14), (7, 10)]
                        for r in range(2, high+1, 2)],
        labeled_all_lengths_audits=[labeled_audit(w, r, m)
                                    for w, high in [(3, 12), (5, 10), (7, 8)]
                                    for r in range(2, high+1, 2)
                                    for m in range(1, r+1)],
        shared_canonical_long_audits=[canonical_audit(w, r, r)
                                for w, capacities in [(3, [20, 24, 30]),
                                                      (5, [14, 18, 22]),
                                                      (7, [14, 16, 18]),
                                                      (9, [18, 20, 22]),
                                                      (11, [12, 14, 16])]
                                for r in capacities],
        shared_canonical_all_lengths_audits=[canonical_audit(w, r, m)
                                            for w, high in [(3, 20), (5, 16),
                                                            (7, 12), (9, 10)]
                                            for r in range(2, high+1, 2)
                                            for m in range(1, r+1)],
        scope_counterexamples=scope_counterexamples(),
    )
    target = Path(__file__).with_name('even-capacity-output.json')
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print('Even-r full SG formula independently verified:',
          sum(row['full_labeled_safe_states'] for key in
              ['labeled_long_audits', 'labeled_all_lengths_audits']
              for row in result[key]),
          'labeled states;',
          sum(row['full_canonical_safe_states'] for key in
              ['shared_canonical_long_audits', 'shared_canonical_all_lengths_audits']
              for row in result[key]),
          'canonical states; scope counterexamples and cap correction checked.')


if __name__ == '__main__':
    main()
