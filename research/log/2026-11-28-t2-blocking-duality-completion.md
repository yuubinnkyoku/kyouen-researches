# 2026-11-28 t>=2 blocking-duality sweep — completion log (declared 9def0879)

- Declaration: commit `9def08790034abc9f87f02203cfd027a7a3733e8`
  (research/log/2026-11-28-t2-blocking-duality-declaration.md), declared at
  HEAD `775e1a6ffde29796511023b7fd2427649316502b`, single owner,
  publish-then-execute. The t>=2 duality cell was unclaimed at declaration time
  (parallel lanes active on n11 / 8x29 / 7x28 / 6x26 / three-row-q4 cells only).
- Kit: `research/experiments/t2-blocking-duality-20261128/` (49 files).
  K item: K1370. All counts below are complete enumerations (2^n full scans).

## Results (all six boards, both runs byte-identical, complement bijection 0 fail both directions)

| board | s | t | maximal safe | minimal t-fold blocking |
|---|---|---|---|---|
| AG(2,3)  | 2 | 1 | 4:54 | 5:54 |
| PG(2,3)  | 2 | 2 | 4:234 | 9:234 |
| AG(2,4)  | 2 | 2 | 4:120, 6:48 | 10:48, 12:120 |
| PG(2,4)  | 3 | 2 | 7:360, 9:11,480 | 12:11,480, 14:360 |
| AG(2,5)  | 3 | 2 | 9:12,500, 10:28,000, 11:9,000 | 14:9,000, 15:28,000, 16:12,500 |
| PG(2,5)  | 4 | 2 | 13:15,500, 14:372,000, 15:604,500, 16:595,975 | 15:595,975, 16:604,500, 17:372,000, 18:15,500 |

Cross-checks with published values: PG(2,3) s=2 maximal 4:234 = K1300;
PG(2,4) s=3 = K1355; AG(2,4) s=2 size set {4,6} = K1300; AG(2,5) s=3 size set
{9,10,11} = K1357 (counts new); PG(2,5) s=4 both sides new.
Pre-declaration calibration (t=1 boards) exactly reproduced 1,240 / 247 /
10,741 / 36,475 with exact size splits (K1367 / K1356+K1366 / K1366 / K1364).

## Verification (four systems)
1. C enumerator: per-mask independent both-side logic + both-direction
   element-level complement check (0 fail), 2 runs byte-identical per board
   (stdout and dumped lists).
2. Pure-Python verifier: independent GF(q) board reconstruction (GF(4)
   addition = XOR), 2-(v,k,1) design check on both the reconstruction and the
   board file, full re-check of every dumped mask (PG(2,5): 1,587,975 x 2
   masks, ~3 min) by direct definitions, complement bijection, count match —
   all_ok on all six boards.
3. Pure-Python third enumeration (no Gray code, direct definitions):
   exact match on the five boards with n<=25 (AG(2,5) ~15 min).
4. Derived-board rerun: C enumerator on independently constructed,
   differently relabeled boards reproduces identical counts on all boards.

## Operational note (disclosure)
Mid-execution the execution environment was reset (a download timed out and
the sandbox was dropped), losing the first-pass scripts and outputs. All
scripts were re-implemented from the declaration's method description and all
runs were redone from scratch in the rebuilt environment; the published kit
contains only this second-pass (canonical) build. Counts matched the
first-pass values in all cases where both exist; the canonical kit is
self-contained and reproducible via scripts/canon.sh (zig 0.13.0, repo pin).

## Finite observations (no unbounded claims)
- PG(2,q) minimal 2-fold blocking minimum size = 3q for q=3,4,5.
- AG(2,q) t=2 minimum sizes: 10 (q=4), 14 (q=5).
- PG(2,5) s=4 maximal sizes 13..16 are parity-mixed (K1298 suggests G>=2
  exists; Grundy NOT computed here).

## Non-claims
K1365 itself was already proved; this is empirical confirmation at element
level plus new census data, not a new proof. All results are finite complete
enumerations. The standard 11x11 empty board, 19 central-reply roots,
two-stone root {60,27}, third move {100,108}, S2, and all closure classes
remain UNKNOWN at all times; no verdict consumed.
