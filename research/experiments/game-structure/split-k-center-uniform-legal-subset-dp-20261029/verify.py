#!/usr/bin/env python3
"""Independent exact checks for the split-graph k-center uniform-legal formula."""
from fractions import Fraction
from functools import lru_cache
from itertools import permutations, product
from math import factorial


def formula(neighborhoods, m):
    """Subset-DP exact formula; uses only neighborhood union cardinalities.

    H(S)=Pr(each center in S precedes all its independent neighbors).
    J_c(S)=Pr(E_c, E_i for i in S, and all i in S precede c).
    """
    k = len(neighborhoods)
    all_subsets = 1 << k
    unions = [0] * all_subsets
    for mask in range(1, all_subsets):
        bit = mask & -mask
        c = bit.bit_length() - 1
        unions[mask] = unions[mask ^ bit] | neighborhoods[c]

    h = [Fraction(0)] * all_subsets
    h[0] = Fraction(1)
    for mask in range(1, all_subsets):
        total = sum((h[mask ^ (1 << i)] for i in range(k) if mask >> i & 1), Fraction(0))
        h[mask] = total / (mask.bit_count() + unions[mask].bit_count())
    p_none = sum(((-1 if mask.bit_count() & 1 else 1) * h[mask]
                  for mask in range(all_subsets)), Fraction(0))

    p_center = []
    for c in range(k):
        j = [Fraction(0)] * all_subsets
        j[0] = Fraction(1, 1 + neighborhoods[c].bit_count())
        for mask in range(1, all_subsets):
            if mask >> c & 1:
                continue
            total = sum((j[mask ^ (1 << i)] for i in range(k) if mask >> i & 1), Fraction(0))
            j[mask] = total / (mask.bit_count() + 1 + unions[mask | (1 << c)].bit_count())
        p = sum(((-1 if mask.bit_count() & 1 else 1) * j[mask]
                 for mask in range(all_subsets) if not (mask >> c & 1)), Fraction(0))
        p_center.append(p)
    assert sum(p_center) + p_none == 1
    return tuple(p_center), p_none


def direct_recurrence(neighborhoods, m):
    """Independent labeled-vertex closed-neighborhood deletion recursion."""
    k = len(neighborhoods)
    i_to_c = [sum(1 << c for c, n in enumerate(neighborhoods) if n >> i & 1)
              for i in range(m)]

    @lru_cache(None)
    def solve(centers, indep):
        if centers == 0:
            return (Fraction(0),) * k + (Fraction(1),)
        n = centers.bit_count() + indep.bit_count()
        ans = [Fraction(0)] * (k + 1)
        for c in range(k):
            if centers >> c & 1:
                ans[c] += Fraction(1, n)
        for i in range(m):
            if indep >> i & 1:
                child = solve(centers & ~i_to_c[i], indep ^ (1 << i))
                for j, val in enumerate(child):
                    ans[j] += val / n
        return tuple(ans)

    out = solve((1 << k) - 1, (1 << m) - 1)
    return out[:-1], out[-1]


def direct_permutations(neighborhoods, m):
    """Independent greedy processing of all (k+m)! vertex priority orders."""
    k = len(neighborhoods)
    counts = [0] * (k + 1)
    for order in permutations(range(k + m)):
        chosen_c = -1
        accepted_i = 0
        for v in order:
            if v < k:
                if chosen_c < 0 and not (neighborhoods[v] & accepted_i):
                    chosen_c = v
            elif chosen_c < 0 or not (neighborhoods[chosen_c] >> (v - k) & 1):
                accepted_i |= 1 << (v - k)
        counts[chosen_c if chosen_c >= 0 else k] += 1
    d = factorial(k + m)
    return tuple(Fraction(x, d) for x in counts[:-1]), Fraction(counts[-1], d)


def run():
    counts = []
    for k, max_m in ((1, 5), (2, 5), (3, 4), (4, 3), (5, 2)):
        total = 0
        for m in range(max_m + 1):
            for assignment in product(range(1 << k), repeat=m):
                nbs = [sum(1 << i for i, mask in enumerate(assignment) if mask >> c & 1)
                       for c in range(k)]
                a = formula(nbs, m)
                b = direct_recurrence(nbs, m)
                assert a == b, (k, m, assignment, a, b)
                if k == 2:
                    d0, d1 = (x.bit_count() for x in nbs)
                    union = (nbs[0] | nbs[1]).bit_count()
                    intersection = (nbs[0] & nbs[1]).bit_count()
                    closed = (Fraction(union + 1, (d0 + 1) * (union + 2)),
                              Fraction(union + 1, (d1 + 1) * (union + 2)))
                    closed_none = Fraction(d0 * d1 * (union + 2) + intersection,
                                           (d0 + 1) * (d1 + 1) * (union + 2))
                    assert a == (closed, closed_none), (k, m, assignment, a)
                if k + m <= 6:
                    c = direct_permutations(nbs, m)
                    assert a == c, (k, m, assignment, a, c)
                total += 1
        counts.append((k, total))
        print('k', k, 'graphs', total, 'PASS', flush=True)
    m = 4
    pairwise_only = [0b0011, 0b0101, 0b0110]
    common_triple = [0b0011, 0b0101, 0b1001]
    p = formula(pairwise_only, m)
    q = formula(common_triple, m)
    print('three-center, pairwise_only', p)
    print('three-center, common_triple', q)
    assert p != q
    print('total', sum(x for _, x in counts), 'graphs PASS')


if __name__ == '__main__':
    run()
