#!/usr/bin/env python3
"""Recheck 12-vertex tricyclic diameters with independent BFS."""
from collections import Counter, deque
import json
from pathlib import Path
import enumerate_tricyclic_cores as core

HERE = Path(__file__).resolve().parent


def diameter(adj):
    n = len(adj)
    maximum = 0
    for source in range(n):
        distance = [-1]*n
        distance[source] = 0
        queue = deque([source])
        while queue:
            u = queue.popleft()
            for v in range(n):
                if adj[u] & (1 << v) and distance[v] == -1:
                    distance[v] = distance[u]+1
                    queue.append(v)
        assert min(distance) >= 0
        maximum = max(maximum, max(distance))
    return maximum


def main():
    expected = json.loads((HERE/'tricyclic-diameter-audit.json').read_text())
    counts = Counter()
    for b in range(1,5):
        for edges in core.cores(b):
            for lengths in core.length_assignments(edges,14):
                adj = core.expand(b,edges,lengths)
                assert len(adj) == 12
                counts[diameter(adj)] += 1
    assert {str(k):v for k,v in sorted(counts.items())} == expected['n12_diameter_counts']
    assert sum(counts.values()) == 18334 and min(counts) >= 4
    print('PASS: 18334 tricyclic 12-vertex cases agree with independent BFS')


if __name__ == '__main__':
    main()
