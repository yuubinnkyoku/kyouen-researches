#!/usr/bin/env python3
"""Independent finite checks for the arbitrary-base fiber reduction theorem.

Two non-general-position planar bases are tested. The checker enumerates all
q-subsets by exact rational affine rank, then compares every cell position and
its direct Grundy recursion with the hyperplane-trace count-vector game.
"""
from functools import lru_cache
from fractions import Fraction
from itertools import combinations
from collections import Counter


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


def audit_case(base, m, q, expected):
    w = len(base)
    points = tuple((x, y, z) for (x, y) in base for z in range(m))
    n = len(points)
    assert q > 2 * w

    # Direct affine-hyperplane enumeration for every q-subset.
    direct_forbidden = set()
    for subset in combinations(range(n), q):
        rows = [(*points[i], 1) for i in subset]
        if rank_q(rows) <= 3:
            direct_forbidden.add(bits(subset))

    # Spheres are excluded by the exact intersection bound 2w < q.
    traces = line_traces(base)
    predicted_forbidden = set()
    for trace in traces:
        cells = [i for i in range(n) if i // m in trace]
        for subset in combinations(cells, q):
            predicted_forbidden.add(bits(subset))

    assert direct_forbidden == predicted_forbidden, (
        direct_forbidden, predicted_forbidden, traces
    )

    @lru_cache(None)
    def direct_safe(mask):
        return all((f & mask) != f for f in direct_forbidden)

    @lru_cache(None)
    def reduced_safe(counts):
        return all(sum(counts[i] for i in t) <= q - 1 for t in traces)

    @lru_cache(None)
    def grundy_reduced(counts):
        children = set()
        for i in range(w):
            if counts[i] == m:
                continue
            nxt = list(counts)
            nxt[i] += 1
            nxt = tuple(nxt)
            if reduced_safe(nxt):
                children.add(grundy_reduced(nxt))
        return mex(children)

    @lru_cache(None)
    def grundy_direct(mask):
        children = set()
        for i in range(n):
            if mask >> i & 1:
                continue
            nxt = mask | (1 << i)
            if direct_safe(nxt):
                children.add(grundy_direct(nxt))
        return mex(children)

    safe_masks = 0
    safe_count_vectors = set()
    histogram = Counter()
    for mask in range(1 << n):
        counts = tuple(
            sum((mask >> (j * m + k)) & 1 for k in range(m))
            for j in range(w)
        )
        ds = direct_safe(mask)
        rs = reduced_safe(counts)
        assert ds == rs, (mask, counts, ds, rs)
        if not ds:
            continue
        safe_masks += 1
        safe_count_vectors.add(counts)
        gd = grundy_direct(mask)
        gr = grundy_reduced(counts)
        assert gd == gr, (mask, counts, gd, gr)
        histogram[gd] += 1

    result = {
        "base_points": w,
        "board_points": n,
        "q": q,
        "m": m,
        "traces": traces,
        "direct_forbidden_q_sets": len(direct_forbidden),
        "safe_cell_positions": safe_masks,
        "safe_count_vectors": len(safe_count_vectors),
        "grundy_histogram": dict(sorted(histogram.items())),
        "direct_grundy_states": grundy_direct.cache_info().currsize,
        "reduced_grundy_states": grundy_reduced.cache_info().currsize,
    }
    assert result["direct_forbidden_q_sets"] == expected["forbidden"]
    assert safe_masks == expected["safe"]
    assert len(safe_count_vectors) == expected["vectors"]
    assert dict(sorted(histogram.items())) == expected["grundy"]
    return result


def main():
    cases = [
        (
            ((0, 0), (1, 0), (2, 0), (0, 1)),
            3,
            9,
            {"forbidden": 1, "safe": 4088, "vectors": 252, "grundy": {0: 2044, 1: 2044}},
        ),
        (
            ((0, 0), (1, 0), (2, 0), (0, 1), (0, 2)),
            4,
            11,
            {
                "forbidden": 24,
                "safe": 1042005,
                "vectors": 2935,
                "grundy": {0: 482049, 1: 483668, 2: 37216, 3: 39072},
            },
        ),
    ]
    for i, (base, m, q, expected) in enumerate(cases, 1):
        result = audit_case(base, m, q, expected)
        print(f"case_{i}=PASS")
        for key, value in result.items():
            print(f"  {key}={value}")
    print("ALL PASS")


if __name__ == "__main__":
    main()
