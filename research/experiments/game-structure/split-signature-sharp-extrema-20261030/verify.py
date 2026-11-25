#!/usr/bin/env python3
"""Exact signature-class optimization for split Node Kayles uniform play."""
from fractions import Fraction
from functools import lru_cache
from itertools import product, permutations


def compositions(total, parts):
    if parts == 0:
        if total == 0:
            yield ()
        return
    if parts == 1:
        yield (total,)
        return
    for x in range(total + 1):
        for rest in compositions(total - x, parts - 1):
            yield (x,) + rest


def balanced(n, s):
    if not n:
        assert not s
        return 1
    a, r = divmod(s, n)
    return (a + 1) ** (n - r) * (a + 2) ** r


def hub_factor(k, n, s):
    """Independent subset recursion for high-degree centers, in exact fractions."""
    H = [Fraction(0)] * (1 << k)
    H[0] = Fraction(1)
    for S in range(1, 1 << k):
        union_weight = sum(n[b] + s[b] for b in range(1 << k) if b & S)
        numerator = sum((H[S ^ (1 << h)] for h in range(k) if (S >> h) & 1), Fraction(0))
        H[S] = numerator / (S.bit_count() + union_weight)
    return sum(((-1 if S.bit_count() % 2 else 1) * H[S]
                for S in range(1 << k)), Fraction(0))


def extrema_by_signatures(m, degrees, L):
    """Return exact sharp extrema and witnesses for any fixed number k of special centers."""
    k = len(degrees)
    G = 1 << k
    minimum = None
    maximum = None
    witnesses = [None, None]
    candidates = 0
    for n in compositions(m, G):
        if any(sum(n[b] for b in range(G) if (b >> h) & 1) != degrees[h]
               for h in range(k)):
            continue
        active = [b for b in range(G) if n[b]]
        for active_s in compositions(L, len(active)):
            s = [0] * G
            for b, v in zip(active, active_s):
                s[b] = v
            factor = hub_factor(k, n, s)
            denominator_min = 1
            denominator_max = 1
            for b in active:
                denominator_min *= balanced(n[b], s[b])
                denominator_max *= s[b] + 1
            lower = factor / denominator_min
            upper = factor / denominator_max
            candidates += 1
            if minimum is None or lower < minimum:
                minimum, witnesses[0] = lower, (n, tuple(s))
            if maximum is None or upper > maximum:
                maximum, witnesses[1] = upper, (n, tuple(s))
    assert candidates > 0
    return minimum, maximum, tuple(witnesses), candidates


def probability_by_game(t, neighbors):
    """Independent labeled-graph recursion, no subset-DP formula used."""
    m = len(t)
    center_neighborhoods = []
    for j, count in enumerate(t):
        center_neighborhoods.extend([1 << j] * count)
    center_neighborhoods.extend(neighbors)

    @lru_cache(None)
    def rec(I, C):
        if C == 0:
            return Fraction(1)
        if I == 0:
            return Fraction(0)
        total = Fraction(0)
        for j in range(m):
            if not (I >> j) & 1:
                continue
            nxt = C
            for h, N in enumerate(center_neighborhoods):
                if (C >> h) & 1 and (N >> j) & 1:
                    nxt &= ~(1 << h)
            total += rec(I ^ (1 << j), nxt)
        return total / (I.bit_count() + C.bit_count())

    return rec((1 << m) - 1, (1 << len(center_neighborhoods)) - 1)


def brute_classes(m, k, L):
    """Enumerate every labeled neighborhood and degree-one-center assignment."""
    classes = {}
    checks = 0
    for neighborhoods in product(range(1 << m), repeat=k):
        degrees = tuple(N.bit_count() for N in neighborhoods)
        for t in compositions(L, m):
            value = probability_by_game(t, neighborhoods)
            if degrees not in classes:
                classes[degrees] = [value, value]
            else:
                classes[degrees][0] = min(classes[degrees][0], value)
                classes[degrees][1] = max(classes[degrees][1], value)
            checks += 1
    return classes, checks


def probability_by_permutations(t, neighbors):
    """Third method: enumerate all vertex priority orders, including skipped vertices."""
    m = len(t)
    centers = []
    for j, count in enumerate(t):
        centers.extend([1 << j] * count)
    centers.extend(neighbors)
    N = m + len(centers)
    successes = 0
    trials = 0
    for order in permutations(range(N)):
        I = (1 << m) - 1
        C = (1 << len(centers)) - 1
        ok = True
        for v in order:
            if v < m:
                if (I >> v) & 1:
                    I ^= 1 << v
                    for c, mask in enumerate(centers):
                        if (mask >> v) & 1:
                            C &= ~(1 << c)
            elif (C >> (v - m)) & 1:
                ok = False
                break
        successes += ok
        trials += 1
    return Fraction(successes, trials)


def main():
    classes_checked = 0
    graph_checks = 0
    signature_candidates = 0
    # All labeled graphs in these ranges, not sampled.
    cases = [(2, 0, 0), (3, 0, 3),
             (2, 1, 2), (3, 1, 3), (4, 1, 3),
             (2, 2, 2), (3, 2, 3), (4, 2, 2),
             (2, 3, 2), (3, 3, 2)]
    for m, k, L in cases:
        actual, checks = brute_classes(m, k, L)
        graph_checks += checks
        for degrees, (true_min, true_max) in actual.items():
            lower, upper, _, candidates = extrema_by_signatures(m, degrees, L)
            assert lower == true_min, ('minimum', m, k, L, degrees, lower, true_min)
            assert upper == true_max, ('maximum', m, k, L, degrees, upper, true_max)
            classes_checked += 1
            signature_candidates += candidates
    # The first counterexample to 'smaller hub overlap always minimizes'.
    m, k, L = 3, 2, 1
    A = 0b011
    B_low = 0b101
    B_high = 0b011
    h_low = min(probability_by_game(t, (A, B_low)) for t in compositions(L, m))
    h_high = min(probability_by_game(t, (A, B_high)) for t in compositions(L, m))
    assert h_low == Fraction(37, 144)
    assert h_high == Fraction(1, 4)
    assert probability_by_permutations((0, 0, 1), (A, B_low)) == h_low
    assert probability_by_permutations((0, 0, 1), (A, B_high)) == h_high
    lower, upper, _, _ = extrema_by_signatures(3, (2, 2), 1)
    assert lower == Fraction(1, 4)
    assert upper == Fraction(3, 10)
    print('PASS:', classes_checked, 'degree classes;', graph_checks,
          'labeled graph configurations;', signature_candidates,
          'signature candidates; two full priority-order audits; no disagreements')
    print('counterexample m=3, degrees=(2,2), L=1: min overlap 1 =', h_low,
          '; min overlap 2 =', h_high, '; global extrema =', lower, upper)


if __name__ == '__main__':
    main()
