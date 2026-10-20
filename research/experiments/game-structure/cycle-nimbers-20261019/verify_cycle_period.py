#!/usr/bin/env python3
"""Certificate checker for exact eventual period of Node Kayles on cycles.

All recurrences are exact; no external dependencies.  The finite certificate
P[n] == P[n+34] for n=52..139 is sufficient by the lemma in README.md.
"""
from functools import lru_cache

PERIOD = 34
START_PATH = 52
START_CYCLE = 38
EXPECTED_WIN_RESIDUES = {7, 11, 23, 27, 31}


def mex(values):
    v = set(values)
    k = 0
    while k in v:
        k += 1
    return k


def path_grundy(limit):
    a = [0]
    for n in range(1, limit + 1):
        # A move at i deletes i and its neighbors.
        children = (
            a[max(0, i - 1)] ^ a[max(0, n - i - 2)]
            for i in range(n)
        )
        a.append(mex(children))
    return a


def direct_cycle_grundy(n):
    """Independent subset-state recursion, for n <= 17."""
    nbr = [(1 << i) | (1 << ((i - 1) % n)) | (1 << ((i + 1) % n))
           for i in range(n)]
    full = (1 << n) - 1

    @lru_cache(None)
    def solve(remaining):
        children = []
        for i in range(n):
            if (remaining >> i) & 1:
                children.append(solve(remaining & ~nbr[i]))
        return mex(children)

    return solve(full)


def check():
    # 174 is the first index covered by the induction step.
    p = path_grundy(600)
    assert all(p[n] == p[n + PERIOD] for n in range(52, 140))
    assert all(p[n] == p[n + PERIOD] for n in range(52, 567))
    assert p[51] != p[85], "52 must be the least starting index for period 34"

    # Every move on C_n leaves P_(n-3); mex of a singleton is 1 or 0.
    c = {n: int(p[n - 3] == 0) for n in range(3, 568)}
    for n in range(3, 18):
        assert c[n] == direct_cycle_grundy(n), (n, c[n])

    assert all(c[n] == c[n + PERIOD] for n in range(38, 534))
    assert c[37] != c[71], "38 is the least start for period 34"
    assert {n % PERIOD for n in range(38, 72) if c[n]} == EXPECTED_WIN_RESIDUES
    for d in (1, 2, 17):
        assert any(c[n] != c[n + d] for n in range(38, 38 + PERIOD)), d
    print("PASS: 88 finite path equalities, induction threshold n=174")
    print("PASS: C_n mex(P_(n-3)) and independent state DP for 3<=n<=17")
    print("PASS: cycle preperiod 38, least eventual period 34")
    print("PASS: C_n=1 for n>=38 iff n mod 34 in {7,11,23,27,31}")
    print("PASS: preperiod winning n=", [n for n in range(3, 38) if c[n]])


if __name__ == "__main__":
    check()
