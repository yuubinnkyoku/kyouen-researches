#!/usr/bin/env python3
"""Closed-form Grundy classification for the t=3, q=7 pure-fiber game.

No base-trace constraints. Safety: sum_b min(c_b, 3) <= 6.

Theorem (full classification). Let w = |B| >= 1, m = |A| >= 2, and let c be
a safe occupancy vector. Write a *position summary* as

    s   = #{b : c_b >= 3}                    (saturated fibers = chains)
    e_i = #{b : c_b == i}  for i = 1, 2      (unsaturated nonzero fibers)
    e_0 = w - #{b : c_b > 0}                 (empty fibers)
    x   = XOR over saturated fibers of (m - c_b) mod 2
    R   = 6 - 3*s - e_1 - 2*e_2              (residual capacity)

Then

    w = 1 :            G(c) = (m - c_1) mod 2
    w >= 2, m odd  :   G(c) = x XOR ( min(R, 3*e_0 + 2*e_1 + e_2) mod 2 )
    w >= 2, m = 2  :   G(c) = min(6 - |S|, 2*w - |S|) mod 2
                       (equivalently min(R, 2*e_0 + e_1) mod 2)
    w >= 2, m even >=4: G(c) = x XOR E(R, min(e_0, R), e_1, e_2)

where E is the universal residual table below (64 states, values 0/1/2).
The m-even table E is the Grundy function of the residual game on
unsaturated fibers with move types 0->1, 1->2, 2->3, in which the 2->3 move
exits to a fresh value-1 chain. Proofs: report.md in this directory.
"""
from __future__ import annotations

T = 3
CAPACITY = 6

# E_TABLE: universal residual game values for m even >= 4 (t=3, q=7).
# key (R, e0, e1, e2), e0 saturated at R (Lemma: E(R,e0,..) = E(R,R,..) for e0 >= R).
# Reachable states satisfy D = R + e1 + 2*e2 in {0, 3, 6}.
E_TABLE = {
    (0, 0, 0, 0): 0,
    (0, 0, 0, 3): 0,
    (0, 0, 1, 1): 0,
    (0, 0, 2, 2): 0,
    (0, 0, 3, 0): 0,
    (0, 0, 4, 1): 0,
    (0, 0, 6, 0): 0,
    (1, 0, 0, 1): 0,
    (1, 0, 1, 2): 2,
    (1, 0, 2, 0): 1,
    (1, 0, 3, 1): 2,
    (1, 0, 5, 0): 1,
    (1, 1, 0, 1): 2,
    (1, 1, 1, 2): 2,
    (1, 1, 2, 0): 1,
    (1, 1, 3, 1): 2,
    (1, 1, 5, 0): 1,
    (2, 0, 0, 2): 0,
    (2, 0, 1, 0): 1,
    (2, 0, 2, 1): 1,
    (2, 0, 4, 0): 0,
    (2, 1, 0, 2): 0,
    (2, 1, 1, 0): 0,
    (2, 1, 2, 1): 1,
    (2, 1, 4, 0): 0,
    (2, 2, 0, 2): 0,
    (2, 2, 1, 0): 0,
    (2, 2, 2, 1): 1,
    (2, 2, 4, 0): 0,
    (3, 0, 0, 0): 0,
    (3, 0, 1, 1): 1,
    (3, 0, 3, 0): 0,
    (3, 1, 0, 0): 0,
    (3, 1, 1, 1): 2,
    (3, 1, 3, 0): 2,
    (3, 2, 0, 0): 1,
    (3, 2, 1, 1): 2,
    (3, 2, 3, 0): 2,
    (3, 3, 0, 0): 1,
    (3, 3, 1, 1): 2,
    (3, 3, 3, 0): 2,
    (4, 0, 0, 1): 0,
    (4, 0, 2, 0): 0,
    (4, 1, 0, 1): 0,
    (4, 1, 2, 0): 1,
    (4, 2, 0, 1): 1,
    (4, 2, 2, 0): 0,
    (4, 3, 0, 1): 1,
    (4, 3, 2, 0): 0,
    (4, 4, 0, 1): 1,
    (4, 4, 2, 0): 0,
    (5, 0, 1, 0): 1,
    (5, 1, 1, 0): 1,
    (5, 2, 1, 0): 0,
    (5, 3, 1, 0): 2,
    (5, 4, 1, 0): 2,
    (5, 5, 1, 0): 2,
    (6, 0, 0, 0): 0,
    (6, 1, 0, 0): 0,
    (6, 2, 0, 0): 0,
    (6, 3, 0, 0): 1,
    (6, 4, 0, 0): 0,
    (6, 5, 0, 0): 0,
    (6, 6, 0, 0): 0,
}


def summary(state: tuple[int, ...], w: int, m: int) -> dict:
    """Position summary from a descending-sorted positive-occupancy multiset."""
    sats = [c for c in state if c >= 3]
    e1 = sum(1 for c in state if c == 1)
    e2 = sum(1 for c in state if c == 2)
    e0 = w - len(state)
    s = len(sats)
    x = 0
    for c in sats:
        x ^= (m - c) % 2
    R = CAPACITY - 3 * s - e1 - 2 * e2
    return {"s": s, "e0": e0, "e1": e1, "e2": e2, "x": x, "R": R,
            "stones": sum(state)}


def formula(state: tuple[int, ...], w: int, m: int) -> int:
    """Closed-form Grundy value. state: descending-sorted positive occupancies."""
    assert all(state[i] >= state[i + 1] for i in range(len(state) - 1))
    assert sum(min(c, T) for c in state) <= CAPACITY
    assert len(state) <= w
    if w == 1:
        c = state[0] if state else 0
        return (m - c) % 2
    if m == 2:
        stones = sum(state)
        return min(CAPACITY - stones, 2 * w - stones) % 2
    d = summary(state, w, m)
    R, e0, e1, e2, x = d["R"], d["e0"], d["e1"], d["e2"], d["x"]
    assert R >= 0 and e0 >= 0
    if m % 2 == 1:
        L = 3 * e0 + 2 * e1 + e2
        return x ^ (min(R, L) % 2)
    key = (R, min(e0, R), e1, e2)
    return x ^ E_TABLE[key]
