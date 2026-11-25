#!/usr/bin/env python3
"""Independent exhaustive check of arbitrary-petal sunflower quota terminal spectra."""
from collections import Counter
from itertools import product
from math import comb, prod
from random import Random


def predicted(c, xs, ps, z=0):
    jmax = min((c, *ps))
    jmin = min(jmax, max(0, min(p - x for p, x in zip(ps, xs))))
    counts = Counter()
    lengths = []
    for j in range(jmin, jmax + 1):
        a = [min(x, p - j) for x, p in zip(xs, ps)]
        k = z + j + sum(a)
        counts[k] += comb(c, j) * prod(comb(x, aa) for x, aa in zip(xs, a))
        lengths.append(k)
    assert lengths == sorted(lengths, reverse=True)
    assert max(counts) == lengths[0] and min(counts) == lengths[-1]
    for j, (before, after) in enumerate(zip(lengths, lengths[1:]), jmin):
        active = sum(p - x <= j for p, x in zip(ps, xs))
        assert before - after == active - 1
    missing = sum(max(0, sum(p - x <= j for p, x in zip(ps, xs)) - 2)
                  for j in range(jmin, jmax))
    assert missing == max(counts) - min(counts) + 1 - len(counts)
    return counts


def brute(c, xs, ps, z=0):
    n = c + sum(xs) + z
    quota_masks = []
    core = (1 << c) - 1
    off = c
    for x in xs:
        quota_masks.append(core | (((1 << x) - 1) << off))
        off += x
    counts = Counter()
    states = 0
    for s in range(1 << n):
        states += 1
        if any((s & e).bit_count() > p for e, p in zip(quota_masks, ps)):
            continue
        # Independently test all one-point extensions; do not reuse j-based formula.
        maximal = True
        for v in range(n):
            if s & (1 << v):
                continue
            child = s | (1 << v)
            if all((child & e).bit_count() <= p for e, p in zip(quota_masks, ps)):
                maximal = False
                break
        if maximal:
            counts[s.bit_count()] += 1
    return counts, states


def main():
    boards = states = 0
    by_r = Counter()
    for r in (2, 3, 4):
        prange = range(1, 4) if r < 4 else range(1, 3)
        for c in range(4):
            for xs in product(range(4), repeat=r):
                if c + sum(xs) > 9:
                    continue
                for ps in product(prange, repeat=r):
                    got, seen = brute(c, xs, ps)
                    want = predicted(c, xs, ps)
                    assert got == want, (r, c, xs, ps, got, want)
                    boards += 1
                    states += seen
                    by_r[r] += 1
    rng = Random(20261101)
    random_boards = random_states = 0
    for _ in range(300):
        r = rng.randint(2, 8)
        c = rng.randint(0, 4)
        xs = tuple(rng.randint(0, 3) for _ in range(r))
        ps = tuple(rng.randint(1, 5) for _ in range(r))
        z = rng.randint(0, 2)
        if c + sum(xs) + z > 12:
            continue
        got, seen = brute(c, xs, ps, z)
        want = predicted(c, xs, ps, z)
        assert got == want, (r, c, xs, ps, z, got, want)
        random_boards += 1
        random_states += seen
    assert predicted(2, (1, 2, 2), (2, 2, 2)) == {2: 1, 4: 8, 5: 1}
    print(f'PASS systematic_boards={boards} systematic_subsets={states} by_r={dict(by_r)} '
          f'random_boards={random_boards} random_subsets={random_states} '
          'irregular_example={2:1,4:8,5:1}')


if __name__ == '__main__':
    main()
