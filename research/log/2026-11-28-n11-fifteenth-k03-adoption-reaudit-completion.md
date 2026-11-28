# Completion: n11 fifteenth ladder-top k03 adoption reaudit flip-census/refresh (single-owner)

Completion of the Part declared at `08a1163d` (kit
`n11-fifteenth-ladder-top-k03-adoption-reaudit-20261128`, kit commit
`e6ceb133`, fetch-back 10/10 byte-exact against the commit-pinned
raw CDN). The kit publishes the SCEN refresh outputs, the adapted
measurer and its census json, and mirrors the declaration.

## Measured results (all under the standing rules: nodes are
bookkeeping, no verdict consumed)

- **The naive ONE-flip prediction HOLDS EXACTLY (no deviation)**:
  the adopted k03 WIN row `6053400849139367936:128` (s5 index
  212536, serving class 5804) has owner union **[5803, 5804]** from
  the frozen graph `54f9c364`; the serving class 5804 is already
  excluded_now at BASE (fourteenth Part), so exactly ONE class
  flips unknown -> excluded_now: **[5803]**.  Census unknown
  34,369 -> 34,368, excluded_now 151 -> 152, free_now 39 -> 39
  (Board-verified both sides, rejected {}), excluded 390 -> 390.
  The measured flip list is a strict subset of the owner union,
  the standing shared-owner pre-exclusion caveat materialising on
  the serving class, exactly as pre-declared.
- **Serving class 5804 STAYS in the closure ladder at rank 1**
  (799 -> 799 rows, no enter/leave, rank churn 0 cells), its
  cost-unknown dropping 2 -> 1: NOT a ladder exit.  k02
  (`6052837899185946628:128`) is now the LAST cost-unknown child of
  the rank-1 ladder class (stage-1 15M UNKNOWN; owner union
  [5788, 5804, 5815, 7678] derived from the graph).
- update8: the adopted s5 index 212536 sits OUTSIDE the frozen
  baseline requirement (resolved 286 -> 286, remaining_now 31,332
  -> 31,332, groups_free_now 131 -> 131); win-hit group set
  unchanged 35 -> 35 (neither owner class is a plan group class).
- per-root coverage: free_now/uncovered identical on all 20 roots;
  two individual greedy re-routes (root 38 2,877 -> 2,876, root 49
  2,691 -> 2,690); joint greedy 43,149 -> 43,148; probing worklist
  64,260 -> 64,259 rows (SCEN regen pin `e165cf36`, 3,714,501 B,
  unpublished per size policy).  All scheduling quantities, not
  coverage claims.
- Runs: SCEN refresh 3 sequential runs byte-identical (summary
  `8e37ad17`, closure `01dd4d85`, per-root `fc771d82`, worklist
  `e165cf36`); BASE-side pin reproduction 1 run of the published
  fifteenth k01 refresh (unchanged bytes `d3282fe3`, CACHE
  `b5f322dd`) reproduced the published outputs (`cafa9c29`,
  `3f3b7154`, `1638c435`) byte-for-byte; measurer 3 runs
  byte-identical (census json `a2cb71f6`), internal tamper battery
  4/4 fail-closed + clean control.

## Chain state

Canonical head of record:
`merged-exact-s5-chain-plus-fifteenth-k03-20261128.cache` sha256
`3a527d39db7acec32b4c688e0bbbafea8015d9d4aac778cf51e7e5c37afe6a3a`
(6,899 rows WIN 217 / LOSS 6,682).  Adoption chain: `a66f636e` ->
`b5f322dd` (fifteenth k01) -> `3a527d39` (fifteenth k03).

## Non-meaning

Flip-census/class-status bookkeeping only: NO verdict consumed, no
class closure, no coverage claim.  Class 5804 is NOT complete (k02
stays 15M UNKNOWN; L50M re-escalation or parking only under a fresh
declaration).  The standard 11x11 empty board, all 19 central-reply
roots, the two-stone root {60,27}, the third-move pair {100,108}
and every closure class stay UNKNOWN.  Nodes are bookkeeping, never
verdicts.

## Disclosures

- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.
- The probe-worklist (3.7 MB) stays unpublished per the standing
  size policy; pinned by sha256 only in the kit MANIFEST.
