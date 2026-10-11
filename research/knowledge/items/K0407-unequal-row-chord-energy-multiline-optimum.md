---
id: K0407
title: 異なる高さの行対の2+2共円数に対する鋭い上界と同時達成
kind: proposition
status: proved
topics:
- geometry
- statistics
- rectangles
aliases: []
relations:
- type: generalizes
  target: K0342
  note: 二行鋭い弦エネルギーを多行同時最適へ拡張
artifacts:
- path: research/experiments/unequal-row-sharp-chord-energy-20261010/README.md
  role: proof
  note: 二行の鋭いエネルギー上界と構成
- path: research/experiments/unequal-row-sharp-chord-energy-20261010/verify_cross_energy.py
  role: verifier
  note: 二行全列挙と構成検査
- path: research/experiments/unequal-row-sharp-chord-energy-20261010/verify_short.py
  role: verifier
  note: 短範囲直接照合
- path: research/experiments/unequal-row-sharp-chord-energy-20261010/audit.json
  role: data
  note: 整数行列式・構成監査
- path: research/experiments/geometry/multiline-chord-20261010/README.md
  role: proof
  note: 任意行数の同時達成証明
- path: research/experiments/geometry/multiline-chord-20261010/verify.py
  role: verifier
  note: 複数行構成監査
- path: research/experiments/geometry/multiline-chord-20261010/audit.log
  role: data
  note: 有限検査
scope: 指定幅・行数・各行占有数に対する水平行の2+2型共円数
evidence: 二行鋭い上界と多行同時等号構成の全称証明。
---

異なる高さの二行にr,t個の整数横座標を置くとき、和が一致する二点対（2+2型共円四点組）の最大値は

`U(r,t)=Σ_{a=0}^{floor(r/2)−1}Σ_{b=0}^{floor(t/2)−1} min(2r−4a−3,2t−4b−3)`。

複数行と各占有数でも、一つの整数配置が全ての行対にUを同時達成する。総数の最大は `Σ_{i<j}U(r_i,r_j)` で、非負の行対重みを用いても同じ配置が同時最適。

二点対和の多重集合と外周鎖区間から全称上界・等号構成を示す。有限列挙・行列式は独立監査。3行2+1+1型や標準盤安全局面は対象外。
