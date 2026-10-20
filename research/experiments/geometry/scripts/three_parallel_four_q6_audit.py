#!/usr/bin/env python3
"""Exact independent checks for the 3-parallel-lines/4-points q=6 theorem.

No floating-point operations or external dependencies. Run from repository root:
  python research/experiments/geometry/scripts/three_parallel_four_q6_audit.py
"""
from collections import Counter
from functools import lru_cache
from itertools import combinations, product
import json


def rank(rows, width):
    """Rational row rank via fraction-free elimination over integers."""
    from fractions import Fraction
    mat = [[Fraction(x) for x in row] for row in rows]
    r = 0
    for col in range(width):
        piv = next((i for i in range(r, len(mat)) if mat[i][col]), None)
        if piv is None:
            continue
        mat[r], mat[piv] = mat[piv], mat[r]
        val = mat[r][col]
        mat[r] = [x / val for x in mat[r]]
        for i in range(r + 1, len(mat)):
            if mat[i][col]:
                fac = mat[i][col]
                mat[i] = [a - fac * b for a, b in zip(mat[i], mat[r])]
        r += 1
        if r == len(mat):
            break
    return r


def forced_zero(equations, test, width):
    return rank(equations, width) == rank(equations + [test], width)


def vector(n, terms):
    v = [0] * n
    for i, coef in terms:
        v[i] += coef
    return v


def patterns():
    # A row has four distinct points, each belonging to exactly two circles.
    # Its incidence multigraph is a four-cycle or a doubled perfect matching.
    out = []
    for a, b, c, d in [(0, 1, 2, 3), (0, 2, 1, 3), (0, 1, 3, 2)]:
        out.append(("cycle", [(a, b), (b, c), (c, d), (d, a)], ((a, c), (b, d))))
    for a, b, c, d in [(0, 1, 2, 3), (0, 2, 1, 3), (0, 3, 1, 2)]:
        out.append(("double", [(a, b), (a, b), (c, d), (c, d)], ((a, b), (c, d))))
    assert len(out) == 6
    return out


def exclude_four_circles():
    ps = patterns()
    candidates = 0
    rejected_centers = 0
    rejected_fourfold = 0
    survivors = []
    for picks in product(range(6), repeat=3):
        shared = Counter(tuple(sorted(edge)) for p in picks for edge in ps[p][1])
        # Equality in the incidence bound requires exactly two common
        # board points for each pair of the four circles.
        if any(shared[pair] != 2 for pair in combinations(range(4), 2)):
            continue
        candidates += 1
        eq_a, neq_a, eq_bc, neq_bc = [], [], [], []
        for y, p in enumerate(picks):
            kind, edges, opposite = ps[p]
            if kind == "cycle":
                (i, j), (k, l) = opposite
                # Sum of the two x roots of circle i is -A_i.
                eq_a.append(vector(4, [(i, 1), (j, 1), (k, -1), (l, -1)]))
                # Equal horizontal centers cannot meet in exactly one point.
                neq_a.extend(vector(4, [(i, 1), (j, -1)]) for i, j in edges)
            else:
                for i, j in opposite:
                    eq_a.append(vector(4, [(i, 1), (j, -1)]))
                    # Equal horizontal centers: equal root sets at this y
                    # iff B_i*y+C_i = B_j*y+C_j.
                    eq_bc.append(vector(8, [(i, y), (j, -y), (4+i, 1), (4+j, -1)]))
                (i, _), (k, _) = opposite
                neq_bc.append((vector(4, [(i, 1), (k, -1)]),
                               vector(8, [(i, y), (k, -y), (4+i, 1), (4+k, -1)])))
        if any(forced_zero(eq_a, v, 4) for v in neq_a):
            rejected_centers += 1
            continue
        if any(forced_zero(eq_a, va, 4) and forced_zero(eq_bc, vbc, 8)
               for va, vbc in neq_bc):
            rejected_fourfold += 1
            continue
        survivors.append(picks)
    assert (candidates, rejected_centers, rejected_fourfold, len(survivors)) == (21, 15, 6, 0)
    return dict(row_patterns=6, ordered_pattern_triples=216,
                pairwise_twice_candidates=candidates,
                impossible_single_intersection=rejected_centers,
                forced_fourfold_row_intersection=rejected_fourfold,
                survivors=survivors)


def construction():
    # Each row has four distinct points ±sqrt(k), represented without sqrt.
    # circle equations are x^2+y^2+B*y+C=0 (A=0).
    rows = [(0, (16, 18)), (1, (15, 14)), (2, (12, 10))]
    points = []
    for y, squares in rows:
        for square in squares:
            for sign in (-1, 1):
                points.append((y, sign, square))
    assert len(points) == 12 and len(set(points)) == 12
    circles = [(0, -16), (1, -16), (2, -18)]
    masks = []
    for b, c in circles:
        indices = [i for i, (y, _, square) in enumerate(points)
                   if square + y*y + b*y + c == 0]
        assert len(indices) == 6
        assert [sum(points[i][0] == y for i in indices) for y in (0, 1, 2)] == [2, 2, 2]
        masks.append(sum(1 << i for i in indices))
    assert len(set(masks)) == 3
    assert all((a & b).bit_count() == 2 for a, b in combinations(masks, 2))
    return points, masks


def grundy_stats(masks):
    n = 12
    full = (1 << n) - 1
    safe = [all((s & edge) != edge for edge in masks) for s in range(1 << n)]
    g = [-1] * (1 << n)
    terminal = Counter()
    for s in range(full, -1, -1):
        if not safe[s]:
            continue
        options = [g[s | (1 << i)] for i in range(n)
                   if not s >> i & 1 and safe[s | (1 << i)]]
        seen = set(options)
        mex = 0
        while mex in seen:
            mex += 1
        g[s] = mex
        if not options:
            terminal[s.bit_count()] += 1
    distribution = Counter(g[s] for s in range(1 << n) if safe[s])
    # Independent top-down memo recursion checks all reachable safe states.
    @lru_cache(None)
    def recursive(s):
        seen = {recursive(s | (1 << i)) for i in range(n)
                if not s >> i & 1 and safe[s | (1 << i)]}
        return next(v for v in range(len(seen)+1) if v not in seen)
    assert recursive(0) == g[0]
    assert recursive.cache_info().currsize == sum(safe)
    assert all(recursive(s) == g[s] for s in range(1 << n) if safe[s])
    assert (g[0], sum(safe), dict(sorted(terminal.items()))) == (0, 3915, {9: 8, 10: 24})
    return dict(empty_grundy=g[0], safe_states=sum(safe),
                grundy_histogram=dict(sorted(distribution.items())),
                maximal_safe_size_histogram=dict(sorted(terminal.items())),
                first_move_grundy=[g[1 << i] for i in range(n)],
                independent_recursive_states=recursive.cache_info().currsize)


def main():
    pattern_audit = exclude_four_circles()
    points, masks = construction()
    data = dict(theorem="At most three six-point circles on three parallel lines with at most four candidate points per line; attained",
                proof_scope="universal real Euclidean geometry; circle count (not grid coordinates)",
                pattern_audit=pattern_audit,
                example=dict(points_y_sign_x_squared=points,
                             circle_equations=["x^2+y^2=16", "x^2+y^2+y=16", "x^2+y^2+2y=18"],
                             forbidden_six_masks=masks),
                finite_game=grundy_stats(masks))
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
