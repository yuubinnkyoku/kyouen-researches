# n11 fifteenth ladder-top k03 adoption reaudit (flip-census/refresh) 2026-11-28

Kit of the WIN-side flip-census/reaudit Part of the fifteenth
class-5804 k03 canonical adoption, declared single-owner
publish-then-execute (declaration commit `08a1163d`, mirrored as
this kit's `DECLARATION.md`), the follow-up Part declared in the
adoption completion log (`d8aca523`).

## What this kit measures

The canonical head of record
`merged-exact-s5-chain-plus-fifteenth-k03-20261128.cache`
(sha256 `3a527d39...`, 6,899 rows WIN 217 / LOSS 6,682, adopted at
`bc535153` + log `d8aca523`) is measured against the BASE head
`b5f322dd...` (6,898 rows WIN 216 / LOSS 6,682, fifteenth k01
head of record, measured by the published fifteenth k01 reaudit
kit: summary `cafa9c29`, closure `3f3b7154`, per-root `1638c435`,
census json `beda7654`, BASE worklist regen pin `0fff5135`
unpublished per size policy).

Adopting solver-trusted S5 labels flips class-status bookkeeping
only: no root verdict is consumed, no root freed, no root excluded,
no coverage claim is made or changed.  The standard 11x11 empty
board and every one of the 19 central-reply roots stay UNKNOWN.

## Results (refresh 3+1 runs byte-identical; measurer 3 runs byte-identical; internal tamper battery 4/4 fail-closed)

- **NO DEVIATION from the naive prediction, which HOLDS EXACTLY**:
  the owner-union classes of the adopted k03 WIN row
  (`6053400849139367936:128`, s5 index 212536) are [5803, 5804],
  and the serving class 5804 is ALREADY excluded_now at BASE (it
  flipped unknown -> excluded_now in the fourteenth Part), so
  exactly ONE class flips unknown -> excluded_now ([5803]); census
  unknown 34,369 -> 34,368, excluded_now 151 -> 152, free_now
  39 -> 39 (Board-verified both sides, rejected {}), excluded
  390 -> 390.  The measured flip list is a strict subset of the
  owner union (the standing shared-owner pre-exclusion caveat
  materialises on the serving class, exactly as pre-declared).
- **Serving class 5804 STAYS in the closure ladder** (799 -> 799
  rows, no enter/leave, rank churn 0 cells): it stays excluded_now
  on both sides while its cost-unknown drops 2 -> 1 (rank 1
  maintained, NOT a ladder exit), exactly the pre-registered
  ladder-stay prediction in the declaration; k02
  (`6052837899185946628:128`) remains its last cost-unknown child
  (15M UNKNOWN).
- update8: the adopted s5 index 212536 sits OUTSIDE the frozen
  baseline requirement (resolved 286 -> 286, remaining_now 31,332
  -> 31,332, groups_free_now 131 -> 131); win-hit group set
  unchanged 35 -> 35 (neither owner class is a plan group class).
- per-root coverage: free_now/uncovered identical on all 20 roots;
  two individual greedy re-routes measured (root 38 2,877 ->
  2,876, root 49 2,691 -> 2,690); joint greedy 43,149 -> 43,148;
  probing worklist 64,260 -> 64,259 rows (SCEN regen pin
  `e165cf36`, 3,714,501 B, unpublished per size policy).  All
  scheduling quantities, not coverage claims.
- Measurer census json: output/census-deltas-fifteenth-k03-adoption.json
  sha256 `a2cb71f6...` (3 runs byte-identical), schema follows the
  fifteenth k01 census json.

## Contents

- `reaudit/scripts/refresh-adoption-fifteenth-k03.py` (also
  mirrored at `scripts/`): byte-clone of the published fifteenth
  k01 adoption-reaudit refresh (script sha `d3282fe3`) differing
  in EXACTLY three regions (docstring, CACHE path, expected cache
  sha `3a527d39`); every computation byte identical.  Three
  sequential runs on this host were byte-identical (stdout
  recorded per run).
- BASE-side pin reproduction: one additional run of the published
  fifteenth k01 reaudit refresh (unchanged bytes, CACHE
  `b5f322dd`) reproduced the published fifteenth k01 reaudit
  outputs (refresh-summary `cafa9c29`, closure `3f3b7154`,
  per-root `1638c435`) byte-for-byte.
- `scripts/measurer-adoption-fifteenth-k03.py`: structural
  descendant of the published fifteenth k01 measurer
  (`fd63fcac`); expected values pre-measured on this host from the
  declared refresh outputs before the final 3-run byte-identical
  gate (u03 precedent).  All sha pins fail-closed; the internal
  tamper battery (verdict flip reverts the flipped owner class
  5803 to unknown while the pre-excluded serving class stays
  excluded_now / row deletion restores the BASE census / row
  append reproduces the SCEN census / tampered caches break the
  sha gate) is 4/4 fail-closed inside every run.
- `reaudit/output/refresh-summary.json`, `closure-classes.csv`,
  `per-root-coverage.csv`: the refreshed measurement of the
  adopted head.  `reaudit/output/probe-worklist.csv` is NOT
  published (3,714,501 B, size policy) and is pinned in the
  MANIFEST.

## Claim status

Flip-census/class-status bookkeeping only: NO verdict consumed, no
class closure, no coverage claim.  Class 5804 completion still
requires k02 (`6052837899185946628:128`, stage-1 15M UNKNOWN,
L50M re-escalation only under a fresh declaration).  The standard
11x11 empty board, all 19 central-reply roots, the two-stone root
{60,27}, the third-move pair {100,108} and every closure class
stay UNKNOWN.  Nodes are bookkeeping, never verdicts.
