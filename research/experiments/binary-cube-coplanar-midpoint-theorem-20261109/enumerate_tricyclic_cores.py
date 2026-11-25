#!/usr/bin/env python3
"""Enumerate simple min-degree-two connected n-vertex (n+2)-edge graphs by cores."""
from itertools import combinations, combinations_with_replacement
import argparse
import json


def cores(branches):
    pairs = [(u,v) for u in range(branches) for v in range(u,branches)]
    for edges in combinations_with_replacement(pairs, branches+2):
        degree = [0]*branches
        adjacency = [set() for _ in range(branches)]
        for u,v in edges:
            degree[u] += 1
            degree[v] += 1
            adjacency[u].add(v)
            adjacency[v].add(u)
        if min(degree) < 3:
            continue
        seen, stack = {0}, [0]
        while stack:
            for v in adjacency[stack.pop()] - seen:
                seen.add(v)
                stack.append(v)
        if len(seen) == branches:
            yield edges


def length_assignments(edges, total):
    minimum = [3 if u == v else 1 for u,v in edges]
    lengths = []

    def visit(i, remaining):
        if i == len(edges):
            if remaining == 0:
                yield tuple(lengths)
            return
        tail = sum(minimum[i+1:])
        for length in range(minimum[i], remaining-tail+1):
            # Parallel core edges may have at most one unsubdivided copy.
            if length == 1 and any(edges[j] == edges[i] and lengths[j] == 1 for j in range(i)):
                continue
            lengths.append(length)
            yield from visit(i+1, remaining-length)
            lengths.pop()
    yield from visit(0,total)


def expand(branches, core, lengths):
    adj = [0]*(branches + sum(length-1 for length in lengths))
    nxt = branches
    for (u,v), length in zip(core,lengths):
        previous = u
        for _ in range(length-1):
            adj[previous] |= 1 << nxt
            adj[nxt] |= 1 << previous
            previous, nxt = nxt, nxt+1
        adj[previous] |= 1 << v
        adj[v] |= 1 << previous
    return adj[:nxt]


def is_c4_free(adj):
    return all((adj[u] & adj[v]).bit_count() <= 1 for u,v in combinations(range(len(adj)),2))


def is_saturated(adj):
    for u,v in combinations(range(len(adj)),2):
        if adj[u] & (1 << v):
            continue
        neighbours = adj[u]
        while neighbours:
            x = (neighbours & -neighbours).bit_length()-1
            neighbours &= neighbours-1
            if adj[x] & adj[v]:
                break
        else:
            return False
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('vertices',type=int,choices=range(6,21))
    args = parser.parse_args()
    n, m = args.vertices, args.vertices+2
    records = []
    for branches in range(1,5):
        core_count = candidates = free = saturated = 0
        example = None
        for core in cores(branches):
            core_count += 1
            for lengths in length_assignments(core,m):
                adj = expand(branches,core,lengths)
                assert len(adj) == n and sum(x.bit_count() for x in adj) == 2*m
                assert min(x.bit_count() for x in adj) >= 2
                candidates += 1
                if not is_c4_free(adj):
                    continue
                free += 1
                if is_saturated(adj):
                    saturated += 1
                    if example is None:
                        example = [[u,v] for u,v in combinations(range(n),2) if adj[u] & (1 << v)]
        records.append({'branch_vertices':branches,'labelled_cores':core_count,
                        'length_assignments':candidates,'c4_free':free,
                        'saturated':saturated,'first_example_edges':example})
    print(json.dumps({'vertices':n,'edges':m,'records':records,
                      'scope':'labelled core and ordered path lengths, not distinct labelled graphs'},indent=2))


if __name__ == '__main__':
    main()
