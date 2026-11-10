#!/usr/bin/env python3
"""Check representatives and orbit sizes independently of the classifier."""
from itertools import combinations, permutations
from math import factorial
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
VERTICES = range(9)
EDGES = list(combinations(VERTICES, 2))


def c4s():
    result = []
    for a, b, c, d in combinations(VERTICES, 4):
        for path in ((a,b,c,d), (a,b,d,c), (a,c,b,d)):
            result.append(frozenset(tuple(sorted((path[i], path[(i+1)%4]))) for i in range(4)))
    return result


def main():
    groups = json.loads((HERE/'d9-minimum-classes.json').read_text())['classes']
    audit = json.loads((HERE/'d9-minimum-degree-audit.json').read_text())
    counts = {tuple(row['degrees']): row for row in audit['degree_sequences']}
    assert len(groups) == len(counts) == 6
    assert sum(row['fixed_edge_count'] for row in counts.values()) == 83160
    cycles = c4s()
    assert len(cycles) == len(set(cycles)) == 378
    seen = set()
    for group in groups:
        mask = group['representative_mask']
        edges = {edge for i, edge in enumerate(EDGES) if mask & (1 << i)}
        assert mask < (1 << len(EDGES)) and len(edges) == 11 and (0,1) in edges
        assert all(not cycle <= edges for cycle in cycles)
        assert all(any(cycle <= edges | {e} for cycle in cycles) for e in EDGES if e not in edges)
        degrees = tuple(sorted(sum(v in e for e in edges) for v in VERTICES))
        assert degrees == tuple(group['degrees']) and degrees not in seen
        seen.add(degrees)
        per_vertex = [sum(v in e for e in edges) for v in VERTICES]
        automorphisms = 0
        for perm in permutations(VERTICES):
            if any(per_vertex[v] != per_vertex[perm[v]] for v in VERTICES):
                continue
            moved = {tuple(sorted((perm[u], perm[v]))) for u,v in edges}
            automorphisms += moved == edges
        assert automorphisms == group['automorphisms'] and factorial(9) % automorphisms == 0
        labelled = factorial(9) // automorphisms
        count = counts[degrees]
        assert labelled == group['all_labelled_count'] == count['all_labelled_count']
        assert group['fixed_edge_count'] == count['fixed_edge_count']
        assert labelled * 11 == count['fixed_edge_count'] * len(EDGES)
    assert seen == set(counts)
    assert sum(row['all_labelled_count'] for row in counts.values()) == 272160
    print('PASS: six C4-saturated representatives, automorphism counts and complete orbits')


if __name__ == '__main__':
    main()
