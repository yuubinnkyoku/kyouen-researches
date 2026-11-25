---
id: K0847
title: "5x34 q=7 row-deficient maximal nonexistence (all 19 canonical classes UNSAT) — witness-free width set of (5,7) extends to {19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34}, M_{5,7} = 19 or >= 36"
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
  note: "5x18 29-stone witness is the lower bound (least witness width 18) and the positive-control board (rediscovered SAT, 343,134 conflicts, bit-exact with the K0821..K0846 lane controls — thirteenth cross-lane reproduction)"
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
  note: "the m=23 nonexistence item; its mid-sweep environment-reset bit-exact re-run reconciliation protocol (not needed this lane: single continuous session)"
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
  note: "the m=32 nonexistence item; this lane reuses its scripts byte-identically and its control reproduces bit-exactly"
- type: depends_on
  target: K0846
  note: "the m=33 nonexistence item; this lane copies its scripts (restored from main with git blob shas verified) and ports mkcnf.sh/qrun.sh/mkrecords5733->5734 m=33 -> m=34, extends the witness-free width set {19,...,33} -> {19,...,34} and moves the frontier to 5x35"
- type: depends_on
  target: K0738
  note: "5x19 witness-free by the occupancy complete enumeration (via the K0759 machine) — the first element of the witness-free width set"
- type: generalizes
  target: K0846
  note: "the same class-split proposition one width further: 5x33 (K0846) -> 5x34; witness-free width set {19,...,33} -> {19,...,34}"
artifacts:
- path: research/experiments/five-row-q7-m34-class-split-20261115/scripts/sat3.js
  role: solver
  note: "class-split / exact-count (--krow) / minpos / lex encoder on the K0810 sat.js census + sat2.js counter core (byte-identical to the K0821..K0846 lanes; git blob shas 6c3262d6 / edfae1d2 / 6dfa7db3), plus kissat model decoding with census-free verifyConfig"
- path: research/experiments/five-row-q7-m34-class-split-20261115/scripts/mkcnf.sh
  role: source
  note: "deterministic CNF generator: 17 direct classes + {0},{1} k=0..4 + k=5 x minpos=0..16 (the m=34 sound bound stays floor((m-1)/2)=16, 17 points per class) + 2 lex=H + 5x18 control (64 CNFs)"
- path: research/experiments/five-row-q7-m34-class-split-20261115/scripts/qrun.sh
  role: source
  note: "2-worker claim-directory queue runner with per-instance timeout caps and interrupted-instance reclaim"
- path: research/experiments/five-row-q7-m34-class-split-20261115/scripts/mkrecords5734.js
  role: source
  note: "records.jsonl / summary.json builder from raw kissat logs (log-name templates match the pushed raw-log names; no c prefix, per the m=30 lane lesson)"
- path: research/experiments/five-row-q7-m34-class-split-20261115/records.jsonl
  role: data
  note: "64 records: 17 direct class UNSAT + 44 k/minpos decomposition UNSAT ({0},{1}: k=0..4 and k=5 x minpos=0..16, 17 points per class at m=34) + 2 lex=H cross-checks + 1 positive control (SAT); deciding-instance conflicts 5,928,015, records total 6,607,549"
- path: research/experiments/five-row-q7-m34-class-split-20261115/summary.json
  role: data
  note: "aggregate: 0 SAT / 0 INDET among the 61 deciding instances; hardest {1} k=5 mp=0 (574,663 conflicts — down 11.9% from its m=33 counterpart); total_conflicts_34 6,264,415 = deciding 5,928,015 + lex=H 336,400 (same convention as m=27..m=33); decomposition soundness note (minpos pins the leftmost stone of the first deficient row; sound bound floor((m-1)/2)=16 at m=34: columns 0..33, min(x_min, 33-x_max) <= 16); environment note (single continuous session, no reset; all 64 raw-log remote blob shas verified against local sha1s, 64/64 OK)"
- path: research/experiments/five-row-q7-m34-class-split-20261115/report.md
  role: proof
  note: "claim, coverage and decomposition-completeness argument (k partitions the row count; leftmost stone column <= 16 by the column mirror: x_min + (33 - x_max) <= 33), verification protocol incl. the thirteenth cross-lane bit-exact control reproduction, per-class results, scope and limits"
- path: research/experiments/five-row-q7-m34-class-split-20261115/raw/r5x34q7_1k5p0.txt
  role: data
  note: "hardest deciding instance raw kissat log ({1} k=5 minpos=0: 574,663 conflicts UNSAT / 20.64 s); all raw logs r5x34q7_*.txt (17 direct + 44 decomposition + 2 lex + control)"
- path: research/experiments/five-row-q7-m34-class-split-20261115/raw/r_ctrl_5x18_c0.txt
  role: data
  note: "positive control log: 5x18 class {0} SAT 343,134 conflicts bit-exact with the K0821..K0846 lane controls (thirteenth cross-lane reproduction); decoded 29 stones rows (5,6,6,6,6), census-free verifyConfig PASS (K0332 witness rediscovered end-to-end)"
scope: "'finite machine verification (kissat 4.0.4: 61 UNSAT instances + 2 lex=H cross-encoding re-checks + positive control); 5x34 q=7 only.'"
evidence: "'complete-enumeration-by-class-split (verification: deterministic-machine + independent-encoding-cross-check + thirteenth cross-lane bit-exact control reproduction + decomposition protocol brute-force-validated in K0816/K0818). See report.md.'"
---

# 5x34 q=7 row-deficient maximal nonexistence — all 19 canonical classes UNSAT

## Claim

1. On the 5x34 integer grid (q=7), for each of the 19 row-mirror-canonical
   deficiency classes D ⊆ {0..4} (canonical representatives of the 31
   non-empty subsets under y -> 4-y), the class-split SAT instance — rows in
   D hold at most 5 stones, rows outside D hold exactly 6 (safety caps every
   row at 6 since a row is a line of length 34 ≥ q), safety ≤ 6 stones per
   census curve, maximality (every empty cell covered by a ≥6-stone curve) —
   is **UNSAT**:
   - 17/19 classes directly UNSAT (kissat 4.0.4, exit 20; hardest {0,1}:
     296,276 conflicts — down 11.3% from its m=33 counterpart 334,184, so
     the m=33 direct-hardest non-decrease was transient; direct total
     1,743,108 — down 3.4% from m=33 1,804,062, the m=33 direct-total
     non-decrease did not continue: 5,256,816 → 4,673,619 → 4,160,006 →
     3,534,969 → 3,307,565 → 2,656,426 → 2,503,468 → 2,261,532 →
     1,960,401 → 1,916,295 → 1,735,912 → 1,804,062 → 1,743,108).
   - {0} and {1}: decided by the **complete k × minpos decomposition**
     (the K0816/K0821/K0834..K0846 protocol): k = 0..4 (exact deficient-row
     stone count; hardest {1} k=4: 349,040 / {0} k=4: 200,212; krow total
     726,502) and k = 5 × minpos = 0..16 (17 points — the m=34 sound bound
     stays floor((m−1)/2) = 16: for columns 0..33, min(x_min,
     33−x_max) ≤ 16 since x_min ≤ x_max; {0}k5p total 1,464,826 / {1}k5p
     total 1,993,579). All 34 sub-instances UNSAT (hardest: {1} k=5 mp=0:
     574,663 conflicts / 20.64 s — down 11.9% from its m=33 counterpart
     651,985; {0} k=5 mp=0: 398,074 — down 10.9% from its m=33 counterpart
     446,878, ending the two-run k5p0 non-decrease streak).
   - Total conflicts across the 61 deciding instances: **5,928,015** (17
     direct: 1,743,108; 10 krow: 726,502; 34 k=5 × minpos: 3,458,405);
     lex=H cross-checks add 336,400 ({0,1}: 249,695 / {2}: 86,705);
     records total 6,607,549. No SAT, no INDET among the deciding
     instances.
2. Coverage: every deficient maximal safe configuration has a non-empty
   exact deficiency set D, the exact-D instances partition them, and
   row-mirror soundness reduces 31 classes to 19. The k × minpos
   decomposition is exhaustive: k = 0..5 partitions the deficient row's
   stone count; for k = 5 the minpos split pins the leftmost stone of
   the first deficient row at column exactly P, and every configuration
   or its column mirror has leftmost stone column ≤ 16 at m = 34 (x_min +
   (33 − x_max) ≤ 33); the column mirror preserves row occupancy, hence
   the class. Therefore **no row-deficient maximal safe configuration
   exists on 5x34**; since a row of length 34 is a line and safety caps
   every row at 6 stones, every maximal safe configuration on 5x34 has
   exactly 30 stones with row occupancy (6,6,6,6,6) — no safe
   configuration can use the extra column capacity beyond the 6-per-row
   cap.
3. Combined with K0738–K0759 (5x19 witness-free), K0816 (5x20), K0821
   (5x21), K0834 (5x22 witness-free), K0835 (5x23 witness-free), K0836
   (5x24 witness-free), K0837 (5x25 witness-free), K0838 (5x26
   witness-free), K0839 (5x27 witness-free), K0840 (5x28 witness-free),
   K0841 (5x29 witness-free), K0842 (5x30 witness-free), K0844 (5x31
   witness-free), K0845 (5x32 witness-free), K0846 (5x33 witness-free)
   and K0332 (29-stone witness at 5x18, least witness width 18): the
   witness-free width set of (5,7) is
   **{19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34}**, so in
   the set form **M_{5,7} ∈ {19,...,34} or M_{5,7} ≥ 35**, sharpened to
   **M_{5,7} = 19 or M_{5,7} ≥ 36** (widths 20–34 are verified
   witness-free and cannot be the threshold; M = 35 would require a
   witness at the verified witness-free width 34, so the next possible
   witness sits at w ≥ 35, forcing M = w + 1 ≥ 36); the upper bound 158
   (K0332/K0024 substitution) is unchanged. The witness-search frontier
   moves to 5x35.

## Verification

- Positive control: 5x18 q=7 class {0} SAT — 343,134 conflicts, bit-exact
  with the K0821, K0834, K0835, K0836, K0837, K0838, K0839, K0840, K0841,
  K0842, K0844, K0845 and K0846 lane control runs (thirteenth cross-lane
  reproduction); decoded model 29 stones rows (5,6,6,6,6) passes the
  census-free `verifyConfig` independent verifier (K0332 witness board
  rediscovered end-to-end through the same encoder+solver path).
- Cross-encoding: {0,1} and {2} re-encoded with --lex=H (column-reflection
  lex-leader — class-preserving, hence sound) are UNSAT again (249,695 /
  86,705 conflicts).
- Environment: single continuous session, no reset. sat.js/sat2.js/sat3.js
  restored from the m=33 lane on main with git blob shas verified
  (6c3262d6 / edfae1d2 / 6dfa7db3) and byte-identical to the K0836..K0846
  lane scripts; the control CNF c5x18q7_0.cnf regenerates md5-identical
  and the control run reproduced 343,134 conflicts bit-exactly before the
  sweep; mkcnf.sh and qrun.sh ported m=33 -> m=34 with no residual
  identifiers (verified by grep); all 64 raw logs were pushed batch-by-
  batch (batch-1 commit b0efe01a, batch-2 6a12b8db, batch-3 8e7a1f1a,
  batch-4 f6822486) and every remote blob sha was verified against the
  local sha1 (64/64 OK); records/summary aggregates recomputed
  independently from records.jsonl (direct 1,743,108 + krow 726,502 +
  k5p 3,458,405 = deciding 5,928,015).
- The deciding-instance difficulty keeps decreasing on average: deciding
  totals m=23→34: 20,916,467 → 17,349,736 → 15,521,919 → 13,845,697 →
  11,363,141 → 10,218,568 → 8,677,594 → 7,809,347 → 7,275,763 →
  6,569,505 → 6,140,609 → 5,928,015 (the pre-run projection ~5.7M was
  accurate to 4%). All three m=33 local exceptions (direct-hardest +16.5%,
  direct-total +3.9%, {0} k5p0 +0.7%) reversed to decreases at m=34.

## Scope

Finite machine verification up to the correctness of the K0810 census, the
class-split encoding and the k×minpos decomposition (protocol
brute-force-validated on small boards in K0816/K0818), and kissat 4.0.4;
not a number-theoretic proof. Persistence at m ≥ 35 remains open: exact
M_{5,7} needs witness-free verification for all widths up to U=158 or a
universal tail argument. The witness frontier moves to 5x35 (a witness
there gives M ≥ 36; witness-free there extends the free set to
{19,...,35}). At m=35 the minpos sound bound grows to floor((35−1)/2) = 17
(columns 0..34: min(x_min, 34−x_max) ≤ 17 — 18 points per class, the CNF
set grows to 66). The 11x11 empty board, two-stone root {49,60}, S2
{59,60}, class 2 and class 4 are unaffected and remain UNKNOWN.
