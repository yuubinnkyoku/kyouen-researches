---
id: K0403
title: 異容量上位h列ゲームの極大配置・終局石数と欠番数
kind: proposition
status: proved
topics:
- variants
- maximal-safe
- statistics
- strategy-length
aliases: []
relations:
- type: generalizes
  target: K0352
  note: 等容量上位h列の終局分類を異容量へ拡張
artifacts:
- path: research/experiments/capacity-unequal-top-h-spectrum-20261010/README.md
  role: proof
  note: 任意hの極大配置・終局スペクトル・欠番数
- path: research/experiments/capacity-unequal-top-h-spectrum-20261010/verify.py
  role: verifier
  note: 全局面監査
- path: research/experiments/capacity-unequal-top-h-spectrum-20261010/verify.log
  role: data
  note: 全h有限監査
- path: research/experiments/capacity-unequal-top-h-spectrum-20261010/hole_audit.py
  role: verifier
  note: 欠番数の直接列挙
- path: research/experiments/capacity-unequal-top-h-spectrum-20261010/hole_audit.log
  role: data
  note: 欠番監査
- path: research/experiments/capacity-unequal-h2-spectrum-20261010/README.md
  role: proof
  note: h=2極大配置・経路数
- path: research/experiments/capacity-unequal-h2-spectrum-20261010/verify.py
  role: verifier
  note: h=2直接列挙
- path: research/experiments/capacity-unequal-h2-spectrum-20261010/verify.log
  role: data
  note: h=2有限監査
- path: research/experiments/capacity-unequal-terminal-gap-20261010/README.md
  role: proof
  note: 一高列の終局gap族
- path: research/experiments/capacity-unequal-terminal-gap-20261010/verify_gap_family.py
  role: verifier
  note: 一高列族の直接mex監査
- path: research/experiments/capacity-unequal-terminal-gap-20261010/verify.log
  role: data
  note: 一高列族の監査
scope: 任意w,h,rと非負整数列容量の上位h和制約
evidence: 極大配置分類、終局差分、欠番数の全称閉公式。
---

降順容量 `c_1>=...>=c_w>=0` と上位h列和制約 `<=r` を考える。`Σ_{i<=h}c_i<=r` なら全容量配置だけが極大。そうでなければ `L=max(0,r−Σ_{i<h}c_i)`, `U=min(c_h,floor(r/h))`。極大局面の第h成分bは `[L,U]` を動き、`x_i=min(c_i,b)+d_i`、正のd_iは高々h−1列、`Σd_i=r−hb`。終局石数は `T(b)=r−hb+Σ_i min(c_i,b)`。

終局石数集合は `{T(b):L<=b<=U}`、隣接差は `#{i:c_i>=b+1}−h`。欠番数H、相異なる終局石数Q、最大最小差Rは

`H=Σ_{i=h+2}^w max(0,min(c_i,U)−L)`,
`Q=1+max(0,min(c_{h+1},U)−L)`（h<w、h=wなら1）、
`R=Σ_{i=h+1}^w max(0,min(c_i,U)−L)=H+Q−1`。

上位2列の特例では極大ベクトル・物理的石集合数・経路数も閉形式で決まる。全称性は極大配置分類と差分から証明され、有限列挙は独立監査。標準二次元共円盤への実現は主張しない。
