#!/usr/bin/env python3
"""Finite independent check for the arbitrary-base fiber reduction theorem.

Example: four vertical fibers over a planar base with one 3-point line,
m=3 and q=9. The geometric checker enumerates every q-subset exactly.
"""
from functools import lru_cache
from fractions import Fraction
from itertools import combinations

BASE = ((0, 0), (1, 0), (2, 0), (0, 1))
M = 3
Q = 9
W = len(BASE)
POINTS = tuple((x, y, z) for x, y in BASE for z in range(M))
N = len(POINTS)


def rank_q(rows):
    a = [[Fraction(v) for v in row] for row in rows]
    r = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        p = a[r][c]
        a[r] = [v / p for v in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c]:
                k = a[i][c]
                a[i] = [a[i][j] - k * a[r][j] for j in range(len(a[i]))]
        r += 1
        if r == len(a):
            break
    return r


def line_traces(base):
    traces = set()
    for i, j in combinations(range(len(base)), 2):
        ax, ay = base[i]
        bx, by = base[j]
        trace = tuple(
            k for k, (cx, cy) in enumerate(base)
            if (bx - ax) * (cy - ay) == (by - ay) * (cx - ax)
        )
        traces.add(trace)
    return tuple(sorted(t for t in traces if len(t) >= 2))


def bits(indices):
    out = 0
    for i in indices:
        out |= 1 << i
    return out


def mex(values):
    x = 0
    while x in values:
        x += 1
    return x


def main():
    assert Q > 2 * W, "the sphere/nonvertical-hyperplane separation is required"

    # Direct geometric enumeration of all q-subsets.
    direct_forbidden = set()
    for subset in combinations(range(N), Q):
        rows = [(*POINTS[i], 1) for i in subset]
        if rank_q(rows) <= 3:
            direct_forbidden.add(bits(subset))

    # A sphere meets each vertical fiber at most twice, so 2W < Q
    # rules out every spherical forbidden q-set.
    traces = line_traces(BASE)
    predicted_forbidden = set()
    for trace in traces:
        cells = [i for i in range(N) if i // M in trace]
        if len(cells) >= Q:
            for subset in combinations(cells, Q):
                predicted_forbidden.add(bits(subset))

    assert direct_forbidden == predicted_forbidden, (
        direct_forbidden, predicted_forbidden, traces
    )

    def is_direct_safe(mask):
        return all((f & mask) != f for f in direct_forbidden)

    def is_reduced_safe(counts):
        return all(sum(counts[i] for i in t) <= Q - 1 for t in traces)

    @lru_cache(None)
    def grundy_reduced(counts):
        children = set()
        for i in range(W):
            if counts[i] == M:
                continue
            nxt = list(counts)
            nxt[i] += 1
            nxt = tuple(nxt)
            if is_reduced_safe(nxt):
                children.add(grundy_reduced(nxt))
        return mex(children)

    @lru_cache(None)
    def grundy_direct(mask):
        children = set()
        for i in range(N):
            if mask >> i & 1:
                continue
            nxt = mask | (1 << i)
            if is_direct_safe(nxt):
                children.add(grundy_direct(nxt))
        return mex(children)

    safe_masks = 0
    safe_count_vectors = set()
    histogram = {}
    for mask in range(1 << N):
        counts = tuple(
            sum((mask >> (j * M + k)) & 1 for k in range(M))
            for j in range(W)
        )
        ds = is_direct_safe(mask)
        rs = is_reduced_safe(counts)
        assert ds == rs, (mask, counts, ds, rs)
        if not ds:
            continue
        safe_masks += 1
        safe_count_vectors.add(counts)
        gd = grundy_direct(mask)
        gr = grundy_reduced(counts)
        assert gd == gr, (mask, counts, gd, gr)
        histogram[gd] = histogram.get(gd, 0) + 1

    assert len(direct_forbidden) == 1
    assert safe_masks == 4088
    assert len(safe_count_vectors) == 252
    assert histogram == {0: 2044, 1: 2044}

    print("PASS")
    print(f"base_points={W}, board_points={N}, q={Q}, m={M}")
    print(f"hyperplane_traces={traces}")
    print(f"direct_forbidden_q_sets={len(direct_forbidden)}")
    print(f"safe_cell_positions={safe_masks}")
    print(f"safe_count_vectors={len(safe_count_vectors)}")
    print(f"grundy_histogram={dict(sorted(histogram.items()))}")
    print(f"direct_grundy_states={grundy_direct.cache_info().currsize}")
    print(f"reduced_grundy_states={grundy_reduced.cache_info().currsize}")


if __name__ == "__main__":
    main()
