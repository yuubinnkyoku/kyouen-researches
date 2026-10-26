#!/usr/bin/env python3
"""Independent exact audit of even q5 period indices. Usage: python verify.py [N]."""
import sys
from math import gcd, isqrt

BASES = (2, 3, 5, 7)
CLASSES = (1, 121, 169, 289, 311, 361, 479, 529, 551, 671, 719, 839)


def character(a, r):
    # Reciprocity formulas for prime r>7; periodic on units modulo 840.
    if a == 2:
        return 1 if r % 8 in (1, 7) else -1
    if a == 3:
        return 1 if r % 12 in (1, 11) else -1
    if a == 5:
        return 1 if r % 5 in (1, 4) else -1
    if a == 7:
        return (1 if r % 7 in (1, 2, 4) else -1) * (1 if r % 4 == 1 else -1)
    raise ValueError(a)


def sieve(n):
    bits = bytearray(b'\x01') * ((n + 1) // 2)
    bits[0] = 0
    for p in range(3, isqrt(n - 1) + 1, 2):
        if bits[p // 2]:
            start = p * p // 2
            count = (len(bits) - 1 - start) // p + 1
            bits[start::p] = b'\x00' * count
    return bits


def prime_factors(n):
    f = 2
    while f * f <= n:
        if n % f == 0:
            yield f
            while n % f == 0:
                n //= f
        f = 3 if f == 2 else f + 2
    if n > 1:
        yield n


def period_index(p):
    L = p - 1
    for q in prime_factors(L):
        while L % q == 0 and all(pow(a, L // q, p) == 1 for a in BASES):
            L //= q
    return (p - 1) // L


def main(n):
    assert n > 37
    classes = set(CLASSES)
    assert len(classes) == 12
    assert tuple(r for r in range(1, 840) if gcd(r, 840) == 1
                 and all(character(a, r) == 1 for a in BASES)) == CLASSES

    total = even = 0
    counts = {r: 0 for r in CLASSES}
    bits = sieve(n)
    for i in range(18, len(bits)):  # odd 37 is the first candidate
        p = 2 * i + 1
        if p >= n:
            break
        if not bits[i]:
            continue
        total += 1
        r = p % 840
        by_classes = r in classes
        if by_classes:
            even += 1
            counts[r] += 1
        if p < 1_000_000:
            by_euler = all(pow(a, (p - 1) // 2, p) == 1 for a in BASES)
            by_orders = period_index(p) % 2 == 0
            assert by_classes == by_euler == by_orders, p

    print("prime_bound_exclusive", n)
    print("primes_p_gt_32", total)
    print("even_index_primes", even)
    print("classes_mod_840", *CLASSES)
    print("class_counts", *[f"{r}:{counts[r]}" for r in CLASSES])
    if n == 1_000_000:
        assert (total, even) == (78_487, 4_831)
    if n == 100_000_000:
        assert (total, even) == (5_761_444, 359_464)
        print("existing_100m_histogram_even_index MATCH")
    print("PASS")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000)
