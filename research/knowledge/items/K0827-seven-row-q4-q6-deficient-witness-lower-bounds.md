---
id: K0827
title: "7xm q=4,5,6 row-deficient witness bands — witnesses 7x4..7x14 (q=4), 7x5..7x22 (q=5), 7x6..7x26 (q=6); M_{7,4} >= 15, M_{7,5} >= 23, M_{7,6} >= 27; first results for the three families"
kind: proposition
status: computed
topics: [rectangles, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0810
  note: "census + sequential-counter/maximality core used verbatim (sat.js/sat2.js); def-mode single clause is the complete encoding of 'total < 7(q-1) iff some row <= q-2'"
- type: depends_on
  target: K0068
  note: "(7,4) upper bound T_7 = 3+2{C(19,3)-6} = 1929 by the general q=4 parity theorem (all maximals 3w stones, g=(3w-|S|) mod2 for m >= T_w); matches K0318 substitution U=1929"
- type: depends_on
  target: K0318
  note: "upper bounds U_{7,6}=862, U_{7,5}=1142 by curve-packing substitution (w7_upper_bounds.json of seven-row-inband-families-20261114)"
- type: depends_on
  target: K0826
  note: "same machinery and runner as the (7,7) search (same session, same binary); q <= w families confirmed to have continuous witness bands from m=q"
artifacts:
- path: research/experiments/seven-row-q4-q6-witness-search-20261114/report.md
  role: proof
  note: "claims, per-family results tables, method (sat2.js all-triples census at q<=w, m>=q minimum width), dual verification protocol, honest unswept frontiers, scope and limits"
- path: research/experiments/seven-row-q4-q6-witness-search-20261114/output/q6-def-search/records.jsonl
  role: data
  note: "21 records m=6..26 all SAT dual-verified: m=6..15 deep deficiency 20..33 stones, m=16..25 single-deficiency 34 stones, m=26 33 stones rows 5/5/5/5/5/3/5 (441,809 conflicts); raw kissat output for m=26 included"
- path: research/experiments/seven-row-q4-q6-witness-search-20261114/output/q5-def-search/records.jsonl
  role: data
  note: "18 records m=5..22 all SAT dual-verified: deep deficiency 14..26 stones then single-deficiency 27 stones (m=20 has a 25-stone witness with a 1-stone row 4/1/4/4/4/4/4); raw kissat output for m=22 included"
- path: research/experiments/seven-row-q4-q6-witness-search-20261114/output/q4-def-search/records.jsonl
  role: data
  note: "11 records m=4..14 all SAT dual-verified 0 conflicts: 8..15 stones, deficiency 13..6, [3,3,3,3,1,1,1]-type at m=12..14; raw kissat output for m=14 included"
scope: "finite machine verification: kissat 4.0.4 (all instances); widths stated per family only; up to census completeness and solver correctness"
evidence: "complete-encoding SAT instances (def mode is exactly 'exists row-deficient maximal safe config') + constructive dual-verified witnesses (census-free sat.js verifyConfig + Python Fraction, all records jsVerify/pyVerify true) + deterministic CNF regeneration from the calibrated sat2.js. See report.md."
---

# 7×m q=4,5,6 行欠損witness帯 — 3ファミリー初の結果（M_{7,4} ≥ 15・M_{7,5} ≥ 23・M_{7,6} ≥ 27）

## 主張

1. **(7,6)**: 行欠損の極大安全配置が **m=6..26 の全幅で存在**
   （m=6..15 深欠損 20..33石・m=16..25 単一欠損34石・m=26 は33石
   rows 5/5/5/5/5/3/5・441,809 conflicts）。
   **M_{7,6} ≥ 27**（上界 862・K0318 代入）。
2. **(7,5)**: **m=5..22 の全幅で存在**（m=16..22 は単一欠損27石を含む。
   m=20 は25石・1石行 4/1/4/4/4/4/4 の深欠損例）。
   **M_{7,5} ≥ 23**（上界 1142・K0318 代入）。
3. **(7,4)**: **m=4..14 の全幅で存在**（8..15石・deficiency 13..6。
   m=12..14 は [3,3,3,3,1,1,1] 型15石）。
   **M_{7,4} ≥ 15**。上界は **K0068 の一般 q=4 偶奇定理 T_7=1929**
   （K0318 代入 U=1929 と一致）。
4. すべて 2系統検証（census 不使用 sat.js verifyConfig + Python Fraction）
   で safe + maximal + 行欠損 PASS。

## 手法と検証

K0810 の sat2.js を verbatim（q ≤ w で genfast.js 不適用・全三つ組census。
census は m ≥ q を要求し、最小幅は m=q）。kissat 4.0.4 公式バイナリ。
決定性: 同一セッションの (7,7) 実験で m=24 conflicts bit-exact 再現を確認
（K0826）・本実験の全 CNF はスクリプトから決定的に再生成可能。

## 観測（全称主張ではない）

q ≤ w の 7行族（q=4,5,6,7）は m=q から継続的な witness 帯を持ち、
深欠損から単一欠損へ移行する。q > w の (7,8)..(7,10) では witness-free 帯が
出現するのと対照的。K0318/K0068 の上界は witness が有限幅で消えることを保証。

## 範囲と限界

有限機械検証。前線は 7×27 (q=6)・7×23 (q=5)・7×15 (q=4)。
sat2.js census の実用範囲（n=7m ≈ 200）を超える延長には
帯状censusの一般化（genfast の q ≤ w 版）が必要。M の確定には
前線評価と上界改善（K0342 型 tail 評価）が残る。

## 備考

K番号は作業時点での仮番号（AGENTS.md の再採番規則による）。
