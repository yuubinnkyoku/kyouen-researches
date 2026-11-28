# n11 fourteenth k01 adoption reaudit (flip-census/refresh) 2026-11-28

Kit of the WIN-side flip-census/reaudit Part of the fourteenth
class-5804 k01 canonical adoption, declared single-owner
publish-then-execute (declaration commit `3686a5c0`, mirrored as
this kit's `DECLARATION.md`), the follow-up Part declared in the
adoption completion log (`e1f8f904`).

## What this kit measures

The canonical head of record
`merged-exact-s5-chain-plus-fourteenth-k01-20261128.cache`
(sha256 `a66f636e...`, 6,897 rows WIN 215 / LOSS 6,682, adopted at
`4f0ba5c9` + fix `0139fd4c`) is measured against the BASE head
`d772f73c...` (6,896 rows WIN 214 / LOSS 6,682, thirteenth k01+k02
head of record, measured by the published thirteenth reaudit kit:
summary `0d02503c`, closure `be8bcff1`, per-root `96cf51b7`,
census json `7b6027d3`, BASE worklist regen pin `da2d22e1`
unpublished per size policy).

Adopting solver-trusted S5 labels flips class-status bookkeeping
only: no root verdict is consumed, no root freed, no root excluded,
no coverage claim is made or changed.  The standard 11x11 empty
board and every one of the 19 central-reply roots stay UNKNOWN.

## Results (refresh 3+1 runs byte-identical; measurer 3 runs byte-identical; internal tamper battery 4/4 fail-closed)

- **ZERO DEVIATION from the declared naive prediction** (the
  u04-style case): the owner-union classes of the adopted k01 WIN
  row (`6053401124017274880:0`, s5 index 198576) are exactly
  [5308, 5804, 8811] and ALL THREE flip unknown -> excluded_now;
  census unknown 34,374 -> 34,371, excluded_now 146 -> 149,
  free_now 39 -> 39 (Board-verified both sides, rejected {}),
  excluded 390 -> 390.
- **Serving class 5804 STAYS in the closure ladder** (799 -> 799
  rows, no enter/leave): unlike the thirteenth Part it is NOT
  pre-excluded at BASE (the rank-1 ladder row); it flips itself
  unknown -> excluded_now while its cost-unknown drops 4 -> 3,
  exactly the pre-registered owner-union precheck prediction
  (`509afbdb`), NOT a ladder exit.
- **First adoption Part with a non-serving ladder-row owner
  churning**: owner 8811 is itself a ladder row and re-ranks
  (rank 17 -> 11, unknown_now 52 -> 51); owner 5308 sits outside
  the ladder on both sides; rank churn 7 cells.
- update8: the adopted s5 index 198576 sits OUTSIDE the frozen
  baseline requirement (resolved 286 -> 286, remaining_now 31,332
  -> 31,332, groups_free_now 131 -> 131); win-hit group set
  unchanged 35 -> 35 (none of the three owner classes is a plan
  group class).
- per-root coverage: free_now/uncovered identical on all 20 roots;
  two individual greedy re-routes measured (root 49 2,693 -> 2,692,
  root 38 2,879 -> 2,878); joint greedy 43,151 -> 43,150; probing
  worklist 64,263 -> 64,261 rows (SCEN regen pin `082a8b59`,
  3,714,609 B, unpublished per size policy).  All scheduling
  quantities, not coverage claims.
- Measurer census json: output/census-deltas-fourteenth-k01-adoption.json
  sha256 `dd577da1...` (3 runs byte-identical), schema follows the
  thirteenth census json.

## Contents

- `reaudit/scripts/refresh-adoption-fourteenth-k01.py` (also
  mirrored at `scripts/`): byte-clone of the published thirteenth
  adoption-reaudit refresh (script sha `c24e9072`) differing in
  EXACTLY three regions (docstring, CACHE path, expected cache sha
  `a66f636e`); every computation byte identical.  Four sequential
  runs on this host were byte-identical (runs 1-3 in the declaring
  execution, plus one post-rebuild reproduction run verified
  against the recorded output shas; stdout sha `2f1c2cb4...` x3).
- `scripts/measurer-adoption-fourteenth-k01.py`: structural
  descendant of the published thirteenth measurer (`d5263fc7`);
  expected values pre-measured on this host from the declared
  refresh outputs before the final 3-run byte-identical gate
  (u03 precedent).  All sha pins fail-closed; the internal tamper
  battery (verdict flip reverts all three owner classes to
  unknown / row deletion restores the BASE census / row append
  reproduces the SCEN census / tampered caches break the sha gate)
  is 4/4 fail-closed inside every run.
- `reaudit/output/refresh-summary.json`, `closure-classes.csv`,
  `per-root-coverage.csv`: the refreshed measurement of the
  adopted head.  `reaudit/output/probe-worklist.csv` is NOT
  published (3,714,609 B, size policy) and is pinned in the
  MANIFEST.

## Honest disclosures

- A bash-call boundary file-loss incident removed the local
  reaudit directory between executions (the known recurring
  failure mode); it was caught by the pinned-sha re-verification,
  the refresh script was rebuilt from the verified mold + pinned
  docstring, and a 4th refresh run reproduced all four outputs
  byte-identically before the measurer ran.  All published
  artifacts come from the post-rebuild, re-verified tree.
- Wall-clock per refresh run was not recorded on this host (no
  /usr/bin/time); each refresh run took on the order of a minute,
  consistent with the published thirteenth/u04 runs.
- Structural adaptation in the measurer beyond value pins: the
  closure-churn loop iterates `sorted(set(bc) & set(sc))` instead
  of the raw set (making the churn list order deterministic);
  the manifest xhost absence assertion (disclosed in the adoption
  completion log: no cross-host replication kit exists for this
  row yet).
- Dependency pins sha-verified on this host before the
  computation: graph `54f9c364`, update8 `b658290a`,
  independent.py `954d3a10`, s5_evidence_policy `78655e94`,
  quarantine `81d23160`, merger `90711961`, BASE cache
  `d772f73c`, SCEN cache `a66f636e`, increment `c87d9afb`,
  adoption manifest `845031dd`.

## Claim status

Flip-census/class-status bookkeeping only: NO verdict consumed, no
class closure, no coverage claim.  Class 5804 completion still
requires k02/k03/k04 (stage-1 2M UNKNOWN, re-escalation only under
future declarations) and Board-verified free_now at adoption time.
The standard 11x11 empty board, all 19 central-reply roots, the
two-stone root {60,27}, the third-move pair {100,108} and every
closure class stay UNKNOWN.  Nodes are bookkeeping, never verdicts.
