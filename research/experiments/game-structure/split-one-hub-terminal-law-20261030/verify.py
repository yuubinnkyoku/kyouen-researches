#!/usr/bin/env python3
"""Independent exact checks for the single-hub split-graph terminal law."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product, permutations
from math import factorial


def formula(t, A):
    m = len(t)
    d = len(A)
    T = sum(t[j] for j in A)
    outside = [j for j in range(m) if j not in A]
    denom = 1
    for j in outside:
        denom *= t[j] + 1
    ans = F(0)
    for bits in range(1 << len(outside)):
        numerator = 1
        power = 0
        for h, j in enumerate(outside):
            if bits >> h & 1:
                numerator *= t[j]
                power += t[j] + 1
        ans += F(numerator, d + T + power + 1)
    return ans / denom


def build(t, A):
    m = len(t)
    n = m + sum(t) + 1
    hub = n - 1
    neigh = [0] * n
    centers = range(m, n)
    for c in centers:
        for h in centers:
            if c != h:
                neigh[c] |= 1 << h
    i = m
    for j, count in enumerate(t):
        for _ in range(count):
            neigh[j] |= 1 << i
            neigh[i] |= 1 << j
            i += 1
    assert i == hub
    for j in A:
        neigh[j] |= 1 << hub
        neigh[hub] |= 1 << j
    return neigh, hub


def brute(t, A):
    m = len(t)
    neigh, hub = build(t, A)
    n = len(neigh)

    @lru_cache(None)
    def rec(mask):
        if not mask:
            return F(0), {0: F(1)}
        count = mask.bit_count()
        hubprob = F(0)
        dist = {}
        for i in range(n):
            if not (mask >> i & 1):
                continue
            nxt = mask & ~(neigh[i] | (1 << i))
            if i == hub:
                ph = F(1)
            elif i >= m:
                ph = F(0)
            else:
                ph = rec(nxt)[0]
            hubprob += ph / count
            for steps, prob in rec(nxt)[1].items():
                dist[steps + 1] = dist.get(steps + 1, F(0)) + prob / count
        return hubprob, dist

    return rec((1 << n) - 1)


def direct_priority(t, A):
    neigh, hub = build(t, A)
    n = len(neigh)
    hit = 0
    lengths = {}
    for perm in permutations(range(n)):
        mask = (1 << n) - 1
        steps = 0
        selected_hub = False
        for v in perm:
            if mask >> v & 1:
                steps += 1
                selected_hub |= v == hub
                mask &= ~(neigh[v] | (1 << v))
        hit += selected_hub
        lengths[steps] = lengths.get(steps, 0) + 1
    return F(hit, factorial(n)), {
        j: F(v, factorial(n)) for j, v in lengths.items()
    }


def main():
    total = 0
    priority = 0
    examples = []
    for m in range(1, 5):
        for t in product(range(3), repeat=m):
            for bits in range(1 << m):
                A = {j for j in range(m) if bits >> j & 1}
                predicted = formula(t, A)
                exact, dist = brute(t, A)
                assert predicted == exact, (t, A, predicted, exact)
                wanted = {m: F(1) - predicted, m - len(A) + 1: predicted}
                if len(A) == 1:
                    wanted = {m: F(1)}
                assert dist == {x: p for x, p in wanted.items() if p}, (
                    t, A, dist, wanted
                )
                total += 1
                if m + sum(t) + 1 <= 7:
                    p2, d2 = direct_priority(t, A)
                    assert (p2, d2) == (exact, dist), (
                        t, A, p2, d2, exact, dist
                    )
                    priority += 1
                if (m, t, bits) in [
                    (3, (0, 1, 2), 3),
                    (4, (1, 2, 0, 1), 5),
                    (3, (2, 1, 0), 7),
                ]:
                    examples.append((
                        m, t, sorted(A), str(predicted),
                        {x: str(y) for x, y in dist.items()}
                    ))

    extremum_cases = 0
    for m in range(1, 6):
        for d in range(1, m + 1):
            A = set(range(d))
            for L in range(7):
                vals = []
                for t in product(range(L + 1), repeat=m):
                    if sum(t) == L:
                        vals.append(formula(t, A))
                minimum = F(1, d + L + 1)
                maximum = (
                    (F(1, d + 1) + F(L, d + L + 2)) / F(L + 1)
                    if d < m else minimum
                )
                assert min(vals) == minimum, (m, d, L)
                assert max(vals) == maximum, (m, d, L)
                extremum_cases += 1
    print(
        "PASS exact_recursion_cases=", total,
        "priority_permutation_cases=", priority,
        "sharp_extremum_classes=", extremum_cases
    )
    print("EXAMPLES", examples)


if __name__ == "__main__":
    main()
