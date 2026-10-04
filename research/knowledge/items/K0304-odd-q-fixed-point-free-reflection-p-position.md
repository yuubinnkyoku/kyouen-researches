---
id: K0304
title: 奇数qの固定点なし鏡映対称安全局面はP局面
kind: proposition
status: proved
topics: [rectangles, variants, grundy]
aliases: []
relations: []
artifacts:
- path: research/experiments/fixed-width/reports/q48-odd-q-reflection.md
  role: proof
  note: 鏡映対称応答の一般定理
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/experiments/fixed-width/output/q48_odd_q_reflection.json
  role: data
  note: 有限例の検算
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
---

# 奇数qの固定点なし鏡映対称安全局面はP局面

遺伝的なq点禁止配置ゲームでqが奇数、盤面の固定点なし鏡映がルールを保ち、現在局面も鏡映対称なら、その局面は後手勝ちP局面になる。相手の着手を鏡像で返すと、奇数個の禁止集合が鏡映対になれないため応答の合法性が保たれる。

特に適用条件を満たす偶数面積の長方形盤では空盤が全長で後手勝ちになる。
