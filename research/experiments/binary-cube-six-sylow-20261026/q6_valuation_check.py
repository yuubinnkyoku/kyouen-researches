"""Exact modular audit of q=6 rooted coefficients and all-d valuation theorem."""
from math import comb, factorial

# k<=9: exact values; k=10..15: independently verified residues modulo 16.
H = {4: 75, 5: 75, 6: 2877, 7: 44437, 8: 480895, 9: 3220820,
     10: 10, 11: 6, 12: 0, 13: 9, 14: 4, 15: 3}
MOD = 4096
INV45 = pow(45, -1, 512)


def stirling_surjections(d):
    s = [[0] * (d + 1) for _ in range(d + 1)]
    s[0][0] = 1
    for n in range(1, d + 1):
        for k in range(1, n + 1):
            s[n][k] = s[n - 1][k - 1] + k * s[n - 1][k]
    return sum(H.get(k, 0) * factorial(k) * s[d][k]
               for k in range(d + 1)) % MOD


def inclusion_exclusion(d):
    return sum(H.get(k, 0) * sum((-1) ** (k - j) * comb(k, j) * pow(j, d, MOD)
                                 for j in range(k + 1))
               for k in range(min(d, 15) + 1)) % MOD


def normalized_residues(max_d):
    # Iterative Stirling recurrence modulo 4096, with no large integers.
    s = [0] * 16
    s[0] = 1
    factorials = [factorial(k) % MOD for k in range(16)]
    residues = {}
    for d in range(max_d + 1):
        if d:
            for k in range(15, 0, -1):
                s[k] = (s[k - 1] + k * s[k]) % MOD
            s[0] = 0
        a = sum(H.get(k, 0) * factorials[k] * s[k]
                for k in range(16)) % MOD
        if d >= 6:
            assert a % 8 == 0
            residues[d] = (a // 8 * INV45) % 512
    return residues


for d, expected in ((10, 2304), (11, 0)):
    a, b = stirling_surjections(d), inclusion_exclusion(d)
    assert a == b == expected, (d, a, b)

# Independent inclusion-exclusion checks at boundary and large dimensions.
residues = normalized_residues(12 + 2 * 1024)
for d in (6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 524, 970, 1035, 1036, 2060):
    a = inclusion_exclusion(d)
    assert a % 8 == 0
    assert residues[d] == (a // 8 * INV45) % 512

# The period follows mathematically from the odd bases modulo 4096;
# these checks audit its 1024 residue classes and prove minimality.
for d in range(12, 12 + 1024):
    assert residues[d] == residues[d + 1024]
assert (residues[12], residues[524]) == (409, 153)

# Complete residue-class audit: all d>=6 reduce to these 1030 cases.
zeros = []
for d in range(6, 12 + 1024):
    value = residues[d]
    if d % 4 in (0, 1):
        assert value & 1
        continue
    root = 970 if d % 4 == 2 else 11
    delta = (d - root) % 1024
    if delta == 0:
        assert value == 0
        zeros.append(d)
    else:
        expected_v2 = (delta & -delta).bit_length() - 2
        assert value and (value & -value).bit_length() - 1 == expected_v2
assert zeros == [11, 970, 1035], zeros
print('h[10..15] mod16 =', [H[k] for k in range(10, 16)])
print('A_10 mod4096 = 2304; A_11 mod4096 = 0')
print('B_12 mod512 = 409; B_524 mod512 = 153; least period = 1024')
print('All 1024 classes checked; exceptional d mod1024 = {11, 970}')
