# n11 thirteenth k01+k02 adoption reaudit (flip-census/refresh) 2026-11-28

Kit of the WIN-side flip-census/reaudit Part of the thirteenth
class-16757 k01+k02 canonical adoption, declared single-owner
publish-then-execute (declaration commit `0bb54826`, also mirrored
as this kit's `DECLARATION.md`), the follow-up Part declared in the
adoption completion log (`35a00c2e`).

## What this kit measures

The canonical head of record
`merged-exact-s5-chain-plus-thirteenth-k01k02-20261128.cache`
(sha256 `d772f73c...`, 6,896 rows WIN 214 / LOSS 6,682, adopted at
`35a00c2e` + `c1aa0eee`) is measured against the BASE head
`beecb024...` (6,894 rows WIN 212 / LOSS 6,682, ultra-cheap u04
head of record, measured by the published u04 adoption-reaudit kit).

Adopting solver-trusted S5 labels flips class-status bookkeeping
only: no root verdict is consumed, no root freed, no root excluded,
no coverage claim is made or changed.  The standard 11x11 empty
board and every one of the 19 central-reply roots stay UNKNOWN.

## Contents

- `reaudit/scripts/refresh-adoption-thirteenth-k01k02.py` (also
  mirrored at `scripts/`): byte-clone of the published ultra-cheap
  u04 adoption-reaudit refresh differing in EXACTLY three regions
  (docstring, CACHE path, expected cache sha); every computation
  byte identical.  Three sequential runs on this host were
  byte-identical (60s/60s/59s; stdout sha256 `38cb8bec...` x3).
- `reaudit/output/refresh-summary.json`: the refreshed measurement
  of the adopted head.  Key numbers: class-status census unknown
  34,374 / excluded_now 146 / free_now 39 / excluded 390;
  Board-verified free 39 (rejected {}); closure ladder 799 classes
  (serving class 16757 departed); joint greedy 43,151; worklist
  64,263 rows.
- `reaudit/output/closure-classes.csv`, `reaudit/output/per-root-coverage.csv`:
  the ladder and per-root coverage of the adopted head.
- `reaudit/output/probe-worklist.csv`: NOT published per size
  policy (3,714,716 B); pinned sha256
  `da2d22e1fd5123283f2921d97e6bd33c4a77d467a41aab65b09118e2292a9dab`.
- `scripts/measurer-adoption-thirteenth-k01k02.py`: structural
  descendant of the published u04 measurer (all fail-closed
  assertions adapted to the MEASURED values of this adoption; the
  pre-exclusion caveat branch asserted).  Two runs byte-identical
  (stdout sha256 `49294f51...` x2), tamper battery 4/4 fail-closed.
- `output/census-deltas-thirteenth-k01k02-adoption.json`: the
  census measurement record (see below).

## MEASURED results (all fail-closed, no assertion violated)

- MEASURED census: BASE unknown 34,376 / excluded_now 144 /
  free_now 39 / excluded 390  ->  SCEN unknown 34,374 /
  excluded_now 146 / free_now 39 / excluded 390.
- MEASURED status flips: exactly TWO classes flip unknown ->
  excluded_now: 16612 (1153204147814662144:0, the k01-only owner)
  and 16740 (1152922672837951488:64, the k02-only owner).
- The declaration's naive FOUR-owner union flip prediction (owner
  union 16612, 16740, 16757, 30542; unknown 34,376 -> 34,372,
  excluded_now 144 -> 148) does NOT hold; the declaration's
  explicitly pre-registered u03-style pre-exclusion caveat
  MATERIALISED: classes 16757 and 30542 were already excluded_now
  on the BASE head (earlier win-hits).  Disclosed in the census
  json's `deviation_from_predeclared_expectation`.
- Serving class 16757 (1153204079095185408:65536): already
  excluded_now at BASE; its last TWO unknown children were exactly
  the two adopted keys (cost-unknown 2 -> 0); it leaves the closure
  ladder 800 -> 799 (all-rank churn, 799 cells, zero unknown_now
  churn, zero entries).
- BOTH adopted s5 indices (k01 556117, k02 558553) sit INSIDE the
  frozen update8 baseline requirement: resolved 284 -> 286,
  remaining_now 31,332 -> 31,332, groups_free_now 131 -> 131, the
  win-hit group set is unchanged (35 -> 35; the serving class
  16757's 5 update8 groups were already win-hit at BASE).
- Per-root greedy re-routes MEASURED: root 48 rises 2,980 -> 3,069,
  root 36 drops 3,029 -> 3,028 (free_now/uncovered identical on all
  20 roots); joint greedy drops 43,830 -> 43,151 and the probing
  worklist row count drops 64,265 -> 64,263 (scheduling quantities,
  not coverage claims).
- Tamper battery 4/4 fail-closed (verdict flip / row delete / row
  append / sha gate).

## Pins verified on this host before measurement

graph `54f9c364...`, update8 `b658290a...`, independent.py
`954d3a10...`, policy `78655e94...`, quarantine `81d23160...`,
BASE cache `beecb024...`, SCEN cache `d772f73c...`, increment
`cebd8dc9...`, manifest `18433ac0...`, merger `90711961...`,
BASE reaudit kit outputs `d35900b9...`/`ef344748...`/`d3c404e9...`,
BASE worklist regen pin `c38831c1...` (3,714,832 B, from the
published u04 census json), SCEN worklist regen `da2d22e1...`
(3,714,716 B).

11x11 UNKNOWN.  No verdict consumed.  Nodes are bookkeeping.
