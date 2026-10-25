#!/usr/bin/env python3
"""Exact arithmetic checks of K0567, independent of the rooted rank verifier."""

C3 = {8: 1, 6: -3, 4: 3, 2: -1}
C5 = {32: 1, 24: -30, 20: 140, 18: 135, 16: -1215,
      14: 2205, 12: -1977, 10: 780, 8: 250,
      6: -495, 4: 255, 2: -49}


def exact(coefficients, denominator, d):
    numerator = sum(coefficient * base**d
                    for base, coefficient in coefficients.items())
    assert numerator % denominator == 0
    return numerator // denominator


def v2(x):
    assert x > 0
    return (x & -x).bit_length() - 1


def main():
    for d in range(3, 65):
        value = exact(C3, 6, d)
        assert v2(value) == d + (d % 2 == 0)
    for d in range(5, 65):
        value = exact(C5, 120, d)
        assert value % (1 << d) == 0
        assert (value // (1 << d)) % 2 == (d % 4 in (1, 2))
    assert exact(C3, 6, 3) == 8
    assert exact(C3, 6, 4) == 160
    assert exact(C5, 120, 5) == 2592
    assert exact(C5, 120, 6) == 256704
    # Existing exact finite counts, illustrating the even-q orbit bound.
    for d, q, count in [(4, 6, 40), (5, 6, 1200), (4, 8, 20)]:
        assert count % (1 << max(0, d - v2(q))) == 0
    print("K0567: all exact arithmetic checks passed (d<=64)")


if __name__ == "__main__":
    main()
