#!/usr/bin/env python3
"""Verify all saved 14-vertex tetracyclic candidates have diameter >= 4."""
from collections import Counter
import gzip
import hashlib
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def expand(line):
    fields = line.split()
    branches = int(fields[0])
    adj, nxt, edges = [0]*14, branches, set()
    for field in fields[1:]:
        u,v,length = map(int,field.split(','))
        for _ in range(length-1):
            edges.add(tuple(sorted((u,nxt))))
            u,nxt = nxt,nxt+1
        edges.add(tuple(sorted((u,v))))
    assert nxt == 14 and len(edges) == 17
    for u,v in edges:
        assert u != v
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    assert min(x.bit_count() for x in adj) >= 2
    return branches,adj


def reachability_witness(adj):
    all_vertices = (1 << len(adj))-1
    for source in range(len(adj)):
        reached = frontier = 1 << source
        for _ in range(3):
            next_frontier = 0
            while frontier:
                bit = frontier & -frontier
                frontier -= bit
                next_frontier |= adj[bit.bit_length()-1]
            frontier = next_frontier & ~reached
            reached |= frontier
        if reached != all_vertices:
            return True
    return False


def path_witness(adj):
    for u,v in combinations(range(len(adj)),2):
        if adj[u] & (1 << v) or adj[u] & adj[v]:
            continue
        neighbours = adj[u]
        while neighbours:
            bit = neighbours & -neighbours
            neighbours -= bit
            if adj[bit.bit_length()-1] & adj[v]:
                break
        else:
            return True
    return False


def main():
    raw = gzip.decompress((HERE/'tetracyclic-n14-candidates.txt.gz').read_bytes())
    by_branches = Counter()
    for line in raw.decode('ascii').splitlines():
        branches,adj = expand(line)
        assert reachability_witness(adj) and path_witness(adj), line
        by_branches[branches] += 1
    assert sum(by_branches.values()) == 109249
    print(json.dumps({'candidate_sha256':hashlib.sha256(raw).hexdigest(),
                      'checked':sum(by_branches.values()),
                      'counts_by_branch_vertices':dict(sorted(by_branches.items())),
                      'all_diameter_at_least_four':True},indent=2))


if __name__ == '__main__':
    main()
