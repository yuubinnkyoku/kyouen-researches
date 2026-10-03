---
id: K0076
title: circle-onlyはq>2wで全未占有点が合法
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
  board: circle-only w×m
  level: strong
  outcome: conditional
  classification:
  - root
  - first-moves
  - all-safe-win-loss
  - all-safe-grundy
  coverage: 全m≥1・全局面
  conditions: circle-only,q≥4,q>2w
  verification:
  - mathematical-proof
  certificate: 禁止なしの一般証明
  independent_check: 円と直線の交点上界
  note: g=(wm−|S|) mod2
---

# circle-onlyはq>2wで全未占有点が合法

一円とw平行行の共有点は高々2w<qなので禁止集合なし。全点を埋めるまで進み、全局面g=(wm−|S|) mod2。空盤先手勝ち iff wm奇数。

line-onlyや標準版の容量w(q−1)とは異なる。任意平行行に候補m_i点なら総点数Σ_i m_iに置き換えられる。
