---
id: K0834
title: "5x22 q=7 row-deficient maximal nonexistence (all 19 canonical classes UNSAT) — witness-free width set of (5,7) extends to {19,20,21,22}, M_{5,7} ∈ {19,20,21,22} or >= 23"
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
  note: "5x18 29-stone witness is the lower bound (least witness width 18) and the positive-control board (rediscovered SAT, 343,134 conflicts, bit-exact with the K0821 lane control)"
- type: depends_on
  target: K0816
  note: "the m=20 nonexistence item; the k x minpos decomposition protocol for the hard singleton classes {0},{1} and the 5x18 positive control are taken from its cross-check lane"
- type: depends_on
  target: K0821
  note: "the m=21 nonexistence item; the completion lane reuses its scripts byte-identically and its control reproduces bit-exactly; witness-free width set {19,20,21} -> {19,20,21,22}"
- type: depends_on
  target: K0738
  note: "5x19 witness-free by the occupancy complete enumeration (via the K0759 machine) — the first element of the witness-free width set"
- type: generalizes
  target: K0821
  note: "the same class-split proposition one width further: 5x21 (K0821) -> 5x22; witness-free width set {19,20,21} -> {19,20,21,22}"
artifacts:
- path: research/experiments/five-row-q7-m22-class-split-20261114/scripts/sat3.js
  role: solver
  note: "class-split / exact-count (--krow) / minpos / lex encoder on the K0810 sat.js census + sat2.js counter core (byte-identical to the K0821 lane), plus kissat model decoding with census-free verifyConfig"
- path: research/experiments/five-row-q7-m22-class-split-20261114/scripts/runall5722.sh
  role: source
  note: "deterministic completion driver: 17 direct class bit-exact re-runs + k x minpos decomposition for {0},{1} + lex=H cross-checks + 5x18 positive control + records build"
- path: research/experiments/five-row-q7-m22-class-split-20261114/scripts/mkrecords5722.js
  role: source
  note: "records.jsonl / summary.json builder from raw kissat logs (batch-1 direct logs + completion-lane decomposition/lex/control logs)"
- path: research/experiments/five-row-q7-m22-class-split-20261114/output/records.jsonl
  role: data
  note: "52 records: 17 direct class UNSAT (batch-1 logs, re-verified bit-exact) + 32 k/minpos decomposition UNSAT ({0},{1}: k=0..4 and k=5 x minpos=0..10) + 2 lex=H cross-checks + 1 positive control (SAT); deciding-instance conflicts 24,581,763, records total 25,519,268"
- path: research/experiments/five-row-q7-m22-class-split-20261114/output/summary.json
  role: data
  note: "aggregate: 0 SAT / 0 INDET among the deciding instances; hardest {0} k=5 mp=0 (3,380,578 conflicts); decomposition soundness note (minpos pins the leftmost stone of the first deficient row; column mirror covers the left half)"
- path: research/experiments/five-row-q7-m22-class-split-20261114/report.md
  role: proof
  note: "claim, coverage and decomposition-completeness argument (k partitions the row count; leftmost stone column <= 10 by the column mirror min(x1,21-x5)<=10), verification protocol incl. the batch-1 bit-exact reconciliation, per-class results, scope and limits"
- path: research/experiments/five-row-q7-m22-class-split-20261114/output/r5x22q7_0k5p0.txt
  role: data
  note: "hardest deciding instance raw kissat log ({0} k=5 minpos=0: 3,380,578 conflicts UNSAT / 153.8 s); all raw logs r5x22q7_*.txt (19 direct from batch-1 + 32 decomposition + 2 lex + control)"
- path: research/experiments/five-row-q7-m22-class-split-20261114/output/r_ctrl_5x18_c0.txt
  role: data
  note: "positive control log: 5x18 class {0} SAT 343,134 conflicts bit-exact with the K0821 lane control; decoded 29 stones rows (5,6,6,6,6), census-free verifyConfig PASS (K0332 witness rediscovered end-to-end)"
scope: "'finite machine verification (kissat 4.0.4: 49 UNSAT instances + 2 lex=H cross-encoding re-checks + positive control); 5x22 q=7 only.'"
evidence: "'complete-enumeration-by-class-split (verification: deterministic-machine + independent-encoding-cross-check + batch-1 bit-exact re-run reconciliation + decomposition protocol brute-force-validated in K0816/K0818). See report.md.'"
---

# 5x22 q=7 row-deficient maximal nonexistence — all 19 canonical classes UNSAT

## Claim

1. On the 5x22 integer grid (q=7), for each of the 19 row-mirror-canonical deficiency classes
   D ⊆ {0..4} (canonical representatives of the 31 non-empty subsets under y -> 4-y), the
   class-split SAT instance — rows in D hold at most 5 stones, rows outside D hold exactly 6
   (safety caps every row at 6 since a row is a line of length 22 ≥ q), safety ≤ 6 stones per
   census curve, maximality (every empty cell covered by a ≥6-stone curve) — is **UNSAT**:
   - 17/19 classes directly UNSAT (kissat 4.0.4, exit 20; batch-1 raw logs; hardest
     {0,1}: 875,682 conflicts / 32.5 s; {1,3}: 553,321; {0,4}: 532,938;
     {0,2,3}: 199,205 / 5.9 s). All 17 re-run by the completion lane reproduce the batch-1
     conflict counts bit-exactly (17/17).
   - {0} and {1}: the plain instances resisted ~142 s single runs (2,849,545 / 3,330,616
     conflicts, superseded batch-1 INDET logs) and are decided by the **complete
     k × minpos decomposition** (the K0816/K0821 protocol): k = 0..4 (exact deficient-row
     stone count) and k = 5 × minpos = 0..10. All 32 sub-instances UNSAT
     (hardest: {0} k=5 mp=0: 3,380,578 conflicts / 153.8 s; {1} k=5 mp=0: 3,111,756 / 144.1 s).
   - Total conflicts across the 49 deciding instances: **24,581,763** (17 direct: 5,256,816;
     32 decomposition: 19,324,947); lex=H cross-checks add 937,505. No SAT, no INDET among
     the deciding instances.
2. Coverage: every deficient maximal safe configuration has a non-empty exact deficiency
   set D, the exact-D instances partition them, and row-mirror soundness reduces 31 classes
   to 19. The k × minpos decomposition is exhaustive: k = 0..5 partitions the deficient
   row's stone count; for k = 5 the minpos split pins the leftmost stone of the first
   deficient row at column exactly P, and every configuration or its column mirror has
   leftmost stone column ≤ 10 at m = 22 (min(x1, 21−x5) ≤ 10 — otherwise x1 ≥ 11 and
   x5 ≤ 10, contradicting x1 ≤ x5); the column mirror preserves row occupancy, hence the
   class. Therefore **no row-deficient maximal safe configuration exists on 5x22**; every
   maximal safe configuration on 5x22 has 30 stones (row occupancy (6,6,6,6,6)).
3. Combined with K0738–K0759 (5x19 witness-free), K0816 (5x20 witness-free), K0821
   (5x21 witness-free) and K0332 (29-stone witness at 5x18, least witness width 18): the
   witness-free width set of (5,7) is **{19, 20, 21, 22}**, so
   **M_{5,7} ∈ {19, 20, 21, 22} or M_{5,7} ≥ 23**; the upper bound 158 (K0332/K0024
   substitution) is unchanged. The witness-search frontier moves to 5x23.

## Verification

- Positive control: 5x18 q=7 class {0} SAT — 343,134 conflicts / 12.5 s, bit-exact with the
  K0821 lane's control run; decoded model 29 stones rows (5,6,6,6,6) passes the
  census-free `verifyConfig` independent verifier (K0332 witness board rediscovered
  end-to-end through the same encoder+solver path).
- Cross-encoding: {0,1} and {2} re-encoded with --lex=H (column-reflection lex-leader —
  class-preserving, hence sound) are UNSAT again (627,149 / 310,356 conflicts).
- Determinism / batch-1 reconciliation: all 17 direct classes re-run by the takeover lane
  reproduce the batch-1 raw-log conflict counts bit-exactly (17/17); the m22 CNF header
  (`p cnf 4989 17791`) matches the batch-1 log's parsed header; the 5x18 control reproduces
  the K0821 lane's 343,134 bit-exactly.

## Scope

Finite machine verification up to the correctness of the K0810 census, the class-split
encoding and the k×minpos decomposition (protocol brute-force-validated on small boards in
K0816/K0818), and kissat 4.0.4; not a number-theoretic proof. Persistence at m ≥ 23 remains
open: exact M_{5,7} needs witness-free verification for all widths up to U=158 or a
universal tail argument. The witness frontier moves to 5x23 (a witness there gives
M ≥ 23; witness-free there extends the free set to {19,20,21,22,23}). The 11x11 empty board,
two-stone root {49,60}, S2 {59,60}, class 2 and class 4 are unaffected and remain UNKNOWN.
