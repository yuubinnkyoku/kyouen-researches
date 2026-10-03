---
id: K0307
title: n≤112の正方形盤に載る円上格子点数の最大値を全中心・全半径で完全分類
kind: computation
status: computed
topics: [geometry]
aliases: []
relations: []
artifacts:
- path: research/geometry-20261003.md
  role: source
  note: 全中心有限盤極値の結果
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/verification/geometry_20261003_scale.json
  role: data
  note: 全盤走査の集計
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/verification/scripts/geometry_20261003_scale.py
  role: verifier
  note: 全中心・全半径の列挙
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
---

# n≤112の正方形盤に載る円上格子点数の最大値を全中心・全半径で完全分類

n≤112について、n×n盤内で一つの円に載る格子点数の最大値を中心や半径を半整数に限定せず完全分類した。代表的にはn=101で40点、n=105で44点、n=106で48点。

旧F-Kの半整数中心走査とは対象範囲が異なり、本項目は有限範囲で全有理中心を含む完全分類である。
