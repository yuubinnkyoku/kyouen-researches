---
id: K0395
title: 90度回転対称点集合の共円・共線四点組数の法4公式
kind: proposition
status: proved
topics:
- geometry
- statistics
aliases: []
relations: []
artifacts:
- path: research/experiments/geometry/reports/quarter-turn-mod4-forbidden-quadruples-20261011.md
  role: proof
  note: 任意の四回回転対称点集合に対する全称証明
- path: research/experiments/geometry/scripts/quarter_turn_mod4_verify.cpp
  role: verifier
  note: n<=11と回転対称部分集合の独立整数行列式検査
- path: research/experiments/geometry/output/quarter_turn_mod4_20261011.json
  role: data
  note: 有限完全列挙の実測値
---

# 四回回転対称点集合の共円・共線四点組の法4公式

任意の有限点集合 P が90度回転で不変とする。回転中心を O とし、各半径 r の対蹠対数を a_r、O を通る各無向直線 L の対蹠対数を b_L とする。相異なる4点の共円型数 C(P)、共線型数 H(P) は

\[
C(P)\equiv\sum_r\binom{a_r}{2}\pmod4,\qquad
H(P)\equiv\sum_L\binom{b_L}{2}\pmod4.
\]

特に H(P) は偶数で、C(P) と禁止四点組総数の偶奇は `( |P|-1_{O in P} )/4` の偶奇に等しい。標準 n×n 盤の禁止四点組総数は n≡2 (mod4) のときに限り奇数となる。

90度回転の四点集合軌道は1,2,4要素であり、法4では半回転固定集合だけを数えればよい。半回転固定の4点集合は二つの対蹠対からなり、共円は同半径、共線は同一直線と同値。詳細な証明と検証の範囲は上記 proof を参照。

**境界**：これは勝敗やGrundy値の定理ではない。有限検査は n<=11 と明示した回転対称集合に限る。全称結論は幾何学的証明に基づく。
