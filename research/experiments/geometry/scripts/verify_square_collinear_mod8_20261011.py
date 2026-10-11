#!/usr/bin/env python3
"""Independent integer-line enumeration for square-board collinear-q mod-8 theorem.

Usage: python research/experiments/geometry/scripts/verify_square_collinear_mod8_20261011.py
Requires only Python standard library; does not reuse a geometry library.
"""
from collections import defaultdict
from math import comb, gcd


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def is_three_mod_four_prime_power(n):
    for p in range(3, n + 1, 4):
        if n % p or any(p % d == 0 for d in range(2, 1 + int(p**0.5))):
            continue
        t = n
        while t % p == 0:
            t //= p
        if t == 1:
            return True
    return False


def theorem(n, q):
    base = 2 * (n + 1) * choose(n, q) + 4 * choose(n, q + 1)
    if n % 2:
        return (base + 4 * choose(2 * ((n - 1) // 4) + 1, q)) % 8
    correction = sum(
        choose(2 * ((n - 1 + b) // (2 * b)), q)
        for b in range(3, n, 2) if is_three_mod_four_prime_power(b)
    )
    return (base + 4 * correction) % 8


def canonical_line(p, v):
    x, y = p
    u, z = v
    a, b = z - y, x - u
    d = gcd(abs(a), abs(b))
    a, b = a // d, b // d
    c = a * x + b * y
    if a < 0 or (a == 0 and b < 0):
        a, b, c = -a, -b, -c
    return a, b, c


def orbit_of_line(n, pts, indices):
    p, v = (pts[i] for i in list(indices)[:2])
    out = set()
    for mirror in (False, True):
        for rotation in range(4):
            def transform(x, y):
                if mirror:
                    x = n - 1 - x
                for _ in range(rotation):
                    x, y = n - 1 - y, x
                return x, y
            out.add(canonical_line(transform(*p), transform(*v)))
    return out


def audit(n):
    pts = [(x, y) for x in range(n) for y in range(n)]
    lines = defaultdict(set)
    for i, p in enumerate(pts):
        for j in range(i + 1, len(pts)):
            lines[canonical_line(p, pts[j])].update((i, j))
    counts = {line: len(indices) for line, indices in lines.items()}
    unseen = set(lines)
    orbit_count = defaultdict(int)
    while unseen:
        line = next(iter(unseen))
        orbit = orbit_of_line(n, pts, lines[line])
        assert orbit <= unseen, ('missing transformed line', n, line)
        assert all(counts[k] == counts[line] for k in orbit)
        a, b, c = line
        special = a == 0 or b == 0 or abs(a) == abs(b)
        if not special:
            through_center = 2 * c == (n - 1) * (a + b)
            assert len(orbit) == (4 if through_center else 8), (n, line, orbit)
        orbit_count[len(orbit)] += 1
        unseen -= orbit
    for q in range(2, min(12, n * n) + 1):
        direct = sum(choose(k, q) for k in counts.values())
        expected = theorem(n, q)
        assert direct % 8 == expected, (n, q, direct, expected)
    return counts, orbit_count


def main():
    pairs = 0
    for n in range(2, 19):
        counts, orbits = audit(n)
        pairs += min(12, n * n) - 1
        if n in (6, 9, 10, 11, 16, 18):
            h4 = sum(choose(k, 4) for k in counts.values())
            print(f'n={n}: lines={len(counts)}, D4-orbits={dict(sorted(orbits.items()))}, H4={h4}, H4 mod 8={h4%8}')
    print(f'PASS: {pairs} (n,q) exact enumerations, n=2..18, q=2..min(12,n^2); D4 orbit checks passed')


if __name__ == '__main__':
    main()
