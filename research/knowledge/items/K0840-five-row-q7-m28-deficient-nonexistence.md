---
id: K0840
title: "5x28 q=7 row-deficient maximal nonexistence (all 19 canonical classes UNSAT) — witness-free width set of (5,7) extends to {19,20,21,22,23,24,25,26,27,28}, M_{5,7} = 19 or >= 30"
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
  note: "5x18 29-stone witness is the lower bound (least witness width 18) and the positive-control board (rediscovered SAT, 343,134 conflicts, bit-exact with the K0821..K0839 lane controls — seventh cross-lane reproduction)"
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
  note: "the m=27 nonexistence item; this lane restores its scripts byte-identically (git blob sha verified on main), extends the witness-free width set {19,...,27} -> {19,...,28} and moves the frontier to 5x29"
- type: depends_on
  target: K0738
  note: "5x19 witness-free by the occupancy complete enumeration (via the K0759 machine) — the first element of the witness-free width set"
- type: generalizes
  target: K0839
  note: "the same class-split proposition one width further: 5x27 (K0839) -> 5x28; witness-free width set {19,...,27} -> {19,...,28}"
artifacts:
- path: research/experiments/five-row-q7-m28-class-split-20261115/scripts/sat3.js
  role: solver
  note: "class-split / exact-count (--krow) / minpos / lex encoder on the K0810 sat.js census + sat2.js counter core (byte-identical to the K0821..K0839 lanes, restored from the m=27 lane directory), plus kissat model decoding with census-free verifyConfig"
- path: research/experiments/five-row-q7-m28-class-split-20261115/scripts/mkcnf.sh
  role: source
  note: "deterministic CNF generator: 17 direct classes + {0},{1} k=0..4 + k=5 x minpos=0..13 (the m=28 sound bound stays floor((m-1)/2)=13, 14 points per class) + 2 lex=H + 5x18 control (58 CNFs)"
- path: research/experiments/five-row-q7-m28-class-split-20261115/scripts/qrun.sh
  role: source
  note: "2-worker claim-directory queue runner with per-instance timeout caps and interrupted-instance reclaim"
- path: research/experiments/five-row-q7-m28-class-split-20261115/scripts/mkrecords5728.js
  role: source
  note: "records.jsonl / summary.json builder from raw kissat logs"
- path: research/experiments/five-row-q7-m28-class-split-20261115/output/records.jsonl
  role: data
  note: "58 records: 17 direct class UNSAT + 38 k/minpos decomposition UNSAT ({0},{1}: k=0..4 and k=5 x minpos=0..13, 14 points per class at m=28) + 2 lex=H cross-checks + 1 positive control (SAT); deciding-instance conflicts 10,218,568, records total 11,025,625"
- path: research/experiments/five-row-q7-m28-class-split-20261115/output/summary.json
  role: data
  note: "aggregate: 0 SAT / 0 INDET among the 53 deciding instances; hardest {1} k=5 mp=0 (1,469,014 conflicts — up 6.6% from its m=27 counterpart, the only local exception to the decreasing trend); decomposition soundness note (minpos pins the leftmost stone of the first deficient row; sound bound floor((m-1)/2)=13 at m=28: columns 0..27, min(x_min, 27-x_max) <= 13)"
- path: research/experiments/five-row-q7-m28-class-split-20261115/report.md
  role: proof
  note: "claim, coverage and decomposition-completeness argument (k partitions the row count; leftmost stone column <= 13 by the column mirror: x_min + (27-x_max) <= 27), verification protocol incl. the seventh cross-lane bit-exact control reproduction, per-class results, scope and limits"
- path: research/experiments/five-row-q7-m28-class-split-20261115/output/r5x28q7_1k5p0.txt
  role: data
  note: "hardest deciding instance raw kissat log ({1} k=5 minpos=0: 1,469,014 conflicts UNSAT / 56.59 s); all raw logs r5x28q7_*.txt (17 direct + 38 decomposition + 2 lex + control)"
- path: research/experiments/five-row-q7-m28-class-split-20261115/output/r_ctrl_5x18_c0.txt
  role: data
  note: "positive control log: 5x18 class {0} SAT 343,134 conflicts bit-exact with the K0821/K0834/K0835/K0836/K0837/K0838/K0839 lane controls (seventh cross-lane reproduction); decoded 29 stones rows (5,6,6,6,6), census-free verifyConfig PASS (K0332 witness rediscovered end-to-end)"
scope: "'finite machine verification (kissat 4.0.4: 53 UNSAT instances + 2 lex=H cross-encoding re-checks + positive control); 5x28 q=7 only.'"
evidence: "'complete-enumeration-by-class-split (verification: deterministic-machine + independent-encoding-cross-check + seventh cross-lane bit-exact control reproduction + decomposition protocol brute-force-validated in K0816/K0818). See report.md.'"
---

# 5x28 q=7 row-deficient maximal nonexistence — all 19 canonical classes UNSAT

## Claim

1. On the 5x28 integer grid (q=7), for each of the 19 row-mirror-canonical
   deficiency classes D ⊆ {0..4} (canonical representatives of the 31 non-empty
   subsets under y -> 4-y), the class-split SAT instance — rows in D hold at
   most 5 stones, rows outside D hold exactly 6 (safety caps every row at 6
   since a row is a line of length 28 ≥ q), safety ≤ 6 stones per census curve,
   maximality (every empty cell covered by a ≥6-stone curve) — is **UNSAT**:
   - 17/19 classes directly UNSAT (kissat 4.0.4, exit 20; hardest {0,1}: 389,650
     conflicts; direct total 2,503,468 — the m=22..28 direct difficulty trend is
     monotonically decreasing: 5,256,816 → 4,673,619 → 4,160,006 → 3,534,969 →
     3,307,565 → 2,656,426 → 2,503,468).
   - {0} and {1}: decided by the **complete k × minpos decomposition** (the
     K0816/K0821/K0834..K0839 protocol): k = 0..4 (exact deficient-row stone
     count; hardest {1} k=4: 515,833 / {0} k=4: 483,130) and k = 5 × minpos =
     0..13 (14 points — the m=28 sound bound stays floor((m−1)/2) = 13: for
     columns 0..27, min(x_min, 27−x_max) ≤ 13 since x_min ≤ x_max). All 38
     sub-instances UNSAT (hardest: {1} k=5 mp=0: 1,469,014 conflicts / 56.59 s
     — slightly above its m=27 counterpart 1,378,345, the first non-decrease in
     the k5p0 series; {0} k=5 mp=0: 834,706 — below its m=27 counterpart
     861,966).
   - Total conflicts across the 53 deciding instances: **10,218,568** (17
     direct: 2,503,468; 38 decomposition: 7,715,100); lex=H cross-checks add
     463,923. No SAT, no INDET among the deciding instances.
2. Coverage: every deficient maximal safe configuration has a non-empty exact
   deficiency set D, the exact-D instances partition them, and row-mirror
   soundness reduces 31 classes to 19. The k × minpos decomposition is
   exhaustive: k = 0..5 partitions the deficient row's stone count; for k = 5
   the minpos split pins the leftmost stone of the first deficient row at
   column exactly P, and every configuration or its column mirror has leftmost
   stone column ≤ 13 at m = 28 (x_min + (27 − x_max) ≤ 27); the column mirror
   preserves row occupancy, hence the class. Therefore **no row-deficient
   maximal safe configuration exists on 5x28**; every maximal safe
   configuration on 5x28 has 30 stones (row occupancy (6,6,6,6,6)).
3. Combined with K0738–K0759 (5x19 witness-free), K0816 (5x20), K0821 (5x21),
   K0834 (5x22 witness-free), K0835 (5x23 witness-free), K0836 (5x24
   witness-free), K0837 (5x25 witness-free), K0838 (5x26 witness-free), K0839
   (5x27 witness-free) and K0332 (29-stone witness at 5x18, least witness
   width 18): the witness-free width set of (5,7) is **{19, 20, 21, 22, 23, 24,
   25, 26, 27, 28}**, so in the set form **M_{5,7} ∈ {19,...,28} or M_{5,7} ≥
   29**, sharpened to **M_{5,7} = 19 or M_{5,7} ≥ 30** (widths 20–28 are
   verified witness-free and cannot be the threshold; M = 29 would require a
   witness at the verified witness-free width 28, so the next possible witness
   sits at w ≥ 29, forcing M = w + 1 ≥ 30); the upper bound 158
   (K0332/K0024 substitution) is unchanged. The witness-search frontier moves
   to 5x29.

## Verification

- Positive control: 5x18 q=7 class {0} SAT — 343,134 conflicts, bit-exact with
  the K0821, K0834, K0835, K0836, K0837, K0838 and K0839 lane control runs
  (seventh cross-lane reproduction); decoded model 29 stones rows (5,6,6,6,6)
  passes the census-free `verifyConfig` independent verifier (K0332 witness
  board rediscovered end-to-end through the same encoder+solver path).
- Cross-encoding: {0,1} and {2} re-encoded with --lex=H (column-reflection
  lex-leader — class-preserving, hence sound) are UNSAT again (313,971 /
  149,952 conflicts).
- Single continuous session (no environment reset): scripts restored
  byte-identically from the m=27 lane (git blob sha verified against main), all
  58 CNFs regenerated deterministically, raw logs pushed batch-by-batch
  (batch-1: 17 direct + 2 lexH + control; batch-2: krow k=0..4; batch-3/4: k=5
  × minpos 0..13 per class).
- The deciding-instance difficulty is still decreasing: deciding totals
  m=23→28: 20,916,467 → 17,349,736 → 15,521,919 → 13,845,697 → 11,363,141 →
  10,218,568 (the only local exception is {1} k=5 mp=0, up 6.6% from m=27).

## Scope

Finite machine verification up to the correctness of the K0810 census, the
class-split encoding and the k×minpos decomposition (protocol
brute-force-validated on small boards in K0816/K0818), and kissat 4.0.4; not a
number-theoretic proof. Persistence at m ≥ 29 remains open: exact M_{5,7}
needs witness-free verification for all widths up to U=158 or a universal
tail argument. The witness frontier moves to 5x29 (a witness there gives
M ≥ 30; witness-free there extends the free set to {19,...,29}). At m=29 the
minpos sound bound grows to floor((29-1)/2) = 14 (15 points per class, 30 k=5
sub-instances — the CNF set grows to 60). The 11x11 empty board, two-stone
root {49,60}, S2 {59,60}, class 2 and class 4 are unaffected and remain
UNKNOWN.
