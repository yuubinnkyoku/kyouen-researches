---
id: K0530
title: 2×k×m・4点共面禁止版の全長容量・三石極大数と2×3×3の全局面
kind: proposition
status: proved
topics: [variants, geometry, maximum-safe, maximal-safe, grundy, first-moves]
aliases: []
relations:
- type: depends_on
  target: K0002
  note: 通常・misèreのGrundy定義
- type: generalizes
  target: K0527
  note: 2×2×mのK・sを含むが、全局面Grundy偶奇則は一般化しない
- type: generalizes
  target: K0526
  note: 2×2×2の容量と最小極大石数を含む
artifacts:
- path: research/experiments/coplanar-two-layer-all-widths-20261024/proof.md
  role: proof
  note: 全k,mの容量・三石極大数の数学的証明と2×3×3の完全列挙境界
- path: research/experiments/coplanar-two-layer-all-widths-20261024/verify.py
  role: verifier
  note: 3×3整数行列式と全安全局面mex
- path: research/experiments/coplanar-two-layer-all-widths-20261024/independent.cpp
  role: verifier
  note: 独立4×4行列式と全局面再帰
- path: research/experiments/coplanar-two-layer-all-widths-20261024/results.md
  role: data
  note: 4盤の独立一致結果と境界盤の局面分布
scope: 3次元2×k×m整数格子・4点共面禁止・全k,m≥1のK,s,三石極大数、2×3×3の全安全局面
solution:
  board: 2×3×3・4点共面禁止
  level: strong
  outcome: conditional
  classification: [root, first-moves, all-safe-win-loss, all-safe-grundy, safe-layers]
  coverage: 2×3×3の全6456安全局面。全k,mのK,s,三石極大数は数学的証明
  conditions: 通常は先手勝ち、misèreは後手勝ち。一般の2×k×mの空盤勝敗は未解決
  verification: [mathematical-proof, exhaustive-enumeration, independent-enumeration]
  certificate: 全k,mの容量・三石極大数の初等証明と2×3×3の全2^18部分集合検査
  independent_check: Python外積とC++4×4行列式展開で4盤の全局面集計が一致
  note: k,m≥3はK=6,s=3。2×3×3ではg(空)=1,h(空)=0、通常勝ち初手8個
---

# 2×k×mの4点共面禁止版

全整数k,m≥1について、Kは(1,1)で2、min(k,m)=1かつkm>1で3、min(k,m)=2で5、k,m≥3で6。最小極大石数sは(1,1)で2、(2,2)で4、それ以外は3。k,m≥2では三石極大配置は共線三石に限り、個数は `2T(k,m)`（Tは格子k×m内の共線三石数）。これらは全称証明済み。

2×3×3は安全局面6456、極大局面は3石16・5石1064・6石368。通常空盤Grundy値1、misère補助値0。通常版は8個の勝ち初手を持つ先手勝ち、misère版は後手勝ち。これらは二方式の独立した有限完全列挙で確定。

[証明と検証手順](../../experiments/coplanar-two-layer-all-widths-20261024/proof.md)。一般の2×k×mの全局面Grundy値や空盤勝敗を主張しない。
