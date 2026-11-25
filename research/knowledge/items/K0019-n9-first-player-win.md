---
id: K0019
title: 9×9は先手必勝
kind: proposition
status: proved
topics:
- square-outcomes
aliases: []
relations:
- type: depends_on
  target: K0007
  note: ''
artifacts:
- path: results/outcomes.csv
  role: data
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: results/certificates.csv
  role: manifest
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: results/all-certificates-check.txt
  role: log
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
solution:
  board: 9×9
  level: weak
  outcome: first-player-win
  classification:
  - root
  coverage: 空盤面からの勝敗維持戦略
  conditions: 標準q=4・完全指摘・通常プレイ
  verification:
  - ranked-and-or-certificate
  - independent-cpp-check
  certificate: 空盤面AND/OR証明書あり
  independent_check: 共通C++全件検査
  note: 全局面分類とは別
---

# 9×9は先手必勝

標準q=4・完全指摘・通常プレイの9×9は先手必勝。空盤面を根にする順位付きAND/OR証明書の全局所条件が独立C++検査済み。

空盤の弱解決は、全局面Grundyや全初手分類とは別の知識。9×9証明書の根証人は中央(4,4)で、証明書単体は全81初手を証明しない。
