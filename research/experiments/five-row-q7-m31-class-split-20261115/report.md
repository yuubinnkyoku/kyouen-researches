# 5x31 q=7 row-deficient maximal nonexistence — class-split sweep report

Date: 2026-11-15 (UTC). Fast lane, successor of K0842 (5x30 witness-free).
Knowledge item: K0843.

## Claim

1. On the 5x31 integer grid (q=7), for each of the 19 row-mirror-canonical
   deficiency classes D ⊆ {0..4} (canonical representatives of the 31
   non-empty subsets under y -> 4-y), the class-split SAT instance — rows in
   D hold at most 5 stones, rows outside D hold exactly 6 (safety caps every
   row at 6 since a row is a line of length 31 ≥ q), safety ≤ 6 stones per
   census curve, maximality (every empty cell covered by a ≥6-stone curve) —
   is **UNSAT**:
   - 17/19 classes directly UNSAT (kissat 4.0.4, exit 20; hardest {0,1}:
     349,508 conflicts — down 10.0% from its m=30 counterpart 388,349, so
     the m=30 direct-hardest non-decrease was transient; direct total
     1,916,295 — the m=22..31 direct-total trend stays monotonically
     decreasing: 5,256,816 → 4,673,619 → 4,160,006 → 3,534,969 →
     3,307,565 → 2,656,426 → 2,503,468 → 2,261,532 → 1,960,401 →
     1,916,295).
   - {0} and {1}: decided by the **complete k × minpos decomposition** (the
     K0816/K0821/K0834..K0842 protocol): k = 0..4 (exact deficient-row stone
     count; hardest {1} k=4: 391,719 / {0} k=4: 320,407; krow total
     967,417) and k = 5 × minpos = 0..15 (16 points — the m=31 sound bound
     grows to floor((m−1)/2) = 15: for columns 0..30, min(x_min,
     30−x_max) ≤ 15 since x_min ≤ x_max; {0}k5p total 1,797,924 / {1}k5p
     total 2,594,127). All 32 sub-instances UNSAT (hardest: {1} k=5 mp=0:
     654,902 conflicts / 24.17 s — down 18.4% from its m=30 counterpart
     802,385; {0} k=5 mp=0: 485,104 — below its m=30 counterpart 545,523).
   - Total conflicts across the 59 deciding instances: **7,275,763** (17
     direct: 1,916,295; 10 krow: 967,417; 32 k=5 × minpos: 4,392,051);
     lex=H cross-checks add 330,737 ({0,1}: 233,024 / {2}: 97,713);
     records total 7,949,634. No SAT, no INDET among the deciding
     instances.
2. Coverage: every deficient maximal safe configuration has a non-empty
   exact deficiency set D, the exact-D instances partition them, and
   row-mirror soundness reduces 31 classes to 19. The k × minpos
   decomposition is exhaustive: k = 0..5 partitions the deficient row's
   stone count; for k = 5 the minpos split pins the leftmost stone of the
   first deficient row at column exactly P, and every configuration or its
   column mirror has leftmost stone column ≤ 15 at m = 31 (x_min +
   (30 − x_max) ≤ 30); the column mirror preserves row occupancy, hence
   the class. Therefore **no row-deficient maximal safe configuration
   exists on 5x31**; since a row of length 31 is a line and safety caps
   every row at 6 stones, every maximal safe configuration on 5x31 has
   exactly 5 × 6 = 30 stones with row occupancy (6,6,6,6,6) — no safe
   configuration can use the extra column capacity beyond the 6-per-row
   cap.
3. Combined with K0738–K0759 (5x19 witness-free), K0816 (5x20), K0821
   (5x21), K0834 (5x22), K0835 (5x23), K0836 (5x24), K0837 (5x25),
   K0838 (5x26), K0839 (5x27), K0840 (5x28), K0841 (5x29), K0842
   (5x30) and K0332 (29-stone witness at 5x18, least witness width 18):
   the witness-free width set of (5,7) is **{19, 20, 21, 22, 23, 24, 25,
   26, 27, 28, 29, 30, 31}**, so in the set form **M_{5,7} ∈ {19,...,31}
   or M_{5,7} ≥ 32**, sharpened to **M_{5,7} = 19 or M_{5,7} ≥ 33**
   (widths 20–31 are verified witness-free and cannot be the threshold;
   M = 32 would require a witness at the verified witness-free width 31,
   so the next possible witness sits at w ≥ 32, forcing M = w + 1 ≥ 33);
   the upper bound 158 (K0332/K0024 substitution) is unchanged. The
   witness-search frontier moves to 5x32.

## Verification

- Positive control: 5x18 q=7 class {0} SAT — 343,134 conflicts, bit-exact
  with the K0821, K0834, K0835, K0836, K0837, K0838, K0839, K0840, K0841
  and K0842 lane control runs (tenth cross-lane reproduction); decoded
  model 29 stones rows (5,6,6,6,6) passes the census-free `verifyConfig`
  independent verifier (K0332 witness board rediscovered end-to-end
  through the same encoder+solver path).
- Cross-encoding: {0,1} and {2} re-encoded with --lex=H (column-reflection
  lex-leader — class-preserving, hence sound) are UNSAT again (233,024 /
  97,713 conflicts).
- Environment: single continuous session, no reset. sat.js/sat2.js/sat3.js
  are byte-identical to the K0836..K0842 lane scripts (git blob shas
  6c3262d6 / edfae1d2 / 6dfa7db3, matching the main copies); mkcnf.sh and
  qrun.sh ported m=30 -> m=31 with no residual identifiers (verified by
  grep); all 62 CNFs generated deterministically by the ported mkcnf.sh;
  records/summary aggregates recomputed independently from records.jsonl
  (direct 1,916,295 + krow 967,417 + k5p 4,392,051 = deciding 7,275,763).
- The deciding-instance difficulty keeps decreasing: deciding totals
  m=23→31: 20,916,467 → 17,349,736 → 15,521,919 → 13,845,697 →
  11,363,141 → 10,218,568 → 8,677,594 → 7,809,347 → 7,275,763 (the m=31
  sweep is the easiest of the series so far; the pre-run projection ~7M
  was accurate).

## Scope

Finite machine verification up to the correctness of the K0810 census, the
class-split encoding and the k×minpos decomposition (protocol
brute-force-validated on small boards in K0816/K0818), and kissat 4.0.4;
not a number-theoretic proof. Persistence at m ≥ 32 remains open: exact
M_{5,7} needs witness-free verification for all widths up to U=158 or a
universal tail argument. The witness frontier moves to 5x32 (a witness
there gives M ≥ 33; witness-free there extends the free set to
{19,...,32}). At m=32 the minpos sound bound stays floor((32−1)/2) = 15
(columns 0..31: min(x_min, 31−x_max) ≤ 15 — 16 points per class, the CNF
set stays 62). The 11x11 empty board, two-stone root {49,60}, S2 {59,60},
class 2 and class 4 are unaffected and remain UNKNOWN.
