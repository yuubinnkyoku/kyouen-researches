# Exact residual-isomorphism snapshot audit

Date: 2026-10-05

**11x11 empty root remains UNKNOWN.**

The sound gated canonicalizer in `scripts/residual_iso.py` was applied to all
826 saved n11 late snapshots.  The key covers the complete minimal residual
clutter (rank 2--4); no pair-graph approximation is used.

## Result

All **826/826** snapshots were below the 200,000-permutation safety gate.
They collapsed to **460 exact residual-isomorphism classes**.  There were
**32 duplicate classes containing 398 states**.  Every one of those duplicate
classes crossed more than one ordinary board-D4 occupancy class, so these are
genuine identifications unavailable to the current board-D4 key.

The effect is sharply concentrated at the end of the game:

| minimum legal moves | snapshots | exact iso classes | saved keys | duplicate groups |
|---:|---:|---:|---:|---:|
| 1 | 826 | 460 | 366 | 32 |
| 2 | 696 | 459 | 237 | 31 |
| 3 | 604 | 457 | 147 | 29 |
| 4 | 538 | 453 | 85 | 25 |
| 5 | 471 | 439 | 32 | 16 |
| 6 | 417 | 413 | 4 | 4 |
| 8 | 323 | 323 | **0** | **0** |
| 10 | 250 | 250 | 0 | 0 |
| 12 | 186 | 186 | 0 | 0 |
| 14 | 133 | 133 | 0 | 0 |

Thus the experiment rejects the naive design “canonicalize every exact node”.
In this saved sample there is no cross-snapshot reuse at all once legal>=8,
while residual construction and canonical labelling would still be charged.

## Integration decision

Do **not** replace the production D4 TT key globally.

If residual-isomorphism memoization is benchmarked in the C++ exact solver,
gate it to a very late frontier (initial candidate: legal<=6).  The ordinary
D4 key remains authoritative above the gate and is the fallback whenever exact
canonical labelling exceeds its work bound.

This is a useful reduction, but the current evidence says it is a
**late-endgame micro-kernel**, not the missing large s5 compression.  The
larger target remains K0344-style residual class quotienting / cheaper state
representation, whose node reduction was already demonstrated independently.

## Limitation

These 826 positions come from saved greedy trajectories, not from all TT nodes
of the 23 cold s5 exact searches.  Deduplicating this corpus is therefore not a
wall-time benchmark and must not be reported as a 44% solver speedup.
