# Declaration: n11 class-20421 k05 adoption reaudit flip-census/refresh (single-owner, publish-then-execute)

Single-owner declaration by the long-term 11x11 lane. Published BEFORE
the SCEN refresh runs of this Part. Any parallel lane must not measure
this adoption's flip-census until this Part's completion log appears.

## Scope

WIN-side flip-census review of the class-20421 k05 canonical adoption
(declaration `cf6a21a6`, completion `50037820`; new head of record
`e1a9cacc...` 6,905 rows WIN 223 / LOSS 6,682): BASE = the nineteenth
k04 head of record `8cc87263...` (6,904 rows WIN 222 / LOSS 6,682;
BASE-side census unknown 34,354 / excluded_now 166 / free_now 39 /
excluded 390, from the published nineteenth k04 reaudit refresh
outputs `d4b8099b`), SCEN = the class-20421 k05 head of record
`e1a9cacc...`. Declaration HEAD pin:
`500378209fc067eb609f1803868bc8c65136b2e2` (k05 canonical adoption
completion log; this lane).

## Pre-registered prediction (with caveat)

- Adopted row: k05 `1152921642046849024:68719477248` (serving class
  20421, s5_index 625899, legal 78, WIN(1) nodes 2,007,513; increment
  `6b525957...`). Owner class union derived from the frozen graph via
  `idx in s4_cost[ci]` (s5_index 625899): **[18683, 18710, 20421]**
  (3 owner classes; matches the adoption kit's owner-union precheck).
- Pre-declaration precheck (published BASE bytes only, this host,
  replicating the refresh's own status logic): at BASE, classes
  18683 / 18710 are `unknown` (unknown_now 59 / 97, no win-hit) and
  the serving class 20421 is ALREADY `excluded_now` (unknown_now 1 =
  exactly k05; win-hit by the previously adopted rows of the chain).
- Predicted: exactly the TWO non-pre-excluded owner classes 18683,
  18710 flip unknown -> excluded_now; the serving class 20421 stays
  excluded_now and EXITS the closure ladder (unknown_now 1 -> 0;
  ladder rows predicted 798 -> 798-1 = 797 with left [20421]; rank
  churn measured). Naive census unknown 34,354 -> 34,352 /
  excluded_now 166 -> 168 / free_now 39.
- The adopted s5 index 625899 sits INSIDE the frozen update8 baseline
  requirement (predicted resolved 290 -> 291, remaining_now 31,332
  unchanged, groups_free_now 131); 18683/18710 are predicted NOT
  update8 win-hit plan group classes (20421 is, on both sides,
  untouched by this adoption's group entries).
- **Caveat (standing, materialised in prior adoption reaudits)**: an
  owner class may hold further unknown children and merely decrement,
  or shared-owner pre-exclusion may suppress a flip; the measured
  census replaces this prediction. The ladder EXIT is expected but is
  a MEASURED quantity of this Part, not an assumption.

## Method (fail-closed, template = nineteenth k04 reaudit kit `2041489d`)

- Refresh: 3-region byte-clone of the published nineteenth k04
  reaudit refresh (docstring, CACHE path to the class-20421 k05
  adoption kit head cache, expected cache sha `e1a9cacc...`); 3
  sequential runs must be byte-identical; outputs to the kit
  reaudit/output.
- BASE-side pin reproduction (disclosed standing anchor, reads BASE
  bytes only, executed before this declaration): 1 run of the
  published nineteenth k04 refresh (unchanged bytes, CACHE
  `8cc87263...`) reproduced the published nineteenth k04 reaudit
  outputs byte-for-byte on this host (summary `d4b8099b`, closure
  `877b5f52`, per-root `0fccacec`, BASE worklist regen pin
  `7e3c73d4` / 3,714,150 B, unpublished per size policy).
- Measurer: structural adaptation of the nineteenth k04 measurer
  with expected values pinned from the first measured run; 3 runs
  byte-identical (census json). External tamper battery 4/4
  fail-closed (SCEN-cache verdict flip, BASE closure byte-tamper,
  adoption-manifest byte-tamper, SCEN worklist row deletion - all
  abort before the census json is written) + clean control re-PASS.

## Non-claims / status guard

- NO verdict consumed. Class-status flips and ladder membership are
  census bookkeeping, not class closures and not root verdicts. Even
  with the ladder EXIT measured, the serving class 20421 exit is a
  scheduling/census statement, NOT a class closure claim and NOT a
  root verdict.
- The standard 11x11 empty board, the 19 central-reply roots, the
  two-stone root {60,27} and its remaining third moves 100/108 stay
  UNKNOWN. Nodes are bookkeeping, never verdicts.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.
