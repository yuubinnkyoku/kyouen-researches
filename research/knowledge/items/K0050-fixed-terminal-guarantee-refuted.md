---
id: K0050
title: 勝者が終局石数を事前宣言して必ず勝てるという仮説は7×7で偽
kind: proposition
status: refuted
topics:
- strategy-length
aliases:
- B040
relations:
- type: depends_on
  target: K0005
  note: ''
- type: depends_on
  target: K0049
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round28-seven-board-original-verdicts.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 勝者が終局石数を事前宣言して必ず勝てるという仮説は7×7で偽

7×7空盤はP、T*={8,10,12,14}、WFT=∅。後手の必勝と固定終局長保証は別で、原文B040は反証済み。
n=1〜6の空盤WFTは順に `{1}, {3}, {5}, {6}, {7}, {9}` であり、最初の反例盤は7×7。

T*に複数値があること自体を反証理由にせず、相手全選択に対するWFTの空性を根拠とする。
