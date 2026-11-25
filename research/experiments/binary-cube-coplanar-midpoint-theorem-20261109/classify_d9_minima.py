#!/usr/bin/env python3
"""Classify the saved fixed-edge minima by exhaustive graph isomorphism."""
from collections import Counter
from itertools import combinations, permutations, product
from math import factorial
import gzip
import hashlib
import json
from pathlib import Path
import sys

N = 9
EDGES = list(combinations(range(N), 2))


def adjacency(mask):
    adj = [0] * N
    for i, (u, v) in enumerate(EDGES):
        if mask & (1 << i):
            adj[u] |= 1 << v
            adj[v] |= 1 << u
    return adj


def isomorphic(a, b):
    da = [x.bit_count() for x in a]
    db = [x.bit_count() for x in b]
    if sorted(da) != sorted(db):
        return False
    frequency = Counter(da)
    order = sorted(range(N), key=lambda i: (frequency[da[i]], -da[i], i))
    mapping = [-1] * N

    def search(depth, used):
        if depth == N:
            return True
        u = order[depth]
        for v in range(N):
            if used & (1 << v) or da[u] != db[v]:
                continue
            if any(bool(a[u] & (1 << w)) != bool(b[v] & (1 << mapping[w]))
                   for w in order[:depth]):
                continue
            mapping[u] = v
            if search(depth + 1, used | (1 << v)):
                return True
            mapping[u] = -1
        return False

    return search(0, 0)


def automorphisms(adj):
    groups = {}
    for v, row in enumerate(adj):
        groups.setdefault(row.bit_count(), []).append(v)
    groups = list(groups.values())
    count = 0
    for choices in product(*(permutations(group) for group in groups)):
        mapping = [0] * N
        for group, choice in zip(groups, choices):
            for u, v in zip(group, choice):
                mapping[u] = v
        if all(bool(adj[u] & (1 << v)) == bool(adj[mapping[u]] & (1 << mapping[v]))
               for u, v in EDGES):
            count += 1
    return count


def main():
    raw = gzip.decompress(Path(sys.argv[1]).read_bytes())
    masks = list(map(int, raw.split()))
    assert len(masks) == 83160 and masks == sorted(set(masks))
    classes = []
    for mask in masks:
        assert mask & 1 and mask.bit_count() == 11 and mask < (1 << len(EDGES))
        adj = adjacency(mask)
        for group in classes:
            if isomorphic(adj, group['adjacency']):
                group['fixed_edge_count'] += 1
                break
        else:
            classes.append({'representative_mask': mask, 'adjacency': adj, 'fixed_edge_count': 1})
    result = []
    for group in classes:
        adj = group.pop('adjacency')
        aut = automorphisms(adj)
        assert factorial(N) % aut == 0
        labelled = factorial(N) // aut
        assert labelled * 11 == group['fixed_edge_count'] * len(EDGES)
        group.update(degrees=sorted(x.bit_count() for x in adj), automorphisms=aut,
                     all_labelled_count=labelled)
        result.append(group)
    assert sum(group['all_labelled_count'] for group in result) == 272160
    print(json.dumps({'fixed_edge_input_sha256': hashlib.sha256(raw).hexdigest(),
                      'fixed_edge_states': len(masks), 'classes': result}, indent=2))


if __name__ == '__main__':
    main()
