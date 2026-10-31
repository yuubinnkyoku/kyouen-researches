"""Independent exact Node Kayles audit for one arbitrary-degree clique center."""
from fractions import Fraction
from functools import lru_cache
from itertools import permutations
from math import factorial


def assignments(m, k):
    if m == 1:
        yield (k,)
    else:
        for a in range(k + 1):
            for tail in assignments(m - 1, k - a):
                yield (a,) + tail


def formula(d, t):
    s = d + sum(t[:d])
    den = 1
    for x in t:
        den *= x + 1
    return Fraction(s, (s + 1) * den)


def bounds(m, d, k):
    a, r = divmod(k, m)
    s = d + d * a + max(0, r - (m - d))
    return (Fraction(s, (s + 1) * (a + 1)**(m-r) * (a + 2)**r),
            Fraction(d + k, (d + k + 1) * (k + 1)))


def closed_neighborhoods(m, d, t):
    n = m + sum(t) + 1
    c = [1 << v for v in range(n)]
    for u in range(m, n):
        for v in range(u + 1, n):
            c[u] |= 1 << v
            c[v] |= 1 << u
    for j in range(d):
        c[j] |= 1 << m
        c[m] |= 1 << j
    v = m + 1
    for j, count in enumerate(t):
        for _ in range(count):
            c[j] |= 1 << v
            c[v] |= 1 << j
            v += 1
    return c


def direct(m, c):
    @lru_cache(None)
    def f(mask):
        if not mask:
            return Fraction(1)
        return sum((f(mask & ~c[v]) for v in range(m) if mask & (1 << v)), Fraction(0)) / mask.bit_count()
    return f((1 << len(c)) - 1)


def priority(m, c):
    n = len(c)
    good = 0
    for order in permutations(range(n)):
        mask = (1 << n) - 1
        for v in order:
            if mask & (1 << v):
                if v >= m:
                    break
                mask &= ~c[v]
        else:
            good += 1
    return Fraction(good, factorial(n))


def main():
    cases = classes = priority_cases = 0
    for m in range(1, 6):
        for d in range(1, m + 1):
            for k in range(7):
                lo, hi = bounds(m, d, k)
                seen_lo = seen_hi = False
                for t in assignments(m, k):
                    p = formula(d, t)
                    c = closed_neighborhoods(m, d, t)
                    assert p == direct(m, c)
                    assert lo <= p <= hi
                    seen_lo |= p == lo
                    seen_hi |= p == hi
                    cases += 1
                    if len(c) <= 7 and sum(t[:d]) in (0, k):
                        assert p == priority(m, c)
                        priority_cases += 1
                assert seen_lo and seen_hi
                classes += 1
    print(f"PASS {cases} configurations, {classes} sharp-bound classes, "
          f"{priority_cases} independent permutation checks, 0 mismatches")


if __name__ == '__main__':
    main()
