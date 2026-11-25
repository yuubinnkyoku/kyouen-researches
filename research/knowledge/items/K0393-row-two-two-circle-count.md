---
id: K0393
title: 標準整数格子の二行二点型共円四点組数の厳密公式
kind: proposition
status: proved
topics:
- geometry
- rectangles
- statistics
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 禁止四点組の円と直線の定義を使用
artifacts:
- path: research/experiments/geometry/reports/row22-exact-count-20261011.md
  role: proof
  note: 任意の行点集合への全称証明と11×11の行型別有限完全列挙
- path: research/experiments/geometry/scripts/verify_row22_20261011.cpp
  role: verifier
  note: 121盤の整数行列式による独立検証
- path: research/experiments/geometry/output/row22-exact-count-20261011.txt
  role: data
  note: 検算実行出力
---

# 二行二点型共円四点組数の全称同和公式と連続区間の三次準多項式

相異なる水平行 y ごとに有限横座標集合 X_y⊂ℝ を与え、p_y(s) を同じ行の異なる二点で横座標和が s になる組の数とする。ちょうど二行に二点ずつある非退化共円四点組数は Σ_{y<z}Σ_s p_y(s)p_z(s) に等しい。証明は各行の弦の中点が円中心の横座標に一致することと、その逆の円中心構成による。

標準 m×h 整数長方形ではこの数は C(h,2)(2m³−3m²+4m−3(m mod 2))/12。全 m,h≥1 について証明済み。11×11の該当成分は10,725組。別の整数行列式完全列挙では2+1+1型39,557組、1+1+1+1型34,960組を得て既知の全円数85,242組と一致する。後二者の数値は11×11の有限完全列挙であり全称公式ではない。
