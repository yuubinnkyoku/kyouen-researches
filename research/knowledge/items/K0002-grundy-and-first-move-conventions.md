---
id: K0002
title: Grundy数・P/Nと勝ち初手の向き
kind: definition
status: active
topics:
- rules
- grundy
- first-moves
aliases: []
relations:
- type: depends_on
  target: K0001
  note: ''
artifacts:
- path: research/hypothesis-bank-2026-09-27.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: night-research/CYCLE4_EXACT_STRUCTURE.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# Grundy数・P/Nと勝ち初手の向き

g(S)=mex{g(S∪{p}):pは合法}、終局はg=0。Pは手番側負け、Nは手番側勝ち。初手pが先手の勝ち手であるための条件は、相手番の子{p}がPであること。CSVのWIN/LOSSが着手者と手番側のどちらを指すかを必ず確認する。

分離した通常プレイ成分のGrundy値はxorで合成できるが、私有パス変種では自動適用しない。
