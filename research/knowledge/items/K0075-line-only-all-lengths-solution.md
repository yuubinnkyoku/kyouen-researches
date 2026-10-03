---
id: K0075
title: line-onlyはq>wで全m強解決
kind: proposition
status: proved
topics:
- variants
- rectangles
- grundy
aliases: []
relations:
- type: depends_on
  target: K0074
  note: ''
artifacts:
- path: research/q-point-rule-variants.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
solution:
  board: line-only w×m
  level: strong
  outcome: conditional
  classification:
  - root
  - first-moves
  - all-safe-win-loss
  - all-safe-grundy
  coverage: 全m≥1・全安全局面
  conditions: line-only,q≥4,q>w
  verification:
  - mathematical-proof
  certificate: 幾何分離証明
  independent_check: 有限検算を一般証明と区別
  note: g=(w min(m,q−1)−|S|) mod2
---

# line-onlyはq>wで全m強解決

q>wなら非水平直線にq点は載らず、禁止集合は同一候補行内だけ。C=w min(m,q−1)として全安全局面g=(C−|S|) mod2、満容量安定化長M=q−1。行点数がm_iならC=Σ_i min(m_i,q−1)。

空盤の勝者はCの偶奇。候補平行行が等間隔である必要はない。
