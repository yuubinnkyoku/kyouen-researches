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
- path: research/experiments/n9-k9-upper-sat-20261115/scripts/gen_n9_cnf.mjs
  role: verifier
  note: F_nの2実装センサスとn=7,8,9共線・共円分解の再検証
---

# 禁止四点組の有限総数と共線・共円の排他的分解

相異なる四点の零行列式は共線か非退化共円に排他的分解し、F_n=Σ_L C(|L|,4)+Σ_C C(|C|,4)。n=1..11の総数は0,1,14,194,826,2491,6364,14564,29152,54441,95670。

直線は最大直線点集合を一度だけ数え、部分線分の重複を避ける。n≤6の四点共線方向は軸と±1、±2/±1/2はn=7から、±3などはn=10から。

共線・共円別の内訳 (2026-11-15、差分三角形一次形式と正規化曲線カタログの2実装一致): n=7は共線660・共円5,704、n=8は共線1,524・共円13,040、n=9は共線3,156・共円25,996。n=9の4点以上カタログは直線92本・円6,722個 (12点円4本はK0061の計数と一致)。
