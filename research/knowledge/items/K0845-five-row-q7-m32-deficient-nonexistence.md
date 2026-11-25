---
id: K0845
title: "5x32 q=7 row-deficient maximal nonexistence (all 19 canonical classes UNSAT) — witness-free width set of (5,7) extends to {19,20,21,22,23,24,25,26,27,28,29,30,31,32}, M_{5,7} = 19 or >= 34"
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
  note: "5x18 29-stone witness is the lower bound (least witness width 18) and the positive-control board (rediscovered SAT, 343,134 conflicts, bit-exact with the K0821..K0844 lane controls — eleventh cross-lane reproduction)"
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
  target: K0835
  note: "the m=23 nonexistence item; its mid-sweep environment-reset bit-exact re-run reconciliation protocol"
- type: depends_on
  target: K0836
  note: "the m=24 nonexistence item; this lane reuses its scripts byte-identically and its control reproduces bit-exactly"
- type: depends_on
  target: K0837
  note: "the m=25 nonexistence item; this lane reuses its scripts byte-identically and its control reproduces bit-exactly"
- type: depends_on
  target: K0838
  note: "the m=26 nonexistence item; this lane reuses its scripts byte-identically and its control reproduces bit-exactly"
- type: depends_on
  target: K0839
  note: "the m=27 nonexistence item; this lane reuses its scripts byte-identically and its control reproduces bit-exactly"
- type: depends_on
  target: K0840
  note: "the m=28 nonexistence item; this lane reuses its scripts byte-identically and its control reproduces bit-exactly"
- type: depends_on
  target: K0841
  note: "the m=29 nonexistence item; this lane reuses its scripts byte-identically and its control reproduces bit-exactly"
- type: depends_on
  target: K0842
  note: "the m=30 nonexistence item; this lane reuses its scripts byte-identically and its control reproduces bit-exactly"
- type: depends_on
  target: K0844
  note: "the m=31 nonexistence item; this lane copies its local scripts (md5 re-verified against the main-restored copies, blob shas 6c3262d6 / edfae1d2 / 6dfa7db3) and ports mkcnf.sh/qrun.sh/mkrecords m=31 -> m=32, extends the witness-free width set {19,...,31} -> {19,...,32} and moves the frontier to 5x33"
- type: depends_on
  target: K0738
  note: "5x19 witness-free by the occupancy complete enumeration (via the K0759 machine) — the first element of the witness-free width set"
- type: generalizes
  target: K0844
  note: "the same class-split proposition one width further: 5x31 (K0844) -> 5x32; witness-free width set {19,...,31} -> {19,...,32}"
artifacts:
- path: research/experiments/five-row-q7-m32-class-split-20261115/scripts/sat3.js
  role: solver
  note: "class-split / exact-count (--krow) / minpos / lex encoder on the K0810 sat.js census + sat2.js counter core (byte-identical to the K0821..K0844 lanes; git blob shas 6c3262d6 / edfae1d2 / 6dfa7db3), plus kissat model decoding with census-free verifyConfig"
- path: research/experiments/five-row-q7-m32-class-split-20261115/scripts/mkcnf.sh
  role: source
  note: "deterministic CNF generator: 17 direct classes + {0},{1} k=0..4 + k=5 x minpos=0..15 (the m=32 sound bound stays floor((m-1)/2)=15, 16 points per class) + 2 lex=H + 5x18 control (62 CNFs)"
- path: research/experiments/five-row-q7-m32-class-split-20261115/scripts/qrun.sh
  role: source
  note: "2-worker claim-directory queue runner with per-instance timeout caps and interrupted-instance reclaim"
- path: research/experiments/five-row-q7-m32-class-split-20261115/scripts/mkrecords5732.js
  role: source
  note: "records.jsonl / summary.json builder from raw kissat logs (log-name templates match the pushed raw-log names; no c prefix, per the m=30 lane lesson)"
- path: research/experiments/five-row-q7-m32-class-split-20261115/records.jsonl
  role: data
  note: "62 records: 17 direct class UNSAT + 42 k/minpos decomposition UNSAT ({0},{1}: k=0..4 and k=5 x minpos=0..15, 16 points per class at m=32) + 2 lex=H cross-checks + 1 positive control (SAT); deciding-instance conflicts 6,569,505, records total 7,273,321"
- path: research/experiments/five-row-q7-m32-class-split-20261115/summary.json
  role: data
  note: "aggregate: 0 SAT / 0 INDET among the 59 deciding instances; hardest {1} k=5 mp=0 (670,375 conflicts — up 2.4% from its m=31 counterpart, the only local non-decrease); total_conflicts_32 6,930,187 = deciding 6,569,505 + lex=H 360,682 (same convention as m=27..m=31); decomposition soundness note (minpos pins the leftmost stone of the first deficient row; sound bound floor((m-1)/2)=15 at m=32: columns 0..31, min(x_min, 31-x_max) <= 15); environment note (single continuous session)"
- path: research/experiments/five-row-q7-m32-class-split-20261115/report.md
  role: proof
  note: "claim, coverage and decomposition-completeness argument (k partitions the row count; leftmost stone column <= 15 by the column mirror: x_min + (31 - x_max) <= 31), verification protocol incl. the eleventh cross-lane bit-exact control reproduction, per-class results, scope and limits"
- path: research/experiments/five-row-q7-m32-class-split-20261115/raw/r5x32q7_1k5p0.txt
  role: data
  note: "hardest deciding instance raw kissat log ({1} k=5 minpos=0: 670,375 conflicts UNSAT / 25.66 s); all raw logs r5x32q7_*.txt (17 direct + 42 decomposition + 2 lex + control)"
- path: research/experiments/five-row-q7-m32-class-split-20261115/raw/r_ctrl_5x18_c0.txt
  role: data
  note: "positive control log: 5x18 class {0} SAT 343,134 conflicts bit-exact with the K0821..K0844 lane controls (eleventh cross-lane reproduction); decoded 29 stones rows (5,6,6,6,6), census-free verifyConfig PASS (K0332 witness rediscovered end-to-end)"
scope: "'finite machine verification (kissat 4.0.4: 59 UNSAT instances + 2 lex=H cross-encoding re-checks + positive control); 5x32 q=7 only.'"
evidence: "'complete-enumeration-by-class-split (verification: deterministic-machine + independent-encoding-cross-check + eleventh cross-lane bit-exact control reproduction + decomposition protocol brute-force-validated in K0816/K0818). See report.md.'"
---

# 5x32 q=7 row-deficient maximal nonexistence — all 19 canonical classes UNSAT

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
     stone count; hardest {1} k=4: 357,539 / {0} k=4: 277,605; krow total
     857,057) and k = 5 × minpos = 0..15 (16 points — the m=32 sound
     bound stays floor((m−1)/2) = 15: for columns 0..31, min(x_min,
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
   exactly 30 stones with row occupancy (6,6,6,6,6).
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
  are byte-identical to the K0836..K0844 lane scripts (git blob shas
  6c3262d6 / edfae1d2 / 6dfa7db3 matching the main copies; md5 re-verified
  against the local m=31 lane; the control CNF c5x18q7_0.cnf regenerates
  md5-identical); mkcnf.sh and qrun.sh ported m=31 -> m=32 with no
  residual identifiers (verified by grep); records/summary aggregates
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
