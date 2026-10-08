#!/usr/bin/env python3
"""Independent finite-difference and stochastic-recursion audit of height bias.

For 3<=w<=5, 2<=h<w, 1<=r<=5, check every safe sorted state.
This script enumerates terminal labelled occupation vectors directly,
without using K0361's bivariate generating-function implementation.
"""
from collections import defaultdict
from functools import lru_cache
from itertools import combinations_with_replacement, product
from fractions import Fraction
from math import comb, factorial, prod


def terminal_shapes(w, h, r):
    result = defaultdict(list)
    for y in product(range(r+1), repeat=w):
        z = sorted(y, reverse=True)
        if sum(z[:h]) == r and all(v == z[h-1] for v in z[h:]):
            result[z[h-1]].append(y)
    return result


def shapes_containing(x, shapes):
    return [y for y in shapes if all(a <= b for a, b in zip(x, y))]


def n_of_m(x, ys, m):
    return sum(prod(comb(m-a, b-a) for a, b in zip(x, y)) for y in ys)


def leading_coefficient(x, ys):
    return sum((Fraction(1, prod(factorial(b-a) for a, b in zip(x, y)))
                for y in ys), Fraction(0))


def random_terminal_distribution(x, h, r, m=None):
    # m=None is limiting uniform legal COLUMN, otherwise choose a legal
    # EMPTY BOARD POINT uniformly, weighting a column by m-x_i.
    @lru_cache(None)
    def recur(state):
        moves = []
        for i, value in enumerate(state):
            child = list(state)
            child[i] += 1
            child = tuple(sorted(child, reverse=True))
            if sum(child[:h]) <= r:
                moves.append((child, 1 if m is None else m-value))
        if not moves:
            return {state[h-1]: Fraction(1)}
        denominator = sum(weight for child, weight in moves)
        result = defaultdict(Fraction)
        for child, weight in moves:
            for t, p in recur(child).items():
                result[t] += Fraction(weight, denominator)*p
        return dict(result)
    return recur(tuple(x))


def audit():
    positions = thresholds = 0
    for w in range(3, 6):
        for h in range(2, w):
            n = w-h
            for r in range(1, 6):
                terminal = terminal_shapes(w,h,r)
                for asc in combinations_with_replacement(range(r+1),w):
                    x = tuple(reversed(asc))
                    if sum(x[:h]) > r:
                        continue
                    A = x[h-1]
                    B = max(t for t in range(r+1)
                            if sum(max(v,t) for v in x[:h]) <= r)
                    lambdas = {}
                    for t, ys_all in terminal.items():
                        ys = shapes_containing(x, ys_all)
                        if not ys:
                            assert not (A <= t <= B)
                            continue
                        assert A <= t <= B
                        ell = r + n*t - sum(x)
                        assert all(sum(y)-sum(x) == ell for y in ys)
                        coef = leading_coefficient(x, ys)
                        assert coef > 0
                        values = [n_of_m(x,ys,m) for m in range(r,r+ell+2)]
                        diffs = values
                        for _ in range(ell):
                            diffs = [b-a for a,b in zip(diffs,diffs[1:])]
                        assert len(set(diffs)) == 1
                        assert Fraction(diffs[0],factorial(ell)) == coef
                        lambdas[t] = coef
                        thresholds += 1
                    assert set(lambdas) == set(range(A,B+1))
                    p = random_terminal_distribution(x,h,r)
                    assert set(p) == set(range(A,B+1))
                    assert all(v>0 for v in p.values()) and sum(p.values()) == 1
                    positions += 1

    example_x=(0,0,0)
    for m in (3,5,10,100):
        paths3 = factorial(3)*3*comb(m,3)
        paths4 = factorial(4)*3*comb(m,2)*m*m
        complete_short = Fraction(paths3, paths3+paths4)
        sequential_short = Fraction((m-1)*(m-2),(3*m-1)*(3*m-2))
        observed = random_terminal_distribution(example_x,2,3,m)
        assert observed == {0:sequential_short,1:1-sequential_short}
        print("EXAMPLE",m,"complete_short",complete_short,
              "sequential_short",sequential_short)
    assert random_terminal_distribution(example_x,2,3) == {
        0:Fraction(1,9), 1:Fraction(8,9)}
    print("PASS positions",positions,"terminal_thresholds",thresholds)
    print("PASS uniform-legal-point exact example and limit {0:1/9,1:8/9}")


if __name__ == "__main__":
    audit()
