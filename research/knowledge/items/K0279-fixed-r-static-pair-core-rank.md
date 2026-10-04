---
id: K0279
title: 固定R内LOSS pairコアのstatic witness順位は深さ一様でない
kind: proposition
status: refuted
topics:
- search-methods
- geometry
aliases:
- Cycle1:H4
relations:
- type: depends_on
  target: K0080
  note: ''
artifacts:
- path: research/log/discovery-cycles/CYCLE1_RESULTS.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/structural-discovery/output/h4-pair-witness.json
  role: data
  note: 固定Rの深さ別pair witness照合
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 固定R内LOSS pairコアのstatic witness順位は深さ一様でない

10×10の固定8石Rの同一入力座標で、pairを含む禁止四点数wを使って各深さのLOSS pairコアを説明する仮説。k3の{90,91}はw87、k4/6の{61,66}はw165で最大だが、k5の{13,91}はw24に対し{66,73}が105となり深さ一様則は失敗する。

これは固定Rのpair被覆順位で、三→四石追加のunique gain非重複定理とは異なる量。石91が全11LOSS五石subsetに現れてもWIN24/45にも現れ、必要だけで十分でない。別々のD4正規化による共通座標の喪失だけを元frame仮説の反証には使わない。
