# 5x32 q=7 row-deficient maximal nonexistence — class-split sweep report

Date: 2026-11-15 (UTC). Fast lane, successor of K0844 (5x31 witness-free).
Knowledge item: K0845.

## Claim

1. On the 5x32 integer grid (q=7), for each of the 19 row-mirror-canonical
   deficiency classes D ⊆ {0..4} (canonical representatives of the 31
   non-empty subsets under y -> 4-y), the class-split SAT instance — rows in
   D hold at most 5 stones, rows outside D hold exactly 6 (safety caps every
   row at 6 since a row is a line of length 32 ≥ q), safety ≤ 6 stones per
   census curve, maximality (every empty cell covered by a ≥6-stone curve) —
   is **UNSAT**:
   - 17/19 classes directly UNSAT (kissat 4.0.4, exit 20; hardest {0,1}:
     286,945 conflicts — down 17.9% from its m=31 counterpart 349,508;
     direct total 1,735,912 — the m=22..32 direct-total trend stays
     monotonically decreasing: 5,256,816 → 4,673,619 → 4,160,006 →
     3,534,969 → 3,307,565 → 2,656,426 → 2,503,468 → 2,261,532 →
     1,960,401 → 1,916,295 → 1,735,912).
   - {0} and {1}: decided by the **complete k × minpos decomposition**
     (the K0816/K0821/K0834..K0844 protocol): k = 0..4 (exact deficient-row
     stone count; hardest {1} k=4: 357,539 / {0} k=4: 277,605;
     krow total 857,057) and k = 5 × minpos = 0..15 (16 points — the m=32
     sound bound stays floor((m−1)/2) = 15: for columns 0..31, min(x_min,
     31−x_max) ≤ 15 since x_min ≤ x_max; {0}k5p total 1,624,108 / {1}k5p
     total 2,352,428). All 32 sub-instances UNSAT (hardest: {1} k=5 mp=0:
     670,375 conflicts / 25.66 s — up 2.4% from its m=31 counterpart
     654,902, the first local non-decrease in the k5p0 sub-series; {0} k=5
     mp=0: 443,637 — down from its m=31 counterpart 485,104).
   - Total conflicts across the 59 deciding instances: **6,569,505** (17
     direct: 1,735,912; 10 krow: 857,057; 32 k=5 × minpos: 3,976,536);
     lex=H cross-checks add 360,682 ({0,1}: 255,846 / {2}: 104,836);
     records total 7,273,321. No SAT, no INDET among the deciding
     instances.
2. Coverage: every deficient maximal safe configuration has a non-empty
   exact deficiency set D, the exact-D instances partition them, and
   row-mirror soundness reduces 31 classes to 19. The k × minpos
   decomposition is exhaustive: k = 0..5 partitions the deficient row's
   stone count; for k = 5 the minpos split pins the leftmost stone of the
   first deficient row at column exactly P, and every configuration or its
   column mirror has leftmost stone column ≤ 15 at m = 32 (x_min +
   (31 − x_max) ≤ 31); the column mirror preserves row occupancy, hence
   the class. Therefore **no row-deficient maximal safe configuration
   exists on 5x32**; since a row of length 32 is a line and safety caps
   every row at 6 stones, every maximal safe configuration on 5x32 has
   exactly 30 stones with row occupancy (6,6,6,6,6) — no safe
   configuration can use the extra column capacity beyond the 6-per-row
   cap.
3. Combined with K0738–K0759 (5x19 witness-free), K0816 (5x20), K0821
   (5x21), K0834 (5x22 witness-free), K0835 (5x23 witness-free), K0836
   (5x24 witness-free), K0837 (5x25 witness-free), K0838 (5x26
   witness-free), K0839 (5x27 witness-free), K0840 (5x28 witness-free),
   K0841 (5x29 witness-free), K0842 (5x30 witness-free), K0844 (5x31
   witness-free) and K0332 (29-stone witness at 5x18, least witness width
   18): the witness-free width set of (5,7) is **{19, 20, 21, 22, 23, 24,
   25, 26, 27, 28, 29, 30, 31, 32}**, so in the set form **M_{5,7} ∈
   {19,...,32} or M_{5,7} ≥ 33**, sharpened to **M_{5,7} = 19 or M_{5,7}
   ≥ 34** (widths 20–32 are verified witness-free and cannot be the
   threshold; M = 33 would require a witness at the verified witness-free
   width 32, so the next possible witness sits at w ≥ 33, forcing
   M = w + 1 ≥ 34); the upper bound 158 (K0332/K0024 substitution) is
   unchanged. The witness-search frontier moves to 5x33.

## Verification

- Positive control: 5x18 q=7 class {0} SAT — 343,134 conflicts, bit-exact
  with the K0821, K0834, K0835, K0836, K0837, K0838, K0839, K0840, K0841,
  K0842 and K0844 lane control runs (eleventh cross-lane reproduction);
  decoded model 29 stones rows (5,6,6,6,6) passes the census-free
  `verifyConfig` independent verifier (K0332 witness board rediscovered
  end-to-end through the same encoder+solver path).
- Cross-encoding: {0,1} and {2} re-encoded with --lex=H (column-reflection
  lex-leader — class-preserving, hence sound) are UNSAT again (255,846 /
  104,836 conflicts).
- Environment: single continuous session, no reset. sat.js/sat2.js/sat3.js
  are byte-identical to the K0836..K0842/K0844 lane scripts (git blob
  shas 6c3262d6 / edfae1d2 / 6dfa7db3, matching the main copies; md5
  re-verified against the local m=31 lane; the control CNF c5x18q7_0.cnf
  regenerates md5-identical); mkcnf.sh and qrun.sh ported m=31 -> m=32
  with no residual identifiers (verified by grep); all 62 CNFs generated
  deterministically by the ported mkcnf.sh; records/summary aggregates
  recomputed independently from records.jsonl (direct 1,735,912 + krow
  857,057 + k5p 3,976,536 = deciding 6,569,505).
- The deciding-instance difficulty keeps decreasing: deciding totals
  m=23→32: 20,916,467 → 17,349,736 → 15,521,919 → 13,845,697 →
  11,363,141 → 10,218,568 → 8,677,594 → 7,809,347 → 7,275,763 →
  6,569,505 (the m=32 sweep is the easiest of the series so far; the
  pre-run projection ~6.8M was close). The only local exception is the
  k5p0 hardest sub-instance (+2.4%).

## Scope

Finite machine verification up to the correctness of the K0810 census, the
class-split encoding and the k×minpos decomposition (protocol
brute-force-validated on small boards in K0816/K0818), and kissat 4.0.4;
not a number-theoretic proof. Persistence at m ≥ 33 remains open: exact
M_{5,7} needs witness-free verification for all widths up to U=158 or a
universal tail argument. The witness frontier moves to 5x33 (a witness
there gives M ≥ 34; witness-free there extends the free set to
{19,...,33}). At m=33 the minpos sound bound grows to floor((33−1)/2) = 16
(columns 0..32: min(x_min, 32−x_max) ≤ 16 — 17 points per class, the CNF
set grows to 64). The 11x11 empty board, two-stone root {49,60}, S2
{59,60}, class 2 and class 4 are unaffected and remain UNKNOWN.
