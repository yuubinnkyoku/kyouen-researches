"""Shared cap-game machinery: secant-line tables, upper-set enumeration,
bottom-up Grundy DP and its local mex certificate.

Plane conventions come from pg.py (the 'field_one' reading, which is the one
that reproduces the board -- see t1_board.py).
"""

from __future__ import annotations

from collections import Counter

import pg

_PLANE = pg.Plane(pg.point_vectors("field_one"))
FULL = _PLANE.FULL


def plane() -> pg.Plane:
    return _PLANE


def mask_of(pts) -> int:
    m = 0
    for p in pts:
        m |= 1 << p
    return m


# LM[i][j] = point mask of the line through i and j
LM: list[list[int]] = [[0] * 91 for _ in range(91)]
for _a in range(91):
    for _b in range(91):
        if _a != _b:
            LM[_a][_b] = _PLANE.line_masks[_PLANE.pair_line[_a][_b]]


def analyze_cap(pts, want_topdown: bool = False) -> dict:
    """Enumerate the full upper set of the cap `pts` and its Grundy values.

    Returns g(root), the upper-set size profile, terminal counts and a flag
    saying whether the computed labelling satisfies the local mex recursion
    on every state (which certifies it is the Grundy function).
    """
    root = mask_of(pts)
    blocked = {root: _PLANE.secant_mask(pts)}
    edges: dict[int, list[int]] = {}
    stack = [root]
    while stack:
        s = stack.pop()
        bl_s = blocked[s]
        cand = FULL & ~bl_s & ~s
        ch = []
        members = pg.bitlist(s)
        while cand:
            low = cand & -cand
            p = low.bit_length() - 1
            cand ^= low
            t = s | low
            bl = bl_s
            for q in members:
                bl |= LM[p][q]
            ch.append(t)
            if t not in blocked:
                blocked[t] = bl
                stack.append(t)
        edges[s] = ch
    states = set(blocked)
    assert all(t in states for s in states for t in edges[s])

    val: dict[int, int] = {}
    for s in sorted(states, key=lambda m: -m.bit_count()):
        vs = {val[t] for t in edges[s]}
        if not vs:
            val[s] = 0
        else:
            m = 0
            while m in vs:
                m += 1
            val[s] = m

    cert = True
    for s in states:
        vs = {val[t] for t in edges[s]}
        m = 0
        while m in vs:
            m += 1
        cert &= (val[s] == m)

    if want_topdown:
        memo: dict[int, int] = {}

        def rec(s):
            if s in memo:
                return memo[s]
            vs = [rec(t) for t in edges[s]]
            seen = set(vs)
            m = 0
            while m in seen:
                m += 1
            memo[s] = m
            return m

        rec(root)
        assert memo == val, "top-down and bottom-up disagree"

    sizes = Counter(m.bit_count() for m in states)
    term_sizes = Counter(m.bit_count() for m in states if not edges[m])
    return {
        "g": val[root],
        "states": len(states),
        "sizes": dict(sorted(sizes.items())),
        "strict": len(states) - 1,
        "terminals": dict(sorted(term_sizes.items())),
        "child_vals": dict(sorted(Counter(val[t] for t in edges[root]).items())),
        "cert": cert,
        "root_children": len(edges[root]),
    }
