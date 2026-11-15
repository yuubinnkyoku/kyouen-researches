# 5x30 q=7 row-deficient maximal nonexistence — class-split sweep report

Date: 2026-11-15 (UTC). Fast lane, successor of K0841 (5x29 witness-free).
Knowledge item: K0842.

## Claim

1. On the 5x30 integer grid (q=7), for each of the 19 row-mirror-canonical
   deficiency classes D ⊆ {0..4} (canonical representatives of the 31
   non-empty subsets under y -> 4-y), the class-split SAT instance — rows in
   D hold at most 5 stones, rows outside D hold exactly 6 (safety caps every
   row at 6 since a row is a line of length 30 ≥ q), safety ≤ 6 stones per
   census curve, maximality (every empty cell covered by a ≥6-stone curve) —
   is **UNSAT**:
   - 17/19 classes directly UNSAT (kissat 4.0.4, exit 20; hardest {0,1}:
     388,349 conflicts — up 6.8% from its m=29 counterpart 363,639, the
     first local non-decrease in the direct-hardest series; direct total
     1,960,401 — the m=22..30 direct-total trend stays monotonically
     decreasing: 5,256,816 → 4,673,619 → 4,160,006 → 3,534,969 → 3,307,565
     → 2,656,426 → 2,503,468 → 2,261,532 → 1,960,401).
   - {0} and {1}: decided by the **complete k × minpos decomposition** (the
     K0816/K0821/K0834..K0841 protocol): k = 0..4 (exact deficient-row stone
     count; hardest {1} k=4: 445,772 / {0} k=4: 350,870; krow total
     1,005,289) and k = 5 × minpos = 0..14 (15 points — the m=30 sound
     bound stays floor((m−1)/2) = 14: for columns 0..29, min(x_min,
     29−x_max) ≤ 14 since x_min ≤ x_max; {0}k5p total 2,040,624 / {1}k5p
     total 2,803,033). All 40 sub-instances UNSAT (hardest: {1} k=5 mp=0:
     802,385 conflicts / 31 s — down 5.7% from its m=29 counterpart
     850,480, so the k5p0 series is decreasing again; {0} k=5 mp=0:
     545,523 — below its m=29 counterpart 690,557).
   - Total conflicts across the 57 deciding instances: **7,809,347** (17
     direct: 1,960,401; 10 krow: 1,005,289; 30 k=5 × minpos: 4,843,657);
     lex=H cross-checks add 401,084 ({0,1}: 276,589 / {2}: 124,495);
     records total 8,553,565. No SAT, no INDET among the deciding
     instances.
2. Coverage: every deficient maximal safe configuration has a non-empty
   exact deficiency set D, the exact-D instances partition them, and
   row-mirror soundness reduces 31 classes to 19. The k × minpos
   decomposition is exhaustive: k = 0..5 partitions the deficient row's
   stone count; for k = 5 the minpos split pins the leftmost stone of the
   first deficient row at column exactly P, and every configuration or its
   column mirror has leftmost stone column ≤ 14 at m = 30 (x_min +
   (29 − x_max) ≤ 29); the column mirror preserves row occupancy, hence
   the class. Therefore **no row-deficient maximal safe configuration
   exists on 5x30**; every maximal safe configuration on 5x30 has exactly
   30 stones (row occupancy (6,6,6,6,6): a row is a line of length 30 ≥
   q = 7, so safety caps every row at 6 stones).
3. Combined with K0738–K0759 (5x19 witness-free), K0816 (5x20), K0821
   (5x21), K0834 (5x22), K0835 (5x23), K0836 (5x24), K0837 (5x25),
   K0838 (5x26), K0839 (5x27), K0840 (5x28), K0841 (5x29) and K0332
   (29-stone witness at 5x18, least witness width 18): the witness-free
   width set of (5,7) is **{19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
   30}**, so in the set form **M_{5,7} ∈ {19,...,30} or M_{5,7} ≥ 31**,
   sharpened to **M_{5,7} = 19 or M_{5,7} ≥ 32** (widths 20–30 are
   verified witness-free and cannot be the threshold; M = 31 would require
   a witness at the verified witness-free width 30, so the next possible
   witness sits at w ≥ 31, forcing M = w + 1 ≥ 32); the upper bound 158
   (K0332/K0024 substitution) is unchanged. The witness-search frontier
   moves to 5x31.

## Verification

- Positive control: 5x18 q=7 class {0} SAT — 343,134 conflicts, bit-exact
  with the K0821, K0834, K0835, K0836, K0837, K0838, K0839, K0840 and
  K0841 lane control runs (ninth cross-lane reproduction); decoded model
  29 stones rows (5,6,6,6,6) passes the census-free `verifyConfig`
  independent verifier (K0332 witness board rediscovered end-to-end
  through the same encoder+solver path). The control was run twice (once
  pre-reset in batch-1, once as post-reset calibration) — both runs
  343,134 conflicts, bit-exact.
- Cross-encoding: {0,1} and {2} re-encoded with --lex=H (column-reflection
  lex-leader — class-preserving, hence sound) are UNSAT again (276,589 /
  124,495 conflicts).
- Environment: a full execution-environment reset occurred between
  batch-1 and batch-2. Recovery followed the established cross-reset
  protocol: batch-1 raw logs (17 direct + 2 lex=H + control) are
  byte-exact on main and were restored from main; scripts restored
  byte-identically (sat.js/sat2.js/sat3.js from the m=29 lane via main);
  kissat 4.0.4 re-downloaded from the official rel-4.0.4 release asset
  (same version hash 8af8e56f174b778aef3aa45af9f739b2a5f492c2); all 60
  CNFs regenerated deterministically; calibration reproduced c2 (103,993)
  and the control (343,134) bit-exactly before continuing with batch-2.
- The deciding-instance difficulty keeps decreasing overall: deciding
  totals m=23→30: 20,916,467 → 17,349,736 → 15,521,919 → 13,845,697 →
  11,363,141 → 10,218,568 → 8,677,594 → 7,809,347 (the m=30 sweep is the
  easiest of the series; two local non-decreases at m=30 — direct-hardest
  {0,1} +6.8% and {1}k5p2 above its m=29 counterpart — do not change the
  totals trend).

## Scope

Finite machine verification up to the correctness of the K0810 census, the
class-split encoding and the k×minpos decomposition (protocol
brute-force-validated on small boards in K0816/K0818), and kissat 4.0.4;
not a number-theoretic proof. Persistence at m ≥ 31 remains open: exact
M_{5,7} needs witness-free verification for all widths up to U=158 or a
universal tail argument. The witness frontier moves to 5x31 (a witness
there gives M ≥ 32; witness-free there extends the free set to
{19,...,31}). At m=31 the minpos sound bound grows to floor((31−1)/2) = 15
(columns 0..30: min(x_min, 30−x_max) ≤ 15 — 16 points per class, the CNF
set grows to 62). The 11x11 empty board, two-stone root {49,60}, S2
{59,60}, class 2 and class 4 are unaffected and remain UNKNOWN.
