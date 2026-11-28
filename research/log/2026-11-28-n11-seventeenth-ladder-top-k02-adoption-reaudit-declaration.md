# Declaration: n11 seventeenth k02 adoption reaudit flip-census/refresh (single-owner, publish-then-execute)

Single-owner declaration by the long-term 11x11 lane. Published BEFORE
the SCEN refresh runs of this Part. Any parallel lane must not measure
this adoption's flip-census until this Part's completion log appears.

## Scope

WIN-side flip-census review of the seventeenth ladder-top k02 canonical
adoption (declaration `d9f75b8b`, completion `b015cf6c`): BASE = the
sixteenth k01 head of record `dbc1d950...` (6,901 rows WIN 219 /
LOSS 6,682; BASE-side census unknown 34,363 / excluded_now 157 /
free_now 39 / excluded 390, from the published sixteenth k01 reaudit
refresh outputs `071993c8`), SCEN = the seventeenth k02 head of record
`e56ca5ca...` (6,902 rows WIN 220 / LOSS 6,682). Declaration HEAD
pin: `b015cf6c5e221e3da4f440a150390b60e0f4ffd2` (completion log: n11 seventeenth ladder-top k02 WIN-row canon...).

## Pre-registered prediction (with caveat)

- Owner class union of the adopted key
  `1156299204327378944:131072` (s5_index 543795), derived from the
  frozen graph `54f9c364` via `idx in s4_cost[ci]` in the seventeenth
  escalation Part: **[16104, 16132, 16656, 20421]** (4 owner classes).
- Predicted: the serving class 20421 is ALREADY excluded_now at BASE
  (win-hit by the sixteenth k01 adopted row's chain) and stays IN the
  ladder with unknown_now 4 -> 3 (no exit; k03-k05 remain 2M UNKNOWN).
  The other 3 owner classes (16104, 16132, 16656) are predicted to
  flip unknown -> excluded_now at most; naive census unknown
  34,363 -> 34,360 / excluded_now 157 -> 160 IF all three were unknown
  at BASE and each held no further unknown children. Ladder row count
  predicted 798 -> 798.
- **Caveat (standing, materialised in every prior adoption reaudit)**:
  an owner class may already be excluded_now on the BASE side
  (shared-owner pre-exclusion), or may hold further unknown children
  and merely decrement; the measured census replaces this prediction.
  No ladder-exit claim is made until measured.

## Method (fail-closed, template = sixteenth k01 reaudit kit `3241928c`)

- Refresh: 3-region byte-clone of the published sixteenth k01
  reaudit refresh (docstring, CACHE path, expected cache sha
  `e56ca5ca...`); 3 sequential runs must be byte-identical; outputs
  to the kit reaudit/output.
- BASE-side pin reproduction (disclosed standing anchor, reads BASE
  bytes only, executed before this declaration): 1 run of the
  published sixteenth k01 refresh (unchanged bytes, CACHE
  `dbc1d950...`) reproduced the published sixteenth k01 reaudit
  outputs byte-for-byte on this host (closure `394f27e7`, per-root
  `d154f890`, summary `071993c8`, BASE worklist regen pin
  `0aa54ad7` / 3,714,327 B, unpublished per size policy).
- Measurer: structural adaptation of the sixteenth k01 measurer
  with expected values pinned from the first measured run; 3 runs
  byte-identical (census json). External tamper battery 4/4
  fail-closed (SCEN-cache verdict flip, BASE closure byte-tamper,
  adoption-manifest byte-tamper, SCEN worklist row deletion - all
  abort before the census json is written) + clean control re-PASS.

## Non-claims / status guard

- NO verdict consumed. Class-status flips and ladder membership are
  census bookkeeping, not class closures and not root verdicts.
- Class 20421 is NOT complete (k03-k05 remain stage-1 2M UNKNOWN).
- The standard 11x11 empty board, the 19 central-reply roots, the
  two-stone root {60,27} and its remaining third moves 100/108 stay
  UNKNOWN. Nodes are bookkeeping, never verdicts.
