---
id: K0818
title: 6x19 q=8 row-deficient maximal nonexistence (all 35 canonical classes UNSAT) — witness-free width set of (6,8) gains 19, M_{6,8} = 19 or >= 21
kind: proposition
status: computed
topics: [rectangles, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0810
  note: "census (circleABC integer triples, line pairs) and the sequential-counter/maximality core are used verbatim (sat.js / sat2.js); the class-split unit clauses are the only addition"
- type: depends_on
  target: K0815
  note: "41-stone deficient-maximal witness at 6x18 (rows 7,6,7,7,7,7) is the lower bound M_{6,8}>=19 and the positive-control board; the 6x19 'unresolved' instance (kissat 255s, 4.52M conflicts single some-deficient clause) is settled by the class split"
- type: depends_on
  target: K0796
  note: "2x8 q=4 5-stone control (SAT rediscovered); 2x9 q=4 UNSAT control consistent with M_{2,4}=9"
- type: generalizes
  target: K0816
  note: "same class-split methodology as the 5x20 q=7 nonexistence, applied at w=6 without the runner system: pure per-class UNSAT sweep with lex cross-checks and small-board ground-truth validation"
artifacts:
- path: research/experiments/six-row-q8-m19-class-split-20261114/scripts/sat3.js
  role: solver
  note: "class-split / exact-count (--krow) / minpos / lex encoder on the K0810 sat.js census + sat2.js counter core, plus kissat model decoding to stones with census-free verifyConfig"
- path: research/experiments/six-row-q8-m19-class-split-20261114/scripts/sweep1.sh
  role: source
  note: "one-class driver: deterministic DIMACS, kissat 4.0.4 with 275s cap, JSONL record with exit code and conflicts"
- path: research/experiments/six-row-q8-m19-class-split-20261114/output/records.jsonl
  role: data
  note: "all 35 canonical class records: result UNSAT, rc=20, conflicts, seconds (sum 15,492,764 conflicts / 920.1s)"
- path: research/experiments/six-row-q8-m19-class-split-20261114/output/summary.json
  role: data
  note: "aggregate: 35 UNSAT / 0 SAT / 0 INDET, controls, lex=H cross-check conflicts, coverage argument, determinism notes"
- path: research/experiments/six-row-q8-m19-class-split-20261114/report.md
  role: proof
  note: "claim, coverage argument (exact deficiency set partitions deficient configurations; row-mirror soundness), verification protocol, per-class results, scope and limits"
- path: research/experiments/six-row-q8-m19-class-split-20261114/output/c6x19q8_2.txt
  role: data
  note: "hardest class raw kissat log ({2}: 4,008,520 conflicts UNSAT); all 35 raw logs c6x19q8_*.txt"
- path: research/experiments/six-row-q8-m19-class-split-20261114/output/crosscheck_lexH_class2.txt
  role: data
  note: "lex=H re-encoded cross-check of class {2} (3,246,250 conflicts UNSAT); classes {1},{1,2},{2,3} also cross-checked"
- path: research/experiments/six-row-q8-m19-class-split-20261114/output/smallboard_validation/validation_result.json
  role: data
  note: "19/19 small-board class-split instances (3x7/3x8/2x8/2x9/3x9 q=4, all canonical classes) match full-mask brute-force ground truth, SAT and UNSAT"
- path: research/experiments/six-row-q8-m19-class-split-20261114/output/positive_control_6x23_class1_witness.json
  role: data
  note: "6x23 q=6 class {1} SAT via kissat: 29 stones rows (5,4,5,5,5,5), census-free verifyConfig + Python Fraction verifier both PASS — end-to-end positive control on a K0815 witness board"
scope: "'finite machine verification (35 kissat 4.0.4 UNSAT instances + lex cross-checks + brute-force-validated class logic); 6x19 q=8 only.'"
evidence: "'complete-enumeration-by-class-split (verification: deterministic-machine + independent-encoding-cross-check + small-board ground-truth). See report.md.'"
---

# 6x19 q=8 row-deficient maximal nonexistence — all 35 canonical classes UNSAT

## Claim

1. On the 6x19 integer grid (q=8), for each of the 35 row-mirror-canonical deficiency classes
   D ⊆ {0..5} (canonical representatives of the 63 non-empty subsets under y -> 5-y), the
   class-split SAT instance — rows in D hold at most 6 stones (unit ¬rowGe[y]), rows outside D
   hold exactly 7 (unit rowGe[y]; safety caps every row at 7 since a row is a line of length 19 ≥ q),
   safety ≤ 7 stones per census curve, maximality (every empty cell covered by a ≥7-stone curve) —
   is **UNSAT** (kissat 4.0.4, exit 20; 15,492,764 conflicts total; hardest class {2}: 4,008,520 conflicts).
2. Coverage: every deficient maximal safe configuration has a non-empty exact deficiency set
   D = {rows with ≤ q-2 stones}, and the instances for exact D partition all such configurations;
   row-mirror soundness reduces 63 classes to 35. Hence **no row-deficient maximal safe
   configuration exists on 6x19**; every maximal safe configuration on 6x19 has 42 stones.
3. With K0815 (41-stone deficient maximal at 6x18, rows 7,6,7,7,7,7), the (6,8) witness
   structure at the frontier is settled: witness width 18 yes, width 19 no. Therefore
   **M_{6,8} = 19 or M_{6,8} ≥ 21** (M ∈ {19} ∪ [21,371]; the K0318/K0024 upper bound 371 is
   unchanged). This refutes the possibility of a 6x19 witness, which was the open witness-search
   frontier of the (6,8) family.

## Method

Class-split encoding on the K0810 census (sat.js circleABC integer triples — a census independent
of the K0738–K0759 runner's circumcenter form) and the sat2.js sequential counter, decided by
kissat 4.0.4 (official linux-amd64 binary). Per-class UNSAT logs are in `output/c6x19q8_*.txt`.

## Verification

- Positive controls: 2x8 q=4 class {0} SAT (5 stones, census-free verifier PASS — K0796 witness
  rediscovered); 6x18 q=8 class {1} SAT (41 stones rows 7,6,7,7,7,7, verifier PASS, 511,895
  conflicts — K0815 board rediscovered, bit-exact across an environment reset);
  6x23 q=6 class {1} SAT (29 stones rows 5,4,5,5,5,5; JS census-free verifier and the Python
  Fraction verifier both PASS — K0815 extend6 witness board rediscovered through SAT).
- Negative control: 2x9 q=4 class {0} UNSAT (M_{2,4}=9 consistent).
- Logic validation: 19/19 small-board class-split instances (3x7, 3x8, 2x8, 2x9, 3x9; q=4; all
  canonical classes) agree with full-mask brute-force ground truth on exactly which deficiency
  classes carry witnesses.
- Cross-encoding: the four hardest classes re-encoded with --lex=H (lex-leader over column
  reflection — class-preserving, hence sound) are all UNSAT again
  ({1}: 2,142,822; {2}: 3,246,250; {1,2}: 2,118,969; {2,3}: 1,348,948 conflicts).
- Determinism: every instance and control reproduces conflict counts bit-exactly across an
  execution-environment reset, and the two encodeCore paths (sat2 vs sat3) yield identical DIMACS.

## Scope

Finite machine verification up to the correctness of the K0810 census, the class-split encoding
(brute-force validated), and kissat 4.0.4; not a number-theoretic proof (same evidence level as
K0816). Persistence at m ≥ 20 remains open: determining M_{6,8} exactly needs either witness-free
verification for all widths up to the K0024 bound T=371, or a universal tail argument in the
spirit of the K0342 chord-energy bound that lowered (5,8) to a 16..100 sweep. The 5x22 q=6 and
6x21 q=7 singleton classes resisted 280s single runs (INDET, not absence); --krow/--minpos
sub-splitting is the natural next step. The 11x11 empty board, two-stone root {49,60}, S2 {59,60},
class 2 and class 4 are unaffected and remain UNKNOWN.
