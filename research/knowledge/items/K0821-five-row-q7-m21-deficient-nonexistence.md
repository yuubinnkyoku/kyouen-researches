---
id: K0821
title: "5x21 q=7 row-deficient maximal nonexistence (all 19 canonical classes UNSAT) — witness-free width set of (5,7) extends to {19,20,21}, M_{5,7} ∈ {19,20,21} or >= 23"
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
  note: "5x18 29-stone witness is the lower bound (least witness width 18) and the positive-control board (rediscovered SAT, 343,134 conflicts)"
- type: depends_on
  target: K0816
  note: "the m=20 nonexistence item; the k x minpos decomposition protocol for the hard singleton classes {0},{1} and the 5x18 positive control are taken from its cross-check lane"
- type: depends_on
  target: K0738
  note: "5x19 witness-free by the occupancy complete enumeration (via the K0759 machine) — the first element of the witness-free width set"
- type: generalizes
  target: K0816
  note: "the same class-split proposition one width further: 5x20 (K0816) -> 5x21; witness-free width set {19,20} -> {19,20,21}"
artifacts:
- path: research/experiments/five-row-q7-m21-class-split-20261114/scripts/sat3.js
  role: solver
  note: "class-split / exact-count (--krow) / minpos / lex encoder on the K0810 sat.js census + sat2.js counter core (verbatim from the K0818 lane), plus kissat model decoding with census-free verifyConfig"
- path: research/experiments/five-row-q7-m21-class-split-20261114/scripts/runall57.sh
  role: source
  note: "deterministic sweep driver: 19 classes + k x minpos decomposition for {0},{1} + lex=H cross-checks + 5x18 positive control"
- path: research/experiments/five-row-q7-m21-class-split-20261114/scripts/mkrecords57.js
  role: source
  note: "records.jsonl / summary.json builder from raw kissat logs"
- path: research/experiments/five-row-q7-m21-class-split-20261114/output/records.jsonl
  role: data
  note: "52 records: 17 direct class UNSAT + 32 k/minpos decomposition UNSAT ({0},{1}: k=0..4 and k=5 x minpos=0..10) + 2 lex=H cross-checks + 1 positive control (SAT); total m=21 conflicts 28,617,104"
- path: research/experiments/five-row-q7-m21-class-split-20261114/output/summary.json
  role: data
  note: "aggregate: 0 SAT / 0 INDET among the deciding instances; hardest {0} k=5 mp=0 (3,295,997 conflicts); decomposition soundness note"
- path: research/experiments/five-row-q7-m21-class-split-20261114/report.md
  role: proof
  note: "claim, coverage and decomposition-completeness argument (k partitions the row count; minpos<=10 by the column mirror min(x1,20-x5)<=10), verification protocol, per-class results, scope and limits"
- path: research/experiments/five-row-q7-m21-class-split-20261114/output/r5x21q7_0k5p0.txt
  role: data
  note: "hardest deciding instance raw kissat log ({0} k=5 minpos=0: 3,295,997 conflicts UNSAT); all 51 raw logs r5x21q7_*.txt"
- path: research/experiments/five-row-q7-m21-class-split-20261114/output/r_ctrl_5x18_c0.txt
  role: data
  note: "positive control log: 5x18 class {0} SAT 343,134 conflicts; decoded 29 stones rows (5,6,6,6,6), census-free verifyConfig PASS (K0332 witness rediscovered end-to-end)"
scope: "'finite machine verification (kissat 4.0.4: 49 UNSAT instances + 2 lex=H cross-encoding re-checks + positive control); 5x21 q=7 only.'"
evidence: "'complete-enumeration-by-class-split (verification: deterministic-machine + independent-encoding-cross-check + decomposition protocol brute-force-validated in K0816/K0818). See report.md.'"
---

# 5x21 q=7 row-deficient maximal nonexistence — all 19 canonical classes UNSAT

## Claim

1. On the 5x21 integer grid (q=7), for each of the 19 row-mirror-canonical deficiency classes
   D ⊆ {0..4} (canonical representatives of the 31 non-empty subsets under y -> 4-y), the
   class-split SAT instance — rows in D hold at most 5 stones, rows outside D hold exactly 6
   (safety caps every row at 6 since a row is a line of length 21 ≥ q), safety ≤ 6 stones per
   census curve, maximality (every empty cell covered by a ≥6-stone curve) — is **UNSAT**:
   - 17/19 classes directly UNSAT (kissat 4.0.4, exit 20; hardest {2}: 708,186 conflicts /
     22.2 s; {0,1}: 1,050,634 / 38.8 s).
   - {0} and {1}: the plain instances resisted single 280 s runs (≈6.0M / 5.7M conflicts)
     and are decided by the **complete k × minpos decomposition** (the K0816 protocol):
     k = 0..4 (exact deficient-row stone count) and k = 5 × minpos = 0..10. All 32
     sub-instances UNSAT (hardest: {0} k=5 mp=0: 3,295,997 conflicts / 162.8 s;
     {1} k=5 mp=0: 2,851,122 / 118.2 s).
   - Total conflicts across all deciding m=21 instances: **28,617,104**. No SAT, no INDET
     among the deciding instances.
2. Coverage: every deficient maximal safe configuration has a non-empty exact deficiency
   set D, the exact-D instances partition them, and row-mirror soundness reduces 31 classes
   to 19. The k × minpos decomposition is exhaustive: k = 0..5 partitions the deficient
   row's stone count; for k = 5 every configuration or its column mirror has minpos ≤ 10 at
   m = 21 (min(x1, 20−x5) ≤ 10 — otherwise x1 ≥ 11 and x5 ≤ 9, contradicting x1 ≤ x5); the
   column mirror preserves row occupancy, hence the class. Therefore **no row-deficient
   maximal safe configuration exists on 5x21**; every maximal safe configuration on 5x21
   has 30 stones (row occupancy (6,6,6,6,6)).
3. Combined with K0738–K0759 (5x19 witness-free), K0816 (5x20 witness-free) and K0332
   (29-stone witness at 5x18): the witness-free width set of (5,7) is **{19, 20, 21}**
   (least witness width 18), so **M_{5,7} ∈ {19, 20, 21} or M_{5,7} ≥ 23**; the upper bound
   158 (K0332/K0024 substitution) is unchanged. The witness-search frontier moves to 5x22.

## Verification

- Positive control: 5x18 q=7 class {0} SAT — 343,134 conflicts / 11.5 s; decoded model
  29 stones rows (5,6,6,6,6) passes the census-free `verifyConfig` independent verifier
  (K0332 witness board rediscovered end-to-end through the same encoder+solver path).
- Cross-encoding: {0,1} and {2} re-encoded with --lex=H (column-reflection lex-leader —
  class-preserving, hence sound) are UNSAT again (639,843 / 488,589 conflicts).
- Determinism: the plain {2} instance reproduces 708,186 conflicts bit-exactly across an
  execution-environment reset that occurred mid-session.
- Encoding-path note: a multi-element-class encoding bug (`--class=01` parsed as
  Number("01") = 1) was detected during the sweep by an exact conflict-count collision with
  the singleton {1} instance and fixed before any use; all recorded multi-element classes
  were encoded with the explicit comma form (per-instance `meta.json` keeps the parsed
  class array).

## Scope

Finite machine verification up to the correctness of the K0810 census, the class-split
encoding and the k×minpos decomposition (protocol brute-force-validated on small boards in
K0816/K0818), and kissat 4.0.4; not a number-theoretic proof. Persistence at m ≥ 22 remains
open: exact M_{5,7} needs witness-free verification for all widths up to U=158 or a
universal tail argument. The witness frontier moves to 5x22 (a witness there gives
M ≥ 23; witness-free there extends the free set to {19,20,21,22}). The 11x11 empty board,
two-stone root {49,60}, S2 {59,60}, class 2 and class 4 are unaffected and remain UNKNOWN.
