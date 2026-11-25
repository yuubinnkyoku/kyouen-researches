# 5x33 q=7 row-deficient maximal nonexistence — class-split sweep report

Date: 2026-11-15 (UTC). Fast lane, successor of K0845 (5x32 witness-free).
Knowledge item: K0846.

## Claim

1. On the 5x33 integer grid (q=7), for each of the 19 row-mirror-canonical
   deficiency classes D ⊆ {0..4} (canonical representatives of the 31
   non-empty subsets under y -> 4-y), the class-split SAT instance — rows in
   D hold at most 5 stones, rows outside D hold exactly 6 (safety caps every
   row at 6 since a row is a line of length 33 ≥ q), safety ≤ 6 stones per
   census curve, maximality (every empty cell covered by a ≥6-stone curve) —
   is **UNSAT**:
   - 17/19 classes directly UNSAT (kissat 4.0.4, exit 20; hardest {0,1}:
     334,184 conflicts — up 16.5% from its m=32 counterpart 286,945, the
     second local non-decrease in the direct-hardest series; direct total
     1,804,062 — up 3.9% from m=32 1,735,912, the first direct-total
     non-decrease in the m=22..33 series: 5,256,816 → 4,673,619 →
     4,160,006 → 3,534,969 → 3,307,565 → 2,656,426 → 2,503,468 →
     2,261,532 → 1,960,401 → 1,916,295 → 1,735,912 → 1,804,062).
   - {0} and {1}: decided by the **complete k × minpos decomposition**
     (the K0816/K0821/K0834..K0845 protocol): k = 0..4 (exact deficient-row
     stone count; hardest {1} k=4: 356,896 / {0} k=4: 218,095; krow total
     760,709) and k = 5 × minpos = 0..16 (17 points — the m=33 sound bound
     grows to floor((m−1)/2) = 16: for columns 0..32, min(x_min,
     32−x_max) ≤ 16 since x_min ≤ x_max; {0}k5p total 1,480,222 / {1}k5p
     total 2,095,616). All 34 sub-instances UNSAT (hardest: {1} k=5 mp=0:
     651,985 conflicts / 25.39 s — down 2.7% from its m=32 counterpart
     670,375; {0} k=5 mp=0: 446,878 — up 0.7% from its m=32 counterpart
     443,637, the second consecutive k5p0 non-decrease).
   - Total conflicts across the 61 deciding instances: **6,140,609** (17
     direct: 1,804,062; 10 krow: 760,709; 34 k=5 × minpos: 3,575,838);
     lex=H cross-checks add 340,968 ({0,1}: 241,070 / {2}: 99,898);
     records total 6,824,711. No SAT, no INDET among the deciding
     instances.
2. Coverage: every deficient maximal safe configuration has a non-empty
   exact deficiency set D, the exact-D instances partition them, and
   row-mirror soundness reduces 31 classes to 19. The k × minpos
   decomposition is exhaustive: k = 0..5 partitions the deficient row's
   stone count; for k = 5 the minpos split pins the leftmost stone of
   the first deficient row at column exactly P, and every configuration
   or its column mirror has leftmost stone column ≤ 16 at m = 33 (x_min +
   (32 − x_max) ≤ 32); the column mirror preserves row occupancy, hence
   the class. Therefore **no row-deficient maximal safe configuration
   exists on 5x33**; since a row of length 33 is a line and safety caps
   every row at 6 stones, every maximal safe configuration on 5x33 has
   exactly 30 stones with row occupancy (6,6,6,6,6) — no safe
   configuration can use the extra column capacity beyond the 6-per-row
   cap.
3. Combined with K0738–K0759 (5x19 witness-free), K0816 (5x20), K0821
   (5x21), K0834 (5x22 witness-free), K0835 (5x23 witness-free), K0836
   (5x24 witness-free), K0837 (5x25 witness-free), K0838 (5x26
   witness-free), K0839 (5x27 witness-free), K0840 (5x28 witness-free),
   K0841 (5x29 witness-free), K0842 (5x30 witness-free), K0844 (5x31
   witness-free), K0845 (5x32 witness-free) and K0332 (29-stone witness at
   5x18, least witness width 18): the witness-free width set of (5,7) is
   **{19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33}**, so in
   the set form **M_{5,7} ∈ {19,...,33} or M_{5,7} ≥ 34**, sharpened to
   **M_{5,7} = 19 or M_{5,7} ≥ 35** (widths 20–33 are verified
   witness-free and cannot be the threshold; M = 34 would require a
   witness at the verified witness-free width 33, so the next possible
   witness sits at w ≥ 34, forcing M = w + 1 ≥ 35); the upper bound 158
   (K0332/K0024 substitution) is unchanged. The witness-search frontier
   moves to 5x34.

## Verification

- Positive control: 5x18 q=7 class {0} SAT — 343,134 conflicts, bit-exact
  with the K0821, K0834, K0835, K0836, K0837, K0838, K0839, K0840, K0841,
  K0842, K0844 and K0845 lane control runs (twelfth cross-lane
  reproduction); decoded model 29 stones rows (5,6,6,6,6) passes the
  census-free `verifyConfig` independent verifier (K0332 witness board
  rediscovered end-to-end through the same encoder+solver path).
- Cross-encoding: {0,1} and {2} re-encoded with --lex=H (column-reflection
  lex-leader — class-preserving, hence sound) are UNSAT again (241,070 /
  99,898 conflicts).
- Environment: the sweep crossed a full execution-environment reset
  between batch-1 and batches 2-4. Recovery followed the established
  protocol: sat.js/sat2.js/sat3.js restored from main with git blob shas
  verified (6c3262d6 / edfae1d2 / 6dfa7db3), kissat re-downloaded from the
  official rel-4.0.4 asset (md5 3a5eba830aa6008a604fcc9bbe99a325), all 64
  CNFs regenerated by the ported mkcnf.sh, and the pre-reset batch-1
  instance {0,1} re-run bit-exactly (334,184 conflicts) alongside the
  5x18 control (343,134) before continuing; the pre-reset batch-1 raw
  logs are byte-exact on main. mkcnf.sh and qrun.sh ported m=32 -> m=33
  with no residual identifiers (verified by grep); records/summary
  aggregates recomputed independently from records.jsonl (direct
  1,804,062 + krow 760,709 + k5p 3,575,838 = deciding 6,140,609).
- The deciding-instance difficulty keeps decreasing on average: deciding
  totals m=23→33: 20,916,467 → 17,349,736 → 15,521,919 → 13,845,697 →
  11,363,141 → 10,218,568 → 8,677,594 → 7,809,347 → 7,275,763 →
  6,569,505 → 6,140,609 (the pre-run projection ~6.1M was accurate). The
  m=33 local exceptions are the direct-hardest (+16.5%), the
  direct-total (+3.9%) and {0} k5p0 (+0.7%).

## Scope

Finite machine verification up to the correctness of the K0810 census, the
class-split encoding and the k×minpos decomposition (protocol
brute-force-validated on small boards in K0816/K0818), and kissat 4.0.4;
not a number-theoretic proof. Persistence at m ≥ 34 remains open: exact
M_{5,7} needs witness-free verification for all widths up to U=158 or a
universal tail argument. The witness frontier moves to 5x34 (a witness
there gives M ≥ 35; witness-free there extends the free set to
{19,...,34}). At m=34 the minpos sound bound stays floor((34−1)/2) = 16
(columns 0..33: min(x_min, 33−x_max) ≤ 16 — 17 points per class, the CNF
set stays 64). The 11x11 empty board, two-stone root {49,60}, S2
{59,60}, class 2 and class 4 are unaffected and remain UNKNOWN.
