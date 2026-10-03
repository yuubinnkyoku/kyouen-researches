---
id: K0106
title: 固定qの最小極大サイズには漸近指数下界2/3がある
kind: proposition
status: proved
topics:
- maximal-safe
- geometry
- variants
aliases: []
relations:
- type: depends_on
  target: K0026
  note: ''
- type: supports
  target: K0147
  note: 下界側の制約
- type: supports
  target: K0148
  note: 指数2/3未満を排除
artifacts:
- path: research/verification/round52-general-saturation-exponent-lower-bound.md
  role: proof
  note: q=4標準版の元の指数下界
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/saturation-20261003.md
  role: proof
  note: 全固定q≥4への拡張と直線被覆係数の改善
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/geometry-20261003.md
  role: proof
  note: §10で平方完成ノルム上界を2(n-1)^6へ改善
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
---

# 固定qの最小極大サイズには漸近指数下界2/3がある

標準q=4だけでなく、全ての固定q≥4について、最小極大サイズs_{n,q}は任意のε>0に対し十分大きいnでs_{n,q}>n^(2/3-ε)。従ってliminf log(s_{n,q})/log n≥2/3。

直線被覆は原始方向殻ごとの容量を使ってO_q(n k^(3/2))に抑え、真円被覆は三格子点円の点数上界R(n)=n^o(1)を使う。平方完成ノルムの有限盤上界は旧224(n-1)^6から2(n-1)^6へ改善された。

円を禁止しないline-only版ではさらに主定数まで評価できるが、その定数を円も禁止する標準版へ移してはいけない。
