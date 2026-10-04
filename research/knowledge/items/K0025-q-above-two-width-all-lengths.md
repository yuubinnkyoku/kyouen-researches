---
id: K0025
title: q>2wでは全長の固定幅盤が分離し強解決
kind: proposition
status: proved
topics:
- rectangles
- variants
- grundy
aliases:
- F-BI
relations:
- type: depends_on
  target: K0002
  note: ''
artifacts:
- path: research/experiments/fixed-width/reports/q-point-fixed-width.md
  role: proof
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
solution:
  board: w×m・q>2w
  level: strong
  outcome: conditional
  classification:
  - root
  - first-moves
  - all-safe-win-loss
  - all-safe-grundy
  coverage: 全m≥1・全安全局面
  conditions: q≥4,q>2w,m≥1
  verification:
  - mathematical-proof
  certificate: 一般分離証明
  independent_check: 整数幾何と容量の証明
  note: g=(w min(m,q−1)−|S|) mod2
---

# q>2wでは全長の固定幅盤が分離し強解決

q>2wでは円はw行と高々2w点共有し、非水平直線は高々w点なので禁止q点は同一行だけ。全m≥1でg(S)=(w min(m,q−1)−|S|) mod2、満容量への真の安定化長M=q−1。

w=2,q≥5は全長で後手勝ち。q=4二行版は別の有限全数と長盤定理を併用して全長強解決する。
