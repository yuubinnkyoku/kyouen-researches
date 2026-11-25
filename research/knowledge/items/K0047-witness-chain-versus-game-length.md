---
id: K0047
title: 証明書のWIN証人鎖の長さは対局長ではない
kind: proposition
status: computed
topics:
- certificates
aliases:
- F-M
relations:
- type: depends_on
  target: K0007
  note: ''
artifacts:
- path: research/archive/hypothesis-ledgers/findings.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: scripts/analysis/explore_cert_game_length.py
  role: verifier
  note: witness鎖とAND分岐の区別
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 証明書のWIN証人鎖の長さは対局長ではない

n≤7のWIN根からwitnessだけを辿ると空盤WIN→一石LOSSで止まる。LOSSは単一witnessを持たず全合法子で証明するので、対局終端に着いたわけではない。後手盤のLOSS根なら初めから単一証人鎖なし。

二ノードという観測を二手で終局するゲーム則と解釈しない。
