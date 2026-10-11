---
id: K0411
title: 三水平行中央弦型の共円完成点が弦内にある場合の鋭い長さ上界
kind: proposition
status: proved
topics:
- geometry
- rectangles
aliases: []
relations: []
artifacts:
- path: research/experiments/geometry/reports/three-line-enclosed-chord-bound-20261011.md
  role: proof
  note: 閉・開区間の鋭い中央弦上界
- path: research/experiments/geometry/scripts/verify_enclosed_chord_bound.py
  role: verifier
  note: 整数行列式と代数条件の独立照合
- path: research/experiments/geometry/output/enclosed_chord_bound_audit_20261011.txt
  role: data
  note: 有限候補監査
scope: 任意p,q>=1の三水平行中央二重点型共円四点組
evidence: 円方程式と端点・内部整数積下界による鋭い全称証明。
---

中央行y=0に `(0,0),(d,0)`、下行y=−pと上行y=qに `(u,−p),(v,q)` を置く。p,q>=1の共円必要十分条件は `q u(d−u)+p v(d−v)=pq(p+q)`。

両完成点が閉区間 `0<=u,v<=d` なら鋭い上界は `d<=1+(p+q)max(p,q)`。両点が厳密内部なら鋭い上界は `d<=1+pq`。双方とも全ての正整数p,qで明示構成により達成される。

円方程式と整数t(d−t)の最小値から全称証明する。整数行列式による有限範囲検査は独立監査。中央弦型の局所結果で、外側二重点Pell族と区別する。
