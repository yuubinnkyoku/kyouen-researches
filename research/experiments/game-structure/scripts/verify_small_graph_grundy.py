#!/usr/bin/env python3
"""Independent exact checks for the seven-vertex Grundy-4 Node Kayles witness."""
import itertools
import json
from functools import lru_cache

WITNESS_EDGES = ((0,4),(0,5),(0,6),(1,2),(1,4),(1,5),(2,3))


def graph_grundy(n, edges):
    neighbors = [1 << i for i in range(n)]
    for a, b in edges:
        neighbors[a] |= 1 << b
        neighbors[b] |= 1 << a

    @lru_cache(None)
    def g(remaining):
        if remaining == 0:
            return 0
        children = {g(remaining & ~neighbors[i])
                    for i in range(n) if remaining & (1 << i)}
        answer = 0
        while answer in children:
            answer += 1
        return answer

    whole = (1 << n) - 1
    return g(whole), sorted({g(whole & ~neighbors[i]) for i in range(n)})


def edges_from_mask(n, mask):
    return [(i, j) for k, (i, j) in enumerate(itertools.combinations(range(n), 2))
            if mask & (1 << k)]


def main():
    counts = {}
    for n in range(1, 7):
        freq = {}
        for mask in range(1 << (n * (n - 1) // 2)):
            g, _ = graph_grundy(n, edges_from_mask(n, mask))
            freq[g] = freq.get(g, 0) + 1
        counts[str(n)] = {str(k): freq[k] for k in sorted(freq)}
        assert max(freq) <= 3
    assert counts['4'] == {'0': 23, '1': 11, '2': 18, '3': 12}
    g4, options4 = graph_grundy(7, WITNESS_EDGES)
    assert (g4, options4) == (4, [0, 1, 2, 3])
    g5, options5 = graph_grundy(8, WITNESS_EDGES)
    assert (g5, options5) == (5, [0, 1, 2, 3, 4])

    leaf_cases = {}
    for mask in range(16):
        # Path 0-1-2, isolated 3, vertex 4 attached to any subset,
        # pendant vertex 5 attached only to vertex 4.
        edges = [(0,1), (1,2), (4,5)] + [
            (4,i) for i in range(4) if mask & (1 << i)]
        val, options = graph_grundy(6, edges)
        assert val <= 2 and 3 in options
        leaf_cases[f'{mask:04b}'] = {'grundy': val, 'options': options}

    # Recursive signatures for A_2 = witness and
    # A_{k+1} = (A_k disjoint-union A_k) join A_k.
    # A_k has option set [0, 2^k), so A_k+A_k has
    # options [2^k,2^(k+1)); the join restores the lower half.
    amplification = []
    for k in range(2, 10):
        amplification.append({'k': k, 'grundy': 2**k,
                              'vertices': 7 * 3**(k-2)})

    print(json.dumps({'counts_all_labeled_graphs': counts,
                      'seven_vertex_witness_edges': WITNESS_EDGES,
                      'seven_vertex_options': options4,
                      'eight_vertex_options': options5,
                      'leaf_cases': leaf_cases,
                      'amplification': amplification},
                     indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
