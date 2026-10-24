---
id: K0544
title: 共超平面禁止の最小極大判定と全三次元直方体のs・三石極大数
kind: proposition
status: proved
topics: [variants, geometry, maximal-safe, statistics]
aliases: []
relations:
- type: depends_on
  target: K0526
  note: 2×2×2の既存全局面列挙と例外の整合性
- type: depends_on
  target: K0530
  note: 2×k×mの三石極大数の既存特殊公式との照合
artifacts:
- path: research/experiments/coplanar-hyperplane-minmax-20261024/proof.md
  role: proof
  note: 一般有限点集合のアフィン階数判定・全直方体のs・三石極大数の全称証明
- path: research/experiments/coplanar-hyperplane-minmax-20261024/verify.py
  role: verifier
  note: 外積直接計数・原始方向公式・全安全局面列挙・有理数階数の照合
- path: research/experiments/coplanar-hyperplane-minmax-20261024/results.md
  role: data
  note: 四盤の全安全局面と七盤の共線三点数の独立一致表
scope: d次元でd+1点共超平面禁止・全空間を張る有限点集合、三次元の全整数直方体、d次元二値立方体
evidence: アフィン階数による全称証明、原始方向両端点の全称計数式、有限独立検算
---

# 最小極大配置のアフィン階数判定

R^dをアフィンに張る有限点集合でd+1点共超平面を禁止するとき、**d石配置が極大である必要十分条件はそのアフィン次元がd−2以下**。従ってs=dとなる条件もこれで完全に決まる。

特に3次元整数直方体a×b×c（a,b,c≥1）の最小極大石数は、abc≤2ならabc、2×2×2だけ4、**それ以外はすべて3**。三次元を張る直方体では三石極大配置は共線三石に限り、原始整数方向vと両端差kvを使う次の全称公式で個数が決まる：

`T(a,b,c)=Σ_(v primitive/±) Σ_(k≥2) (k−1) ∏_(i=1)^3 (n_i−k|v_i|)_+`、`(n_1,n_2,n_3)=(a,b,c)`。

さらにd≥4の二値立方体ではs=d。一方3次元二値立方体はs=4であり、**次元3から4への例外的な変化**がある。

[全称証明](../../experiments/coplanar-hyperplane-minmax-20261024/proof.md)・[再現コード](../../experiments/coplanar-hyperplane-minmax-20261024/verify.py)・[有限検算](../../experiments/coplanar-hyperplane-minmax-20261024/results.md)。最大容量・空盤勝敗・Grundy値は対象外。
