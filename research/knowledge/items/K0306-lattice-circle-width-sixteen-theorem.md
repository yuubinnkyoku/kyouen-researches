---
id: K0306
title: 幅w≥16の連続整数行に任意の円が持つ格子点は高々w
kind: proposition
status: proved
topics: [geometry, rectangles]
aliases: []
relations:
- type: generalizes
  target: K0072
  note: 固定幅で円が消える領域を別方向から拡張する
artifacts:
- path: research/geometry_20261003_extended.md
  role: proof
  note: 幅16定理と最小性
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/verification/geometry_20261003_extended.json
  role: data
  note: 幅1..15の鋭い極値と達成例
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/verification/scripts/check_geometry_20261003.py
  role: verifier
  note: 短時間再現
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
---

# 幅w≥16の連続整数行に任意の円が持つ格子点は高々w

連続するw本の整数水平行に対し、w≥16なら任意の円上の格子点数は高々w。開始幅16は最小で、w≤15には反例がある。

このためw≥16かつq>wの固定幅q点版では、非水平q点直線もq点円も存在できず、禁止集合は同一行q点だけになる。従って全長・全安全局面を行容量の偶奇で強解決できる。
