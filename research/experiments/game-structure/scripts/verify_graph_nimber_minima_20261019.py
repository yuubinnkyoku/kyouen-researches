#!/usr/bin/env python3
"""Self-contained exact audit for minimal vertex counts of Node Kayles nimbers 0..11."""
from functools import lru_cache
from itertools import combinations
import json

BASE3 = ((0, 1), (0, 2))
BASE7 = ((0, 1), (0, 2), (0, 5), (1, 4), (2, 3), (3, 5), (3, 6))
BASE13 = (
    (0, 1), (0, 2), (0, 4), (0, 5), (1, 2), (1, 3), (1, 6),
    (3, 6), (5, 6), (8, 10), (9, 10), (11, 12), (2, 11),
    (7, 11), (8, 11),
)


def evaluate(n, edges, children=False):
    adjacency = [0] * n
    for a, b in edges:
        assert 0 <= a < b < n, (n, a, b)
        assert not (adjacency[a] >> b & 1), (a, b)
        adjacency[a] |= 1 << b
        adjacency[b] |= 1 << a

    @lru_cache(maxsize=None)
    def g(remaining):
        options = 0
        bits = remaining
        while bits:
            bit = bits & -bits
            v = bit.bit_length() - 1
            bits -= bit
            value = g(remaining & ~(bit | adjacency[v]))
            options |= 1 << value
        return ((~options) & (options + 1)).bit_length() - 1

    root = (1 << n) - 1
    result = g(root)
    if children:
        return result, [g(root & ~((1 << v) | adjacency[v])) for v in range(n)]
    return result


def union(*components):
    n, edges = 0, []
    for size, part in components:
        edges.extend((a + n, b + n) for a, b in part)
        n += size
    return n, tuple(edges)


def exhaustive_small():
    summary = []
    for n in range(7):
        pairs = list(combinations(range(n), 2))
        hist = {}
        for mask in range(1 << len(pairs)):
            edges = [pair for i, pair in enumerate(pairs) if mask >> i & 1]
            value = evaluate(n, edges)
            hist[value] = hist.get(value, 0) + 1
        summary.append({"vertices": n, "graphs": 1 << len(pairs),
                        "nimber_histogram": {str(k): v for k, v in sorted(hist.items())}})
    return summary


def main():
    E = (0, ())
    I = (1, ())
    P3 = (3, BASE3)
    H7 = (7, BASE7)
    H13 = (13, BASE13)
    constructions = [
        E, I, P3, union(P3, I), H7, union(H7, I),
        union(H7, P3), union(H7, P3, I), H13, union(H13, I),
        union(H13, P3), union(H13, P3, I),
    ]
    expected = [0, 1, 3, 4, 7, 8, 10, 11, 13, 14, 16, 17]
    witnesses = []
    for target, ((n, edges), size) in enumerate(zip(constructions, expected)):
        value, children = evaluate(n, edges, children=True)
        assert value == target, (target, value)
        assert n == size, (target, n, size)
        witnesses.append({"nimber": target, "vertices": n,
                          "edges": len(edges), "children": children})
    assert evaluate(7, BASE7) == 4
    assert evaluate(13, BASE13) == 8
    small = exhaustive_small()
    assert [max(map(int, item["nimber_histogram"])) for item in small] == [0, 1, 1, 2, 3, 3, 3]
    print(json.dumps({"small_labeled_graphs": small,
                      "minimum_witnesses": witnesses}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
