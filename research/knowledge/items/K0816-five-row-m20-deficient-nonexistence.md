---
id: K0816
title: 5x20 q=7 row-deficient maximal nonexistence (all 19 classes) — witness-free widths extend to 20, M_{5,7} ∈ {19,20} or ≥22
kind: proposition
status: computed
topics: [rectangles, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0759
  note: "同一runner機械（multi_deficient_runner.ts）の 5x20 移植。occupancy分類・blocker割当DFS・fillRows全列挙をM=20で完走"
- type: depends_on
  target: K0332
  note: "5x18 29石witnessが下界（M≥19）と5x18陽性対照の由来"
- type: depends_on
  target: K0815
  note: "5×20はkissat/貪欲/SA/portfolio全てで未決着だった前線（K0815 note・frontier-portfolio-20261114）。今回完全列挙で不在確定"
- type: depends_on
  target: K0810
  note: "SAT交叉確認はK0810 sat.jsのcensus（circleABC整数三元組・runnerの外心形式と独立）を使用"
artifacts:
- path: research/experiments/five-row-q7-m20-20261114/scripts/m20_runner.ts
  role: solver
  note: "K0738-K0759 runnerの5x20移植（W=5,M=20・スライス駆動・制御: 5x19 [0,1] slice A1と完全一致 done=117, maxCase 28,488 @ idx 39, nC=95）"
- path: research/experiments/five-row-q7-m20-20261114/scripts/run_class.sh
  role: source
  note: "クラス単位のスライス再開ドライバ（JSONL永続化・witness検出時停止）"
- path: research/experiments/five-row-q7-m20-20261114/scripts/census_check.js
  role: source
  note: "5x18/19/20円census長ヒストグラム（5x19=95でK0759公表値と一致・5x20=104・最大長8）"
- path: research/experiments/five-row-q7-m20-20261114/output/class_01234.jsonl
  role: data
  note: "5行欠損クラス [0,1,2,3,4] 完全走査（10,878代表・witnesses 0・leaves 0）— 他18クラスの class_*.jsonl も同形式"
- path: research/experiments/five-row-q7-m20-20261114/output/summary.json
  role: data
  note: "全19クラス集計（206,682代表・witnesses 0・leaves 0・census 104円・クラス別最大case nodes）"
- path: research/experiments/five-row-q7-m20-20261114/output/census.json
  role: data
  note: "5x18/19/20の円census（nC 84/95/104・長は7と8のみ）"
- path: research/experiments/five-row-q7-m20-20261114/sat-crosscheck/class_sat.js
  role: source
  note: "クラス分割SAT符号化（K0810 counter流用・rows∈D ≤5 / rows∉D ==6・k/minpos分割option）"
- path: research/experiments/five-row-q7-m20-20261114/sat-crosscheck/records_final.jsonl
  role: data
  note: "kissat 4.0.4による全19クラスUNSAT記録50件（17クラス直接・[0]/[1]はk×minpos分解・conflictsとwall time込み）"
- path: research/experiments/five-row-q7-m20-20261114/sat-crosscheck/control_5x18_sat.json
  role: data
  note: "陽性対照 5x18 [0] SAT→29石 rows (5,6,6,6,6) census不使用検証PASS（符号化のend-to-end検証）"
- path: research/experiments/five-row-q7-m20-20261114/report.md
  role: proof
  note: "手法・完全性根拠（L≥9円不在・行鏡映19類・列鏡映代表）・両系統の制御と限界の記録"
scope: "'有限完全列挙（DFS機）+ 独立SAT交叉確認（CDCL）の2系統。5x20のみ。'"
evidence: "'complete-enumeration（verification: deterministic-machine + independent-sat-cross-check）。本文の記述を参照。'"
---

# 5x20 q=7 row-deficient maximal nonexistence — all 19 canonical classes

## Claim

1. On the 5x20 integer grid (q=7), for every one of the 19 row-mirror-canonical deficiency
   classes D ⊆ {0..4} (rows in D hold ≤5 stones, rows outside D hold exactly 6), the complete
   enumeration of the K0738–K0759 machine over all 10,878 column-mirror representatives of the
   first deficient row's contents finds **witnesses 0 and leaves 0** (total 206,682
   representatives across classes).
2. Corollary: **every maximal safe configuration on 5x20 has row occupancy (6,6,6,6,6)**
   (exactly 30 stones); no deficient maximal safe configuration exists on 5x20.
3. Combined with K0332 (29-stone witness at 5x18) and K0738–K0759 (witness-free 5x19):
   the witness-free width set is {19, 20} and the least witness width is 18, so
   **M_{5,7} ∈ {19, 20} or M_{5,7} ≥ 22**; the witness-search frontier moves to 5x21.
   The upper bound 158 (K0332/K0024 substitution) is unchanged.

## Method

Complete finite enumeration by the K0738–K0759 machine ported to M=20
(`m20_runner.ts`; algorithm, search order and node counting identical to the m=19 machine).
Census completeness premise: the blocker DFS admits only circles of size 7–8 (a size-L blocking
circle needs exactly q−1=6 stones among L−1 other cells; L≥9 would need ≥2 further empties that the
DFS does not enumerate). The 5x20 census has 104 circles, sizes 7 and 8 only — no L≥9 circle
exists, so the DFS branch is complete at M=20 (as at M=19, nC=95 matching the K0759 census).
Controls: 5x19 DEF_ROWS=[0,1] NODE_CAP=600k reproduces the published pair-version slice A1
bit-exactly (done=117, maxCaseNodes=28,488 at idx 39, witnesses 0, leaves 0).

## Independent SAT cross-check

Class-split encoding (safety ≤6 per census curve via sequential ≥-counters, maximality
(empty cell ⇒ some curve through it has ≥6 stones), rows∈D ≤5, rows∉D exactly 6) on the K0810
census (circleABC integer triples — a census implementation independent of the runner's
circumcenter form), decided by kissat 4.0.4 (official linux-amd64 binary):

- 17/19 classes directly UNSAT (e.g. [0,1,2,3,4] 142,715 conflicts / 4.3 s; [0,1] 913,253 / 28.5 s).
- [0] and [1]: split by the deficient row's stone count k=0..5 (each an exact-partition unit
  constraint on the row counter), and k=5 further split by the row's leftmost-stone column
  minpos=0..9 (sound column-mirror symmetry break: every configuration or its mirror has
  minpos ≤ 9). All sub-instances UNSAT (hardest: [1] k=5 mp=0, 2.88M conflicts / 133.5 s).
- Positive control: 5x18 class [0] is SAT; the decoded model (29 stones, rows (5,6,6,6,6))
  passes the census-free independent verifier.

The two systems share no census, search or encoding code and agree on all classes and the
positive control. Raw run records (including superseded smaller-budget timeouts) are in
`records.jsonl`; deterministic conflict counts reproduced exactly across environment resets.

## Scope

Finite machine verification up to the correctness of the two independent implementations;
not a number-theoretic proof. Persistence at m ≥ 21 remains open (5x21 is the new frontier);
the full-capacity class structure, other widths, and the 11x11 empty board / two-stone root
{49,60} / S2 {59,60} / class 2 / class 4 are unaffected and remain UNKNOWN.
