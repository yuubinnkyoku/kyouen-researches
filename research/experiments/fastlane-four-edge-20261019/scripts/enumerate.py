#!/usr/bin/env python3
"""Exact rank<=4, <=4-edge avoidance-game classification by incidence multiplicities.
No third-party dependencies. Python 3.10+.
"""
import json
from collections import Counter
from functools import lru_cache
from itertools import permutations
from pathlib import Path


def classify(h: int):
    types = range(1, 1 << h)
    memberships = [tuple(i for i in range(h) if t >> i & 1) for t in types]

    @lru_cache(None)
    def grundy(counts):
        sizes = [sum(counts[t - 1] for t in types if t >> i & 1) for i in range(h)]
        if 0 in sizes:
            return -1  # forbidden, not a legal position
        reachable = set()
        for t in types:
            if counts[t - 1] and all(sizes[i] > 1 for i in memberships[t - 1]):
                nxt = list(counts)
                nxt[t - 1] -= 1
                reachable.add(grundy(tuple(nxt)))
        mex = 0
        while mex in reachable:
            mex += 1
        return mex

    distributions = Counter()
    uniform = Counter()
    min_witness = {}
    uniform_witness = {}
    maximal_patterns = []
    all_vectors = 0
    minimal = 0

    def rec(j, counts, sizes):
        nonlocal all_vectors, minimal
        if j == len(memberships):
            all_vectors += 1
            if not all(2 <= s <= 4 for s in sizes):
                return
            # All h edges are inclusion-minimal (antichain).
            for i in range(h):
                for k in range(h):
                    if i != k and not any(counts[t - 1] and (t >> i & 1) and not (t >> k & 1) for t in types):
                        return
            minimal += 1
            g = grundy(tuple(counts))
            distributions[g] += 1
            if h == 4 and g == 5:
                maximal_patterns.append(tuple(counts))
            if all(s == 4 for s in sizes):
                uniform[g] += 1
                if g not in uniform_witness or sum(counts) < uniform_witness[g]['vertices']:
                    uniform_witness[g] = {'vertices': sum(counts), 'membership_counts': {str(t): counts[t-1] for t in types if counts[t-1]}}
            witness = {'vertices': sum(counts), 'edge_sizes': list(sizes),
                       'membership_counts': {str(t): counts[t - 1] for t in types if counts[t - 1]}}
            if g not in min_witness or (witness['vertices'], tuple(counts)) < (min_witness[g]['vertices'], tuple(min_witness[g]['counts'])):
                witness['counts'] = list(counts)
                min_witness[g] = witness
            return
        t = j + 1
        inds = memberships[j]
        cap = min(4 - sizes[i] for i in inds)
        for x in range(cap + 1):
            counts.append(x)
            rec(j + 1, counts, tuple(sizes[i] + (x if i in inds else 0) for i in range(h)))
            counts.pop()

    rec(0, [], (0,) * h)
    orbits = set()
    for c in maximal_patterns:
        representatives = []
        for perm in permutations(range(h)):
            transformed = [0] * len(types)
            for t in types:
                target = sum(1 << perm[i] for i in range(h) if t >> i & 1)
                transformed[target - 1] = c[t - 1]
            representatives.append(tuple(transformed))
        orbits.add(min(representatives))
    for w in min_witness.values():
        del w['counts']
    return {'h': h, 'all_multiplicity_vectors': all_vectors, 'minimal_nonempty_h_edge_vectors': minimal,
            'grundy_distribution': dict(sorted(distributions.items())),
            'all_edges_size_four_distribution': dict(sorted(uniform.items())),
            'minimum_vertex_witness_by_grundy': dict(sorted(min_witness.items())),
            'uniform_four_witness_by_grundy': dict(sorted(uniform_witness.items())),
            'memo_states': grundy.cache_info().currsize,
            'maximal_nimber_orbits': len(orbits),
            'maximal_nimber_vertices': dict(sorted(Counter(sum(c) for c in maximal_patterns).items()))}


def direct_subset_grundy(membership_counts, h):
    """Independent small witness check: explicit vertex bitmask recursion, not count transitions."""
    vertex_memberships = [int(t) for t, count in membership_counts.items() for _ in range(count)]
    edges = [sum(1 << j for j, t in enumerate(vertex_memberships) if t >> i & 1) for i in range(h)]
    n = len(vertex_memberships)

    @lru_cache(None)
    def g(occupied):
        successors = set()
        for j in range(n):
            if occupied >> j & 1:
                continue
            after = occupied | (1 << j)
            if all((after & e) != e for e in edges):
                successors.add(g(after))
        v = 0
        while v in successors:
            v += 1
        return v

    return g(0), [list(i for i in range(n) if e >> i & 1) for e in edges]


def main():
    summary = [classify(h) for h in range(1, 5)]
    for item in summary:
        for g, w in list(item['minimum_vertex_witness_by_grundy'].items()) + list(item['uniform_four_witness_by_grundy'].items()):
            got, edges = direct_subset_grundy(w['membership_counts'], item['h'])
            assert got == g, (item['h'], g, got)
            w['explicit_edges_zero_based'] = edges
    assert summary[3]['all_multiplicity_vectors'] == 92550
    assert summary[3]['minimal_nonempty_h_edge_vectors'] == 37592
    assert summary[3]['grundy_distribution'] == {0: 13508, 1: 13427, 2: 5111, 3: 5270, 4: 240, 5: 36}
    assert summary[3]['maximal_nimber_orbits'] == 2
    assert summary[3]['maximal_nimber_vertices'] == {9:24, 11:12}
    assert summary[3]['all_edges_size_four_distribution'] == {0: 1269, 1: 1294, 2: 429, 3: 602, 4: 36, 5: 12}
    result = {'rank_at_most': 4, 'no_free_vertices': True,
              'labeled_edge_classes': summary,
              'global_max_grundy': max(max(s['grundy_distribution']) for s in summary)}
    script_dir = Path(__file__).resolve().parent
    path = (script_dir.parent / 'output' / 'results.json') if script_dir.name == 'scripts' else (script_dir / 'results.json')
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    for s in summary:
        print('h=', s['h'], 'all=', s['all_multiplicity_vectors'], 'antichains=', s['minimal_nonempty_h_edge_vectors'],
              'grundy=', s['grundy_distribution'], 'uniform4=', s['all_edges_size_four_distribution'])
    print('wrote', path)


if __name__ == '__main__':
    main()
