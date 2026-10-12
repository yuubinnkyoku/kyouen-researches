#!/usr/bin/env python3
"""Shared S4 classification for the first-player WIN side (K0371 polarity).

Fixed-first-player view, verdicts never flipped across turns (K0371, K0002).
Cache codes: WIN=1, LOSS=2, UNKNOWN/missing=0.

K0371 aggregation table (relevant rows):

| layer | first-player WIN        | first-player LOSS       |
|-------|-------------------------|-------------------------|
| S4 (OR, even)  | >= 1 child is WIN  | all legal children LOSS |
| S5 (AND, odd)  | all legal children WIN | >= 1 child is LOSS   |

Empty legal-child set: even layer LOSS, odd layer WIN.

An S4 (first player to move, stone 5) is therefore already WIN as soon as one
S5 child is cached WIN.  It is LOSS (dead for WIN-side use) when every legal
child is cached LOSS, or when it has no legal child at all.  Otherwise it is
open: optimistically usable iff at least one unknown child later becomes WIN
(whose own closure needs ALL of its S6 children WIN).

This module is the single source of truth for that classification, shared by
win_side.py, win_witness_masks.py, and test_s4_win_polarity.py, so the
polarity cannot drift between implementations again.
"""
from __future__ import annotations

FREE = "free"
OPEN = "open"
DEAD = "dead"

WIN = 1
LOSS = 2
UNKNOWN = 0


def verdict_of(cache: dict, key: tuple[int, int]) -> int:
    """Cache verdict for one child key; missing rows count as UNKNOWN (0)."""
    return cache.get(key, {}).get("verdict", UNKNOWN)


def classify_s4(child_verdicts: list[int]) -> str:
    """Classify one S4 from its legal children's fixed-player verdicts.

    ``child_verdicts`` holds one entry per legal fifth-move child
    (WIN=1, LOSS=2, UNKNOWN=0).  An empty list is the even-layer terminal,
    hence LOSS.
    """
    if not child_verdicts:
        return DEAD
    if WIN in child_verdicts:
        return FREE
    if UNKNOWN in child_verdicts:
        return OPEN
    return DEAD
