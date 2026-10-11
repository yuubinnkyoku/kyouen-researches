---
id: K0383
title: 非原始二重点行の最小幅 F(k)：2〜32本
kind: proposition
status: proved
topics:
- geometry
- rectangles
- variants
aliases: []
relations: []
artifacts:
- path: research/experiments/fixed-width/reports/nonprimitive-double-rows-first-widths-2-32-20261010.md
  role: proof
  note: 訂正版：F(9)=43とせず41<=F(9)<=43
- path: research/experiments/fixed-width/scripts/check_nonprimitive_rows_2_32.py
  role: verifier
  note: 明示円の整数平方根走査とgcd確認
- path: research/experiments/fixed-width/scripts/run_nonprimitive_rows_2_32.py
  role: verifier
  note: 二方式のC++合同マスク照合
- path: research/experiments/fixed-width/output/nonprimitive_rows_2_32_audit.csv
  role: data
  note: 30値とF(9)境界の監査表
- path: research/log/2026-10-10-fast-nonprimitive-2-32.md
  role: log
  note: 訂正版の検討・検証経緯
scope: 非原始二重点行の最小幅F(k)、2<=k<=32（k=9を除く）とF(9)の境界
evidence: 合同必要条件の完全排除、明示円構成、独立平方根検査。
---

一本の実円が異なる整数格子点を2点ずつ持つ水平行からk本を選び、行番号差の最大公約数が2以上となる最小連続幅を `F(k)` とする。`2<=k<=32` のうち9を除く30個は厳密に決定された。

| k | F(k) | k | F(k) |
|---:|---:|---:|---:|
| 2 | 3 | 3 | 5 |
| 4 | 7 | 5 | 13 |
| 6 | 15 | 7 | 21 |
| 8 | 23 | 10 | 45 |
| 11 | 49 | 12 | 51 |
| 13 | 85 | 14 | 87 |
| 15 | 91 | 16 | 95 |
| 17 | 165 | 18 | 173 |
| 19 | 187 | 20 | 191 |
| 21 | 199 | 22 | 201 |
| 23 | 209 | 24 | 211 |
| 25 | 421 | 26 | 427 |
| 27 | 441 | 28 | 451 |
| 29 | 463 | 30 | 465 |
| 31 | 469 | 32 | 471 |

`F(9)` は未確定で `41<=F(9)<=43`。幅41・42の合同条件では候補が残るため、旧版の `F(9)=43` は採用しない。上界証人は円 `x²+y²=650`。

下界は円係数・半径に有限上限を置かず、平方剰余必要条件を各法で完全列挙する。上界は整数平方根の直接走査とgcd確認による。T(w)の厳密値への含意は主張しない。
