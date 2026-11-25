#!/usr/bin/env python3
"""Exact occupancy mex and independent rational lifted-rank subset audit."""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, combinations_with_replacement
import json
from pathlib import Path


def rational_rank(rows):
    a = [[Fraction(x) for x in row] for row in rows]
    rank = 0
    for column in range(len(a[0])):
        pivot = next((i for i in range(rank, len(a)) if a[i][column]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        scale = a[rank][column]
        a[rank] = [x / scale for x in a[rank]]
        for i in range(rank + 1, len(a)):
            factor = a[i][column]
            if factor:
                a[i] = [x - factor * y for x, y in zip(a[i], a[rank])]
        rank += 1
        if rank == len(a):
            break
    return rank


def mex(values):
    result = 0
    while result in values:
        result += 1
    return result


def occupancy_game(w, m, r):
    @lru_cache(None)
    def grundy(x):
        values = set()
        for i in range(w):
            if x[i] == m:
                continue
            y = list(x)
            y[i] += 1
            y.sort(reverse=True)
            if y[0] + y[1] <= r:
                values.add(grundy(tuple(y)))
        return mex(values)
    return grundy


def occupancy_audit(w, r, m=None):
    if m is None:
        m = r
    grundy = occupancy_game(w, m, r)
    terminals = set()
    histogram = Counter()
    count = 0
    for asc in combinations_with_replacement(range(m + 1), w):
        x = tuple(reversed(asc))
        if x[0] + x[1] > r:
            continue
        count += 1
        value = grundy(x)
        histogram[value] += 1
        options = []
        for i in range(w):
            if x[i] < m:
                y = list(x)
                y[i] += 1
                y.sort(reverse=True)
                if y[0] + y[1] <= r:
                    options.append(tuple(y))
        if not options:
            terminals.add(x)
        if w % 2 == 0:
            assert value == (min(2*m, r) - sum(x)) % 2, (w, r, m, x, value)
    expected = ({(m,) * w} if 2*m <= r else
                {(a,) + (r - a,) * (w - 1)
                 for a in range((r + 1) // 2, min(m, r) + 1)})
    assert terminals == expected, (w, r, terminals, expected)
    a = (r + 1) // 2
    witness = (a,) + (r - a - 1,) * (w - 1)
    if w % 2 and m >= a + 1:
        assert grundy(witness) == 2, (w, r, witness)
    if w % 2:
        assert (max(histogram) <= 1) == (m <= (r + 1)//2)
    return {
        'w': w, 'q': r + 1, 'm': m,
        'safe_occupancy_orbits': count,
        'grundy_histogram_over_occupancy_orbits': dict(sorted(histogram.items())),
        'empty_grundy': grundy((0,) * w),
        'terminal_occupancies': sorted(terminals),
        'terminal_sizes': sorted({sum(x) for x in terminals}),
        'explicit_witness': witness if m >= a + 1 else None,
        'witness_grundy': grundy(witness) if m >= a + 1 else None,
    }


def geometric_subset_audit(base, m, q):
    points = [(x, y, z) for x, y in base for z in range(m)]
    n, w, r = len(points), len(base), q - 1
    lifted = [[x*x + y*y + z*z, x, y, z, 1] for x, y, z in points]
    forbidden = []
    for indices in combinations(range(n), q):
        if rational_rank([lifted[i] for i in indices]) < 5:
            forbidden.append(sum(1 << i for i in indices))
    # Subset DP derives safety solely from exact lifted rank, independently
    # of the occupancy theorem. Occupancy is only used after this for comparison.
    values = {}
    safe_by_size = Counter()
    grundy_histogram = Counter()
    terminals = set()
    occupancy = occupancy_game(w, m, r)
    for size in range(n, -1, -1):
        for indices in combinations(range(n), size):
            mask = sum(1 << i for i in indices)
            safe = not any(mask & edge == edge for edge in forbidden)
            counts = tuple(sum(bool(mask & (1 << (i*m + j))) for j in range(m)) for i in range(w))
            ordered = tuple(sorted(counts, reverse=True))
            predicted = ordered[0] + ordered[1] <= r
            assert safe == predicted, (base, m, q, indices, counts)
            if not safe:
                continue
            next_values = {values[mask | (1 << i)] for i in range(n)
                           if not mask & (1 << i) and mask | (1 << i) in values}
            value = mex(next_values)
            assert value == occupancy(ordered), (counts, value, occupancy(ordered))
            if not next_values:
                terminals.add(counts)
            values[mask] = value
            safe_by_size[size] += 1
            grundy_histogram[value] += 1
    assert values, 'zero-state audit is invalid'
    return {
        'base': base, 'm': m, 'q': q, 'points': n,
        'q_subsets_rank_checked': sum(1 for _ in combinations(range(n), q)),
        'forbidden_q_subsets': len(forbidden),
        'subsets_safety_checked': 1 << n,
        'safe_subsets_grundy_checked': len(values),
        'safe_by_size': dict(sorted(safe_by_size.items())),
        'grundy_histogram': dict(sorted(grundy_histogram.items())),
        'empty_grundy': values[0],
        'terminal_sizes': sorted({sum(x) for x in terminals}),
    }


def main():
    if not __debug__:
        raise SystemExit('Assertions must remain enabled.')
    # Non-cospherical full-rank points and a plane independently exercise the
    # rank routine; all single points/small row sets would be deficient anyway.
    assert rational_rank([[0, 0, 0, 0, 1], [1, 1, 0, 0, 1],
                          [1, 0, 1, 0, 1], [1, 0, 0, 1, 1],
                          [4, 2, 0, 0, 1]]) == 5
    result = {
        'scope': '3D q-point hyperplane/hypersphere variant, not standard 2D game',
        'occupancy_audits': [occupancy_audit(w, r) for w in range(3, 7)
                            for r in range(2*w, 2*w + 3)],
        'all_length_boundary_audits': [occupancy_audit(w, r, m)
                                      for w in range(3, 7)
                                      for r in range(2*w, 2*w + 3)
                                      for m in range(1, r + 1)],
        'independent_geometric_subset_audits': [
            geometric_subset_audit([(0, 0), (1, 0), (0, 1)], 4, 7),
            geometric_subset_audit([(0, 0), (2, 0), (1, 3)], 4, 7),
            geometric_subset_audit([(0, 0), (0, 1), (1, 0), (1, 1)], 3, 9),
        ],
    }
    target = Path(__file__).with_name('output.json')
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f"{len(result['occupancy_audits'])} long and "
          f"{len(result['all_length_boundary_audits'])} boundary occupancy audits; "
          f"{len(result['independent_geometric_subset_audits'])} independent rank subset audits passed")


if __name__ == '__main__':
    main()
