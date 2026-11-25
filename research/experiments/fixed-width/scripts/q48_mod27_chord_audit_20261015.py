#!/usr/bin/env python3
"""Two independent residue audits for four-row eight-point circles.

Proof does not rely on the finite census. The modulo-27 enumerations here
independently check the four residue patterns from (C,N) and (d0,d1).
"""
from math import isqrt

MOD = 27
SQUARES = {x * x % MOD for x in range(MOD)}
EXPECTED = {
    (1, 9, 9, 1),
    (10, 9, 0, 10),
    (10, 0, 9, 10),
    (19, 0, 0, 19),
}
EXPECTED_CN = {(24, 10), (6, 19), (15, 19), (24, 1)}


def center_audit():
    admissible = {}
    for c in range(MOD):
        for n in range(MOD):
            pattern = tuple((n - (c + 2 * i) ** 2) % MOD for i in range(4))
            if all(v in SQUARES for v in pattern):
                admissible[(c, n)] = pattern
    assert set(admissible) == EXPECTED_CN, admissible
    assert set(admissible.values()) == EXPECTED
    return admissible


def chord_audit():
    patterns = set()
    for a in range(MOD):
        for b in range(MOD):
            aa, bb = a * a % MOD, b * b % MOD
            cc = (2 * bb - aa - 8) % MOD
            dd = (3 * bb - 2 * aa - 24) % MOD
            if cc in SQUARES and dd in SQUARES:
                patterns.add((aa, bb, cc, dd))
    assert patterns == EXPECTED, patterns
    return patterns


def finite_direct(max_chord):
    """No sieve: small-bound independent complete enumeration."""
    result = set()
    bound = max_chord * max_chord
    for a in range(1, max_chord + 1):
        for b in range(1, max_chord + 1):
            c2 = 2 * b * b - a * a - 8
            d2 = 3 * b * b - 2 * a * a - 24
            if not (0 < c2 <= bound and 0 < d2 <= bound):
                continue
            c, d = isqrt(c2), isqrt(d2)
            if c * c == c2 and d * d == d2 and (a - b) % 2 == 0:
                assert (a - c) % 2 == 0 and (a - d) % 2 == 0
                pattern = tuple(x * x % MOD for x in (a, b, c, d))
                assert pattern in EXPECTED
                result.add((a, b, c, d))
    return sorted(result)


def pell_mod27_audit():
    # The Pell transition matrix has order 9 modulo 27.
    u, v = 1, 0
    triples = []
    for n in range(1, 10):
        u, v = (19 * u + 60 * v) % MOD, (6 * u + 19 * v) % MOD
        chords = (9 * v - u, 3 * u - v, 3 * u + v, u + 9 * v)
        triples.append(tuple(x * x % MOD for x in chords))
    assert (u, v) == (1, 0)
    assert triples == [
        (10, 9, 0, 10), (10, 0, 9, 10), (1, 9, 9, 1)
    ] * 3
    return triples


def main():
    cn = center_audit()
    patterns = chord_audit()
    pell = pell_mod27_audit()
    print('center residues:', sorted(cn.items()))
    print('independent chord residues:', sorted(patterns))
    print('Pell residues over its 9-step period:', pell)
    for bound in (73, 150, 300):
        circles = finite_direct(bound)
        print('max chord', bound, 'patterns', len(circles), circles)
    print('PASS: independent mod27 residue enumerations and direct finite census')


if __name__ == '__main__':
    main()
