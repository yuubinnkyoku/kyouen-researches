---
id: K0846
title: "5x33 q=7 row-deficient maximal nonexistence (all 19 canonical classes UNSAT) — witness-free width set of (5,7) extends to {19,20,21,22,23,24,25,26,27,28,29,30,31,32,33}, M_{5,7} = 19 or >= 35"
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
  note: "5x18 29-stone witness is the lower bound (least witness width 18) and the positive-control board (rediscovered SAT, 343,134 conflicts, bit-exact with the K0821..K0845 lane controls — twelfth cross-lane reproduction)"
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
  note: "the m=31 nonexistence item; this lane reuses its scripts byte-identically and its control reproduces bit-exactly"
- type: depends_on
  target: K0845
  note: "the m=32 nonexistence item; this lane copies its scripts (blob shas 6c3262d6 / edfae1d2 / 6dfa7db3, restored from main after an environment reset) and ports mkcnf.sh/qrun.sh/mkrecords m=32 -> m=33, extends the witness-free width set {19,...,32} -> {19,...,33} and moves the frontier to 5x34"
- type: depends_on
  target: K0738
  note: "5x19 witness-free by the occupancy complete enumeration (via the K0759 machine) — the first element of the witness-free width set"
- type: generalizes
  target: K0845
  note: "the same class-split proposition one width further: 5x32 (K0845) -> 5x33; witness-free width set {19,...,32} -> {19,...,33}"
artifacts:
- path: research/experiments/five-row-q7-m33-class-split-20261115/scripts/sat3.js
  role: solver
  note: "class-split / exact-count (--krow) / minpos / lex encoder on the K0810 sat.js census + sat2.js counter core (byte-identical to the K0821..K0845 lanes; git blob shas 6c3262d6 / edfae1d2 / 6dfa7db3), plus kissat model decoding with census-free verifyConfig"
- path: research/experiments/five-row-q7-m33-class-split-20261115/scripts/mkcnf.sh
  role: source
  note: "deterministic CNF generator: 17 direct classes + {0},{1} k=0..4 + k=5 x minpos=0..16 (the m=33 sound bound grows to floor((m-1)/2)=16, 17 points per class) + 2 lex=H + 5x18 control (64 CNFs)"
- path: research/experiments/five-row-q7-m33-class-split-20261115/scripts/qrun.sh
  role: source
  note: "2-worker claim-directory queue runner with per-instance timeout caps and interrupted-instance reclaim"
- path: research/experiments/five-row-q7-m33-class-split-20261115/scripts/mkrecords5733.js
  role: source
  note: "records.jsonl / summary.json builder from raw kissat logs (log-name templates match the pushed raw-log names; no c prefix, per the m=30 lane lesson)"
- path: research/experiments/five-row-q7-m33-class-split-20261115/records.jsonl
  role: data
  note: "64 records: 17 direct class UNSAT + 44 k/minpos decomposition UNSAT ({0},{1}: k=0..4 and k=5 x minpos=0..16, 17 points per class at m=33) + 2 lex=H cross-checks + 1 positive control (SAT); deciding-instance conflicts 6,140,609, records total 6,824,711"
- path: research/experiments/five-row-q7-m33-class-split-20261115/summary.json
  role: data
  note: "aggregate: 0 SAT / 0 INDET among the 61 deciding instances; hardest {1} k=5 mp=0 (651,985 conflicts — down 2.7% from its m=32 counterpart); total_conflicts_33 6,481,577 = deciding 6,140,609 + lex=H 340,968 (same convention as m=27..m=32); decomposition soundness note (minpos pins the leftmost stone of the first deficient row; sound bound floor((m-1)/2)=16 at m=33: columns 0..32, min(x_min, 32-x_max) <= 16); environment note (batch-1 pre-reset byte-exact on main, batches 2-4 post-reset with scripts restored from main, kissat re-downloaded md5-verified, CNFs regenerated, control 343,134 and {0,1} 334,184 reproduced bit-exactly)"
- path: research/experiments/five-row-q7-m33-class-split-20261115/report.md
  role: proof
  note: "claim, coverage and decomposition-completeness argument (k partitions the row count; leftmost stone column <= 16 by the column mirror: x_min + (32 - x_max) <= 32), verification protocol incl. the twelfth cross-lane bit-exact control reproduction and the cross-reset calibration, per-class results, scope and limits"
- path: research/experiments/five-row-q7-m33-class-split-20261115/raw/r5x33q7_1k5p0.txt
  role: data
  note: "hardest deciding instance raw kissat log ({1} k=5 minpos=0: 651,985 conflicts UNSAT / 25.39 s); all raw logs r5x33q7_*.txt (17 direct + 44 decomposition + 2 lex + control)"
- path: research/experiments/five-row-q7-m33-class-split-20261115/raw/r_ctrl_5x18_c0.txt
  role: data
  note: "positive control log: 5x18 class {0} SAT 343,134 conflicts bit-exact with the K0821..K0845 lane controls (twelfth cross-lane reproduction); decoded 29 stones rows (5,6,6,6,6), census-free verifyConfig PASS (K0332 witness rediscovered end-to-end)"
scope: "'finite machine verification (kissat 4.0.4: 61 UNSAT instances + 2 lex=H cross-encoding re-checks + positive control); 5x33 q=7 only.'"
evidence: "'complete-enumeration-by-class-split (verification: deterministic-machine + independent-encoding-cross-check + twelfth cross-lane bit-exact control reproduction + cross-reset bit-exact calibration + decomposition protocol brute-force-validated in K0816/K0818). See report.md.'"
---

# 5x33 q=7 row-deficient maximal nonexistence — all 19 canonical classes UNSAT

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
