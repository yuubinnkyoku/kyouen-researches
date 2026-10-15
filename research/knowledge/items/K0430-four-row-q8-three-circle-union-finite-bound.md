---
id: K0430
title: 2000001列まで異なる三つの4行8点円は合併20点以上
kind: proposition
status: computed
topics: [geometry, rectangles, variants]
aliases: []
relations:
- type: depends_on
  target: K0317
  note: 200万までの有限完全弦長型分類を用いる
artifacts:
- path: research/experiments/fixed-width/reports/q48_triple_union_2000000_20261015.md
  role: proof
  note: 有限型分類と相対水平移動の全列挙による境界証明
- path: research/experiments/fixed-width/scripts/q48_triple_union_2000000_20261015.py
  role: verifier
  note: 交差する相対配置から三円の集合和を直接計数
- path: research/experiments/fixed-width/scripts/q48_triple_union_independent_2000000_20261015.cpp
  role: verifier
  note: 二点共有円対を起点とする独立有限検査
- path: research/experiments/fixed-width/output/q48_circle_census_2000000_20261015.csv
  role: data
  note: 合併計算の入力となる11弦長型
scope: 標準4行q=8で、各円が盤内に全て含まれる幅m≤2000001の有限範囲。
evidence: 異なる3円の8点集合の合併は20点以上。したがって異なる4円の合併は22点以上。最小20点は612個の順序付き三円相対配置で達成し、19点以下の例は有限監査で0件。
---

盤内に現れる弦長型を11型へ完全に絞り、全ての順序付き型と共有可能な相対水平移動を列挙する。どの円対も高々2点で交わるため、三円中に非交差の組があれば合併は20点以上。残る三組全てが交差する候補を直接数え、最小値20を得る。4円については最初の3円の下界と、4本目の円が既存各円と高々2点共有することから22点以上となる。

有限完全分類に依存するため、幅2000002以上への外挿や全盤長の下界は主張しない。
