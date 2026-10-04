---
id: K0034
title: 10×10の最小極大安全サイズは9≤s_10≤10
kind: proposition
status: proved
topics:
- maximal-safe
aliases:
- F-AJ
- F-AK
relations:
- type: depends_on
  target: K0033
  note: ''
- type: depends_on
  target: K0038
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round56-ten-board-eight-stone-exclusion.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round56_complete_verified.json
  role: data
  note: 接頭部・再開部分・全五分割の接続監査
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/reports/round59-60-final-ten-board-search.md
  role: source
  note: 九石UNKNOWNと最終境界
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 10×10の最小極大安全サイズは9≤s_10≤10

八石候補を初点0..4に分け、旧完了接頭部とRound56の全再開部分を接続して八石以下の全域排除を監査した。安全十石極大があるので9≤s_10≤10。

九石SATは600秒でUNKNOWN。旧の7..11などの区間は現在の境界ではない。九石不存在もs_10=10もまだ証明されていない。
