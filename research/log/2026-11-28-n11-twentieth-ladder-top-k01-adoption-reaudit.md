# 2026-11-28 n11 twentieth ladder-top k01 adoption reaudit COMPLETE

Completion record for the Part declared at commit `2b96c5d9`
(single owner, publish-then-execute). Kit published at commit
`d2d3c398` with raw fetch-back byte-verification 10/10.

## Measured outcome (BASE `e1a9cacc...` -> SCEN `1f1430f3...`)

- **Status flips: exactly [769, 34269] unknown -> excluded_now**
  (the declaration's naive TWO-flip prediction holds exactly).
  Census unknown 34,352 -> 34,350 / excluded_now 168 -> 170 /
  free_now 39 (Board-verified both sides) / excluded 390. Unlike
  the k05 adoption, the serving class 34269 is NOT pre-excluded at
  BASE; it becomes win-hit by its OWN adopted child, so the
  measured flip list EQUALS the owner union [769, 34269].
- **Serving class 34269 STAYS in the closure ladder: 797 -> 797
  rows, entered [], left [], ZERO rank-churn cells** (unknown_now
  11 -> 10, rank 1 -> 1). Owner class 769 sits OUTSIDE the ladder
  on both sides. Ladder stay is census bookkeeping, NOT a class
  closure claim and NOT a root verdict.
- Per-root: free_now/uncovered identical on all 20 roots; two
  greedy re-routes (root 12: 2,931 -> 2,930; root 24: 2,775 ->
  2,774; scheduling churns, NOT coverage claims). Joint greedy
  43,184 -> 43,183. Worklist 64,251 -> 64,250 (SCEN regen pin
  `55778a3f` / 3,713,956 B, unpublished per size policy).
- update8: adopted s5 index 38891 inside the frozen baseline
  requirement (resolved 291 -> 292, groups_free_now 131).
  **ONE DISCLOSED DEVIATION from the declaration's naive
  prediction: the win-hit group set MEASURES 35 -> 40, not 35 ->
  35** - the serving class 34269 IS an update8 plan group class,
  so its own adoption win-hits its 5 plan groups (all 5 added
  groups have s4_class_index 34269, none removed) and drops
  remaining_now 31,332 -> 31,321. The other owner 769 is NOT a
  plan group class. The declaration's standing caveat (measured
  census replaces prediction) covers exactly this case.

## Gates

- BASE-side pin reproduction (before the declaration, reads BASE
  bytes only): 1 run of the published class20421 k05 refresh
  (unchanged bytes, CACHE `e1a9cacc`) reproduced the published k05
  reaudit outputs byte-for-byte (summary `dae1f1b3`, closure
  `a33f0cb9`, per-root `ecfe4a0c`, worklist pin `09865553` /
  3,714,021 B).
- Refresh (3-region byte-clone of the k05 reaudit refresh, CACHE
  `1f1430f3`): 3 sequential runs byte-identical (~70s/run):
  summary `7e69da46`, closure `1a96311e`, per-root `f83a73c5`.
- Measurer (structural adaptation of the k05 measurer, expected
  values pinned from the first measured run): 3 runs
  byte-identical, census json `b7a70814`. External tamper battery
  4/4 fail-closed (MT1 SCEN-cache verdict flip / MT2 BASE closure
  byte-tamper / MT3 adoption-manifest byte-tamper / MT4 SCEN
  worklist row deletion; each aborted at its own sha pin BEFORE
  the census json was written; census sha snapshot unchanged) +
  clean control re-PASS byte-identical.

## Standing interpretation

Adoption reaudit bookkeeping only: NO verdict consumed. The
standard 11x11 empty board, all 19 central-reply roots, the
two-stone root {60,27} and third moves 100/108 stay UNKNOWN.
Nodes are bookkeeping, never verdicts. This lane runs without
access to the user's computer (scheduled task); publication is
via the GitHub API only.

## Next

The twentieth ladder-top k01 WIN row is adopted and its census
measured. Next highest-value step for this lane: the ladder's
serving class 34269 retains rank 1 with unknown_now 10 (k02-k11
of the twentieth escalation remain parked at 2M UNKNOWN), so the
twenty-first ladder-top selection/escalation (or a re-probe of the
parked k02-k11 at higher budget) is the natural continuation.
