---
id: K0851
title: "5x37 q=7 row-deficient maximal nonexistence (all 19 canonical classes UNSAT) — witness-free width set of (5,7) extends to {19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37}, M_{5,7} = 19 or >= 39; independent cross-check of the band-closure def-mode decision at m=37"
kind: proposition
status: computed
topics: [rectangles, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0810
  note: "census (circleABC integer triples, line pairs) and the sequential-counter/maximality core are used verbatim (sat.js / sat2.js / sat3.js); the class-split unit clauses and the k/minpos splits are the only additions"
- type: depends_on
  target: K0332
  note: "5x18 29-stone witness is the lower bound (least witness width 18) and the positive-control board (rediscovered SAT, 343,134 conflicts, bit-exact with the K0821..K0850 lane controls — sixteenth cross-lane reproduction)"
- type: depends_on
  target: K0816
  note: "the m=20 nonexistence item; the k x minpos decomposition protocol for the hard singleton classes {0},{1} and the 5x18 positive control are taken from its cross-check lane"
- type: depends_on
  target: K0821
  note: "the m=21 nonexistence item; the witness-free width set {19,20,21} and the minpos coverage convention floor((m-1)/2)"
- type: depends_on
  target: K0834
  note: "the m=22 nonexistence item; its audit-20261115 sharpening convention (M = 19 or >= maxwitnessfree+2) is applied to the extended free set"
- type: depends_on
  target: K0836
  note: "the m=24 nonexistence item; this lane reuses its scripts byte-identically and its control reproduces bit-exactly"
- type: depends_on
  target: K0847
  note: "the m=34 nonexistence item; the m=34..m=36 counterpart conflict counts used for the per-sub-series difficulty comparisons"
- type: depends_on
  target: K0850
  note: "the m=36 nonexistence item; this lane copies its scripts (blob shas verified) and ports mkcnf.sh/qrun.sh/mkrecords5736->5737 m=36 -> m=37 (the minpos sound bound grows to floor((37-1)/2)=18, 19 points per class), extends the witness-free width set {19,...,36} -> {19,...,37}; per the five-row-q7-band-closure-35-157-20261115 coordination note this lane is the independent-encoding cross-check of that lane's def-mode UNSAT at m=37"
- type: depends_on
  target: K0738
  note: "5x19 witness-free by the occupancy complete enumeration (via the K0759 machine) — the first element of the witness-free width set"
- type: generalizes
  target: K0850
  note: "the same class-split proposition one width further: 5x36 (K0850) -> 5x37; witness-free width set {19,...,36} -> {19,...,37}; the third doubly decided width after 5x35 (K0849) and 5x36 (K0850)"
artifacts:
- path: research/experiments/five-row-q7-m37-class-split-20261115/scripts/sat3.js
  role: solver
  note: "class-split / exact-count (--krow) / minpos / lex encoder on the K0810 sat.js census + sat2.js counter core (byte-identical to the K0821..K0850 lanes; git blob shas 6c3262d6 / edfae1d2 / 6dfa7db3), plus kissat model decoding with census-free verifyConfig"
- path: research/experiments/five-row-q7-m37-class-split-20261115/scripts/mkcnf.sh
  role: source
  note: "deterministic CNF generator: 17 direct classes + {0},{1} k=0..4 + k=5 x minpos=0..18 (the sound bound grows to floor((m-1)/2)=18 at m=37, 19 points per class) + 2 lex=H + 5x18 control (68 CNFs)"
- path: research/experiments/five-row-q7-m37-class-split-20261115/scripts/qrun.sh
  role: source
  note: "2-worker claim-directory queue runner with per-instance timeout caps and interrupted-instance reclaim"
- path: research/experiments/five-row-q7-m37-class-split-20261115/scripts/mkrecords5737.js
  role: source
  note: "records.jsonl / summary.json builder from raw kissat logs; erratum: the claim-time version omitted minpos '18' from the k5p record list (sed anchor mismatch), caught before records generation (66 vs expected 68 records) and fixed in the experiment-dir commit 4756a5a3; CNFs and raw logs were unaffected (mkcnf.sh had the correct 0..18 loop from the start)"
- path: research/experiments/five-row-q7-m37-class-split-20261115/records.jsonl
  role: data
  note: "68 records: 17 direct class UNSAT + 48 k/minpos decomposition UNSAT ({0},{1}: k=0..4 and k=5 x minpos=0..18, 19 points per class at m=37) + 2 lex=H cross-checks + 1 positive control (SAT); deciding-instance conflicts 4,729,308, records total 5,371,726"
- path: research/experiments/five-row-q7-m37-class-split-20261115/summary.json
  role: data
  note: "aggregate: 0 SAT / 0 INDET among the 65 deciding instances; hardest {1} k=5 mp=0 (472,443 conflicts — down 4.1% from its m=36 counterpart); total_conflicts_37 5,028,592 = deciding 4,729,308 + lex=H 299,284 (same convention as m=27..m=36); decomposition soundness note (minpos pins the leftmost stone of the first deficient row; sound bound floor((m-1)/2)=18 at m=37: columns 0..36, min(x_min, 36-x_max) <= 18); environment note (single continuous session, no reset; all 68 raw-log remote blob shas verified against local git-hashes, 68/68 OK)"
- path: research/experiments/five-row-q7-m37-class-split-20261115/report.md
  role: proof
  note: "claim, coverage and decomposition-completeness argument (k partitions the row count; leftmost stone column <= 18 by the column mirror: x_min + (36 - x_max) <= 36), verification protocol incl. the sixteenth cross-lane bit-exact control reproduction and the band-closure def-mode cross-check agreement, per-class results, scope and limits"
- path: research/experiments/five-row-q7-m37-class-split-20261115/raw/r5x37q7_1k5p0.txt
  role: data
  note: "hardest deciding instance raw kissat log ({1} k=5 minpos=0: 472,443 conflicts UNSAT / 18.82 s); all raw logs r5x37q7_*.txt (17 direct + 48 decomposition + 2 lex + control)"
- path: research/experiments/five-row-q7-m37-class-split-20261115/raw/r_ctrl_5x18_c0.txt
  role: data
  note: "positive control log: 5x18 class {0} SAT 343,134 conflicts bit-exact with the K0821..K0850 lane controls (sixteenth cross-lane reproduction); decoded 29 stones rows (5,6,6,6,6), census-free verifyConfig PASS (K0332 witness rediscovered end-to-end)"
scope: "'finite machine verification (kissat 4.0.4: 65 UNSAT instances + 2 lex=H cross-encoding re-checks + positive control); 5x37 q=7 only.'"
evidence: "'complete-enumeration-by-class-split (verification: deterministic-machine + independent-encoding-cross-check + sixteenth cross-lane bit-exact control reproduction + decomposition protocol brute-force-validated in K0816/K0818 + agreement with the five-row-q7-band-closure-35-157-20261115 def-mode UNSAT at m=37, a different census and encoding — the third doubly decided width). See report.md.'"
---

# 5x37 q=7 row-deficient maximal nonexistence — all 19 canonical classes UNSAT

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
     the m=36 direct-hardest non-decrease (+1.9%) was transient; direct
     total 1,480,209 — down 3.6% from m=36 1,535,197, the m=22..37 series:
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
     floor((m−1)/2) = 18 at m=37: for columns 0..36,
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
   exactly 30 stones with row occupancy (6,6,6,6,6) — no safe
   configuration can use the extra column capacity beyond the 6-per-row
   cap.
3. Combined with K0738–K0759 (5x19 witness-free), K0816 (5x20), K0821
   (5x21), K0834 (5x22 witness-free), K0835 (5x23 witness-free), K0836
   (5x24 witness-free), K0837 (5x25 witness-free), K0838 (5x26
   witness-free), K0839 (5x27 witness-free), K0840 (5x28 witness-free),
   K0841 (5x29 witness-free), K0842 (5x30 witness-free), K0844 (5x31
   witness-free), K0845 (5x32 witness-free), K0846 (5x33 witness-free),
   K0847 (5x34 witness-free), K0849 (5x35 witness-free), K0850 (5x36
   witness-free) and K0332 (29-stone witness at 5x18, least witness
   width 18): the witness-free width set of (5,7) is **{19, 20, 21, 22,
   23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37}**, so in
   the set form **M_{5,7} ∈ {19,...,37} or M_{5,7} ≥ 38**, sharpened to
   **M_{5,7} = 19 or M_{5,7} ≥ 39** (widths 20–37 are verified
   witness-free and cannot be the threshold; M = 38 would require a
   witness at the verified witness-free width 37, so the next possible
   witness sits at w ≥ 38, forcing M = w + 1 ≥ 39); the upper bound 158
   (K0332/K0024 substitution) is unchanged.
4. **Independent cross-check agreement (two encodings)**: the
   five-row-q7-band-closure-35-157-20261115 lane had already decided
   5x37 witness-free by def-mode UNSAT (genfast3 chord-pair
   abstract-circle census, single instance, kissat 4.0.4) before this
   sweep; this 65-instance class-split sweep (sat3 census, different
   encoding) reaches the same verdict. 5x37 is thus **doubly decided**,
   like 5x35 (K0849) and 5x36 (K0850) — the third doubly decided width.
   The band-closure lane has additionally swept m=40..49 def-mode UNSAT
   (IN FLIGHT, records on main, knowledge integration pending with that
   lane); its remaining frontier is m=38, 39, 50..157, which this lane
   does not encroach on.

## Verification

- Positive control: 5x18 q=7 class {0} SAT — 343,134 conflicts, bit-exact
  with the K0821..K0850 lane control runs (sixteenth cross-lane
  reproduction); decoded model 29 stones rows (5,6,6,6,6) passes the
  census-free `verifyConfig` independent verifier (K0332 witness board
  rediscovered end-to-end through the same encoder+solver path; control
  run before the sweep; control CNF md5 identical to the earlier lanes:
  0bb6187d36e537a170e4fb451359bb94).
- Cross-encoding: {0,1} and {2} re-encoded with --lex=H (column-reflection
  lex-leader — class-preserving, hence sound) are UNSAT again (200,526 /
  98,758 conflicts).
- Environment: single continuous session, no reset. sat.js/sat2.js/sat3.js
  byte-identical to the K0836..K0850 lane scripts (blob shas verified:
  6c3262d6 / edfae1d2 / 6dfa7db3); the control CNF c5x18q7_0.cnf
  regenerates md5-identical and the control run reproduced 343,134
  conflicts bit-exactly before the sweep; mkcnf.sh and qrun.sh ported
  m=36 -> m=37 with no residual identifiers (verified by grep; the
  minpos loop grows 0..17 -> 0..18 since floor((37−1)/2) = 18); all 68
  raw logs were pushed batch-by-batch (batch-1 commit dd717220, batch-2
  3343286f, batch-3 9aff2907, batch-4 5c48968f) and every remote blob sha
  was verified against the local git-hash (68/68 OK); records/summary
  aggregates recomputed independently from records.jsonl (direct
  1,480,209 + krow 467,058 + k5p 2,782,041 = deciding 4,729,308; lex=H
  299,284; control 343,134; records total 5,371,726).
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
universal tail argument. The class-split lane is fully caught up with the
band-closure def-mode record through m=37; the band-closure lane has
already decided m=40..49 witness-free by def-mode (IN FLIGHT, integration
pending with that lane), and its remaining frontier is m=38, 39 and
50..157. The 11x11 empty board, two-stone root {49,60}, S2 {59,60},
class 2 and class 4 are unaffected and remain UNKNOWN.
