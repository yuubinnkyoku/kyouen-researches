#!/usr/bin/env python3
"""Closed-form Grundy classifications for the t=3 pure fiber games, q=4,5,6.

Rule (K0832 conventions): board fibers b in B (w=|B|>=2), height m=|A|>=2.
State = occupancy vector c (0<=c_b<=m). Safety: sum_b min(c_b,3) <= q-1.
Move: increment one c_b by 1, legal iff the child is safe.
Grundy: mex over legal children.

This module holds ONLY the closed forms; the game engines live in
verify_t3_q456.py and are generated independently (multiset and labeled
representations).
"""
from __future__ import annotations


def _even_ge4(m: int) -> bool:
    return m % 2 == 0 and m >= 4


def formula(s: tuple[int, ...], w: int, m: int, q: int) -> int:
    """Closed-form Grundy value of the safe multiset state s (positive parts,
    descending), width w, height m, forbidden size q, t=3."""
    s = tuple(sorted((x for x in s if x), reverse=True))
    total = sum(s)
    if q == 4:  # LIMIT = 3 = t: saturated single chains + tiny combos
        if len(s) == 0:
            return 1
        if len(s) == 1:
            a = s[0]
            if a == 1:
                return 0
            if a == 2:
                return 2 if _even_ge4(m) else 1
            return (m - a) % 2  # a >= 3: pure chain (cap == LIMIT)
        if s == (1, 1):
            return 1
        if s == (2, 1):
            return 0
        if s == (1, 1, 1):
            return 0
        raise AssertionError((q, w, m, s))
    if q == 5:  # LIMIT = 4 = t+1
        if len(s) == 0:
            return 0
        if len(s) == 1:
            a = s[0]
            if a == 1:
                return 2 if _even_ge4(m) else 1
            if a == 2:
                return 1 if _even_ge4(m) else 0
            return (m - a + 1) % 2  # a >= 3: mex{chain child, pair child}
        if len(s) == 2:
            if s == (1, 1):
                return 0
            if s == (2, 1):
                return 2 if _even_ge4(m) else 1
            if s[0] >= 3 and s[1] == 1:
                return (m - s[0]) % 2  # pure chain on the saturated fiber
            if s == (2, 2):
                return 0
            raise AssertionError((q, w, m, s))
        if len(s) == 3:
            if s == (1, 1, 1):
                return 1
            if s == (2, 1, 1):
                return 0
            raise AssertionError((q, w, m, s))
        if len(s) == 4:
            if s == (1, 1, 1, 1):
                return 0
            raise AssertionError((q, w, m, s))
        raise AssertionError((q, w, m, s))
    if q == 6:  # LIMIT = 5 = t+2
        if w == 2:
            # unique terminal type (m,2): fixed length m+2-|S|
            return (m + 2 - total) % 2
        if m == 2:
            # all terminals have exactly 5 stones
            return (5 - total) % 2
        if m % 2 == 1:
            # all terminals odd stone count (m+2 and 5 coincide mod 2)
            return (m + 2 - total) % 2
        # m even >= 4, w >= 3: mixed terminal parity, per-type mex table
        if len(s) == 0:
            return 0
        if len(s) == 1:
            a = s[0]
            if a == 1:
                return 1
            if a == 2:
                return 0
            return (m - a) % 2
        a, b = s[0], s[1]
        if len(s) == 2:
            if s == (1, 1):
                return 2
            if a == 2 and b == 1:
                return 1
            if a >= 3 and b == 1:
                return (m - a + 1) % 2
            if s == (2, 2):
                return 2
            if a >= 3 and b == 2:
                return (m - a) % 2
            raise AssertionError((q, w, m, s))
        if len(s) == 3:
            if s == (1, 1, 1):
                return 0
            if s == (2, 1, 1):
                return 2
            if a >= 3 and s[1:] == (1, 1):
                return (m - a) % 2
            if s == (2, 2, 1):
                return 0
            raise AssertionError((q, w, m, s))
        if len(s) == 4:
            if s == (1, 1, 1, 1):
                return 1
            if s == (2, 1, 1, 1):
                return 0
            raise AssertionError((q, w, m, s))
        if len(s) == 5:
            if s == (1, 1, 1, 1, 1):
                return 0
            raise AssertionError((q, w, m, s))
        raise AssertionError((q, w, m, s))
    raise AssertionError(q)
