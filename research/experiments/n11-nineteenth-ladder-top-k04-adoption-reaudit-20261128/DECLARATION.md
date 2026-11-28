# Declaration: n11 nineteenth ladder-top k04 adoption reaudit flip-census/refresh (single-owner, publish-then-execute)

Single-owner declaration by the long-term 11x11 lane. Published BEFORE
the SCEN refresh runs of this Part. Any parallel lane must not measure
this adoption's flip-census until this Part's completion log appears.

## Scope

WIN-side flip-census review of the nineteenth ladder-top k04 canonical
adoption (declaration `1043d552`, completion `dacc6445`; new head of
record `8cc87263...` 6,904 rows WIN 222 / LOSS 6,682): BASE = the
eighteenth k03 head of record `3abecf8b...` (6,903 rows WIN 221 /
LOSS 6,682; BASE-side census unknown 34,357 / excluded_now 163 /
free_now 39 / excluded 390, from the published eighteenth k03 reaudit
refresh outputs `23561801`), SCEN = the nineteenth k04 head of record
`8cc87263...`. Declaration HEAD pin:
`2205ec6579e6c2c2d7264132eaf5c15dbc6ba034` (completion log + K1371:
min-double-blocking q7 SAT / orbit classification; unrelated lane).

## Pre-registered prediction (with caveat)

- Adopted row: k04 `1153062242096250880:540672` (serving class 20421,
  s5_index 620742, legal 83, WIN(1) nodes 6,877,739; increment
  `7cc20141...`). Owner class union derived from the frozen graph via
  `idx in s4_cost[ci]` (s5_index 620742): **[18534, 18554, 19885,
  20421]** (4 owner classes; matches the adoption completion log's
  precheck).
- Pre-declaration precheck (published BASE bytes only, this host):
  at BASE, classes 18534 / 18554 / 19885 are `unknown` (unknown_now
  104 / 112 / 108, no win-hit) and the serving class 20421 is ALREADY
  `excluded_now` (unknown_now 2; k05 still 2M UNKNOWN).
- Predicted: exactly the THREE non-pre-excluded owner classes
  18534, 18554, 19885 flip unknown -> excluded_now; serving class
  20421 stays excluded_now and stays IN the closure ladder with
  unknown_now 2 -> 1 (k05 `1152921642046849024:68719477248` remains
  stage-1 2M UNKNOWN; no exit expected). Naive census unknown 34,357
  -> 34,354 / excluded_now 163 -> 166 / free_now 39. Ladder row count
  predicted 798 -> 798.
- The adopted s5 index 620742 sits INSIDE the frozen update8 baseline
  requirement (predicted resolved 289 -> 290, remaining_now 31,332
  unchanged, groups_free_now 131); none of 18534/18554/19885 appears
  among the update8 win-hit plan group classes at BASE (20421 does,
  on both sides, untouched by this adoption).
- **Caveat (standing, materialised in prior adoption reaudits)**: an
  owner class may hold further unknown children and merely decrement,
  or shared-owner pre-exclusion may suppress a flip; the measured
  census replaces this prediction. No ladder-exit claim is made until
  measured.

## Method (fail-closed, template = eighteenth k03 reaudit kit `6ee6e212`)

- Refresh: 3-region byte-clone of the published eighteenth k03
  reaudit refresh (docstring, CACHE path to the nineteenth k04
  adoption kit head cache, expected cache sha `8cc87263...`); 3
  sequential runs must be byte-identical; outputs to the kit
  reaudit/output.
- BASE-side pin reproduction (disclosed standing anchor, reads BASE
  bytes only, executed before this declaration): 1 run of the
  published eighteenth k03 refresh (unchanged bytes, CACHE
  `3abecf8b...`) reproduced the published eighteenth k03 reaudit
  outputs byte-for-byte on this host (summary `23561801`, closure
  `77521463`, per-root `340e5a9c`, BASE worklist regen pin
  `115e3c60` / 3,714,209 B, unpublished per size policy).
- Measurer: structural adaptation of the eighteenth k03 measurer
  with expected values pinned from the first measured run; 3 runs
  byte-identical (census json). External tamper battery 4/4
  fail-closed (SCEN-cache verdict flip, BASE closure byte-tamper,
  adoption-manifest byte-tamper, SCEN worklist row deletion - all
  abort before the census json is written) + clean control re-PASS.

## Non-claims / status guard

- NO verdict consumed. Class-status flips and ladder membership are
  census bookkeeping, not class closures and not root verdicts.
- Class 20421 is NOT complete (k05 remains stage-1 2M UNKNOWN).
- The standard 11x11 empty board, the 19 central-reply roots, the
  two-stone root {60,27} and its remaining third moves 100/108 stay
  UNKNOWN. Nodes are bookkeeping, never verdicts.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.
