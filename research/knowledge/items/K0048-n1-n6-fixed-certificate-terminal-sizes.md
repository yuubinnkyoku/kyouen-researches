---
id: K0048
title: 1×1〜6×6証明書の固定witness戦略での終局石数
kind: proposition
status: computed
topics:
- strategy-length
- certificates
aliases:
- F-Q
relations:
- type: depends_on
  target: K0007
  note: ''
artifacts:
- path: research/findings.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: scripts/analysis/explore_game_length_canon.py
  role: verifier
  note: 固定witness戦略と正規化済み子の追跡
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 1×1〜6×6証明書の固定witness戦略での終局石数

WINで保存witnessだけ、LOSSで全合法手を選んだとき、n=1〜6の終局サイズ集合は順に `{1}, {3}, {5}, {6}, {7,9}, {7,9,11}`。D4正規化を含めて合法子を再生成した記録。

F-Qの「最適終局」は固定証明書戦略に限る。後の独立全状態計算では5×5のT*は{5,7,9}なので、この族が全勝敗維持対局を尽くさないことが確認済み。F-Yの全最適対局への外挿は反証項目を参照する。
