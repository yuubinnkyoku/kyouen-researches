# 5x37 q=7 row-deficient maximal nonexistence — class-split sweep report

Date: 2026-11-15 (UTC). Fast lane, successor of K0850 (5x36 witness-free).
Knowledge item: K0851 (to be confirmed at integration). Cross-check of the
five-row-q7-band-closure-35-157 def-mode decision at m=37 (different
census, different encoding).

## Claim

1. On the 5x37 integer grid (q=7), for each of the 19 row-mirror-canonical
   deficiency classes D ⊆ {0..4} (canonical representatives of the 31
   non-empty subsets under y -> 4-y), the class-split SAT instance — rows in
   D hold at most 5 stones, rows outside D hold exactly 6 (safety caps every
   row at 6 since a row is a line of length 37 ≥ q), safety ≤ 6 stones per
   census curve, maximality (every empty cell covered by a ≥6-stone curve) —
   is **UNSAT**:
   - 17/19 classes directly UNSAT (kissat 4.0.4, exit 20; hardest {0,1}:
     223,591 conflicts — down 13.0% from its m=36 counterpart 257,251, so
     the m=36 direct-hardest non-decrease was transient; direct total
     1,480,209 — down 3.6% from m=36 1,535,197, the m=22..37 series:
     5,256,816 → 4,673,619 → 4,160,006 → 3,534,969 → 3,307,565 →
     2,656,426 → 2,503,468 → 2,261,532 → 1,960,401 → 1,916,295 →
     1,735,912 → 1,804,062 → 1,743,108 → 1,636,361 → 1,535,197 →
     1,480,209).
   - {0} and {1}: decided by the **complete k × minpos decomposition**
     (the K0816/K0821/K0834..K0850 protocol): k = 0..4 (exact deficient-row
     stone count; hardest {1} k=4: 172,488 — down 22.1% from its m=36
     counterpart 221,525; {0} k=4: 133,829 — down 10.2% from 149,006;
     krow total 467,058 — down 10.9% from 524,103) and k = 5 ×
     minpos = 0..18 (19 points — the sound bound grows to
     floor((37−1)/2) = 18 at m=37: for columns 0..36,
     min(x_min, 36−x_max) ≤ 18 since x_min ≤ x_max; {0}k5p total
     1,149,751 / {1}k5p total 1,632,290; the new minpos=18 instances cost
     5,019 / 6,218). All 48 sub-instances UNSAT (hardest: {1} k=5 mp=0:
     472,443 conflicts / 18.82 s — down 4.1% from its m=36 counterpart
     492,545; {0} k=5 mp=0: 345,111 — up 15.6% from its m=36 counterpart
     298,680, the only local non-decrease at m=37).
   - Total conflicts across the 65 deciding instances: **4,729,308** (17
     direct: 1,480,209; 10 krow: 467,058; 38 k=5 × minpos: 2,782,041);
     lex=H cross-checks add 299,284 ({0,1}: 200,526 / {2}: 98,758);
     records total 5,371,726. No SAT, no INDET among the deciding
     instances.
2. Coverage: every deficient maximal safe configuration has a non-empty
   exact deficiency set D, the exact-D instances partition them, and
   row-mirror soundness reduces 31 classes to 19. The k × minpos
   decomposition is exhaustive: k = 0..5 partitions the deficient row's
   stone count; for k = 5 the minpos split pins the leftmost stone of
   the first deficient row at column exactly P, and every configuration
   or its column mirror has leftmost stone column ≤ 18 at m = 37 (x_min +
   (36 − x_max) ≤ 36); the column mirror preserves row occupancy, hence
   the class. Therefore **no row-deficient maximal safe configuration
   exists on 5x37**; since a row of length 37 is a line and safety caps
   every row at 6 stones, every maximal safe configuration on 5x37 has
   exactly 30 stones with row occupancy (6,6,6,6,6).
3. Combined with K0738–K0759 (5x19 witness-free), K0816 (5x20), K0821
   (5x21), K0834..K0847 (5x22..5x34 witness-free), K0849 (5x35), K0850
   (5x36) and K0332 (29-stone witness at 5x18, least witness width 18):
   the witness-free width set of (5,7) is now
   **{19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35,
   36, 37}**, so in the set form **M_{5,7} ∈ {19,...,37} or M_{5,7} ≥ 38**,
   sharpened to **M_{5,7} = 19 or M_{5,7} ≥ 39** (widths 20–37 are
   verified witness-free and cannot be the threshold; M = 38 would
   require a witness at the verified witness-free width 37); the upper
   bound 158 (K0332/K0024 substitution) is unchanged.
4. **Independent cross-check agreement**: the five-row-q7-band-closure
   35-157-20261115 lane (genfast3 chord-pair abstract-circle census,
   def-mode single instance, kissat 4.0.4) has also decided 5x37
   UNSAT — a different census implementation and a different encoding
   from this 65-instance class-split sweep, reaching the same verdict.
   5x37 is therefore the third doubly decided width (two independent
   encodings), after 5x35 (K0849) and 5x36 (K0850). The band-closure lane
   has additionally swept m=40..49 def-mode UNSAT (IN FLIGHT, records on
   main, knowledge integration pending with that lane); per its
   coordination note, m=38, 39 and 50..157 are its remaining frontier,
   and this lane does not encroach on them.

## Verification

- Positive control: 5x18 q=7 class {0} SAT — 343,134 conflicts, bit-exact
  with the K0821..K0850 lane control runs (sixteenth cross-lane
  reproduction); decoded model 29 stones rows (5,6,6,6,6) passes the
  census-free `verifyConfig` independent verifier (K0332 witness board
  rediscovered end-to-end through the same encoder+solver path; control
  run before the sweep; control CNF md5 identical to the K0836..K0850
  lanes: 0bb6187d36e537a170e4fb451359bb94).
- Cross-encoding: {0,1} and {2} re-encoded with --lex=H (column-reflection
  lex-leader — class-preserving, hence sound) are UNSAT again (200,526 /
  98,758 conflicts).
- Environment: single continuous session, no reset. sat.js/sat2.js/sat3.js
  byte-identical to the K0836..K0850 lane scripts (blob shas verified:
  6c3262d6 / edfae1d2 / 6dfa7db3); mkcnf.sh and qrun.sh ported m=36 ->
  m=37 with no residual identifiers (verified by grep; the minpos loop
  grows 0..17 -> 0..18 since floor((37−1)/2) = 18); all 68 raw logs were
  pushed batch-by-batch (batch-1 through batch-4) and every remote blob
  sha was verified against the local git-hash (68/68 OK); records/summary
  aggregates recomputed independently from records.jsonl (direct 1,480,209
  + krow 467,058 + k5p 2,782,041 = deciding 4,729,308; lexH 299,284;
  control 343,134; records total 5,371,726).
- mkrecords5737.js erratum: the claim-time version omitted minpos '18'
  from the k5p record list (a sed anchor mismatch — the closing bracket
  was targeted with a parenthesis); caught before records.jsonl was
  generated (record count 66 vs expected 68), fixed, and the fixed script
  is pushed with the experiment dir. CNFs and raw logs were unaffected:
  mkcnf.sh had the correct 0..18 loop from the start (68 CNFs generated,
  including both minpos=18 instances, both of which were solved and
  pushed with their batches).
- The deciding-instance difficulty keeps decreasing on average: deciding
  totals m=23→37: 20,916,467 → 17,349,736 → 15,521,919 → 13,845,697 →
  11,363,141 → 10,218,568 → 8,677,594 → 7,809,347 → 7,275,763 →
  6,569,505 → 6,140,609 → 5,928,015 → 5,423,024 → 5,011,486 →
  4,729,308 (the pre-run projection ~4.7M was accurate to 0.6%). The
  only local non-decrease at m=37 is {0}k5p0 +15.6%; the m=36
  direct-hardest non-decrease ({0,1} +1.9%) resolved back to strongly
  decreasing (−13.0%).

## Scope

Finite machine verification up to the correctness of the K0810 census, the
class-split encoding and the k×minpos decomposition (protocol
brute-force-validated on small boards in K0816/K0818), and kissat 4.0.4;
not a number-theoretic proof. Persistence at m ≥ 38 remains open: exact
M_{5,7} needs witness-free verification for all widths up to U=158 or a
universal tail argument. The band-closure lane's remaining frontier is
m=38, 39, 50..157 (its territory). The 11x11 empty board, two-stone root
{49,60}, S2 {59,60}, class 2 and class 4 are unaffected and remain
UNKNOWN.
