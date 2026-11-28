# Declaration: n11 fifteenth k03 adoption reaudit flip-census/refresh (single-owner, publish-then-execute)

Single-owner declaration by the long-term 11x11 lane. Published BEFORE
the SCEN refresh runs of this Part. Any parallel lane must not measure
this adoption's flip-census until this Part's completion log appears.

## Scope

WIN-side flip-census review of the fifteenth ladder-top k03 canonical
adoption (declaration `764ee708`, completion `d8aca523`): BASE = the
fifteenth k01 head of record `b5f322dd...` (6,898 rows WIN 216 /
LOSS 6,682; BASE-side census unknown 34,369 / excluded_now 151 /
free_now 39 / excluded 390, from the published fifteenth k01 reaudit
census deltas `beda7654`), SCEN = the fifteenth k03 head of record
`3a527d39...` (6,899 rows WIN 217 / LOSS 6,682). Declaration HEAD
pin: `d8aca52367128d39d30921027189eb46928d0b6a`.

## Pre-registered prediction (with caveat)

- Owner class union of the adopted key `6053400849139367936:128`
  (s5_index 212536), derived from the frozen graph `54f9c364` via
  `idx in s4_cost[ci]`: **[5803, 5804]** (2 owner classes; distinct
  from k01's [5601, 5804, 8675]).
- Predicted flip: the serving class 5804 is ALREADY excluded_now at
  BASE (measured by the fifteenth k01 reaudit), so at most class
  5803 flips unknown -> excluded_now; naive census unknown
  34,369 -> 34,368 / excluded_now 151 -> 152.
- **Caveat (standing, materialised in the thirteenth/fourteenth/
  fifteenth-k01 adoptions)**: an owner class may already be
  excluded_now on the BASE side (shared-owner pre-exclusion), or may
  hold further unknown children and merely decrement; the measured
  census replaces this prediction. Serving class 5804 holds 1
  remaining unknown child after this adoption (k02 at 15M UNKNOWN),
  so 5804 stays in the closure ladder (unknown_now 2 -> 1, NOT a
  ladder exit). No ladder-exit claim is made here.

## Method

1. Refresh: byte-clone of the published fifteenth k01 reaudit refresh
   (`d3282fe3...`), differing in exactly the three regions
   (docstring, CACHE path to the k03 adoption kit head cache,
   expected cache sha `3a527d39...`); 3 runs byte-identical
   (sequential; memory-heavy).
2. BASE-side pin reproduction: 1 additional run of the published
   fifteenth k01 reaudit refresh (unchanged bytes, CACHE `b5f322dd...`)
   must reproduce the published fifteenth reaudit outputs
   (refresh-summary `cafa9c29`, closure `3f3b7154`,
   per-root `1638c435`) byte-for-byte (and the BASE worklist regen
   pin `0fff5135` unpublished per size policy).
3. Measurer: fresh structural adaptation of the published fifteenth
   k01 measurer (`fd63fcac...`) with expected values pinned from the
   first measured run; 3 runs byte-identical; tamper battery 4
   cases fail-closed + clean control.

## Non-meaning

Measurement bookkeeping only: NO verdict is consumed. Class-status
flips are census bookkeeping, not class closures and not root
verdicts. Class 5804 is NOT complete (k02 stays 15M UNKNOWN;
parking/L50M only under a fresh declaration). The standard 11x11
empty board, all 19 central-reply roots, the two-stone root {60,27}
and its remaining third moves 100/108 stay UNKNOWN. Nodes are
bookkeeping, never verdicts.

## Disclosures

- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.
- The probe-worklist (3.7 MB) stays unpublished per the standing size
  policy; pinned by sha256 only.
