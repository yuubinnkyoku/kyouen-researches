"""Exact Stirling aggregation for rooted six-section support census."""
from math import comb, factorial

H = [0, 0, 0, 0, 75, 75, 2877, 44437, 480895]
EXPECTED = {4: 40, 5: 1200, 6: 206528, 7: 47884928, 8: 9324142464}


def stirling(n: int, k: int) -> int:
    dp = [0] * (k + 1)
    dp[0] = 1
    for _ in range(n):
        nxt = [0] * (k + 1)
        for j in range(1, k + 1):
            nxt[j] = dp[j - 1] + j * dp[j]
        dp = nxt
    return dp[k]


def e(d: int) -> int:
    ordered_rooted = sum(
        H[k] * factorial(k) * stirling(d, k)
        for k in range(min(d, len(H) - 1) + 1)
    )
    assert (ordered_rooted * 2**d) % factorial(6) == 0
    return ordered_rooted * 2**d // factorial(6)


def verify_known_transforms() -> None:
    # Coefficients of q! E(d,q) / 2^d = sum_i a_i i^d,
    # read from the independent q=4,5 all-dimensional formulas.
    for q, a, expected_h in [
        (4, {8: 1, 6: -12, 5: 30, 4: -35, 3: 27, 2: -16, 1: 5},
         [0, 0, 3, 3, 5, 14, 16, 8, 1]),
        (5, {16: 1, 12: -30, 10: 140, 9: 135, 8: -1215,
             7: 2205, 6: -1977, 5: 780, 4: 250, 3: -495, 2: 255, 1: -49},
         [0, 0, 0, 0, 0, 81, 466, 1825, 4320, 6375, 6168,
          4008, 1790, 560, 120, 16, 1]),
    ]:
        h = [sum(comb(i, j) * v for i, v in a.items() if i >= j)
             for j in range(2 ** (q - 1) + 1)]
        assert h == expected_h
        assert all(v >= 0 for v in h)
        if q == 5:
            for ell in range(17, 33):
                g = sum(h[j] * comb(j, ell-j) * 2 ** (2*j-ell)
                        for j in range(len(h)) if 0 <= ell-j <= j)
                high = (comb(32, ell)
                        - (30 * comb(24, ell) if ell <= 24 else 0)
                        + (140 * comb(20, ell) if ell <= 20 else 0)
                        + (135 * comb(18, ell) if ell <= 18 else 0))
                assert g == high


if __name__ == "__main__":
    verify_known_transforms()
    for d, expected in EXPECTED.items():
        actual = e(d)
        assert actual == expected, (d, actual, expected)
        rooted = 6 * actual // 2**d
        assert rooted * 2**d == 6 * actual
        v2 = (actual & -actual).bit_length() - 1
        print(f"d={d} rooted={rooted} E={actual} v2={v2}")
