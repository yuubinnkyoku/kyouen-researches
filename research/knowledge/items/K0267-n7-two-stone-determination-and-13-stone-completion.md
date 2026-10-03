---
id: K0267
title: 7×7最大配置は全て二石で一意に決まり、十三石部分集合は一意完了
kind: proposition
status: computed
topics:
- maximum-safe
- reconfiguration
aliases:
- Cycle8:min_det
relations:
- type: depends_on
  target: K0051
  note: ''
artifacts:
- path: night-research/FINAL_SELECTION_THEOREM.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: results/cycle8_c_determining_n7.csv
  role: data
  note: 全16配置の最小識別核
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: results/cycle9_small_n_min_det.json
  role: data
  note: 小盤最大族の独立比較
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 7×7最大配置は全て二石で一意に決まり、十三石部分集合は一意完了

最大族内でSを一意に特定する最小部分集合サイズmin_detはn7全16で2。全224個の十三石部分集合は元の最大配置だけへ完了する。従って異なる最大間を一石追加・削除で移るには一度十二石以下が必要。

n3..6のmin_det最小は4,3,3,3。n6の全464ヒストグラムは{3:160,4:240,5:40,6:24}。これは最大族内識別であって、二石からのゲーム継続を一意に決める主張ではない。
