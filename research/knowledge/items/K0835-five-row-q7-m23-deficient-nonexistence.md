---
id: K0835
title: "5x23 q=7 row-deficient maximal nonexistence (all 19 canonical classes UNSAT) — witness-free width set of (5,7) extends to {19,20,21,22,23}, M_{5,7} = 19 or >= 25"
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
  note: "5x18 29-stone witness is the lower bound (least witness width 18) and the positive-control board (rediscovered SAT, 343,134 conflicts, bit-exact with the K0821 and K0834 lane controls)"
- type: depends_on
  target: K0816
  note: "the m=20 nonexistence item; the k x minpos decomposition protocol for the hard singleton classes {0},{1} and the 5x18 positive control are taken from its cross-check lane"
- type: depends_on
  target: K0821
  note: "the m=21 nonexistence item; the witness-free width set {19,20,21} and the minpos coverage convention floor((m-1)/2)"
- type: depends_on
  target: K0834
  note: "the m=22 nonexistence item; this lane reuses its scripts byte-identically and its control reproduces bit-exactly; witness-free width set {19,20,21,22} -> {19,20,21,22,23}; its audit-20261115 sharpening convention (M = 19 or >= maxwitness+2) is applied to the extended free set"
- type: depends_on
  target: K0738
  note: "5x19 witness-free by the occupancy complete enumeration (via the K0759 machine) — the first element of the witness-free width set"
- type: generalizes
  target: K0834
  note: "the same class-split proposition one width further: 5x22 (K0834) -> 5x23; witness-free width set {19,20,21,22} -> {19,20,21,22,23}"
artifacts:
- path: research/experiments/five-row-q7-m23-class-split-20261115/scripts/sat3.js
  role: solver
  note: "class-split / exact-count (--krow) / minpos / lex encoder on the K0810 sat.js census + sat2.js counter core (byte-identical to the K0821/K0834 lanes), plus kissat model decoding with census-free verifyConfig"
- path: research/experiments/five-row-q7-m23-class-split-20261115/scripts/mkcnf.sh
  role: source
  note: "deterministic CNF generator: 17 direct classes + {0},{1} k=0..4 + k=5 x minpos=0..11 + 2 lex=H + 5x18 control (54 CNFs)"
- path: research/experiments/five-row-q7-m23-class-split-20261115/scripts/qrun.sh
  role: source
  note: "2-worker claim-directory queue runner with per-instance timeout caps and interrupted-instance reclaim"
- path: research/experiments/five-row-q7-m23-class-split-20261115/scripts/mkrecords5723.js
  role: source
  note: "records.jsonl / summary.json builder from raw kissat logs"
- path: research/experiments/five-row-q7-m23-class-split-20261115/output/records.jsonl
  role: data
  note: "54 records: 17 direct class UNSAT + 34 k/minpos decomposition UNSAT ({0},{1}: k=0..4 and k=5 x minpos=0..11) + 2 lex=H cross-checks + 1 positive control (SAT); deciding-instance conflicts 20,916,467, records total 22,084,999"
- path: research/experiments/five-row-q7-m23-class-split-20261115/output/summary.json
  role: data
  note: "aggregate: 0 SAT / 0 INDET among the 51 deciding instances; hardest {1} k=5 mp=0 (2,555,137 conflicts); decomposition soundness note (minpos pins the leftmost stone of the first deficient row; sound bound floor((m-1)/2)=11 at m=23); environment-reset determinism note"
- path: research/experiments/five-row-q7-m23-class-split-20261115/report.md
  role: proof
  note: "claim, coverage and decomposition-completeness argument (k partitions the row count; leftmost stone column <= 11 by the column mirror: x1 >= 12 forces mirror leftmost 22-x5 <= 10), verification protocol incl. the cross-reset bit-exact re-run reconciliation, per-class results, scope and limits"
- path: research/experiments/five-row-q7-m23-class-split-20261115/output/r5x23q7_1k5p0.txt
  role: data
  note: "hardest deciding instance raw kissat log ({1} k=5 minpos=0: 2,555,137 conflicts UNSAT / 107.96 s); all raw logs r5x23q7_*.txt (17 direct + 34 decomposition + 2 lex + control)"
- path: research/experiments/five-row-q7-m23-class-split-20261115/output/r_ctrl_5x18_c0.txt
  role: data
  note: "positive control log: 5x18 class {0} SAT 343,134 conflicts bit-exact with the K0821/K0834 lane controls; decoded 29 stones rows (5,6,6,6,6), census-free verifyConfig PASS (K0332 witness rediscovered end-to-end)"
scope: "'finite machine verification (kissat 4.0.4: 51 UNSAT instances + 2 lex=H cross-encoding re-checks + positive control); 5x23 q=7 only.'"
evidence: "'complete-enumeration-by-class-split (verification: deterministic-machine + independent-encoding-cross-check + cross-reset bit-exact re-run reconciliation + decomposition protocol brute-force-validated in K0816/K0818). See report.md.'"
---

# 5x23 q=7 row-deficient maximal nonexistence — all 19 canonical classes UNSAT

## Claim

1. On the 5x23 integer grid (q=7), for each of the 19 row-mirror-canonical deficiency
   classes D ⊆ {0..4} (canonical representatives of the 31 non-empty subsets under
   y -> 4-y), the class-split SAT instance — rows in D hold at most 5 stones, rows
   outside D hold exactly 6 (safety caps every row at 6 since a row is a line of length
   23 ≥ q), safety ≤ 6 stones per census curve, maximality (every empty cell covered by
   a ≥6-stone curve) — is **UNSAT**:
   - 17/19 classes directly UNSAT (kissat 4.0.4, exit 20; hardest {0,1}: 708,108
     conflicts / 22.3 s; {1,3}: 413,739; {0,4}: 542,893; {2}: 392,089; direct total
     4,673,619 conflicts — slightly easier than m=22's 5,256,816).
   - {0} and {1}: decided by the **complete k × minpos decomposition** (the
     K0816/K0821/K0834 protocol): k = 0..4 (exact deficient-row stone count; hardest
     {0} k=4: 1,185,996 / {1} k=4: 1,098,229) and k = 5 × minpos = 0..11 (12 points —
     the sound bound is floor((m−1)/2) = 11 at m = 23). All 34 sub-instances UNSAT
     (hardest: {1} k=5 mp=0: 2,555,137 conflicts / 107.96 s; {0} k=5 mp=0:
     2,135,466 / 89.5 s).
   - Total conflicts across the 51 deciding instances: **20,916,467** (17 direct:
     4,673,619; 34 decomposition: 16,242,848); lex=H cross-checks add 825,398. No SAT,
     no INDET among the deciding instances.
2. Coverage: every deficient maximal safe configuration has a non-empty exact deficiency
   set D, the exact-D instances partition them, and row-mirror soundness reduces 31
   classes to 19. The k × minpos decomposition is exhaustive: k = 0..5 partitions the
   deficient row's stone count; for k = 5 the minpos split pins the leftmost stone of
   the first deficient row at column exactly P, and every configuration or its column
   mirror has leftmost stone column ≤ 11 at m = 23 (if x1 ≥ 12 then the mirror has
   leftmost column 22−x5 ≤ 22−12 = 10); the column mirror preserves row occupancy, hence
   the class. Therefore **no row-deficient maximal safe configuration exists on 5x23**;
   every maximal safe configuration on 5x23 has 30 stones (row occupancy (6,6,6,6,6)).
3. Combined with K0738–K0759 (5x19 witness-free), K0816 (5x20 witness-free), K0821
   (5x21 witness-free), K0834 (5x22 witness-free) and K0332 (29-stone witness at 5x18,
   least witness width 18): the witness-free width set of (5,7) is
   **{19, 20, 21, 22, 23}**, so in the set form **M_{5,7} ∈ {19,20,21,22,23} or
   M_{5,7} ≥ 24**, sharpened to **M_{5,7} = 19 or M_{5,7} ≥ 25** (widths 20–23 are
   verified witness-free and cannot be the threshold; M = 24 would require a witness at
   the verified witness-free width 23, so the next possible witness sits at w ≥ 24,
   forcing M = w + 1 ≥ 25); the upper bound 158 (K0332/K0024 substitution) is unchanged.
   The witness-search frontier moves to 5x24.

## Verification

- Positive control: 5x18 q=7 class {0} SAT — 343,134 conflicts / 10.4 s, bit-exact with
  the K0821 and K0834 lane control runs; decoded model 29 stones rows (5,6,6,6,6) passes
  the census-free `verifyConfig` independent verifier (K0332 witness board rediscovered
  end-to-end through the same encoder+solver path).
- Cross-encoding: {0,1} and {2} re-encoded with --lex=H (column-reflection lex-leader —
  class-preserving, hence sound) are UNSAT again (504,359 / 321,039 conflicts).
- Determinism across an execution-environment reset: the local scratch was lost
  mid-sweep (27/51 deciding instances finished locally); the full sweep was re-run from
  freshly generated CNFs and the freshly downloaded official kissat 4.0.4 binary
  (arminbiere/kissat rel-4.0.4 linux-amd64 asset), and every pre-reset instance
  reproduces its conflict count bit-exactly in the re-run (e.g. {0,1}: 708,108;
  {0}k4: 1,185,995; {1}k5p3: 240,999), with raw logs pushed batch-by-batch so no
  evidence could be lost again.

## Scope

Finite machine verification up to the correctness of the K0810 census, the class-split
encoding and the k×minpos decomposition (protocol brute-force-validated on small boards
in K0816/K0818), and kissat 4.0.4; not a number-theoretic proof. Persistence at m ≥ 24
remains open: exact M_{5,7} needs witness-free verification for all widths up to U=158
or a universal tail argument. The witness frontier moves to 5x24 (a witness there gives
M ≥ 25; witness-free there extends the free set to {19,...,24}). The 11x11 empty board,
two-stone root {49,60}, S2 {59,60}, class 2 and class 4 are unaffected and remain
UNKNOWN.
