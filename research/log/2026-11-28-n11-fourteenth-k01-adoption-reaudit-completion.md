# 2026-11-28 n11 fourteenth k01 adoption reaudit (flip-census/refresh) complete

Completion log of the Part declared in
`research/log/2026-11-28-n11-fourteenth-k01-adoption-reaudit-declaration.md`
(declaration commit `3686a5c0`, single owner, publish-then-execute;
all computation ran only after the declaration was on main).

## Results (refresh 3+1 runs byte-identical; measurer 3 runs byte-identical; tamper 4/4 fail-closed)

- **ZERO DEVIATION** from the declared naive three-owner union flip
  prediction: the adopted k01 WIN row `6053401124017274880:0`
  (s5 index 198576, serving class 5804, legal 86, nodes 4,360,661
  bookkeeping) has owner classes exactly **[5308, 5804, 8811]** and
  ALL THREE flip unknown -> excluded_now.  Census (BASE
  `d772f73c` 6,896/214/6,682 -> SCEN `a66f636e` 6,897/215/6,682):
  unknown 34,374 -> 34,371, excluded_now 146 -> 149, free_now
  39 -> 39 (Board-verified both sides, rejected {}), excluded
  390 -> 390.  The declaration's pre-exclusion caveat did NOT
  materialise (u04-style zero-deviation case).
- **Serving class 5804 STAYS in the closure ladder** (799 -> 799
  rows, entered [], left []): unlike the thirteenth Part it is NOT
  pre-excluded at BASE (the rank-1 ladder row) and flips itself
  unknown -> excluded_now while its cost-unknown drops **4 -> 3**
  (NOT a ladder exit) - exactly the pre-registered owner-union
  precheck prediction (`509afbdb`).
- **First adoption Part with a non-serving ladder-row owner
  churning**: owner 8811 is itself a ladder row (rank 17 -> 11,
  unknown_now 52 -> 51); owner 5308 sits outside the ladder; rank
  churn 7 cells.
- update8: adopted s5 index 198576 sits OUTSIDE the frozen baseline
  requirement (resolved 286 -> 286, remaining_now 31,332,
  groups_free_now 131); win-hit group set unchanged 35 -> 35
  (none of the three owner classes is a plan group class).
- per-root: free_now/uncovered identical on all 20 roots; two
  greedy re-routes (root 49 2,693 -> 2,692, root 38 2,879 ->
  2,878); joint greedy 43,151 -> 43,150; probing worklist
  64,263 -> 64,261 rows (SCEN regen pin `082a8b59`, 3,714,609 B,
  unpublished per size policy).  All scheduling quantities, not
  coverage claims.
- Kit `n11-fourteenth-k01-adoption-reaudit-20261128`
  (part 1 `061b8880`, part 2 `259f5fce`): byte-clone refresh
  (sha `50b60d64`, 3 regions differ from the thirteenth refresh
  `c24e9072`), measurer (`5cd64ecc`, structural descendant of
  `d5263fc7`, pre-measured expectations per the u03 precedent),
  refresh-summary `e61ed3df`, closure-classes `8fe6125f`,
  per-root `0549b028`, census-deltas json `dd577da1`
  (3 runs byte-identical).  Internal tamper battery 4/4 fail-closed
  (verdict flip reverts all three owner classes to unknown / row
  deletion restores the BASE census / row append reproduces the
  SCEN census / tampered caches break the sha gate).
- Fetch-back: all 10 published kit files byte-identical (git blob
  sha equal on every file).

## Honest disclosures

- A bash-call boundary file-loss incident removed the local
  reaudit directory between executions (the known recurring
  failure mode); caught by pinned-sha re-verification, the
  refresh script was rebuilt from the verified mold, and a 4th
  refresh run reproduced all four outputs byte-identically
  before the measurer ran.
- Wall-clock per refresh run not recorded on this host (no
  /usr/bin/time); order-of-a-minute per run, consistent with the
  published thirteenth/u04 runs.
- Measurer structural adaptation beyond value pins: the
  closure-churn loop iterates sorted class indices (deterministic
  churn list order); the manifest xhost absence assertion (no
  cross-host replication kit exists for this row yet, disclosed
  in the adoption completion log).
- Dependency pins sha-verified before the computation: graph
  `54f9c364`, update8 `b658290a`, independent.py `954d3a10`,
  policy `78655e94`, quarantine `81d23160`, merger `90711961`,
  BASE cache `d772f73c`, SCEN cache `a66f636e`, increment
  `c87d9afb`, adoption manifest `845031dd`.

## Claim status

Flip-census/class-status bookkeeping only: NO verdict consumed, no
class closure, no coverage claim.  Class 5804 completion still
requires k02/k03/k04 (stage-1 2M UNKNOWN) and Board-verified
free_now at adoption time.  The standard 11x11 empty board, all 19
central-reply roots, the two-stone root {60,27}, the third-move
pair {100,108} and every closure class stay UNKNOWN.  Nodes are
bookkeeping, never verdicts.
(declaration `3686a5c0`, kit `061b8880` + `259f5fce`)
