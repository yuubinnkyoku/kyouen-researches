# Declaration: n11 twentieth ladder-top k01 adoption reaudit flip-census/refresh (single-owner, publish-then-execute)

Single-owner declaration by the long-term 11x11 lane. Published BEFORE
the SCEN refresh runs of this Part. Any parallel lane must not measure
this adoption's flip-census until this Part's completion log appears.

## Scope

WIN-side flip-census review of the twentieth ladder-top k01 canonical
adoption (declaration `35f902c6`, completion `6292a823`; new head of
record `1f1430f3...` 6,906 rows WIN 224 / LOSS 6,682): BASE = the
class-20421 k05 head of record `e1a9cacc...` (6,905 rows WIN 223 /
LOSS 6,682; BASE-side census unknown 34,352 / excluded_now 168 /
free_now 39 / excluded 390, from the published class20421 k05 reaudit
refresh outputs `dae1f1b3`), SCEN = the twentieth ladder-top k01 head
of record `1f1430f3...`. Declaration HEAD pin:
`6292a8239831af0f7697735a61b6aeb2592c5c81` (twentieth k01 adoption
completion log; this lane).

## Pre-registered prediction (with caveat)

- Adopted row: k01 `10376293541479448576:68719476736` (serving class
  34269, s5_index 38891, legal 87, WIN(1) nodes 10,752,246; increment
  `57c5314a...`). Owner class union derived from the frozen graph via
  `idx in s4_cost[ci]` (s5_index 38891): **[769, 34269]** (2 owner
  classes; matches the adoption kit's owner-union precheck).
- Pre-declaration precheck (published BASE bytes only, this host,
  replicating the refresh's own status logic): at BASE, BOTH owner
  classes are `unknown` with NO win-hit (class 769: unknown_now 104;
  the serving class 34269: unknown_now 11, ladder rank 1 with 4 served
  groups).
- Predicted: exactly the TWO owner classes [769, 34269] flip unknown ->
  excluded_now (unlike the k05 adoption, the serving class 34269 is
  NOT pre-excluded at BASE: it becomes win-hit by its own adopted
  child). Naive census unknown 34,352 -> 34,350 / excluded_now
  168 -> 170 / free_now 39 / excluded 390.
- The serving class 34269 STAYS in the closure ladder (unknown_now
  11 -> 10 != 0; ladder rows predicted 797 -> 797, entered [], left
  []; rank churn measured; NO ladder EXIT). Owner class 769 is NOT in
  the ladder at BASE and is not predicted to enter (its 103 remaining
  unknowns keep it out of the cheapest-option ranking; re-routes
  measured).
- Probing worklist naive 64,251 -> 64,250 (the adopted key's own
  worklist row leaves; greedy re-route churn measured, NOT coverage
  claims). Joint greedy 43,184 measured both sides.
- The adopted s5 index 38891 sits INSIDE the frozen update8 baseline
  requirement (predicted resolved 291 -> 292, remaining_now
  31,332 -> 31,331, groups_free_now 131); win-hit group set predicted
  unchanged 35 -> 35 (neither 769 nor 34269 appears among the 35
  BASE win-hit plan group classes; measured).
- **Caveat (standing, materialised in prior adoption reaudits)**: an
  owner class may hold further unknown children and merely decrement,
  or shared-owner pre-exclusion may suppress a flip; greedy re-routes
  may churn per-root and joint quantities; the measured census replaces
  this prediction. The ladder STAY is expected but is a MEASURED
  quantity of this Part, not an assumption.

## Method (fail-closed, template = class20421 k05 reaudit kit `868d8b39`)

- Refresh: 3-region byte-clone of the published class20421 k05
  reaudit refresh (docstring, CACHE path to the twentieth k01
  adoption kit head cache, expected cache sha `1f1430f3...`); 3
  sequential runs must be byte-identical; outputs to the kit
  reaudit/output.
- BASE-side pin reproduction (disclosed standing anchor, reads BASE
  bytes only, executed before this declaration): 1 run of the
  published class20421 k05 refresh (unchanged bytes, CACHE
  `e1a9cacc...`) reproduced the published class20421 k05 reaudit
  outputs byte-for-byte on this host (summary `dae1f1b3`, closure
  `a33f0cb9`, per-root `ecfe4a0c`, SCEN worklist regen pin
  `09865553` / 3,714,021 B, unpublished per size policy).
- Measurer: structural adaptation of the class20421 k05 measurer
  with expected values pinned from the first measured run; 3 runs
  byte-identical (census json). External tamper battery 4/4
  fail-closed (SCEN-cache verdict flip, BASE closure byte-tamper,
  adoption-manifest byte-tamper, SCEN worklist row deletion - all
  abort before the census json is written) + clean control re-PASS.

## Non-claims / status guard

- NO verdict consumed. Class-status flips and ladder membership are
  census bookkeeping, not class closures and not root verdicts. Even
  with the ladder STAY measured, the serving class 34269 exit/stay is
  a scheduling/census statement, NOT a class closure claim and NOT a
  root verdict.
- The standard 11x11 empty board, the 19 central-reply roots, the
  two-stone root {60,27} and its remaining third moves 100/108 stay
  UNKNOWN. Nodes are bookkeeping, never verdicts.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.
