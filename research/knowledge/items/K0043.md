---
id: K0043
title: 5×5の勝ち初手は市松偶色から四隅を除く9点、負け初手後のgは3
kind: proposition
status: computed
topics:
- first-moves
- grundy
aliases: []
relations:
- type: depends_on
  target: K0004
  note: ''
artifacts:
- path: night-research/CYCLE4_EXACT_STRUCTURE.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: night-research/CYCLE5_GRUNDY_STRUCTURE.md
  role: source
  note: 一石Grundyの完全分布
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 5×5の勝ち初手は市松偶色から四隅を除く9点、負け初手後のgは3

W_5={(x,y):x+y偶数}から四隅を除く9点。勝ち初手の子g=0、残り16初手の子g=3。相手の勝ち応手は角の負け初手で4個、他の負け初手で2個。

初手後の合法手数は常に24なので勝ち負けを区別しない。Python全数とRust初手実装でセル単位照合。標準の両禁止条件を使い、circle-only/line-onlyへの流用はしない。
