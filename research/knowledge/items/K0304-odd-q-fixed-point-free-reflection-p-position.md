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
- path: research/experiments/game-structure/reports/symmetry-scope-20261005.md
  role: proof
  note: 円・直線への適用範囲を明示し、任意禁止族への過大な拡張を訂正
scope: 平面の有限点集合における円・直線のq点禁止、真の直線鏡映、奇数q≥3
---

# 奇数qの固定点なし鏡映対称安全局面はP局面

平面の有限点集合で円・直線のq点を禁止するゲームでは、qが奇数、盤面が真の直線鏡映を保ち、その鏡映に固定点がなく、現在局面も鏡映対称なら、その局面は後手勝ちP局面になる。circle-onlyとline-onlyにも適用できる。

相手の合法着手pの鏡像τ(p)を返す。禁止曲線が両方の新点を含まなければ、鏡像曲線が最初の手で既に禁止を作る。両新点を含む円・直線は鏡映不変となり、元の対称局面上の点数が偶数なので、初めて奇数q点に達することができない。この幾何条件が応手の合法性を保証する。

旧本文の「遺伝的なq点禁止配置ゲーム」という量化は広すぎた。任意の禁止q点集合族へは拡張できず、奇数q≥3ごとにq+1頂点の反例がある（K0337）。既存証明の平面円・直線定理は有効であり、今回その適用範囲を正確にした。

特に適用条件を満たす偶数面積の長方形盤では空盤が全長で後手勝ちになる。
