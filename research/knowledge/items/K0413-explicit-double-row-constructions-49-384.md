---
id: K0413
title: 整数円の二重点行49〜384本に対する明示的構成下界
kind: proposition
status: proved
topics:
- geometry
- rectangles
aliases: []
relations: []
artifacts:
- path: research/experiments/fixed-width/reports/large-double-row-witnesses-49-96.md
  role: proof
  note: 48個の明示的な下界と検証・探索の区別
- path: research/experiments/fixed-width/scripts/verify_large_double_row_windows.py
  role: verifier
  note: 独立した整数平方根検証器
- path: research/experiments/fixed-width/output/bounds_49_96.csv
  role: data
  note: 48個のk・w・ノルム・区間端点
- path: research/experiments/fixed-width/reports/double-rows-97-256-construction-20261009.md
  role: proof
  note: 160個の構成下界の式と適用範囲
- path: research/experiments/fixed-width/scripts/construct_double_rows_97_256.py
  role: verifier
  note: Y座標の整数平方根による全列挙
- path: research/experiments/fixed-width/scripts/verify_double_rows_97_256.cpp
  role: verifier
  note: 独立したX座標の整数平方根による全列挙
- path: research/experiments/fixed-width/output/double_rows_97_256.csv
  role: data
  note: k=97〜256の160構成証人
- path: research/experiments/fixed-width/reports/double-rows-257-384-20261009.md
  role: proof
  note: 二つの整数円の構成と128件の量化範囲
- path: research/experiments/fixed-width/scripts/construct_double_rows_257_384.py
  role: solver
  note: Gaussian整数の積による有限構成
- path: research/experiments/fixed-width/scripts/verify_double_rows_257_384.py
  role: verifier
  note: 独立した整数平方根による全二重点行の列挙と128件の直接代入
- path: research/experiments/fixed-width/output/double_rows_257_384.csv
  role: data
  note: 257〜384本の128個の円・幅・包含区間
scope: 標準整数格子の各k=49..384に対する個別の有限幅証人
evidence: 明示円の有限整数点列挙と独立座標走査。厳密最大値ではなく構成下界。
---

各整数k=49,...,384について、有限幅 `w_k` と明示的整数円が少なくともk本の水平行に異なる格子点を2点ずつ持つ。従って `T(w_k)>=k`。これは48件、160件、128件の連続範囲の構成表を統合したもの。T(w_k)=kや最小達成幅は主張しない。

各範囲で円のノルム因数分解から候補を構成し、横座標走査または独立X/Y走査で二重点行を確認する。証人・幅・係数と監査記録をartifactに示す。範囲外のkや最適性は未確定。
