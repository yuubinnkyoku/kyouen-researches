# Declaration: n11 sixteenth k01 adoption reaudit flip-census/refresh (single-owner, publish-then-execute)

Single-owner declaration by the long-term 11x11 lane. Published BEFORE
the SCEN refresh runs of this Part. Any parallel lane must not measure
this adoption's flip-census until this Part's completion log appears.

## Scope

WIN-side flip-census review of the sixteenth ladder-top k01 canonical
adoption (declaration `e1618d8b`, completion `d555c1d6`): BASE = the
fifteenth k02 head of record `58110025...` (6,900 rows WIN 218 /
LOSS 6,682; BASE-side census unknown 34,365 / excluded_now 155 /
free_now 39 / excluded 390, from the published fifteenth k02 reaudit
census deltas `b089b269`), SCEN = the sixteenth k01 head of record
`dbc1d950...` (6,901 rows WIN 219 / LOSS 6,682). Declaration HEAD
pin: `d555c1d6c97fba7cfd766ab4345b7c93cf53697d`.

## Pre-registered prediction (with caveat)

- Owner class union of the adopted key
  `1155454779397246976:131072` (s5_index 528689), derived from the
  frozen graph `54f9c364` via `idx in s4_cost[ci]` in the sixteenth
  escalation Part: **[15647, 16901, 20421]** (3 owner classes).
- Predicted: the serving class 20421 is unknown_now at BASE (the
  rank-1 closure ladder row with 5 cost-unknown children; k01 was
  one of them), so 20421 stays IN the ladder with unknown_now 5 -> 4
  (no exit; k02-k05 remain 2M UNKNOWN). The other 2 owner classes
  (15647, 16901) are predicted to flip unknown -> excluded_now at
  most; naive census unknown 34,365 -> 34,363 / excluded_now
  155 -> 157 IF both were unknown at BASE and each held no further
  unknown children. Ladder row count predicted 798 -> 798.
- **Caveat (standing, materialised in every prior adoption reaudit)**:
  an owner class may already be excluded_now on the BASE side
  (shared-owner pre-exclusion), or may hold further unknown children
  and merely decrement; the measured census replaces this
  prediction. No ladder-exit claim is made until measured.

## Method (fail-closed, template = fifteenth k02 reaudit kit `c40b2648`)

- Refresh: 3-region byte-clone of the published fifteenth k02
  reaudit refresh (docstring, CACHE path, expected cache sha
  `dbc1d950...`); 3 sequential runs must be byte-identical; outputs
  to the kit reaudit/output.
- BASE-side pin reproduction (disclosed standing anchor, reads BASE
  bytes only, executed before this declaration): 1 run of the
  published fifteenth k02 refresh (unchanged bytes, CACHE
  `58110025...`) reproduced the published fifteenth k02 reaudit
  outputs byte-for-byte on this host (closure `e10b5765`, per-root
  `f2d5d2a7`, summary `df5e7607`, BASE worklist regen pin
  `a8ebeffc` / 3,714,446 B, unpublished per size policy).
- Measurer: structural adaptation of the fifteenth k02 measurer
  with expected values pinned from the first measured run; 3 runs
  byte-identical (census json). External tamper battery 4/4
  fail-closed (SCEN-cache verdict flip, BASE closure byte-tamper,
  adoption-manifest byte-tamper, SCEN worklist row deletion - all
  abort before the census json is written) + clean control re-PASS.

## Non-claims / status guard

- NO verdict consumed. Class-status flips and ladder membership are
  census bookkeeping, not class closures and not root verdicts.
- Class 20421 is NOT complete (k02-k05 remain stage-1 2M UNKNOWN).
- The standard 11x11 empty board, the 19 central-reply roots, the
  two-stone root {60,27} and its remaining third moves 100/108 stay
  UNKNOWN. Nodes are bookkeeping, never verdicts.
