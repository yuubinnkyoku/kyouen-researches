---
id: K0021
title: 9×9では81個すべての初手が先手勝ち
kind: computation
status: computed
topics:
- first-moves
- square-outcomes
aliases:
- H4
relations:
- type: depends_on
  target: K0002
  note: ''
- type: proves
  target: K0019
  note: 全初手の分類から空盤の勝敗が従う
artifacts:
- path: night-research/first-moves-9x9.csv
  role: data
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: README.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: cpp/solvers/kyouen_solver_9_root.cpp
  role: solver
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
solution:
  board: 9×9（全初手）
  level: weak
  outcome: first-player-win
  classification:
  - root
  - first-moves
  coverage: 81/81 first moves
  conditions: 標準q=4・完全指摘・通常プレイ
  verification:
  - exact-search
  certificate: 中央初手の空盤証明書あり。全81初手は別探索
  independent_check: 14非中央D4クラスの独立探索記録
  note: 全81初手が先手勝ち
---

# 9×9では81個すべての初手が先手勝ち

中央以外の14 D4クラスを逐次独立に厳密探索し、中央を含む全81点が勝ち初手と確定した。H4の「中央以外にも勝ち手がある」は未確定ではなく成立済み。

初手CSVと空盤面から中央へ進む共通証明書は別の根拠。全81初手を一つの同じ空盤証明書が直接検査したとは言わない。
