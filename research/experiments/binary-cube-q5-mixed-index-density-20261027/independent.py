#!/usr/bin/env python3
"""Independent audit: factor p-1, calculate four orders, then their lcm."""
import argparse
from collections import defaultdict
from math import isqrt, lcm

BASES = (2, 3, 5, 7)
ODD = (3, 5, 7, 9, 15, 21, 35, 105)


def primes_below(n):
    sieve = bytearray(b"\x01") * n
    sieve[:2] = b"\x00\x00"
    for p in range(2, isqrt(n - 1) + 1):
        if sieve[p]:
            sieve[p * p::p] = b"\x00" * ((n - 1 - p * p) // p + 1)
    return [p for p in range(2, n) if sieve[p]]


def common_index(p, trial_primes):
    rem, factors = p - 1, []
    for q in trial_primes:
        if q * q > rem:
            break
        if rem % q == 0:
            factors.append(q)
            while rem % q == 0:
                rem //= q
    if rem > 1:
        factors.append(rem)
    orders = []
    for a in BASES:
        order = p - 1
        for q in factors:
            while order % q == 0 and pow(a, order // q, p) == 1:
                order //= q
        orders.append(order)
    return (p - 1) // lcm(*orders)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("limit", type=int, nargs="?", default=1000000)
    args = parser.parse_args()
    if not 37 <= args.limit <= 1000000:
        parser.error("use 37 <= limit <= 1000000")
    primes = primes_below(args.limit)
    trial = [p for p in primes if p * p < args.limit]
    count, first = defaultdict(int), {}
    for p in primes:
        if p <= 32:
            continue
        index = common_index(p, trial)
        for r in range(1, 5):
            for n in ODD:
                if index % ((1 << r) * n) == 0:
                    count[r, n] += 1
                    first.setdefault((r, n), p)
    print(f"p<{args.limit} primes={sum(p > 32 for p in primes)}")
    for r in range(1, 5):
        for n in ODD:
            print(f"r={r} n={n} count={count[r, n]} first={first.get((r, n), 0)}")


if __name__ == "__main__":
    main()
