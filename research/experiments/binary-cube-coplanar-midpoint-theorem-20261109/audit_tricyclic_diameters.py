#!/usr/bin/env python3
"""Audit 12-vertex tricyclic core diameters and 13-to-12 reductions."""
from collections import Counter
import json
import enumerate_tricyclic_cores as core
from audit_bicyclic_diameters import diameter


def edges_of(adj):
    return {(u,v) for u in range(len(adj)) for v in range(u+1,len(adj)) if adj[u] & (1 << v)}


def valid_lengths(edges, lengths):
    if any(l < (3 if u == v else 1) for (u,v),l in zip(edges,lengths)):
        return False
    return all(sum(e == edge and length == 1 for e,length in zip(edges,lengths)) <= 1
               for edge in set(edges))


def main():
    distributions = Counter()
    n12 = n13 = core_count = 0
    max_minimum = 0
    for branches in range(1,5):
        for edges in core.cores(branches):
            core_count += 1
            loops = sum(u==v for u,v in edges)
            distinct_pairs = len({(u,v) for u,v in edges if u != v})
            minimum = 2*len(edges) + loops - distinct_pairs
            max_minimum = max(max_minimum, minimum)
            assert minimum <= 12
            for lengths in core.length_assignments(edges,14):
                adj = core.expand(branches,edges,lengths)
                assert len(adj) == 12 and sum(x.bit_count() for x in adj) == 28
                value = diameter(12,edges_of(adj))
                assert value >= 4, (branches,edges,lengths,value)
                distributions[value] += 1
                n12 += 1
            for lengths in core.length_assignments(edges,15):
                assert any(valid_lengths(edges,lengths[:i]+(lengths[i]-1,)+lengths[i+1:])
                           for i in range(len(lengths)))
                n13 += 1
    assert core_count == 63 and n12 == 18334
    print(json.dumps({'labelled_cores':core_count,'maximum_minimum_edge_sum':max_minimum,
                      'n12_assignments':n12,'n12_diameter_counts':dict(sorted(distributions.items())),
                      'n13_assignments_with_valid_reduction':n13},indent=2))


if __name__ == '__main__':
    main()
