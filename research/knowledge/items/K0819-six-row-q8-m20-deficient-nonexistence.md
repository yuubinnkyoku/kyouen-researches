---
id: K0819
title: "6x20 q=8 row-deficient maximal nonexistence (all 35 canonical classes UNSAT) — witness-free width set of (6,8) extends to {19,20}, M_{6,8} ∈ {19,20} or >= 22"
kind: proposition
status: computed
topics: [rectangles, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0810
  note: "census (circleABC integer triples, line pairs) and the sequential-counter/maximality core are used verbatim (sat.js / sat2.js / sat3.js); the class-split unit clauses are the only addition"
- type: depends_on
  target: K0815
  note: "41-stone deficient-maximal witness at 6x18 (rows 7,6,7,7,7,7) is the lower bound M_{6,8}>=19 and the positive-control board (rediscovered SAT, conflicts bit-exact with K0818)"
- type: depends_on
  target: K0796
  note: "2x8 q=4 5-stone control (SAT rediscovered); 2x9 q=4 UNSAT control consistent with M_{2,4}=9"
- type: generalizes
  target: K0818
  note: "the m=19 class-split sweep extended to m=20 with the identical machinery; 6x20 was the witness-search frontier opened by K0818"
artifacts:
- path: research/experiments/six-row-q8-m20-class-split-20261114/scripts/sat3.js
  role: solver
  note: "class-split / exact-count (--krow) / minpos / lex encoder on the K0810 sat.js census + sat2.js counter core (verbatim from the K0818 lane), plus kissat model decoding with census-free verifyConfig"
- path: research/experiments/six-row-q8-m20-class-split-20261114/scripts/runall.sh
  role: source
  note: "deterministic 35-class sweep driver (encode + kissat 4.0.4 timeout 285 + lex=H cross-checks + 6x18 positive control)"
- path: research/experiments/six-row-q8-m20-class-split-20261114/scripts/mkrecords.js
  role: source
  note: "records.jsonl / summary.json builder from raw kissat logs (conflicts and process-time extracted per log)"
- path: research/experiments/six-row-q8-m20-class-split-20261114/output/records.jsonl
  role: data
  note: "all 35 canonical class records (result UNSAT, rc=20, conflicts, seconds; sum 16,446,081 conflicts) + 2 lex=H cross-checks + 1 positive control"
- path: research/experiments/six-row-q8-m20-class-split-20261114/output/summary.json
  role: data
  note: "aggregate: 35 UNSAT / 0 SAT / 0 INDET, hardest class {2} 2,763,766 conflicts, controls, claim"
- path: research/experiments/six-row-q8-m20-class-split-20261114/report.md
  role: proof
  note: "claim, coverage argument (exact deficiency set partitions deficient configurations; row-mirror soundness), verification protocol, per-class table, scope and limits"
- path: research/experiments/six-row-q8-m20-class-split-20261114/output/r6x20q8_c2.txt
  role: data
  note: "hardest class raw kissat log ({2}: 2,763,766 conflicts UNSAT); all 35 raw logs r6x20q8_c*.txt + lexH cross-checks"
- path: research/experiments/six-row-q8-m20-class-split-20261114/output/r_ctrl_6x18_c1.txt
  role: data
  note: "positive control log: 6x18 class {1} SAT 511,895 conflicts (bit-exact with K0818), decoded model 41 stones rows (7,6,7,7,7,7), census-free verifyConfig PASS"
scope: "'finite machine verification (35 kissat 4.0.4 UNSAT instances + lex=H cross-encoding re-checks on the hardest singleton classes + positive/negative controls); 6x20 q=8 only.'"
evidence: "'complete-enumeration-by-class-split (verification: deterministic-machine + independent-encoding-cross-check + small-board ground-truth from K0818). See report.md.'"
---

# 6x20 q=8 row-deficient maximal nonexistence — all 35 canonical classes UNSAT

## Claim

1. On the 6x20 integer grid (q=8), for each of the 35 row-mirror-canonical deficiency classes
   D ⊆ {0..5} (canonical representatives of the 63 non-empty subsets under y -> 5-y), the
   class-split SAT instance — rows in D hold at most 6 stones (unit ¬rowGe[y]), rows outside D
   hold exactly 7 (unit rowGe[y]; safety caps every row at 7 since a row is a line of length
   20 ≥ q), safety ≤ 7 stones per census curve, maximality (every empty cell covered by a
   ≥7-stone curve) — is **UNSAT** (kissat 4.0.4, exit 20; 16,446,081 conflicts total; hardest
   class {2}: 2,763,766 conflicts / 128.9 s).
2. Coverage: every deficient maximal safe configuration has a non-empty exact deficiency set
   D = {rows with ≤ q-2 stones}, and the instances for exact D partition all such configurations;
   row-mirror soundness reduces 63 classes to 35 (class logic brute-force-validated on 19/19
   small-board instances in K0818). Hence **no row-deficient maximal safe configuration exists
   on 6x20**; every maximal safe configuration on 6x20 has 42 stones.
3. With K0818 (6x19 witness-free) and K0815 (41-stone deficient maximal at 6x18, rows
   7,6,7,7,7,7), the witness-free width set of (6,8) is **{19, 20}** (least witness width 9:
   witnesses at 6x9..6x18), so **M_{6,8} ∈ {19, 20} or M_{6,8} ≥ 22**; the upper bound 371
   (K0318/K0024 substitution) is unchanged. The witness-search frontier moves to 6x21.

## Method

Identical machinery to K0818: `sat3.js` class-split encoder on the K0810 census and
sequential-counter core, decided by kissat 4.0.4 (official linux-amd64 binary). Classes run
pairwise in parallel (2 workers, `timeout 285` each); per-class conflicts and process-time
are taken from each kissat log.

## Verification

- Positive control: 6x18 q=8 class {1} SAT — 511,895 conflicts / 20.1 s, **bit-exact with the
  K0818 control**; decoded model 41 stones rows (7,6,7,7,7,7) passes the census-free
  `verifyConfig` independent verifier (K0815 witness board rediscovered end-to-end through
  the same encoder+solver path as the 35 UNSAT instances).
- Negative controls: 2x8 q=4 class {0} SAT (K0796 witness rediscovered); 2x9 q=4 class {0}
  UNSAT (M_{2,4}=9 consistent).
- Cross-encoding: the two hardest singleton classes re-encoded with --lex=H (lex-leader over
  column reflection — class-preserving, hence sound) are UNSAT again
  ({1}: 2,038,080 conflicts / 108.7 s; {2}: 2,331,073 conflicts / 112.5 s).
- Determinism: the 6x18 control conflicts reproduce the K0818-published count exactly;
  all per-class conflict counts come from completed kissat runs (exit 20), no INDET.

## Scope

Finite machine verification up to the correctness of the K0810 census, the class-split
encoding (brute-force validated in K0818), and kissat 4.0.4; not a number-theoretic proof
(same evidence level as K0818/K0816). Persistence at m ≥ 21 remains open: exact M_{6,8}
needs either witness-free verification for all widths up to the K0024/K0318 bound U=371 or
a universal tail argument in the spirit of the K0342 chord-energy bound. The witness
frontier moves to 6x21: a witness there gives M_{6,8} ≥ 22; witness-free there extends the
free set to {19,20,21} (M ∈ {19,20,21} or ≥ 23). The 11x11 empty board, two-stone root
{49,60}, S2 {59,60}, class 2 and class 4 are unaffected and remain UNKNOWN.
