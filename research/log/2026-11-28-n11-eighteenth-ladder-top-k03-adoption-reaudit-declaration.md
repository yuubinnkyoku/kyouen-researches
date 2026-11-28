# Declaration: n11 eighteenth k03 adoption reaudit flip-census/refresh (single-owner, publish-then-execute)

Single-owner declaration by the long-term 11x11 lane. Published BEFORE
the SCEN refresh runs of this Part. Any parallel lane must not measure
this adoption's flip-census until this Part's completion log appears.

## Scope

WIN-side flip-census review of the eighteenth ladder-top k03 canonical
adoption (declaration `7fe49b5e`, completion `86cec4cd`; new head of
record `3abecf8b...` 6,903 rows WIN 221 / LOSS 6,682): BASE = the
seventeenth k02 head of record `e56ca5ca...` (6,902 rows WIN 220 /
LOSS 6,682; BASE-side census unknown 34,360 / excluded_now 160 /
free_now 39 / excluded 390, from the published seventeenth k02 reaudit
refresh outputs `e22be6db`), SCEN = the eighteenth k03 head of record
`3abecf8b...`. Declaration HEAD pin:
`86cec4cd54b21fa77c0bcb6b4d616a18a7469ae3` (completion log: n11
eighteenth k03 canonical adoption).

## Pre-registered prediction (with caveat)

- Adopted row: k03 `1155173441859489792:131072` (serving class 20421,
  s5_index 605961, legal 73, WIN(1) nodes 5,266,012; increment
  `c208891e...`). Owner class union derived from the frozen graph via
  `idx in s4_cost[ci]` (s5_index 605961): **[18136, 18143, 20128,
  20421]** (4 owner classes; matches the adoption completion log's
  precheck).
- Pre-declaration precheck (published BASE bytes only, this host):
  at BASE, classes 18136 / 18143 / 20128 are `unknown` (unknown_now
  103 / 102 / 98, no win-hit) and the serving class 20421 is ALREADY
  `excluded_now` (unknown_now 3; k03/k04/k05 still 2M UNKNOWN).
- Predicted: exactly the THREE non-pre-excluded owner classes
  18136, 18143, 20128 flip unknown -> excluded_now; serving class
  20421 stays excluded_now and stays IN the closure ladder with
  unknown_now 3 -> 2 (k04 `1153062242096250880:540672`, k05
  `1152921642046849024:68719476748` remain stage-1 2M UNKNOWN; no
  exit expected). Naive census unknown 34,360 -> 34,357 /
  excluded_now 160 -> 163 / free_now 39. Ladder row count predicted
  798 -> 798.
- The adopted s5 index 605961 sits INSIDE the frozen update8 baseline
  requirement (predicted resolved 288 -> 289, remaining_now 31,332
  unchanged, groups_free_now 131); none of 18136/18143/20128 appears
  among the update8 win-hit plan group classes at BASE (20421 does,
  on both sides, untouched by this adoption).
- **Caveat (standing, materialised in prior adoption reaudits)**: an
  owner class may hold further unknown children and merely decrement,
  or shared-owner pre-exclusion may suppress a flip; the measured
  census replaces this prediction. No ladder-exit claim is made until
  measured.

## Method (fail-closed, template = seventeenth k02 reaudit kit `ef730ced`)

- Refresh: 3-region byte-clone of the published seventeenth k02
  reaudit refresh (docstring, CACHE path to the eighteenth k03
  adoption kit head cache, expected cache sha `3abecf8b...`); 3
  sequential runs must be byte-identical; outputs to the kit
  reaudit/output.
- BASE-side pin reproduction (disclosed standing anchor, reads BASE
  bytes only, executed before this declaration): 1 run of the
  published seventeenth k02 refresh (unchanged bytes, CACHE
  `e56ca5ca...`) reproduced the published seventeenth k02 reaudit
  outputs byte-for-byte on this host (closure `32f0e4f1`, per-root
  `b1aae491`, summary `e22be6db`, BASE worklist regen pin
  `6d3cf3ad` / 3,714,268 B, unpublished per size policy).
- Measurer: structural adaptation of the seventeenth k02 measurer
  with expected values pinned from the first measured run; 3 runs
  byte-identical (census json). External tamper battery 4/4
  fail-closed (SCEN-cache verdict flip, BASE closure byte-tamper,
  adoption-manifest byte-tamper, SCEN worklist row deletion - all
  abort before the census json is written) + clean control re-PASS.

## Non-claims / status guard

- NO verdict consumed. Class-status flips and ladder membership are
  census bookkeeping, not class closures and not root verdicts.
- Class 20421 is NOT complete (k04-k05 remain stage-1 2M UNKNOWN).
- The standard 11x11 empty board, the 19 central-reply roots, the
  two-stone root {60,27} and its remaining third moves 100/108 stay
  UNKNOWN. Nodes are bookkeeping, never verdicts.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.
