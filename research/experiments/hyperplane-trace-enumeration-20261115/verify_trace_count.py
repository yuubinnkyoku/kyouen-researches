#!/usr/bin/env python3
"""Exact finite audit for affine-hyperplane traces."""
from fractions import Fraction
from itertools import combinations, product
from math import comb
import json


def rank(rows):
    if not rows:
        return 0
    a = [[Fraction(x) for x in row] for row in rows]
    m, n = len(a), len(a[0])
    pivot = 0
    for col in range(n):
        p = next((i for i in range(pivot, m) if a[i][col]), None)
        if p is None:
            continue
        a[pivot], a[p] = a[p], a[pivot]
        v = a[pivot][col]
        a[pivot] = [x / v for x in a[pivot]]
        for i in range(m):
            if i != pivot and a[i][col]:
                z = a[i][col]
                a[i] = [a[i][j] - z * a[pivot][j] for j in range(n)]
        pivot += 1
        if pivot == m:
            break
    return pivot


def affine_rank(points):
    if len(points) <= 1:
        return 0
    p0 = points[0]
    return rank([[x-y for x,y in zip(p,p0)] for p in points[1:]])


def closure(base, seed):
    if not seed:
        return frozenset()
    r = affine_rank(seed)
    return frozenset(p for p in base if affine_rank(seed + (p,)) == r)


def basis_traces(base, dim):
    out = {frozenset()}
    for k in range(1, min(dim, len(base)) + 1):
        for seed in combinations(base, k):
            out.add(closure(base, seed))
    return out


def normal_traces(base, dim, bound):
    out = {frozenset()}
    for normal in product(range(-bound, bound+1), repeat=dim):
        if not any(normal):
            continue
        offsets = {sum(a*x for a,x in zip(normal,p)) for p in base}
        for c in offsets:
            out.add(frozenset(
                p for p in base if sum(a*x for a,x in zip(normal,p)) == c
            ))
    return out


def has_normal(base, trace, dim, bound):
    if not trace:
        return True
    p0 = next(iter(trace))
    outside = set(base) - set(trace)
    for normal in product(range(-bound, bound+1), repeat=dim):
        if not any(normal):
            continue
        c = sum(a*x for a,x in zip(normal,p0))
        if all(sum(a*x for a,x in zip(normal,p)) == c for p in trace) and all(
            sum(a*x for a,x in zip(normal,p)) != c for p in outside
        ):
            return True
    return False


def audit(dim, grid, normal_bound):
    bases = trace_sum = max_traces = max_bound = 0
    for mask in range(1 << len(grid)):
        base = tuple(grid[i] for i in range(len(grid)) if mask >> i & 1)
        generated = basis_traces(base, dim)
        direct = normal_traces(base, dim, normal_bound)
        assert direct <= generated, (dim, base, direct-generated)
        for trace in generated:
            assert has_normal(base, trace, dim, normal_bound), (dim, base, trace)
        upper = sum(comb(len(base), i) for i in range(min(dim, len(base))+1))
        assert len(generated) <= upper
        bases += 1
        trace_sum += len(generated)
        if len(generated) > max_traces:
            max_traces, max_bound = len(generated), upper
    return {
        "ambient_dimension": dim,
        "base_sets_checked": bases,
        "distinct_trace_count_sum": trace_sum,
        "maximum_trace_count": max_traces,
        "maximum_trace_bound_at_that_base": max_bound,
        "normal_search_bound": normal_bound,
        "result": "PASS",
    }


def main():
    cases = [
        (1, list(product(range(3), repeat=1)), 2),
        (2, list(product(range(3), repeat=2)), 4),
        (3, list(product(range(2), repeat=3)), 4),
    ]
    rows = [audit(*case) for case in cases]
    print(json.dumps({
        "method": "Fraction Gaussian elimination vs bounded integer-normal enumeration",
        "finite_only": True,
        "dimensions": rows,
        "total_base_sets": sum(x["base_sets_checked"] for x in rows),
        "total_distinct_trace_count_sum": sum(x["distinct_trace_count_sum"] for x in rows),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
