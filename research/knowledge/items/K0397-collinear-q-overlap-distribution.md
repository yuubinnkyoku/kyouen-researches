---
id: K0397
title: 共線q点組の交差分布と局所次数は直線長で決まる
kind: proposition
status: proved
topics:
- geometry
- statistics
aliases: []
relations: []
artifacts:
- path: research/experiments/geometry/reports/collinear-hyperedge-overlap-20261011.md
  role: proof
  note: 任意有限実点集合の2点以上の共線禁則重複と局所次数の全称証明
- path: research/experiments/geometry/scripts/verify_collinear_overlaps_20261011.py
  role: verifier
  note: 22条件の点対完全列挙と5条件の小行列式による独立照合
- path: research/experiments/geometry/output/collinear-overlaps-20261011.txt
  role: data
  note: 全照合結果と11×11の厳密計数
scope: 任意有限実点集合の共線q点組、q>=3、2<=j<q。直方格子の最大s点次数。
evidence: 全称数学的証明。22条件の有限完全照合と5条件の別方式照合。
---

# 共線q点組の2点以上の重複分布と局所次数

任意の有限実点集合で、相異なる共線q点組二つがj>=2点を共有する場合は同一直線上にある。直線上点数kの分布E_kを用いれば、そのような順序なしの組数は

`O_(q,j)=1/2 sum_(k>=2q-j) E_k C(k,q) C(q,j) C(k-q,q-j)`。

また、s>=2点の共線q点組次数は、点を通る直線にk点あれば `C(k-s,q-s)`。直方格子では原始方向の二階差分公式でE_kを厳密に計算できる。11×11の共線四点組の重複は2点共有559440組、3点共有131160組。証明と独立照合の詳細はartifactを参照。
