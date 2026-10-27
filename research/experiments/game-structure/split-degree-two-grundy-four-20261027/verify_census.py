#!/usr/bin/env python3
"""Independent signature-projection census, different from direct C++ vertex recursion."""
from functools import lru_cache
from itertools import combinations_with_replacement

K = 5
TYPES = tuple(s for s in range(1, 1 << K) if s.bit_count() <= 2)
EXPECTED = (9240, 11055, 197015, 102440, 20)


def norm(n):
    return 0 if n == 0 else 1 if n & 1 else 2


@lru_cache(None)
def projection(k, s):
    keep = [i for i in range(k) if not s & (1 << i)]
    return tuple(sum(((t >> i) & 1) << j for j, i in enumerate(keep)) for t in range(1 << k))


@lru_cache(None)
def grundy(k, counts):
    # Independent free vertices contribute xor parity, not extra clique moves.
    if counts[0]:
        return grundy(k, (0,) + counts[1:]) ^ (counts[0] & 1)
    if k == 0:
        return 0
    children = set()
    for j in range(k):
        children.add(sum(n for s, n in enumerate(counts) if not s & (1 << j)) & 1)
    for s in range(1, 1 << k):
        if not counts[s]:
            continue
        mapping = projection(k, s)
        projected = [0] * (1 << (k - s.bit_count()))
        for t, n in enumerate(counts):
            projected[mapping[t]] += n - (t == s)
        children.add(grundy(k - s.bit_count(), tuple(map(norm, projected))))
    return next(x for x in range(8) if x not in children)


def run():
    histogram = [0] * 8
    witnesses = []
    for combo in combinations_with_replacement(TYPES, 8):
        counts = [0] * (1 << K)
        for s in combo:
            counts[s] += 1
        value = grundy(K, tuple(map(norm, counts)))
        histogram[value] += 1
        if value == 4:
            witnesses.append(combo)
    assert tuple(histogram[:5]) == EXPECTED, histogram
    assert not any(histogram[5:]), histogram
    assert len(witnesses) == 20
    assert all(sum(s.bit_count() for s in w) == 14 for w in witnesses)
    print('all_multisets=', sum(histogram))
    print('grundy_histogram=', tuple(histogram))
    print('g4_multisets=', len(witnesses), 'all_cross_edges=14')
    print('all checks passed')


if __name__ == '__main__':
    run()
