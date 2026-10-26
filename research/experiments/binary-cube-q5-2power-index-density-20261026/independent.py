#!/usr/bin/env python3
"""Independent common-order reduction for the four bases, p < 10^6."""
import math
import sys

limit = int(sys.argv[1]) if len(sys.argv) > 1 else 1000000
if not 37 <= limit <= 1000000:
    raise SystemExit("use 37 <= limit <= 1000000")
spf = list(range(limit))
for q in range(2, math.isqrt(limit - 1) + 1):
    if spf[q] == q:
        for x in range(q * q, limit, q):
            if spf[x] == x:
                spf[x] = q

counts = [0] * 9
first = [0] * 9
total = 0
for p in range(37, limit, 2):
    if spf[p] != p:
        continue
    total += 1
    x = p - 1
    factors = []
    while x > 1:
        q = spf[x]
        factors.append(q)
        while x % q == 0:
            x //= q
    L = p - 1
    for q in factors:
        while L % q == 0 and all(pow(a, L // q, p) == 1 for a in (2, 3, 5, 7)):
            L //= q
    I = (p - 1) // L
    for r in range(1, 9):
        if I % (1 << r) == 0:
            counts[r] += 1
            if not first[r]:
                first[r] = p
print("limit", limit, "primes", total)
for r in range(1, 9):
    print(r, counts[r], "first", first[r])
if limit == 1000000:
    assert total == 78487
    assert counts[1:5] == [4831, 112, 6, 0]
    assert first[1:5] == [311, 14449, 71761, 0]
