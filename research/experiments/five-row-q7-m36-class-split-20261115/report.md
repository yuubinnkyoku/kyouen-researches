# 5x36 q=7 row-deficient maximal nonexistence — class-split sweep report

Date: 2026-11-15 (UTC). Fast lane, successor of K0849 (5x35 witness-free).
Knowledge item: K0850. Cross-check of the five-row-q7-band-closure-35-157
def-mode decision at m=36 (different census, different encoding).

## Claim

1. On the 5x36 integer grid (q=7), for each of the 19 row-mirror-canonical
   deficiency classes D ⊆ {0..4} (canonical representatives of the 31
   non-empty subsets under y -> 4-y), the class-split SAT instance — rows in
   D hold at most 5 stones, rows outside D hold exactly 6 (safety caps every
   row at 6 since a row is a line of length 36 ≥ q), safety ≤ 6 stones per
   census curve, maximality (every empty cell covered by a ≥6-stone curve) —
   is **UNSAT**:
   - 17/19 classes directly UNSAT (kissat 4.0.4, exit 20; hardest {0,1}:
     257,251 conflicts — up 1.9% from its m=35 counterpart 252,381, a
     local non-decrease; direct total 1,535,197 — down 6.2% from m=35
     1,636,361, the m=22..36 series: 5,256,816 → 4,673,619 → 4,160,006 →
     3,534,969 → 3,307,565 → 2,656,426 → 2,503,468 → 2,261,532 →
     1,960,401 → 1,916,295 → 1,735,912 → 1,804,062 → 1,743,108 →
     1,636,361 → 1,535,197).
   - {0} and {1}: decided by the **complete k × minpos decomposition**
     (the K0816/K0821/K0834..K0849 protocol): k = 0..4 (exact deficient-row
     stone count; hardest {1} k=4: 221,525 — down 37.1% from its m=35
     counterpart 352,023; {0} k=4: 149,006 — down 28.3% from 207,921;
     krow total 524,103 — down 28.1% from 729,321, resolving the m=35
     krow-total non-decrease as transient) and k = 5 × minpos = 0..17
     (18 points — the sound bound stays floor((m−1)/2) = 17 at m=36:
     for columns 0..35, min(x_min, 35−x_max) ≤ 17 since x_min ≤ x_max;
     {0}k5p total 1,177,015 / {1}k5p total 1,775,171). All 36
     sub-instances UNSAT (hardest: {1} k=5 mp=0: 492,545 conflicts /
     17.61 s — down 0.8% from its m=35 counterpart 496,388; {0} k=5
     mp=0: 298,680 — down 11.8% from its m=35 counterpart 338,617).
   - Total conflicts across the 63 deciding instances: **5,011,486** (17
     direct: 1,535,197; 10 krow: 524,103; 36 k=5 × minpos: 2,952,186);
     lex=H cross-checks add 293,505 ({0,1}: 196,313 / {2}: 97,192);
     records total 5,648,125. No SAT, no INDET among the deciding
     instances.
2. Coverage: every deficient maximal safe configuration has a non-empty
   exact deficiency set D, the exact-D instances partition them, and
   row-mirror soundness reduces 31 classes to 19. The k × minpos
   decomposition is exhaustive: k = 0..5 partitions the deficient row's
   stone count; for k = 5 the minpos split pins the leftmost stone of
   the first deficient row at column exactly P, and every configuration
   or its column mirror has leftmost stone column ≤ 17 at m = 36 (x_min +
   (35 − x_max) ≤ 35); the column mirror preserves row occupancy, hence
   the class. Therefore **no row-deficient maximal safe configuration
   exists on 5x36**; since a row of length 36 is a line and safety caps
   every row at 6 stones, every maximal safe configuration on 5x36 has
   exactly 30 stones with row occupancy (6,6,6,6,6) — no safe
   configuration can use the extra column capacity beyond the 6-per-row
   cap.
3. Combined with K0738–K0759 (5x19 witness-free), K0816 (5x20), K0821
   (5x21), K0834..K0847 (5x22..5x34 witness-free), K0849 (5x35
   witness-free) and K0332 (29-stone witness at 5x18, least witness
   width 18): the witness-free width set of (5,7) is now
   **{19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35,
   36}**, so in the set form **M_{5,7} ∈ {19,...,36} or M_{5,7} ≥ 37**,
   sharpened to **M_{5,7} = 19 or M_{5,7} ≥ 38** (widths 20–36 are
   verified witness-free and cannot be the threshold; M = 37 would
   require a witness at the verified witness-free width 36); the upper
   bound 158 (K0332/K0024 substitution) is unchanged.
4. **Independent cross-check agreement**: the five-row-q7-band-closure
   35-157-20261115 lane (genfast3 chord-pair abstract-circle census,
   def-mode single instance, kissat 4.0.4) has also decided 5x36
   UNSAT — a different census implementation and a different encoding
   from this 63-instance class-split sweep, reaching the same verdict.
   5x36 is therefore doubly decided (two independent encodings), like
   5x35 (K0849 + the same def-mode sweep). The band-closure lane has
   additionally swept m=37 and m=40..49 def-mode UNSAT (IN FLIGHT,
   records on main, knowledge integration pending with that lane);
   per its coordination note, m=38, 39 and 50..157 are its remaining
   frontier, and this lane does not encroach on them.

## Verification

- Positive control: 5x18 q=7 class {0} SAT — 343,134 conflicts, bit-exact
  with the K0821..K0847 and K0849 lane control runs (fifteenth cross-lane
  reproduction); decoded model 29 stones rows (5,6,6,6,6) passes the
  census-free `verifyConfig` independent verifier (K0332 witness board
  rediscovered end-to-end through the same encoder+solver path; control
  run before the sweep; control CNF md5 identical to the K0836..K0849
  lanes: 0bb6187d36e537a170e4fb451359bb94).
- Cross-encoding: {0,1} and {2} re-encoded with --lex=H (column-reflection
  lex-leader — class-preserving, hence sound) are UNSAT again (196,313 /
  97,192 conflicts).
- Environment: single continuous session, no reset. sat.js/sat2.js/sat3.js
  byte-identical to the K0836..K0849 lane scripts (blob shas verified:
  6c3262d6 / edfae1d2 / 6dfa7db3); mkcnf.sh and qrun.sh ported m=35 ->
  m=36 with no residual identifiers (verified by grep; the minpos loop
  stays 0..17 since floor((36−1)/2) = 17); all 66 raw logs were pushed
  batch-by-batch (batch-1 through batch-4) and every remote blob sha was
  verified against the local sha1 (66/66 OK); records/summary aggregates
  recomputed independently from records.jsonl (direct 1,535,197 + krow
  524,103 + k5p 2,952,186 = deciding 5,011,486; lexH 293,505; control
  343,134; records total 5,648,125).
- The deciding-instance difficulty keeps decreasing on average: deciding
  totals m=23→36: 20,916,467 → 17,349,736 → 15,521,919 → 13,845,697 →
  11,363,141 → 10,218,568 → 8,677,594 → 7,809,347 → 7,275,763 →
  6,569,505 → 6,140,609 → 5,928,015 → 5,423,024 → 5,011,486 (the
  pre-run projection ~5.1M was accurate to 0.2%). The only local
  non-decrease at m=36 is direct-hardest {0,1} +1.9%; the m=35 krow
  non-decreases ({1}k4 +0.9%, {0}k4 +3.8%, krow total +0.4%) all
  resolved back to strongly decreasing at m=36.

## Scope

Finite machine verification up to the correctness of the K0810 census, the
class-split encoding and the k×minpos decomposition (protocol
brute-force-validated on small boards in K0816/K0818), and kissat 4.0.4;
not a number-theoretic proof. Persistence at m ≥ 37 remains open: exact
M_{5,7} needs witness-free verification for all widths up to U=158 or a
universal tail argument. The class-split witness frontier would be 5x37;
the band-closure lane has already decided 5x37 and 5x40..5x49 witness-free
by def-mode (IN FLIGHT, integration pending), and its remaining frontier
is m=38, 39, 50..157. The 11x11 empty board, two-stone root {49,60}, S2
{59,60}, class 2 and class 4 are unaffected and remain UNKNOWN.
