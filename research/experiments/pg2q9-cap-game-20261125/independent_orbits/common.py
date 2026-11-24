"""common.py -- shared setup for the independent orbit verification.

Holds the four claimed start caps (board labels) and the (model, board, iso)
triple.  Every task script re-derives the isomorphism from scratch; the search
takes a few milliseconds.
"""

from __future__ import annotations

import pgcore as pc

# Start caps, board labels, as given in the claim.
STARTS = {
    6: [4, 9, 20, 32, 69, 84],
    7: [16, 47, 51, 56, 60, 80, 82],
    8: [32, 39, 42, 47, 56, 59, 84, 87],
    10: [6, 9, 27, 32, 34, 37, 45, 75, 77, 82],
}

# Claimed orbit sizes ("family counts") and stabilizer orders.
CLAIM_ORBIT = {6: 707616, 7: 2021760, 8: 5307120, 10: 58968}
CLAIM_STAB = {6: 60, 7: 21, 8: 8, 10: 720}
CLAIM_PGL = 42456960


def setup():
    """(model Plane, board Plane, phi) with phi: board point -> model point."""
    M = pc.build_model()
    B = pc.read_board()
    phi = pc.find_isomorphism(B, M)
    return M, B, phi


def model_cap(phi, cap):
    return sorted(phi[p] for p in cap)


def board_cap(phi, mcap):
    inv = [0] * len(phi)
    for b, m in enumerate(phi):
        inv[m] = b
    return sorted(inv[m] for m in mcap)
