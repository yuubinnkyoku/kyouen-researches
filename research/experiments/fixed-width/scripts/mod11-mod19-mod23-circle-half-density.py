#!/usr/bin/env python3
"""Exact CRT audit for the lattice-circle double-row half-density bound.

For a lattice circle meeting row i in two lattice points, K0072's Vieta
reduction gives integers d_i,C,N with
    d_i^2 + (2*i+C)^2 = N.
Modulo an odd prime p, a necessary condition is therefore that
N-(2*i+C)^2 is a quadratic residue (zero included).

A translation of i absorbs C, so for a set of primes we may enumerate N
modulo their product and every cyclic start.  This script verifies the
new L=19,20 boundary for p=11,19,23 and also prints L=18 to show where
this particular congruence certificate stops.
"""

from itertools import product
from math import prod

PRIMES = (11, 19, 23)
PERIOD = prod(PRIMES)


def residue_table(p):
    qr = {x*x % p for x in range(p)}
    return [[((n - (2*i)*(2*i)) % p) in qr for i in range(p)]
            for n in range(p)]


TABLES = {p: residue_table(p) for p in PRIMES}


def allowed(n, i):
    return all(TABLES[p][n % p][i % p] for p in PRIMES)


def audit_length(length):
    best = -1
    witness = None
    for n in range(PERIOD):
        seq = [1 if allowed(n, i) else 0 for i in range(PERIOD)]
        cur = sum(seq[:length])
        local_best = cur
        local_start = 0
        for s in range(1, PERIOD):
            cur += seq[(s + length - 1) % PERIOD] - seq[s - 1]
            if cur > local_best:
                local_best = cur
                local_start = s
        if local_best > best:
            best = local_best
            witness = (n, local_start)
    return best, witness


def main():
    print("primes", PRIMES, "period", PERIOD)
    for length in (18, 19, 20):
        best, witness = audit_length(length)
        print(length, best, witness)
    assert audit_length(19)[0] == 10
    assert audit_length(20)[0] == 10
    assert audit_length(18)[0] == 10


if __name__ == "__main__":
    main()
