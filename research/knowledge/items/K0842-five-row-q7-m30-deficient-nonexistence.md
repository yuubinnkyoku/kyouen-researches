---
id: K0842
title: "5x30 q=7 row-deficient maximal nonexistence (all 19 canonical classes UNSAT) — witness-free width set of (5,7) extends to {19,20,21,22,23,24,25,26,27,28,29,30}, M_{5,7} = 19 or >= 32"
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
  note: "5x18 29-stone witness is the lower bound (least witness width 18) and the positive-control board (rediscovered SAT, 343,134 conflicts, bit-exact with the K0821..K0841 lane controls — ninth cross-lane reproduction, run twice: pre-reset batch-1 and post-reset calibration, both bit-exact)"
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
  note: "the m=29 nonexistence item; this lane restores its scripts byte-identically (sat.js/sat2.js/sat3.js via main, git blob sha verified; mkcnf.sh/qrun.sh ported m=29 -> m=30), extends the witness-free width set {19,...,29} -> {19,...,30} and moves the frontier to 5x31"
- type: depends_on
  target: K0738
  note: "5x19 witness-free by the occupancy complete enumeration (via the K0759 machine) — the first element of the witness-free width set"
- type: generalizes
  target: K0841
  note: "the same class-split proposition one width further: 5x29 (K0841) -> 5x30; witness-free width set {19,...,29} -> {19,...,30}"
artifacts:
- path: research/experiments/five-row-q7-m30-class-split-20261115/scripts/sat3.js
  role: solver
  note: "class-split / exact-count (--krow) / minpos / lex encoder on the K0810 sat.js census + sat2.js counter core (byte-identical to the K0821..K0841 lanes, restored from the m=29 lane via main), plus kissat model decoding with census-free verifyConfig"
- path: research/experiments/five-row-q7-m30-class-split-20261115/scripts/mkcnf.sh
  role: source
  note: "deterministic CNF generator: 17 direct classes + {0},{1} k=0..4 + k=5 x minpos=0..14 (the m=30 sound bound stays floor((m-1)/2)=14, 15 points per class) + 2 lex=H + 5x18 control (60 CNFs)"
- path: research/experiments/five-row-q7-m30-class-split-20261115/scripts/qrun.sh
  role: source
  note: "2-worker claim-directory queue runner with per-instance timeout caps and interrupted-instance reclaim"
- path: research/experiments/five-row-q7-m30-class-split-20261115/scripts/mkrecords5730.js
  role: source
  note: "records.jsonl / summary.json builder from raw kissat logs (log-name templates match the pushed raw-log names)"
- path: research/experiments/five-row-q7-m30-class-split-20261115/records.jsonl
  role: data
  note: "60 records: 17 direct class UNSAT + 40 k/minpos decomposition UNSAT ({0},{1}: k=0..4 and k=5 x minpos=0..14, 15 points per class at m=30) + 2 lex=H cross-checks + 1 positive control (SAT); deciding-instance conflicts 7,809,347, records total 8,553,565"
- path: research/experiments/five-row-q7-m30-class-split-20261115/summary.json
  role: data
  note: "aggregate: 0 SAT / 0 INDET among the 57 deciding instances; hardest {1} k=5 mp=0 (802,385 conflicts — down 5.7% from its m=29 counterpart); total_conflicts_30 8,210,431 = deciding 7,809,347 + lex=H 401,084 (same convention as m=27..m=29); decomposition soundness note (minpos pins the leftmost stone of the first deficient row; sound bound floor((m-1)/2)=14 at m=30: columns 0..29, min(x_min, 29-x_max) <= 14); environment note (full reset between batch-1 and batch-2, cross-reset recovery)"
- path: research/experiments/five-row-q7-m30-class-split-20261115/report.md
  role: proof
  note: "claim, coverage and decomposition-completeness argument (k partitions the row count; leftmost stone column <= 14 by the column mirror: x_min + (29 - x_max) <= 29), verification protocol incl. the ninth cross-lane bit-exact control reproduction and the cross-reset recovery record, per-class results, scope and limits"
- path: research/experiments/five-row-q7-m30-class-split-20261115/raw/r5x30q7_1k5p0.txt
  role: data
  note: "hardest deciding instance raw kissat log ({1} k=5 minpos=0: 802,385 conflicts UNSAT / 31.07 s); all raw logs r5x30q7_*.txt (17 direct + 40 decomposition + 2 lex + control)"
- path: research/experiments/five-row-q7-m30-class-split-20261115/raw/r_ctrl_5x18_c0.txt
  role: data
  note: "positive control log: 5x18 class {0} SAT 343,134 conflicts bit-exact with the K0821..K0841 lane controls (ninth cross-lane reproduction; run twice, pre-reset and as post-reset calibration, both bit-exact); decoded 29 stones rows (5,6,6,6,6), census-free verifyConfig PASS (K0332 witness rediscovered end-to-end)"
scope: "'finite machine verification (kissat 4.0.4: 57 UNSAT instances + 2 lex=H cross-encoding re-checks + positive control); 5x30 q=7 only.'"
evidence: "'complete-enumeration-by-class-split (verification: deterministic-machine + independent-encoding-cross-check + ninth cross-lane bit-exact control reproduction + cross-reset recovery with bit-exact calibration + decomposition protocol brute-force-validated in K0816/K0818). See report.md.'"
---

# 5x30 q=7 row-deficient maximal nonexistence — all 19 canonical classes UNSAT

## Claim

1. On the 5x30 integer grid (q=7), for each of the 19 row-mirror-canonical
   deficiency classes D ⊆ {0..4} (canonical representatives of the 31
   non-empty subsets under y -> 4-y), the class-split SAT instance — rows in
   D hold at most 5 stones, rows outside D hold exactly 6 (safety caps every
   row at 6 since a row is a line of length 30 ≥ q), safety ≤ 6 stones per
   census curve, maximality (every empty cell covered by a ≥6-stone curve) —
   is **UNSAT**:
   - 17/19 classes directly UNSAT (kissat 4.0.4, exit 20; hardest {0,1}:
     388,349 conflicts — up 6.8% from its m=29 counterpart 363,639, the
     first local non-decrease in the direct-hardest series; direct total
     1,960,401 — the m=22..30 direct-total trend stays monotonically
     decreasing: 5,256,816 → 4,673,619 → 4,160,006 → 3,534,969 →
     3,307,565 → 2,656,426 → 2,503,468 → 2,261,532 → 1,960,401).
   - {0} and {1}: decided by the **complete k × minpos decomposition**
     (the K0816/K0821/K0834..K0841 protocol): k = 0..4 (exact deficient-row
     stone count; hardest {1} k=4: 445,772 / {0} k=4: 350,870; krow total
     1,005,289) and k = 5 × minpos = 0..14 (15 points — the m=30 sound
     bound stays floor((m−1)/2) = 14: for columns 0..29, min(x_min,
     29−x_max) ≤ 14 since x_min ≤ x_max; {0}k5p total 2,040,624 / {1}k5p
     total 2,803,033). All 40 sub-instances UNSAT (hardest: {1} k=5 mp=0:
     802,385 conflicts / 31.07 s — down 5.7% from its m=29 counterpart
     850,480, so the k5p0 series is decreasing again; {0} k=5 mp=0:
     545,523 — below its m=29 counterpart 690,557).
   - Total conflicts across the 57 deciding instances: **7,809,347** (17
     direct: 1,960,401; 10 krow: 1,005,289; 30 k=5 × minpos: 4,843,657);
     lex=H cross-checks add 401,084 ({0,1}: 276,589 / {2}: 124,495);
     records total 8,553,565. No SAT, no INDET among the deciding
     instances.
2. Coverage: every deficient maximal safe configuration has a non-empty
   exact deficiency set D, the exact-D instances partition them, and
   row-mirror soundness reduces 31 classes to 19. The k × minpos
   decomposition is exhaustive: k = 0..5 partitions the deficient row's
   stone count; for k = 5 the minpos split pins the leftmost stone of the
   first deficient row at column exactly P, and every configuration or its
   column mirror has leftmost stone column ≤ 14 at m = 30 (x_min +
   (29 − x_max) ≤ 29); the column mirror preserves row occupancy, hence
   the class. Therefore **no row-deficient maximal safe configuration
   exists on 5x30**; every maximal safe configuration on 5x30 has exactly
   30 stones (row occupancy (6,6,6,6,6)).
3. Combined with K0738–K0759 (5x19 witness-free), K0816 (5x20), K0821
   (5x21), K0834 (5x22 witness-free), K0835 (5x23 witness-free), K0836
   (5x24 witness-free), K0837 (5x25 witness-free), K0838 (5x26
   witness-free), K0839 (5x27 witness-free), K0840 (5x28 witness-free),
   K0841 (5x29 witness-free) and K0332 (29-stone witness at 5x18, least
   witness width 18): the witness-free width set of (5,7) is
   **{19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30}**, so in the set form
   **M_{5,7} ∈ {19,...,30} or M_{5,7} ≥ 31**, sharpened to **M_{5,7} = 19
   or M_{5,7} ≥ 32** (widths 20–30 are verified witness-free and cannot be
   the threshold; M = 31 would require a witness at the verified
   witness-free width 30, so the next possible witness sits at w ≥ 31,
   forcing M = w + 1 ≥ 32); the upper bound 158 (K0332/K0024
   substitution) is unchanged. The witness-search frontier moves to 5x31.

## Verification

- Positive control: 5x18 q=7 class {0} SAT — 343,134 conflicts, bit-exact
  with the K0821, K0834, K0835, K0836, K0837, K0838, K0839, K0840 and
  K0841 lane control runs (ninth cross-lane reproduction); the control was
  run twice — pre-reset in batch-1 and again as post-reset calibration —
  and both runs are 343,134 conflicts, bit-exact; decoded model 29 stones
  rows (5,6,6,6,6) passes the census-free `verifyConfig` independent
  verifier (K0332 witness board rediscovered end-to-end through the same
  encoder+solver path).
- Cross-encoding: {0,1} and {2} re-encoded with --lex=H (column-reflection
  lex-leader — class-preserving, hence sound) are UNSAT again (276,589 /
  124,495 conflicts).
- Environment: a full execution-environment reset occurred between
  batch-1 and batch-2 (the workspace, kissat binary and all local files
  were lost). Recovery followed the established cross-reset protocol:
  batch-1 raw logs (17 direct + 2 lex=H + control) are byte-exact on main
  and were restored from main; scripts restored byte-identically
  (sat.js/sat2.js/sat3.js from the m=29 lane via main, git blob sha
  verified); kissat 4.0.4 re-downloaded from the official rel-4.0.4
  release asset (same version hash 8af8e56f174b778aef3aa45af9f739b2a5f492c2);
  all 60 CNFs regenerated deterministically; calibration reproduced c2
  (103,993) and the control (343,134) bit-exactly before continuing with
  batch-2.
- The deciding-instance difficulty keeps decreasing overall: deciding
  totals m=23→30: 20,916,467 → 17,349,736 → 15,521,919 → 13,845,697 →
  11,363,141 → 10,218,568 → 8,677,594 → 7,809,347 (the m=30 sweep is the
  easiest of the series so far; two local non-decreases at m=30 —
  direct-hardest {0,1} +6.8% and {1}k5p2 above its m=29 counterpart — do
  not change the totals trend).

## Scope

Finite machine verification up to the correctness of the K0810 census, the
class-split encoding and the k×minpos decomposition (protocol
brute-force-validated on small boards in K0816/K0818), and kissat 4.0.4;
not a number-theoretic proof. Persistence at m ≥ 31 remains open: exact
M_{5,7} needs witness-free verification for all widths up to U=158 or a
universal tail argument. The witness frontier moves to 5x31 (a witness
there gives M ≥ 32; witness-free there extends the free set to
{19,...,31}). At m=31 the minpos sound bound grows to floor((31−1)/2) = 15
(columns 0..30: min(x_min, 30−x_max) ≤ 15 — 16 points per class, the CNF
set grows to 62). The 11x11 empty board, two-stone root {49,60}, S2
{59,60}, class 2 and class 4 are unaffected and remain UNKNOWN.
