---
id: K0072
title: 標準整数行のmod9制約は高q全長分離領域を拡大する
kind: proposition
status: proved
topics:
- rectangles
- geometry
- variants
aliases:
- F-BN
relations:
- type: depends_on
  target: K0001
  note: ''
artifacts:
- path: research/q2w-boundary-structure.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/q2w_boundary_structure.json
  role: data
  note: mod9全剰余とlifted determinant照合
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
solution:
  board: 高qの標準整数格子
  level: strong
  outcome: conditional
  classification:
  - root
  - first-moves
  - all-safe-win-loss
  - all-safe-grundy
  coverage: 全m≥1・全安全局面
  conditions: 連続整数行、(q=2w,w≥5)または(q=2w−1,w≥6)
  verification:
  - mathematical-proof
  certificate: mod9有限剰余証明
  independent_check: 円条件の独立determinant照合
  note: M=q−1
---

# 標準整数行のmod9制約は高q全長分離領域を拡大する

整数格子の連続行で、円は5連続行の全てを二重点で通れず、6連続行のうち二重点行は高々4。平方剰余mod9の有限分類で証明する。

従ってq=2w,w≥5およびq=2w−1,w≥6では行をまたぐ禁止q集合なし。全m≥1でg(S)=(w min(m,q−1)−|S|) mod2、M=q−1。任意の平行線配置へは主張しない。
