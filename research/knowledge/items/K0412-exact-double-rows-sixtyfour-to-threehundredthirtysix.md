---
id: K0412
title: 標準整数格子64〜336行で円が二点ずつ通る行数の厳密最大値
kind: proposition
status: proved
topics:
- geometry
- rectangles
- variants
aliases: []
relations:
- type: depends_on
  target: K0369
  note: T(63)=16を帰納基底とする
artifacts:
- path: research/experiments/fixed-width/reports/exact-double-rows-64-211-20261009.md
  role: proof
  note: 64〜211行の累積上界・構成
- path: research/experiments/fixed-width/reports/exact-double-rows-64-256-20261009.md
  role: proof
  note: 212〜256行の接続証明
- path: research/experiments/fixed-width/reports/exact-double-rows-257-300-20261009.md
  role: proof
  note: 257〜300行の接続証明
- path: research/experiments/fixed-width/reports/exact-double-rows-301-310-20261009.md
  role: proof
  note: 301〜310行の接続証明
- path: research/experiments/fixed-width/reports/exact-double-rows-311-320-20261009.md
  role: proof
  note: 311〜320行の接続証明
- path: research/experiments/fixed-width/reports/exact-double-rows-321-326-20261009.md
  role: proof
  note: 321〜326行の接続証明
- path: research/experiments/fixed-width/reports/exact-double-rows-327-336-20261009.md
  role: proof
  note: 327〜336行の接続証明
- path: research/experiments/fixed-width/scripts/verify_double_rows_64_256.cpp
  role: verifier
  note: 64〜256行の有限合同検査
- path: research/experiments/fixed-width/scripts/verify_double_rows_257_320.cpp
  role: verifier
  note: 257〜320行の合同マスク検査
- path: research/experiments/fixed-width/scripts/verify_double_rows_301_310.cpp
  role: verifier
  note: 301〜310行の有限排除
- path: research/experiments/fixed-width/scripts/verify_double_rows_311_320.cpp
  role: verifier
  note: 311〜320行の有限排除
- path: research/experiments/fixed-width/scripts/verify_double_rows_321_326.cpp
  role: verifier
  note: 321〜326行の有限排除
- path: research/experiments/fixed-width/scripts/verify_double_rows_327_336.cpp
  role: verifier
  note: 327〜336行の有限排除
scope: 標準整数格子、全連続幅64<=w<=336
evidence: T(63)=16を基底とした合同必要条件の有限完全排除および明示円の構成。
---

連続する `w` 本の整数水平行に対し、一本の実円が相異なる整数格子点を2点ずつ含む行数の最大値を `T(w)` とする。全ての `64<=w<=336` の厳密値は以下。

| w | T(w) |
|---|---:|
| 64〜82 | 16 |
| 83〜86 | 17 |
| 87〜93 | 18 |
| 94〜95 | 19 |
| 96〜99 | 20 |
| 100 | 21 |
| 101〜104 | 22 |
| 105 | 23 |
| 106〜210 | 24 |
| 211〜213 | 25 |
| 214〜220 | 26 |
| 221〜225 | 27 |
| 226〜231 | 28 |
| 232 | 29 |
| 233〜234 | 30 |
| 235 | 31 |
| 236〜336 | 32 |

上界は二重点行差のgcdと平方剰余の必要条件から有限候補へ帰着し、全候補を排除する計算機援用証明。下界は明示的整数円で達成し、整数判別式・座標を直接確認する。区間証明を `T(63)=16` の基底から順に接続し、301〜336区間も直前の値を基底とする。

有限完全な合同条件排除と構成による全称結果で、形式証明器による検証ではない。横方向と円中心・半径に制限はない。w>336の個別値は含まない。
