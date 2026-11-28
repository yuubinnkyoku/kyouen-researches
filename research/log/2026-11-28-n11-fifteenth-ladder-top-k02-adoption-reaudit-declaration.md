# Declaration: n11 fifteenth k02 adoption reaudit flip-census/refresh (single-owner, publish-then-execute)

Single-owner declaration by the long-term 11x11 lane. Published BEFORE
the SCEN refresh runs of this Part. Any parallel lane must not measure
this adoption's flip-census until this Part's completion log appears.

## Scope

WIN-side flip-census review of the fifteenth ladder-top k02 canonical
adoption (declaration `12d43eb9`, completion `3e316cb9`): BASE = the
fifteenth k03 head of record `3a527d39...` (6,899 rows WIN 217 /
LOSS 6,682; BASE-side census unknown 34,368 / excluded_now 152 /
free_now 39 / excluded 390, from the published fifteenth k03 reaudit
census deltas `a2cb71f6`), SCEN = the fifteenth k02 head of record
`58110025...` (6,900 rows WIN 218 / LOSS 6,682). Declaration HEAD
pin: `3e316cb9cbd05405ca72ab1cba27e6b5d6b58e93`.

## Pre-registered prediction (with caveat)

- Owner class union of the adopted key `6052837899185946628:128`
  (s5_index 212115), derived from the frozen graph `54f9c364` via
  `idx in s4_cost[ci]` in the L50M escalation Part:
  **[5788, 5804, 5815, 7678]** (4 owner classes; distinct from k01's
  [5601, 5804, 8675] and k03's [5803, 5804]).
- Predicted: the serving class 5804 is ALREADY excluded_now at BASE
  (measured by the fifteenth k01/k03 reaudits) and k02 is its LAST
  cost-unknown child (unknown_now 1 at BASE), so 5804 is predicted to
  EXIT the closure ladder (799 -> 798 rows, subject to Board-verified
  free_now at audit time). The other 3 owner classes (5788, 5815,
  7678) are predicted to flip unknown -> excluded_now at most; naive
  census unknown 34,368 -> 34,365 / excluded_now 152 -> 155 IF all
  three were unknown at BASE and each held no further unknown
  children.
- **Caveat (standing, materialised in the thirteenth/fourteenth/
  fifteenth-k01/k03 adoptions)**: an owner class may already be
  excluded_now on the BASE side (shared-owner pre-exclusion), or may
  hold further unknown children and merely decrement; the measured
  census replaces this prediction. No ladder-exit claim is made
  until measured.

## Method

1. Refresh: byte-clone of the published fifteenth k03 reaudit refresh
   (`b02869ef...`), differing in exactly the three regions
   (docstring, CACHE path to the k02 adoption kit head cache,
   expected cache sha `58110025...`); 3 runs byte-identical
   (sequential; memory-heavy, ~66s/run).
2. BASE-side pin reproduction (pre-declaration anchor, disclosed):
   1 run of the published fifteenth k03 reaudit refresh (unchanged
   bytes, CACHE `3a527d39...`) must reproduce the published k03
   reaudit outputs (refresh-summary `8e37ad17`, closure `01dd4d85`,
   per-root `fc771d82`) byte-for-byte, plus the BASE worklist regen
   pin `e165cf36` (3,714,501 B, unpublished per size policy).
3. Measurer: fresh structural adaptation of the published k03
   measurer (`4a2680aa...`) with expected values pinned from the
   first measured run; 3 runs byte-identical; tamper battery 4
   cases fail-closed + clean control.

## Non-meaning

Measurement bookkeeping only: NO verdict is consumed. Class-status
flips are census bookkeeping, not class closures and not root
verdicts. A closure-ladder exit measured here is a scheduling
statement, not a claim that any root is decided. The standard 11x11
empty board, all 19 central-reply roots, the two-stone root {60,27}
and its remaining third moves 100/108 stay UNKNOWN. Nodes are
bookkeeping, never verdicts.

## Disclosures

- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.
- The BASE-side pin reproduction run was executed BEFORE this
  declaration was published (as the standing anchor exception,
  disclosed): it reproduces published BASE outputs and reads BASE
  bytes only, measuring nothing new.
- The probe-worklist (3.7 MB) stays unpublished per the standing size
  policy; pinned by sha256 only.
