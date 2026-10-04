---
id: K0057
title: 禁止四点組の有限総数と共線・共円の排他的分解
kind: proposition
status: computed
topics:
- geometry
aliases:
- F-L
- F-AI
- F-AW
relations:
- type: depends_on
  target: K0001
  note: ''
artifacts:
- path: research/archive/hypothesis-ledgers/findings.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: scripts/analysis/explore_geometry_closed_form.py
  role: verifier
  note: 線・円由来の四点組と直接整数行列式の照合
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 禁止四点組の有限総数と共線・共円の排他的分解

相異なる四点の零行列式は共線か非退化共円に排他的分解し、F_n=Σ_L C(|L|,4)+Σ_C C(|C|,4)。n=1..11の総数は0,1,14,194,826,2491,6364,14564,29152,54441,95670。

直線は最大直線点集合を一度だけ数え、部分線分の重複を避ける。n≤6の四点共線方向は軸と±1、±2/±1/2はn=7から、±3などはn=10から。
