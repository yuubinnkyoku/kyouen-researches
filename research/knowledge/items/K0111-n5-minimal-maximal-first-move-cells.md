---
id: K0111
title: 5×5の5石極大四配置は各々勝ち初手セル4・負け初手セル1を含む
kind: proposition
status: computed
topics:
- maximal-safe
- first-moves
aliases:
- F-AA
relations:
- type: depends_on
  target: K0030
  note: ''
- type: depends_on
  target: K0043
  note: ''
artifacts:
- path: research/findings.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: scripts/analysis/explore_n5_size5_reachability.py
  role: verifier
  note: 全四配置と初手セルの照合
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 5×5の5石極大四配置は各々勝ち初手セル4・負け初手セル1を含む

全四配置のセル分類はそれぞれ勝ち初手9点中4点、負け初手16点中1点。一方、安全配置の任意順の部分集合も安全なので、勝ち初手を選んでも任意対局ではこの五石集合へ到達可能。

F-AAの「五石終局は負け初手のときだけ理論上あり得る」という説明は過剰。最適戦略または証明書戦略で五石終局を避けることと、通常の到達可能性を分ける。
