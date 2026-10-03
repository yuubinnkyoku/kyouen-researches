---
id: K0068
title: 標準q=4固定幅盤はm≥3+2{C(3w−2,3)−(w−1)}で全局面偶奇式
kind: proposition
status: proved
topics:
- rectangles
- grundy
aliases:
- B212
- B215
- B216
relations:
- type: depends_on
  target: K0024
  note: ''
- type: refutes
  target: K0154
  note: 本文の証明・証人が原文に与える帰結
- type: refutes
  target: K0155
  note: 本文の証明・証人が原文に与える帰結
- type: refutes
  target: K0262
  note: 本文の証明・証人が原文に与える帰結
- type: refutes
  target: K0263
  note: 本文の証明・証人が原文に与える帰結
artifacts:
- path: research/verification/round4-fixed-width.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
solution:
  board: w×m・標準q=4
  level: strong
  outcome: conditional
  classification:
  - root
  - first-moves
  - all-safe-win-loss
  - all-safe-grundy
  coverage: 全安全局面
  conditions: w固定、m≥T_w=3+2{C(3w−2,3)−(w−1)}
  verification:
  - mathematical-proof
  certificate: 全称証明
  independent_check: 有限長方形検算は支持
  note: g=(3w−|S|) mod2
---

# 標準q=4固定幅盤はm≥3+2{C(3w−2,3)−(w−1)}で全局面偶奇式

w固定、T_w=3+2{C(3w−2,3)−(w−1)}とする。m≥T_wなら全極大集合は3w石で、全安全局面のg(S)=(3w−|S|) mod2。
幅w=1〜6の十分長さT_wは順に `3, 9, 69, 237, 567, 1,113`。

全局面強解決の一般証明で、真の最小開始長はこの上界とは限らない。幅3の最終非周期性・固定幅の部分勝ち初手が無限にあるという予想を否定する。
