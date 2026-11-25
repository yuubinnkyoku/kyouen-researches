#!/usr/bin/env python3
"""Independently check tricyclic core coverage and four-cycle mask verdicts."""
from itertools import combinations
import json
import enumerate_tricyclic_cores as core


def connected(adj):
    seen, todo = {0}, [0]
    while todo:
        u = todo.pop()
        for v in range(len(adj)):
            if adj[u] & (1 << v) and v not in seen:
                seen.add(v)
                todo.append(v)
    return len(seen) == len(adj)


def compress(adj):
    branch = [v for v,a in enumerate(adj) if a.bit_count() >= 3]
    order = {v:i for i,v in enumerate(branch)}
    used, paths = set(), []
    for start in branch:
        for neighbour in range(len(adj)):
            if not (adj[start] & (1 << neighbour)):
                continue
            edge = tuple(sorted((start,neighbour)))
            if edge in used:
                continue
            used.add(edge)
            previous, current, length = start, neighbour, 1
            while current not in order:
                assert adj[current].bit_count() == 2
                next_mask = adj[current] & ~(1 << previous)
                assert next_mask.bit_count() == 1
                nxt = next_mask.bit_length()-1
                edge = tuple(sorted((current,nxt)))
                assert edge not in used
                used.add(edge)
                previous, current, length = current, nxt, length+1
            paths.append((tuple(sorted((order[start],order[current]))),length))
    assert len(used) == sum(a.bit_count() for a in adj)//2
    return tuple(sorted(paths))


def mask_verdict(adj):
    n = len(adj)
    edges = list(combinations(range(n),2))
    ix = {e:i for i,e in enumerate(edges)}
    state = sum(1 << i for i,(u,v) in enumerate(edges) if adj[u] & (1 << v))
    blocked = 0
    for a,b,c,d in combinations(range(n),4):
        for q in ((a,b,c,d),(a,b,d,c),(a,c,b,d)):
            mask = sum(1 << ix[tuple(sorted((q[i],q[(i+1)%4])))] for i in range(4))
            overlap = state & mask
            if overlap == mask:
                return False, False
            if overlap.bit_count() == 3:
                blocked |= mask & ~state
    return True, (((1 << len(edges))-1) & ~state & ~blocked) == 0


def audit_small(n):
    n_edges = n+2
    generated = set()
    for b in range(1,5):
        for edges in core.cores(b):
            for lengths in core.length_assignments(edges,n_edges):
                generated.add(tuple(sorted(zip(edges,lengths))))
    all_edges = list(combinations(range(n),2))
    graphs = 0
    for choice in combinations(all_edges,n_edges):
        adj = [0]*n
        for u,v in choice:
            adj[u] |= 1 << v
            adj[v] |= 1 << u
        if min(a.bit_count() for a in adj)<2 or not connected(adj):
            continue
        assert compress(adj) in generated
        graphs += 1
    return {'vertices':n,'labelled_graphs_checked':graphs,'generated_core_length_types':len(generated)}


def audit_eleven():
    checked = free = saturated = 0
    for b in range(1,5):
        for edges in core.cores(b):
            for lengths in core.length_assignments(edges,13):
                adj = core.expand(b,edges,lengths)
                assert compress(adj) == tuple(sorted(zip(edges,lengths)))
                actual_free,actual_sat = mask_verdict(adj)
                assert actual_free == core.is_c4_free(adj)
                if actual_free:
                    assert actual_sat == core.is_saturated(adj)
                    free += 1
                    saturated += actual_sat
                checked += 1
    assert (checked,free,saturated) == (10408,4452,0)
    return {'vertices':11,'core_length_assignments':checked,'c4_free':free,'saturated':saturated}


if __name__ == '__main__':
    print(json.dumps({'small_coverage':[audit_small(n) for n in (6,7)],
                      'independent_cycle_masks':audit_eleven()},indent=2))
