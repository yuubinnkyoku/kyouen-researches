---
id: K0829
title: "6x21 q=8 row-deficient maximal nonexistence (all 3 row-mirror rowY classes UNSAT) — witness-free width set of (6,8) extends to {19,20,21}, M_{6,8} ∈ {19,20,21} or >= 23"
kind: proposition
status: computed
topics: [rectangles, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0810
  note: "census (circleABC integer triples, line pairs) and the sequential-counter/maximality core used verbatim (sat.js / sat2.js); the rowfixed unit clause is the only addition"
- type: depends_on
  target: K0815
  note: "41-stone deficient-maximal witness at 6x18 (rows 7,6,7,7,7,7) is the lower bound M_{6,8}>=19 and the positive-control board (row-mirror rows 7,7,7,7,6,7 rediscovered by the def-OR control here)"
- type: depends_on
  target: K0819
  note: "6x19/6x20 witness-free by the 35-class deficiency split; K0819 opened the 6x21 frontier and stated exactly this extension branch"
- type: depends_on
  target: K0822
  note: "row-mirror canonical class logic (y -> 5-y pairs the 6 rows into 3 mirror classes), brute-force-validated in K0818"
- type: depends_on
  target: K0825
  note: "rowY fixed-row split technique (used there on the SAT side for seven-row witnesses), applied here on the UNSAT side with all mirror classes swept"
artifacts:
- path: research/experiments/six-row-q8-m21-row-split-20261114/report.md
  role: proof
  note: "claim, coverage argument (deficient config has a deficient row y in a rowfixed(y) instance; row-mirror soundness y<->5-y reduces 6 rows to 3 classes), verification protocol, honest negatives, scope and limits"
- path: research/experiments/six-row-q8-m21-row-split-20261114/output/records.jsonl
  role: data
  note: "6 records: def-OR INDET (240s cap, 5,011,833 conflicts, honest negative), rowY 0/1/2 UNSAT (327,636 / 2,862,649 / 1,767,690 conflicts), rowY=1 lex=H cross-encoding UNSAT (2,337,998 conflicts), 6x18 positive control SAT (492,432 conflicts) with js+py dual verification"
- path: research/experiments/six-row-q8-m21-row-split-20261114/output/r6x21q8_rowY1.txt
  role: data
  note: "hardest class raw kissat log (rowY=1: 2,862,649 conflicts UNSAT, 180.5s); sibling logs r6x21q8_rowY0.txt / r6x21q8_rowY2.txt / r6x21q8_rowY1_lexH.txt / r6x21q8_defOR.txt / r_ctrl_6x18_def.txt"
- path: research/experiments/six-row-q8-m21-row-split-20261114/output/r6x21q8_defOR.txt
  role: data
  note: "def-mode OR instance raw log: INDET at the 240s cap (5,011,833 conflicts) — the honest negative that motivated the row split"
- path: research/experiments/six-row-q8-m21-row-split-20261114/output/r_ctrl_6x18_def.witness.json
  role: data
  note: "positive-control decoded model: 41 stones rows (7,7,7,7,6,7), sat.js census-free verifyConfig PASS and verify_witness.py (Python Fraction) PASS"
scope: "'finite machine verification (3 kissat 4.0.4 rowfixed UNSAT instances covering all 6 rows by mirror soundness + lex=H cross-encoding re-check on the hardest class + positive control); 6x21 q=8 only.'"
evidence: "'complete-coverage-by-row-mirror-split (verification: deterministic-machine + independent-encoding-cross-check + positive control rediscovering the K0815 board). See report.md.'"
---

# 6x21 q=8 row-deficient maximal nonexistence — 3 row-mirror rowY classes UNSAT

## Claim

1. On the 6x21 integer grid (q=8), for each of the 3 row-mirror-canonical row classes
   y ∈ {0,1,2} (covering all 6 rows via the V mirror y -> 5-y), the rowfixed SAT instance —
   row y holds at most 6 stones (unit ¬rowGe[y]), other rows free, safety ≤ 7 stones per row
   (a row is a line of length 21 ≥ q) and per census curve, maximality (every empty cell
   covered by a ≥7-stone curve) — is **UNSAT** (kissat 4.0.4, exit 20):
   y=0: 327,636 conflicts / 13.9 s; y=1: 2,862,649 conflicts / 180.5 s; y=2: 1,767,690
   conflicts / 92.4 s.
2. Coverage: every deficient maximal safe configuration has some row with ≤ 6 stones, and it
   appears as a solution of the rowfixed(y) instance for that row. The V mirror y -> 5-y is a
   board symmetry (safety, maximality, deficiency all invariant), so rowfixed(y) is
   equisatisfiable with rowfixed(5-y); the 3 classes y ∈ {0,1,2} therefore cover all 6 rows.
   Hence **no row-deficient maximal safe configuration exists on 6x21**; every maximal safe
   configuration on 6x21 has 42 stones.
3. With K0818 (6x19 free), K0819 (6x20 free) and K0815 (41-stone deficient maximal at
   6x18, least witness width 9), the witness-free width set of (6,8) is **{19, 20, 21}**, so
   **M_{6,8} ∈ {19, 20, 21} or M_{6,8} ≥ 23**; the upper bound 371 (K0318/K0024
   substitution) is unchanged. The witness-search frontier moves to 6x22.

## Method

`sat2.js` (K0810 census + sequential-counter + maximality core, used verbatim from the
seven-row-q7-witness-search-20261114 lane, byte-identical) in `--deficient` and
`--rowY=Y` / `--lex=H` modes; kissat 4.0.4 official linux-amd64 binary. The def-mode OR
instance (`--deficient`: some row ≤ 6) resisted the 240 s cap at 5,011,833 conflicts —
recorded as an honest negative — and the rowY split (which constrains *which* row is
deficient but leaves all other rows free) refuted each of the 3 mirror classes within
budget. Cross-encoding: the hardest class (y=1) re-encoded with `--lex=H` (column-mirror
lex-leader; rowY-preserving, hence sound) is UNSAT again (2,337,998 conflicts / 144.0 s).

## Verification

- Positive control: 6x18 q=8 def-mode OR SAT — 492,432 conflicts / 15.8 s; decoded model
  41 stones rows (7,7,7,7,6,7) (row-mirror of the K0815 board rows 7,6,7,7,7,7) passes the
  census-free `verifyConfig` (sat.js) and the independent Python `Fraction` verifier
  (`verify_witness.py`): safe + maximal + deficient PASS. This is a sat2.js def-OR instance
  and is distinct from the K0818/K0819 sat3.js class-{1} control (511,895 conflicts); both
  independently confirm the same 6x18 witness board through different encodings.
- Determinism calibration: the same sat2.js + kissat 4.0.4 machine reproduced, bit-exact,
  the published (7,7) m=24 def-OR (2,105,329), m=25 rowY=3 (756,785), m=26 rowY=3
  (1,951,966) and (7,9) m=100 def (18,075) conflict counts in the parallel-run calibration
  of 2026-11-14, and the 2x8/2x9 q=4 controls (37/316).
- Honest negatives: the 6x21 def-OR instance is INDET at the 240 s cap (5,011,833
  conflicts); the nonexistence claim rests on the 3-class row split, not on the OR run.
  lex=H re-checks were run for the hardest class only (sufficient: the first-encoding
  3-class sweep is already a complete coverage).

## Scope

Finite machine verification up to the correctness of the K0810 census, the rowfixed
encoding (mirror soundness brute-force-validated in K0818), and kissat 4.0.4; not a
number-theoretic proof (same evidence level as K0818/K0819/K0821). Persistence at m ≥ 22
remains open: exact M_{6,8} needs either witness-free verification for all widths up to
the K0024/K0318 bound U=371 or a universal tail argument in the spirit of the K0342
chord-energy bound. The witness frontier moves to 6x22: a witness there gives M_{6,8} ≥ 22;
witness-free there extends the free set to {19,20,21,22} (M ∈ {19,20,21,22} or ≥ 24). If the
rowY split hits the budget wall at m=22, the next lever is the 35-class exact-deficiency
split (K0818/K0819 machine), which partitions each rowfixed class further. The 11x11 empty
board, two-stone root {49,60}, S2 {59,60}, class 2 and class 4 are unaffected and remain
UNKNOWN.

## 備考

K番号は作業時点での仮番号（AGENTS.md の再採番規則による）。
