# 2026-11-28 n11 fifteenth k01 adoption reaudit (flip-census/refresh) complete

Completion log of the Part declared in
`research/log/2026-11-28-n11-fifteenth-k01-adoption-reaudit-declaration.md`
(declaration commit `04cb8fba`, single owner, publish-then-execute;
all computation ran only after the declaration was on main).

## Results (refresh 3+1 runs byte-identical; measurer 3 runs byte-identical; tamper 4/4 fail-closed)

- **DEVIATION from the declared naive three-owner union flip
  prediction, exactly the pre-declared caveat (shared-owner
  pre-exclusion)**: the adopted k01 WIN row
  `6053682324116078592:0` (s5 index 207094, serving class 5804,
  legal 82, nodes 12,803,283 bookkeeping) has owner classes
  exactly **[5601, 5804, 8675]**, but the serving class 5804 is
  ALREADY excluded_now at BASE (it flipped unknown ->
  excluded_now in the fourteenth Part), so only TWO classes
  flip unknown -> excluded_now: **[5601, 8675]** (the measured
  flip list is a strict subset of the owner union).  Census (BASE
  `a66f636e` 6,897/215/6,682 -> SCEN `b5f322dd` 6,898/216/6,682):
  unknown 34,371 -> 34,369, excluded_now 149 -> 151, free_now
  39 -> 39 (Board-verified both sides, rejected {}), excluded
  390 -> 390.
- **Serving class 5804 STAYS in the closure ladder** (799 -> 799
  rows, entered [], left [], rank churn 0 cells): it stays
  excluded_now on both sides while its cost-unknown drops
  **3 -> 2** (rank 1 maintained, NOT a ladder exit) - exactly the
  pre-registered ladder-stay prediction in the declaration.
- update8: adopted s5 index 207094 sits OUTSIDE the frozen baseline
  requirement (resolved 286 -> 286, remaining_now 31,332,
  groups_free_now 131); win-hit group set unchanged 35 -> 35
  (none of the three owner classes is a plan group class).
- per-root: free_now/uncovered identical on all 20 roots; two
  greedy re-routes (root 38 2,878 -> 2,877, root 49 2,692 ->
  2,691); joint greedy 43,150 -> 43,149; probing worklist
  64,261 -> 64,260 rows (SCEN regen pin `0fff5135`, 3,714,556 B,
  unpublished per size policy).  All scheduling quantities, not
  coverage claims.
- Kit `n11-fifteenth-k01-adoption-reaudit-20261128` (kit commit
  `3395d0ec`, single commit): byte-clone refresh (sha `d3282fe3`,
  3 regions differ from the fourteenth refresh `50b60d64`),
  measurer (`fd63fcac`, structural descendant of `5cd64ecc`,
  pre-measured expectations per the u03 precedent), refresh-summary
  `cafa9c29`, closure-classes `3f3b7154`, per-root `1638c435`,
  census-deltas json `beda7654` (3 runs byte-identical).
  Internal tamper battery 4/4 fail-closed (verdict flip reverts
  the two flipped owner classes to unknown while the pre-excluded
  serving class stays excluded_now / row deletion restores the
  BASE census / row append reproduces the SCEN census / tampered
  caches break the sha gate).
- BASE-side pin reproduction: one additional run of the published
  fourteenth refresh (unchanged bytes, CACHE `a66f636e`)
  reproduced the published fourteenth reaudit outputs
  (refresh-summary `e61ed3df`, closure `8fe6125f`, per-root
  `0549b028`) byte-for-byte.
- Fetch-back: all 10 published kit files byte-identical (raw CDN
  sha256 equal on every file, commit-pinned `3395d0ec`).

## Honest disclosures

- The GitHub App read endpoints (list_commits / get_file_contents)
  intermittently returned 404 for this repository during this
  execution (auth-side flakeness); the pre-push HEAD check could
  not be repeated via the API, but the push itself is
  branch-ref-atomic (main was at the declaration `04cb8fba` when
  last verifiable and the push fast-forwarded cleanly).  All
  verification used commit-pinned raw CDN fetch-backs.
- Wall-clock per refresh run ~59s on this host (3 SCEN runs
  byte-identical + 1 BASE reproduction run); measurer ~8s per
  run, 3 runs byte-identical.
- Measurer structural adaptation beyond value pins: the flip list
  is asserted as a strict subset of the owner union (the
  caveat-materialisation case) with the pre-excluded serving
  class asserted not to flip; the manifest owner_union_precheck
  assertion matches the fifteenth manifest's "none for this key"
  string (the pre-check kit does not exist for this row, the
  union was pre-registered in the declaration instead).
- Dependency pins sha-verified before the computation: graph
  `54f9c364`, update8 `b658290a`, independent.py `954d3a10`,
  policy `78655e94`, quarantine `81d23160`, merger `90711961`,
  BASE cache `a66f636e`, SCEN cache `b5f322dd`, increment
  `e35ffbf6`, adoption manifest `b0a48ccc`.

## Next

- k02 `6052837899185946628:128` / k03 `6053400849139367936:128`
  re-escalation requires FRESH declarations before any run.
- Closure-ladder selection: rank 1 = class 5804 (unknown_now 2
  after this Part, k02/k03 at stage-1 2M UNKNOWN).

## Claim status

Flip-census/class-status bookkeeping only: NO verdict consumed, no
class closure, no coverage claim.  Class 5804 completion still
requires k02/k03 (stage-1 2M UNKNOWN) and Board-verified free_now
at adoption time.  The standard 11x11 empty board, all 19
central-reply roots, the two-stone root {60,27}, the third-move
pair {100,108} and every closure class stay UNKNOWN.  Nodes are
bookkeeping, never verdicts.
(declaration `04cb8fba`, kit `3395d0ec`)
