"""Two independent integer calculations of A_d=720 E_(d,6)/2**d mod 4096."""
from math import comb, factorial

H = {4: 75, 5: 75, 6: 2877, 7: 44437, 8: 480895, 9: 3220820,
     10: 10, 11: 6}  # last two are residues modulo 16
MOD = 4096


def stirling_surjections(d):
    s = [[0] * (d + 1) for _ in range(d + 1)]
    s[0][0] = 1
    for n in range(1, d + 1):
        for k in range(1, n + 1):
            s[n][k] = s[n - 1][k - 1] + k * s[n - 1][k]
    return sum(H.get(k, 0) * factorial(k) * s[d][k]
               for k in range(d + 1)) % MOD


def inclusion_exclusion(d):
    return sum(H.get(k, 0) * sum((-1) ** (k - j) * comb(k, j) * j ** d
                                 for j in range(k + 1))
               for k in range(d + 1)) % MOD


for d, expected in ((10, 2304), (11, 0)):
    a = stirling_surjections(d)
    b = inclusion_exclusion(d)
    assert a == b == expected, (d, a, b, expected)
    print(f'd={d} A_d mod 4096 = {a} (both methods)')
