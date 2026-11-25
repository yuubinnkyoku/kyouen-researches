#!/usr/bin/env python3
"""Independent named-vertex Node Kayles verifier; no quotient/formula in mex.

Run: python3 verify_named.py
"""
from functools import lru_cache


def grundy_from_adjacency(adjacency):
    closed = [(1 << i) | mask for i, mask in enumerate(adjacency)]

    @lru_cache(None)
    def g(remaining):
        seen = 0
        todo = remaining
        while todo:
            bit = todo & -todo
            i = bit.bit_length() - 1
            todo -= bit
            seen |= 1 << g(remaining & ~closed[i])
        value = 0
        while (seen >> value) & 1:
            value += 1
        return value

    value = g((1 << len(adjacency)) - 1)
    return value, g.cache_info().currsize


def build_split_graph(private, pairs):
    k = len(private)
    adjacency = [((1 << k) - 1) ^ (1 << i) for i in range(k)]

    def append_independent(neighbors):
        v = len(adjacency)
        adjacency.append(0)
        for i in neighbors:
            adjacency[v] |= 1 << i
            adjacency[i] |= 1 << v

    for i, count in enumerate(private):
        for _ in range(count):
            append_independent((i,))
    for (i, j), count in pairs.items():
        for _ in range(count):
            append_independent((i, j))
    return adjacency


def star_family(k):
    assert k >= 4
    private = [1, 0, 0, 0] + [2] * (k - 4)
    pairs = {(0, i): 2 for i in (1, 2, 3)}
    return build_split_graph(private, pairs)


def independent_symbolic(k):
    # F(n): K_n with exactly two private leaves per clique vertex.
    F = [0] * k
    for n in range(1, k):
        opts = {0, F[n - 1] ^ 1}
        F[n] = next(x for x in range(4) if x not in opts)
    # H(m): distinguished vertex 0, three pair-only vertices,
    # and m extra vertices with two private leaves each.
    H = []
    for m in range(k - 3):
        n = m + 3
        options = {0, 1, F[n], F[n - 1]}
        if m:
            options.add(H[m - 1] ^ 1)
        H.append(next(x for x in range(6) if x not in options))
    return F, H


def check_clique_vertex_correction():
    base = build_split_graph([1, 1, 1], {})
    extended = build_split_graph([1, 1, 1, 0, 0], {})
    b, bstates = grundy_from_adjacency(base)
    e, estates = grundy_from_adjacency(extended)
    assert (b, e) == (1, 2)
    print(f"uncovered-clique correction: K3+3 leaves g={b} states={bstates}; "
          f"K5+3 leaves g={e} states={estates}; removing 2 clique vertices is invalid")


def main():
    for k in range(4, 11):
        graph = star_family(k)
        named, states = grundy_from_adjacency(graph)
        F, H = independent_symbolic(k)
        assert F[0] == 0 and F[1] == 2
        assert all(x == 1 for x in F[2:])
        assert all(x == 2 for x in H)
        assert named == H[k - 4] == 2
        # Parent independent parity is 1; clique incidence is (1,0,...,0).
        predicted = 3
        print(f"k={k} vertices={len(graph)} direct_g={named} symbolic_g={H[k-4]} "
              f"old_prediction={predicted} direct_states={states}")
    check_clique_vertex_correction()
    print("PASS: seven independent named-vertex counterexamples, "
          "symbolic recurrence, and correction")


if __name__ == '__main__':
    main()
