---
id: K0539
title: 2×k×m・4点共面禁止版の空盤勝敗と全初手Grundy値の完全分類
kind: proposition
status: proved
topics: [variants, geometry, grundy, first-moves]
aliases: []
relations:
- type: depends_on
  target: K0530
  note: k,m≥3かつk+m≥10の無界全局面Grundy定理
- type: depends_on
  target: K0527
  note: 2×2×m（m≥3）の無界全局面偶奇則
- type: depends_on
  target: K0526
  note: 2×2×2の例外と独立有限完全列挙
artifacts:
- path: research/experiments/coplanar-two-layer-all-openings-20261024/proof.md
  role: proof
  note: 無界既存定理と有限境界の合成による全正整数の証明
- path: research/experiments/coplanar-two-layer-all-openings-20261024/results.md
  role: data
  note: 11盤の空盤・初手値分布と二方式一致範囲
- path: research/experiments/coplanar-two-layer-all-openings-20261024/direction_audit.cpp
  role: verifier
  note: 二層の原始方向集合による全安全局面列挙とmex
- path: research/experiments/coplanar-two-layer-all-openings-20261024/determinant_audit.cpp
  role: verifier
  note: 整数行列式による独立した全安全局面列挙とmex
scope: 3次元2×k×m整数格子・4点共面禁止・全正整数k,mの空盤と全初手、通常・misère
solution:
  board: 2×k×m・4点共面禁止
  level: weak
  outcome: conditional
  classification: [root, first-moves]
  coverage: 全正整数k,mの空盤と全2km初手について通常Grundy・misère補助値を分類
  conditions: 通常先手勝ちは薄い非正方断面または3×3断面。misère先手勝ちは1×1断面または3×3以外の両辺3以上
  verification: [mathematical-proof, exhaustive-enumeration, independent-enumeration]
  certificate: K0527・K0530の無界定理と有限境界6盤の完全mex列挙、2×2例外の完全列挙
  independent_check: 原始方向集合方式と直接整数行列式方式で7盤の全初手値分布まで一致
  note: 3×3断面のみ通常初手の値が三種類(0,2,3)に分かれる。2×2断面は両ルール後手勝ち
---

# 2×k×m・4点共面禁止版の空盤と全初手

**全正整数 k,m で、通常・misèreの空盤勝敗と全初手後のGrundy値を完全分類した。**

通常版で先手必勝となる必要十分条件は、**`min(k,m)∈{1,2}` かつ `max(k,m)>min(k,m)`、または `(k,m)=(3,3)`**。前者には (1,2),(1,3),…,(2,3),(2,4),… が含まれ、(1,1),(2,2) は含まれない。

misère版で先手必勝となる必要十分条件は **`(k,m)=(1,1)`、または `k,m≥3` かつ `(k,m)≠(3,3)`**。2×2×2では両ルールとも後手必勝。

初手後の値は `(1,1)` なら全2点で `(g,h)=(1,0)`、薄い非正方断面なら全点で `(0,1)`、`(2,2)` なら全8点で `(2,1)`、`k,m≥3` で `(3,3)` 以外なら全点で `(1,0)`。**例外の `(3,3)` だけ**、初手後が各層辺中央8点で `(0,1)`、各層中央2点で `(2,1)`、各層四隅8点で `(3,1)` と分かれる。

証明はK0527・K0530の全称定理と、境界盤の独立した二方式の有限完全列挙を組み合わせる。薄盤の (1,1) は直接証明、(2,2) は例外を全数検算。全称部分と有限計算を混同しない。

[証明](../../experiments/coplanar-two-layer-all-openings-20261024/proof.md)・[結果](../../experiments/coplanar-two-layer-all-openings-20261024/results.md)。
