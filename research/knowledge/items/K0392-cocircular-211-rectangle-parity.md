---
id: K0392
title: 長方形盤の2+1+1型共円四点組数の法4公式
kind: proposition
status: proved
topics:
- geometry
- rectangles
- statistics
aliases: []
relations: []
artifacts:
- path: research/experiments/geometry/reports/rectangle-cocircular-211-parity-20261011.md
  role: proof
  note: 二つの鏡映による全称証明と検証範囲
- path: research/experiments/geometry/scripts/verify_211_formula_20261011.py
  role: verifier
  note: 二次方程式の整数根による全数計数
- path: research/experiments/geometry/scripts/verify_211_determinant_20261011.cpp
  role: verifier
  note: 独立した整数行列式による全数計数
- path: research/experiments/geometry/output/cocircular_211_counts_20261011.csv
  role: data
  note: 1..11×1..11の全計数と偶奇
scope: 任意の正整数w,h、w×h整数格子盤の共円四点組のうち水平行分布が2+1+1型
evidence: 横縦鏡映の二重固定点計数による全称証明、121盤の二実装独立完全列挙
---

# 長方形盤の2+1+1型共円四点組数の偶奇

C211(w,h) は、ある水平行に2点、別の二行に1点ずつある共円四点集合の数。

- w または h が偶数なら C211(w,h) は偶数。
- w,h がともに奇数なら C211(w,h) ≡ (min(w,h)-1)/2 (mod 2)。

証明：横反転Xと縦反転Yは可換な対合である。二重の固定点計数により全数の偶奇は両反転で不変な四点組の個数の偶奇に等しい。そのような四点組は盤中心から水平±t、垂直±s の十字型だけであり、共円の必要十分条件はt=s。整数tの個数は(min(w,h)-1)/2。詳細と独立検算はartifactsの証明・検証器を参照。

11×11では C211=39557、3×6では80、3×7では109（いずれも有限完全列挙）。本項目は勝敗・Grundyの解決を主張しない。
