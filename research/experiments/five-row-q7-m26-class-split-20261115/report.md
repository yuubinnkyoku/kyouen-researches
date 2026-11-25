# 5x26 q=7 row-deficient maximal nonexistence — report

Date: 2026-11-15 (UTC). Fast lane, successor of K0837 (5x25 witness-free).
Knowledge item: K0838.

## Claim

1. On the 5x26 integer grid (q=7), for each of the 19 row-mirror-canonical
   deficiency classes D ⊆ {0..4} (canonical representatives of the 31
   non-empty subsets under y -> 4-y), the class-split SAT instance — rows in D
   hold at most 5 stones, rows outside D hold exactly 6 (safety caps every row
   at 6 since a row is a line of length 26 ≥ q), safety ≤ 6 stones per census
   curve, maximality (every empty cell covered by a ≥6-stone curve) — is
   **UNSAT**:
   - 17/19 classes directly UNSAT (kissat 4.0.4, exit 20; hardest {0,1}:
     654,569 conflicts / 22.1 s; direct total 3,307,565 — the m=22..26 direct
     difficulty trend is monotonically decreasing: 5,256,816 → 4,673,619 →
     4,160,006 → 3,534,969 → 3,307,565).
   - {0} and {1}: decided by the **complete k × minpos decomposition** (the
     K0816/K0821/K0834..K0837 protocol): k = 0..4 (exact deficient-row stone
     count; hardest {1} k=4: 913,377 / {0} k=4: 620,428) and k = 5 × minpos =
     0..12 (13 points — the m=26 sound bound is floor((m-1)/2) = 12, same as
     m=25: for columns 0..25, min(x_min, 25-x_max) ≤ 12 since x_min ≤ x_max).
     All 36 sub-instances UNSAT (hardest: {1} k=5 mp=0: 1,758,742 conflicts /
     71.28 s; {0} k=5 mp=0: 1,202,057 / 47.17 s — both below their m=25
     counterparts 2,021,531 / 1,620,423).
   - Total conflicts across the 53 deciding instances: **13,845,697** (17
     direct: 3,307,565; 36 decomposition: 10,538,132); lex=H cross-checks add
     683,091; records total (56 incl. control) 14,871,922. No SAT, no INDET
     among the deciding instances.
2. Coverage: every deficient maximal safe configuration has a non-empty exact
   deficiency set D, the exact-D instances partition them, and row-mirror
   soundness reduces 31 classes to 19. The k × minpos decomposition is
   exhaustive: k = 0..5 partitions the deficient row's stone count; for k = 5
   the minpos split pins the leftmost stone of the first deficient row at
   column exactly P, and every configuration or its column mirror has leftmost
   stone column ≤ 12 at m = 26 (x_min + (25 − x_max) ≤ 25); the column mirror
   preserves row occupancy, hence the class. Therefore **no row-deficient
   maximal safe configuration exists on 5x26**; every maximal safe
   configuration on 5x26 has 30 stones (row occupancy (6,6,6,6,6)).
3. Combined with K0738–K0759 (5x19), K0816 (5x20), K0821 (5x21), K0834
   (5x22), K0835 (5x23), K0836 (5x24), K0837 (5x25) and K0332 (29-stone
   witness at 5x18, least witness width 18): the witness-free width set of
   (5,7) is **{19, 20, 21, 22, 23, 24, 25, 26}**, so in the set form
   **M_{5,7} ∈ {19,...,26} or M_{5,7} ≥ 27**, sharpened to **M_{5,7} = 19 or
   M_{5,7} ≥ 28** (widths 20–26 are verified witness-free and cannot be the
   threshold; M = 27 would require a witness at the verified witness-free
   width 26, so the next possible witness sits at w ≥ 27, forcing M = w + 1
   ≥ 28); the upper bound 158 (K0332/K0024 substitution) is unchanged. The
   witness-search frontier moves to 5x27.

## Verification

- Positive control: 5x18 q=7 class {0} SAT — 343,134 conflicts / 10.32 s,
  bit-exact with the K0821, K0834, K0835, K0836 and K0837 lane control runs
  (fifth cross-lane reproduction); decoded model 29 stones rows (5,6,6,6,6)
  passes the census-free `verifyConfig` independent verifier (K0332 witness
  board rediscovered end-to-end through the same encoder+solver path).
- Cross-encoding: {0,1} and {2} re-encoded with --lex=H (column-reflection
  lex-leader — class-preserving, hence sound) are UNSAT again (446,133 /
  236,958 conflicts).
- Cross-run determinism (environment-outage resume): the sweep ran across a
  full execution-environment reset between batch-1 and batch-2 (pre-reset
  local scratch lost; the 20 batch-1 raw logs were already on main, git blob
  sha verified). The resuming session re-downloaded the official kissat
  4.0.4 linux-amd64 release binary, restored the five scripts from main
  (blob sha verified byte-identical), regenerated all 56 CNFs, and re-ran
  c2 (248,556) plus the 5x18 control (343,134) as cross-run calibration,
  matching the pre-reset logs bit-exactly — the third demonstrated
  cross-reset bit-exactness of this protocol (after K0835 and K0837).
- The deciding-instance difficulty is still decreasing: deciding totals
  m=23→26: 20,916,467 → 17,349,736 → 15,521,919 → 13,845,697.

## Scope

Finite machine verification up to the correctness of the K0810 census, the
class-split encoding and the k×minpos decomposition (protocol
brute-force-validated on small boards in K0816/K0818), and kissat 4.0.4; not a
number-theoretic proof. Persistence at m ≥ 27 remains open: exact M_{5,7}
needs witness-free verification for all widths up to U=158 or a universal
tail argument. The witness frontier moves to 5x27 (a witness there gives
M ≥ 28; witness-free there extends the free set to {19,...,27}). At m=27 the
minpos sound bound grows to floor((27-1)/2) = 13 (14 points per class, 28
k=5 sub-instances — the next lane's CNF set is 58). The 11x11 empty board,
two-stone root {49,60}, S2 {59,60}, class 2 and class 4 are unaffected and
remain UNKNOWN.
