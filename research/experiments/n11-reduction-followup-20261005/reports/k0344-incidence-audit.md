# Sequential K0344 kernel incidence audit

Date: 2026-10-05

**11x11 empty root remains UNKNOWN.**

This audit replays the exact `exchangeable_classes` and `class_kernel`
definitions from `scripts/module_core.py` on all 826 saved n11 late
snapshots.  It measures only the immediate/sequential vertex deletion exposed
by K0344; it is not a solver wall-time benchmark.

## Result

- snapshots: **826**
- snapshots with at least one deletion: **253**
- total legal vertices deleted across the corpus: **471**
- maximum deletion in one snapshot: **7**
- one 7-legal snapshot reduced all the way to 0 residual vertices after four
  sequential class reductions.

Deletion histogram:

| deleted vertices | snapshots |
|---:|---:|
| 0 | 573 |
| 1 | 114 |
| 2 | 80 |
| 3 | 45 |
| 4 | 11 |
| 5 | 1 |
| 6 | 1 |
| 7 | 1 |

The effect is again late-heavy, but unlike residual-isomorphism it still has a
few hits above legal=8:

| legal | snapshots | hit | vertices deleted |
|---:|---:|---:|---:|
| 2 | 92 | 92 | 146 |
| 3 | 66 | 46 | 122 |
| 4 | 67 | 45 | 94 |
| 5 | 54 | 26 | 46 |
| 6 | 43 | 17 | 25 |
| 7 | 51 | 12 | 21 |
| 8 | 32 | 3 | 4 |
| 9 | 41 | 7 | 8 |
| 10 | 30 | 0 | 0 |
| 11 | 34 | 2 | 2 |
| 12 | 31 | 3 | 3 |
| 13--18 | 155 | 0 | 0 |

## Interpretation

A production count-vector representation for every exact node is not justified
by this incidence profile alone.  The theorem-backed sequential kernel is
valuable primarily in the deep exact endgame.  The correct implementation
target is therefore a **small-legal residual micro-solver**, where K0344
deletion, component splitting, and (at an even deeper gate) exact residual
isomorphism can be composed before recursion.

This avoids paying residual construction and quotient bookkeeping throughout
the s5 search while preserving the already-measured reductions where they
actually occur.

The existing aggregate memo reduction reported by the K0344 experiment
(17,324 baseline -> 10,477 modules -> 9,341 modules+components) remains the
stronger solver-state evidence.  This audit adds the activation profile needed
to choose a gate; it does not replace that benchmark.
