---
id: K0342
title: r点の同和弦energyには等差数列で達成される鋭い三次上界がある
kind: proposition
status: proved
topics: [geometry, rectangles]
aliases: []
relations:
- type: supports
  target: K0332
  note: 六石の外部行対ごとの同和弦予算29を与える
artifacts:
- path: research/experiments/q57-frontier-followup-20261005/general-energy-proof.md
  role: proof
  note: 任意の異なる実数座標に対する鎖分解・重み付け証明と等差数列の等号
- path: research/experiments/q57-frontier-followup-20261005/scripts/verify_packing.py
  role: verifier
  note: 外周鎖の構成、重み和、有限座標集合の直接energy検査
- path: research/experiments/q57-frontier-followup-20261005/output/packing-audit.json
  role: data
  note: r=1..30等差数列検算と有限座標集合の監査
scope: 任意の有限な異なる実数座標集合。対は異なる二点の非順序対。
evidence: 外周鎖分解の全称証明と等差数列による鋭さ。有限検算は実装監査。
---

# r点の同和弦energyには等差数列で達成される鋭い三次上界がある

異なる実数r点について `c_s=#{i<j:a_i+a_j=s}` と定めると

\[
 \sum_s c_s^2\le
 E_r=\frac{2r^3-3r^2+4r-3\mathbf1_{r\text{ odd}}}{12}.
\]

等差数列で等号になり、r=0はE_0=0とする。
添字対を長さ `2r-4k-3` の外周鎖に分け、鎖kの重みを `2k+1` とすると、
同じ和のc対は異なるc鎖を使うため総重みがc²以上となる。

サイズr,tの二行の同和弦対数は `floor(sqrt(E_r E_t))` 以下。
同サイズの二行で同じ等差数列を使えばE_rが達成される。
六石以下の行対では29以下となり、K0332の円充填上界に使用できる。
自己対や順序付き対の加法energyとは定義が異なる。
