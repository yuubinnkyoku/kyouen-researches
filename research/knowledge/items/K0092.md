---
id: K0092
title: 11×11 DFPN hybridの局所完了と回帰は空盤勝敗を閉じていない
kind: proposition
status: observed
topics:
- search-methods
- verification
aliases: []
relations:
- type: depends_on
  target: K0023
  note: ''
artifacts:
- path: research/verification/N11-DFPN-NIGHT-REPORT-2026-09-30.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: cpp/solvers/kyouen_dfpn_root.cpp
  role: solver
  note: 128-bit DFPNとexact handoff
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/N11-DFPN-VALIDATION.md
  role: verifier
  note: 小盤回帰とUNKNOWN伝播
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 11×11 DFPN hybridの局所完了と回帰は空盤勝敗を閉じていない

後日のDFPN報告も空盤UNKNOWN。hybrid小盤n4..7回帰、forced abortでも同勝敗、n6 replay6942/6942一致、23keyは順序反転でもresult/node決定的。

選択s5局面23件はcold10M budgetで全完了（12WIN/11LOSS）だが、11×11空盤のAND/OR全証明にはならない。proof number、TIMEOUT、量子heuristic、未完探索から根ラベルを推測しない。
