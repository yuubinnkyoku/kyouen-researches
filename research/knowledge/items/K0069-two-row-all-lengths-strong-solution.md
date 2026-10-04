---
id: K0069
title: 標準二行盤は全mで強解決、m≥6の空盤は後手勝ち
kind: proposition
status: proved
topics:
- rectangles
- grundy
aliases:
- B548
- B211
- B542
- B550
relations:
- type: depends_on
  target: K0068
  note: ''
- type: refutes
  target: K0260
  note: 本文の証明・証人が原文に与える帰結
- type: proves
  target: K0259
  note: 本文の証明・証人が原文に与える帰結
artifacts:
- path: research/experiments/original-claims/reports/round4-two-row-order-strategy.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/reports/round4-fixed-width.md
  role: proof
  note: 長さ9以上と短盤全数の接続
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
solution:
  board: 2×m・q=4
  level: strong
  outcome: conditional
  classification:
  - root
  - first-moves
  - all-safe-win-loss
  - all-safe-grundy
  coverage: 全m≥1・全安全局面
  conditions: q=4,m≥1
  verification:
  - exhaustive-enumeration
  - mathematical-proof
  certificate: 短盤全数＋長盤一般証明
  independent_check: 短盤参照mex検算
  note: m≥6は空盤後手勝ち。短盤は個別分類
---

# 標準二行盤は全mで強解決、m≥6の空盤は後手勝ち

q=4の2×mはm=1..8の全安全局面計算とm≥9の一般定理で全長強解決。全mでg≤3、空盤はm≥6でg=0、m=6..8の順序型戦略表も構成済み。m≥9では全極大6石で全局面g=(6−|S|) mod2。

十分長い二行盤の全極大6石というB548もこの一般証明で成立済み。q≥5の全長分離結果と合わせ、全q≥4・全mの二行版を強解決できる。
