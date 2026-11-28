# Declaration: n11 fifteenth k01 adoption reaudit flip-census/refresh (single-owner, publish-then-execute)

Single-owner declaration by the long-term 11x11 lane. Published BEFORE
the SCEN refresh runs of this Part. Any parallel lane must not measure
this adoption's flip-census until this Part's completion log appears.

## Scope

WIN-side flip-census review of the fifteenth ladder-top k01 canonical
adoption (declaration `6ffc8a38`, completion `d2795d25`): BASE = the
fourteenth head of record `a66f636e...` (6,897 rows WIN 215 /
LOSS 6,682; BASE-side census unknown 34,371 / excluded_now 149 /
free_now 39 / excluded 390, from the published fourteenth reaudit
census `dd577da1`), SCEN = the fifteenth head of record `b5f322dd...`
(6,898 rows WIN 216 / LOSS 6,682). Declaration HEAD pin: current
main at push time.

## Pre-registered prediction (with caveat)

- Owner class union of the adopted key `6053682324116078592:0`
  (s5_index 207094), derived from the frozen graph `54f9c364` via
  `idx in s4_cost[ci]`: **[5601, 5804, 8675]** (3 owner classes).
- Predicted flip (if all 3 owner classes have the adopted key as
  their last cost-unknown child): unknown 34,371 -> 34,368 /
  excluded_now 149 -> 152.
- **Caveat (standing, materialised in the thirteenth and fourteenth
  adoptions)**: an owner class may already be excluded_now on the
  BASE side (shared-owner pre-exclusion), or may hold further unknown
  children and merely decrement; the measured census replaces this
  prediction.  Serving class 5804 holds 2 remaining unknown children
  after this adoption (k02/k03 at 2M UNKNOWN), so 5804 is predicted
  to stay in the closure ladder (unknown_now 3 -> 2, NOT a ladder
  exit), pending measurement.  No ladder-exit claim is made here.

## Method

1. Refresh: byte-clone of the published fourteenth reaudit refresh
   (`50b60d64...`), differing in exactly the three regions
   (docstring, CACHE path to the fifteenth adoption kit head cache,
   expected cache sha `b5f322dd...`); 3 runs byte-identical
   (sequential; memory-heavy).
2. BASE-side pin reproduction: 1 additional run of the published
   fourteenth refresh (unchanged bytes, CACHE `a66f636e...`) must
   reproduce the published fourteenth reaudit outputs
   (refresh-summary `e61ed3df`, closure `8fe6125f`,
   per-root `0549b028`) byte-for-byte.
3. Measurer: fresh structural adaptation of the published fourteenth
   measurer (`5cd64ecc...`) with expected values pinned from the
   first measured run; 3 runs byte-identical; tamper battery 4
   cases fail-closed + clean control.

## Non-meaning

Measurement bookkeeping only: NO verdict is consumed. Class-status
flips are census bookkeeping, not class closures and not root
verdicts. Class 5804 is NOT complete (k02/k03 stay 2M UNKNOWN). The
standard 11x11 empty board, all 19 central-reply roots, the two-stone
root {60,27} and its remaining third moves 100/108 stay UNKNOWN.
Nodes are bookkeeping, never verdicts.

## Disclosures

- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.
- The probe-worklist (3.7 MB) stays unpublished per the standing size
  policy; pinned by sha256 only.
