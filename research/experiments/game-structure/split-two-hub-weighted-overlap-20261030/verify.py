"""Exact independent audits for two clique hubs plus degree-one centers."""
from fractions import Fraction
from functools import lru_cache
from itertools import permutations
from math import factorial


def assignments(m, k):
    if m == 1:
        yield (k,)
    else:
        for t in range(k + 1):
            for tail in assignments(m - 1, k - t):
                yield (t,) + tail


def formula(t, A, B):
    m = len(t)
    assert 0 < A < (1 << m) and 0 < B < (1 << m)
    a = sum(t[j] + 1 for j in range(m) if (A >> j) & 1)
    b = sum(t[j] + 1 for j in range(m) if (B >> j) & 1)
    c = sum(t[j] + 1 for j in range(m) if ((A & B) >> j) & 1)
    u = a + b - c
    q = 1
    for v in t:
        q *= v + 1
    return Fraction(a*b*(u+2)+c, q*(a+1)*(b+1)*(u+2))


def neighborhoods(t, A, B):
    m = len(t)
    n = m + 2 + sum(t)
    closed = [1 << v for v in range(n)]
    for v in range(m, n):
        for w in range(v + 1, n):
            closed[v] |= 1 << w
            closed[w] |= 1 << v
    for j in range(m):
        for hub, mask in ((m, A), (m + 1, B)):
            if mask & (1 << j):
                closed[j] |= 1 << hub
                closed[hub] |= 1 << j
    v = m + 2
    for j, count in enumerate(t):
        for _ in range(count):
            closed[j] |= 1 << v
            closed[v] |= 1 << j
            v += 1
    assert v == n
    return closed


def direct(m, closed):
    @lru_cache(None)
    def rec(mask):
        if not mask:
            return Fraction(1)
        return sum((rec(mask & ~closed[v]) for v in range(m) if mask & (1 << v)), Fraction(0)) / mask.bit_count()
    return rec((1 << len(closed)) - 1)


def priority(m, closed):
    n = len(closed)
    good = 0
    for order in permutations(range(n)):
        remaining = (1 << n) - 1
        for v in order:
            if remaining & (1 << v):
                if v >= m:
                    break
                remaining &= ~closed[v]
        else:
            good += 1
    return Fraction(good, factorial(n))


def main():
    cases = priorities = bound_classes = 0
    for m in range(1, 5):
        for k in range(5):
            for t in assignments(m, k):
                for A in range(1, 1 << m):
                    for B in range(1, 1 << m):
                        closed = neighborhoods(t, A, B)
                        f = formula(t, A, B)
                        assert f == direct(m, closed), (m, t, A, B, f)
                        cases += 1
                        if len(closed) <= 7 and (A & B in (0, A, B)):
                            assert f == priority(m, closed), (m, t, A, B)
                            priorities += 1
    for m in range(2, 7):
        for r in range(3):
            t = (r,) * m
            for da in range(1, m + 1):
                for db in range(1, m + 1):
                    values = {}
                    for A in range(1, 1 << m):
                        if A.bit_count() != da:
                            continue
                        for B in range(1, 1 << m):
                            if B.bit_count() != db:
                                continue
                            overlap = (A & B).bit_count()
                            p = formula(t, A, B)
                            if overlap in values:
                                assert values[overlap] == p
                            else:
                                values[overlap] = p
                    lo = max(0, da + db - m)
                    hi = min(da, db)
                    assert set(values) == set(range(lo, hi + 1))
                    assert all(values[z] < values[z+1] for z in range(lo, hi))
                    bound_classes += 1
    print(f'PASS {cases} exact recursive configurations, {priorities} independent full-order audits, '
          f'{bound_classes} uniform-weight sharp overlap classes; 0 mismatches')


if __name__ == '__main__':
    main()
