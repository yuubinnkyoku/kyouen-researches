#!/usr/bin/env python3
"""Sound bounded canonical labels for minimal residual clutters.

This is an experiment gate, not a production DFPN key.  It refines the full
rank-2..4 hypergraph incidence structure, then enumerates permutations only
inside unresolved vertex-colour cells.  If that exact enumeration would exceed
max_permutations it returns None: callers MUST fall back to the ordinary D4 key.

Hence a collision returned by this module is an exact residual-game
isomorphism; an expensive case is merely missed, never merged unsafely.
"""
from __future__ import annotations

from collections import defaultdict
from itertools import permutations, product
from math import factorial


def bits(mask: int):
    while mask:
        b = mask & -mask
        yield b.bit_length() - 1
        mask ^= b


def _refine(vertices: tuple[int, ...], edges: tuple[tuple[int, ...], ...]):
    n = len(vertices)
    incidence = [[] for _ in range(n)]
    for ei, edge in enumerate(edges):
        for v in edge:
            incidence[v].append(ei)

    vcolor = [tuple(sum(v in edge for edge in edges if len(edge) == r)
                    for r in (2, 3, 4)) for v in range(n)]
    while True:
        vu = {x: i for i, x in enumerate(sorted(set(vcolor)))}
        vc = [vu[x] for x in vcolor]
        esig = [(len(edge), tuple(sorted(vc[v] for v in edge)))
                for edge in edges]
        eu = {x: i for i, x in enumerate(sorted(set(esig)))}
        ec = [eu[x] for x in esig]
        nsig = [(vc[v], tuple(sorted(ec[ei] for ei in incidence[v])))
                for v in range(n)]
        nu = {x: i for i, x in enumerate(sorted(set(nsig)))}
        nc = [nu[x] for x in nsig]
        if nc == vc:
            return nc
        vcolor = nc


def canonical_label(vertices_mask: int, edge_masks: tuple[int, ...],
                    max_permutations: int = 200_000):
    """Return an exact isomorphism-invariant label, or None when gated out."""
    vertices = tuple(bits(vertices_mask))
    index = {v: i for i, v in enumerate(vertices)}
    edges = tuple(sorted(tuple(sorted(index[v] for v in bits(edge)))
                         for edge in edge_masks))
    colors = _refine(vertices, edges)
    groups = defaultdict(list)
    for v, color in enumerate(colors):
        groups[color].append(v)
    cells = [groups[c] for c in sorted(groups)]

    work = 1
    for cell in cells:
        work *= factorial(len(cell))
        if work > max_permutations:
            return None

    best = None
    for choices in product(*(permutations(cell) for cell in cells)):
        order = tuple(v for choice in choices for v in choice)
        pos = {v: i for i, v in enumerate(order)}
        code = tuple(sorted(tuple(sorted(pos[v] for v in edge))
                            for edge in edges))
        if best is None or code < best:
            best = code
    # Cell sizes are redundant for isomorphism but useful for audit/debugging.
    return (len(vertices), tuple(len(c) for c in cells), best)


def relabel(vertices_mask: int, edge_masks: tuple[int, ...], mapping: dict[int, int]):
    out_vertices = 0
    for v in bits(vertices_mask):
        out_vertices |= 1 << mapping[v]
    out_edges = []
    for edge in edge_masks:
        e = 0
        for v in bits(edge):
            e |= 1 << mapping[v]
        out_edges.append(e)
    return out_vertices, tuple(sorted(out_edges))


def self_test():
    # Rank-3 information must matter: the pair graph alone cannot define a key.
    a = (0b1111, (0b0011, 0b1101))
    b = (0b1111, (0b0011,))
    assert canonical_label(*a) != canonical_label(*b)

    # A non-D4-style arbitrary relabeling must preserve the exact label.
    mapping = {0: 2, 1: 0, 2: 3, 3: 1}
    assert canonical_label(*a) == canonical_label(*relabel(*a, mapping))

    # Gating is conservative: high-symmetry empty clutter is skipped.
    assert canonical_label((1 << 10) - 1, (), max_permutations=1000) is None
    return "VERIFIED"


if __name__ == "__main__":
    print(self_test())
