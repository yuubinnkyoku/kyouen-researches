# 5x29 q=7 row-deficient maximal nonexistence — report

Date: 2026-11-15 (UTC). Fast lane, successor of K0840 (5x28 witness-free).
Knowledge item: K0841.

## Claim

1. On the 5x29 integer grid (q=7), for each of the 19 row-mirror-canonical
   deficiency classes D ⊆ {0..4} (canonical representatives of the 31 non-empty
   subsets under y -> 4-y), the class-split SAT instance — rows in D hold at
   most 5 stones, rows outside D hold exactly 6 (safety caps every row at 6
   since a row is a line of length 29 ≥ q), safety ≤ 6 stones per census
   curve, maximality (every empty cell covered by a ≥6-stone curve) — is
   **UNSAT**:
   - 17/19 classes directly UNSAT (kissat 4.0.4, exit 20; hardest {0,1}:
     363,639 conflicts; direct total 2,261,532 — the m=22..29 direct
     difficulty trend is monotonically decreasing: 5,256,816 → 4,673,619 →
     4,160,006 → 3,534,969 → 3,307,565 → 2,656,426 → 2,503,468 → 2,261,532).
   - {0} and {1}: decided by the **complete k × minpos decomposition** (the
     K0816/K0821/K0834..K0840 protocol): k = 0..4 (exact deficient-row stone
     count; hardest {1} k=4: 509,585 / {0} k=4: 372,205) and k = 5 × minpos =
     0..14 (15 points — the m=29 sound bound grows to floor((m−1)/2) = 14:
     for columns 0..28, min(x_min, 28−x_max) ≤ 14 since x_min ≤ x_max). All
     40 sub-instances UNSAT (hardest: {1} k=5 mp=0: 850,480 conflicts /
     31.21 s — down 42% from its m=28 counterpart 1,469,014, so the m=28
     non-decrease in the k5p0 series was transient; {0} k=5 mp=0: 690,557 —
     also below its m=28 counterpart 834,706).
   - Total conflicts across the 57 deciding instances: **8,677,594** (17
     direct: 2,261,532; 10 krow: 1,135,398; 30 k=5 × minpos: 5,280,664);
     lex=H cross-checks add 464,888. No SAT, no INDET among the deciding
     instances.
2. Coverage: every deficient maximal safe configuration has a non-empty exact
   deficiency set D, the exact-D instances partition them, and row-mirror
   soundness reduces 31 classes to 19. The k × minpos decomposition is
   exhaustive: k = 0..5 partitions the deficient row's stone count; for k = 5
   the minpos split pins the leftmost stone of the first deficient row at
   column exactly P, and every configuration or its column mirror has leftmost
   stone column ≤ 14 at m = 29 (x_min + (28 − x_max) ≤ 28); the column mirror
   preserves row occupancy, hence the class. Therefore **no row-deficient
   maximal safe configuration exists on 5x29**; every maximal safe
   configuration on 5x29 has 30 stones (row occupancy (6,6,6,6,6)).
3. Combined with K0738–K0759 (5x19), K0816 (5x20), K0821 (5x21), K0834
   (5x22), K0835 (5x23), K0836 (5x24), K0837 (5x25), K0838 (5x26), K0839
   (5x27), K0840 (5x28) and K0332 (29-stone witness at 5x18, least witness
   width 18): the witness-free width set of (5,7) is **{19, 20, 21, 22, 23, 24,
   25, 26, 27, 28, 29}**, so in the set form **M_{5,7} ∈ {19,...,29} or
   M_{5,7} ≥ 30**, sharpened to **M_{5,7} = 19 or M_{5,7} ≥ 31** (widths 20–29
   are verified witness-free and cannot be the threshold; M = 30 would require
   a witness at the verified witness-free width 29, so the next possible
   witness sits at w ≥ 30, forcing M = w + 1 ≥ 31); the upper bound 158
   (K0332/K0024 substitution) is unchanged. The witness-search frontier moves
   to 5x30.

## Verification

- Positive control: 5x18 q=7 class {0} SAT — 343,134 conflicts, bit-exact
  with the K0821, K0834, K0835, K0836, K0837, K0838, K0839 and K0840 lane
  control runs (eighth cross-lane reproduction); decoded model 29 stones rows
  (5,6,6,6,6) passes the census-free `verifyConfig` independent verifier
  (K0332 witness board rediscovered end-to-end through the same
  encoder+solver path).
- Cross-encoding: {0,1} and {2} re-encoded with --lex=H (column-reflection
  lex-leader — class-preserving, hence sound) are UNSAT again (328,996 /
  135,892 conflicts).
- Single continuous session (no environment reset): scripts restored
  byte-identically from the m=28 lane (sat.js/sat2.js/sat3.js; mkcnf.sh and
  qrun.sh ported m=28 → m=29, git blob sha verified against main), all 60
  CNFs regenerated deterministically, raw logs pushed batch-by-batch
  (batch-1: 17 direct + 2 lexH + control; batch-2: krow k=0..4; batch-3/4:
  k=5 × minpos 0..14 per class).
- The deciding-instance difficulty is monotonically decreasing again:
  deciding totals m=23→29: 20,916,467 → 17,349,736 → 15,521,919 →
  13,845,697 → 11,363,141 → 10,218,568 → 8,677,594 (the m=28 local exception
  {1} k=5 mp=0 is resolved: it dropped 42%, and the m=29 sweep is the easiest
  of the series so far).

## Scope

Finite machine verification up to the correctness of the K0810 census, the
class-split encoding and the k×minpos decomposition (protocol
brute-force-validated on small boards in K0816/K0818), and kissat 4.0.4; not a
number-theoretic proof. Persistence at m ≥ 30 remains open: exact M_{5,7}
needs witness-free verification for all widths up to U=158 or a universal
tail argument. The witness frontier moves to 5x30 (a witness there gives
M ≥ 31; witness-free there extends the free set to {19,...,30}). At m=30 the
minpos sound bound stays floor((30-1)/2) = 14 (columns 0..29: min(x_min,
29−x_max) ≤ 14 — 15 points per class, the CNF set stays at 60). The 11x11
empty board, two-stone root {49,60}, S2 {59,60}, class 2 and class 4 are
unaffected and remain UNKNOWN.
