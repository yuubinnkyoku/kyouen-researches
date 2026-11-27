"""Sanity test of the combinatorial-number-system rank used by census.c.

rank(x) = sum_{i=0..5} C(x_i, i+1)  for x_0 < ... < x_5
is the standard colex rank; it must be a bijection onto [0, C(n,6)).
"""
import random
from itertools import combinations
from math import comb


def rank6(x):
    return sum(comb(x[i], i + 1) for i in range(6))


def main():
    # exhaustive: n=10, all 6-subsets -> exactly range(C(10,6))
    n = 10
    ranks = sorted(rank6(c) for c in combinations(range(n), 6))
    assert ranks == list(range(comb(n, 6))), "rank is not a bijection for n=10"
    print("n=10 exhaustive rank bijection: PASS (%d subsets)" % len(ranks))

    # exhaustive: n=12
    n = 12
    ranks = sorted(rank6(c) for c in combinations(range(n), 6))
    assert ranks == list(range(comb(n, 6))), "rank is not a bijection for n=12"
    print("n=12 exhaustive rank bijection: PASS (%d subsets)" % len(ranks))

    # n=91: max rank must be C(91,6)-1
    top = (85, 86, 87, 88, 89, 90)
    assert rank6(top) == comb(91, 6) - 1
    print("n=91 top subset rank = C(91,6)-1 = %d: PASS" % rank6(top))

    # n=91: random subsets: a rank is never shared by different subsets
    rng = random.Random(1)
    seen = {}
    collisions = 0
    for _ in range(200000):
        c = tuple(sorted(rng.sample(range(91), 6)))
        r = rank6(c)
        assert 0 <= r < comb(91, 6)
        if r in seen:
            assert seen[r] == c, "rank collision between different subsets"
            collisions += 1
        else:
            seen[r] = c
    print("n=91 200000 random 6-subsets: no rank collision between distinct "
          "subsets (%d repeated subsets): PASS" % collisions)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
