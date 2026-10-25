#!/usr/bin/env python3
"""Exact q=5 2-adic root lifts and finite-range valuation maxima.

No large-d integer powers are formed: modular exponentiation is used.
The all-t uniqueness theorem is K0567 theorem 7; this script computes and
independently checks the finite residue representatives.
"""
from math import comb

# P(d)=120 E_{d,5}/2**d for d>=5, from K0561.
COEFF = {
    16: 1, 12: -30, 10: 140, 9: 135, 8: -1215, 7: 2205,
    6: -1977, 5: 780, 4: 250, 3: -495, 2: 255, 1: -49,
}
# Independently evaluated rooted-support representation.
SUPPORT = {
    5: 81, 6: 466, 7: 1825, 8: 4320, 9: 6375, 10: 6168,
    11: 4008, 12: 1790, 13: 560, 14: 120, 15: 16, 16: 1,
}


def b_direct(d, t):
    """B_d modulo 2**t from the closed exponential formula."""
    assert d >= 5 and t >= 1
    modulus = 1 << (t + 3)
    p = sum(c * pow(base, d, modulus) for base, c in COEFF.items()) % modulus
    assert p % 8 == 0
    return (p // 8 * pow(15, -1, 1 << t)) % (1 << t)


def b_rooted(d, t):
    """Stirling/inclusion-exclusion evaluation from rooted h_k."""
    assert d >= 5 and t >= 1
    modulus = 1 << (t + 3)
    p = 0
    for k, h in SUPPORT.items():
        surjections = sum((-1) ** (k - j) * comb(k, j) * pow(j, d, modulus)
                          for j in range(k + 1))
        p = (p + h * surjections) % modulus
    assert p % 8 == 0
    return (p // 8 * pow(15, -1, 1 << t)) % (1 << t)


def representative(residue, modulus, minimum):
    return residue + max(0, (minimum - residue + modulus - 1) // modulus) * modulus


def roots_through(limit=60):
    assert b_direct(8, 1) == 0 and b_direct(7, 1) == 0
    roots = {1: (0, 3)}
    for t in range(1, limit):
        period = 1 << (t + 2)  # period of B mod 2**(t+1)
        new = []
        for residue in roots[t]:
            candidates = (residue, residue + (period >> 1))
            survivors = []
            for cand in candidates:
                d = representative(cand, period, max(5, t + 5))
                direct = b_direct(d, t + 1)
                rooted = b_rooted(d, t + 1)
                assert direct == rooted, (t, d, direct, rooted)
                if direct == 0:
                    survivors.append(cand)
            assert len(survivors) == 1, (t, residue, survivors)
            new.extend(survivors)
        roots[t + 1] = tuple(sorted(new))
    return roots


def check_interval(bound, t, roots):
    """Certify maximum excess valuation t on 5<=d<=bound.

    K0567 theorem 7 classifies B_d mod 2**t for d>=t+4.
    Smaller dimensions are checked by exact modular arithmetic.
    """
    assert bound >= t + 5
    low = t + 4
    for d in range(5, low + 1):
        assert b_direct(d, t + 1) != 0
        assert b_rooted(d, t + 1) != 0
        if d < low:
            assert b_direct(d, t) != 0
            assert b_rooted(d, t) != 0
    period = 1 << (t + 1)
    maximizers = []
    for r in roots[t]:
        first = representative(r, period, low)
        maximizers.extend(range(first, bound + 1, period))
    maximizers.sort()
    assert maximizers
    next_period = period * 2
    for r in roots[t + 1]:
        assert representative(r, next_period, low + 1) > bound
    for d in maximizers:
        assert b_direct(d, t) == 0
        assert b_rooted(d, t) == 0
        assert b_direct(d, t + 1) != 0
        assert b_rooted(d, t + 1) != 0
    return maximizers


def main():
    # Full-integer comparison for small dimensions.
    for d in range(5, 65):
        numerator = sum(c * base ** d for base, c in COEFF.items())
        assert numerator % 120 == 0
        for t in (1, 4, 8, 16, 32, 60):
            expected = (numerator // 120) % (1 << t)
            assert b_direct(d, t) == expected
            assert b_rooted(d, t) == expected

    # Check rooted-support coefficients from the binomial basis identity.
    for k in range(17):
        h = sum(c * comb(j, k) for j, c in COEFF.items() if j >= k)
        assert h == SUPPORT.get(k, 0), (k, h)

    roots = roots_through(60)
    expected = {
        1: (0, 3), 9: (492, 659), 10: (492, 1683),
        18: (14828, 398995), 19: (398995, 539116),
        40: (569366821356, 1763551090323),
        41: (1763551090323, 2768390076908),
        59: (16256943456130707, 642416626174015980),
        60: (1169178448062977683, 1795338130780862956),
    }
    for t, expected_roots in expected.items():
        assert roots[t] == expected_roots, (t, roots[t])
    bounds = {100_000: 18, 10**12: 40, 10**18: 59}
    for bound, t in bounds.items():
        maximizers = check_interval(bound, t, roots)
        print(f"5<=d<={bound}: max(v2(E_d5)-d)={t}, at d={maximizers}")
    print("all independent q5 2-adic lifts and interval certificates passed")


if __name__ == "__main__":
    main()
