---
id: K0643
title: グラフ星型q点共円ゲームの終局長欠番のq不変性・係数多項式・偶奇法則
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants]
aliases: []
relations:
- type: depends_on
  target: K0602
  note: 任意qのグラフ星型構成・全極大母関数と最短石数公式
artifacts:
- path: research/experiments/graph-star-q-spectrum-20261102/proof.md
  role: proof
  note: 最短石数で平行移動した終局母関数の全称恒等式と支配集合数の奇数性の対合証明
- path: research/experiments/graph-star-q-spectrum-20261102/verify.py
  role: verifier
  note: 全1094グラフ・1855禁止超辺直接列挙条件と有限差分・偶奇の独立監査
scope: 少なくとも1辺のある任意有限単純グラフG、任意整数q>=4のK0602星型整数共円・共線禁止構成。標準全格子盤は対象外。
evidence: K0602母関数の指数差の全称恒等式、非負係数性、支配集合数の奇数性の対合証明。1855条件の禁止超辺直接完全列挙は独立の有限監査。
---

# 禁止点数qを変えても終局長の欠番は移動するだけ

Gの頂点数n、辺数e>=1、q>=4、r=q-3、全点数N_q=1+n+re、最短極大石数s_q=N_q-eとする。極大配置の石数母関数P_{G,q}(u)を最短石数で平行移動すると

\[
\boxed{u^{-s_q}P_{G,q}(u)=u^{e-1}+\sum_{j=0}^e (q-3)^j C_{G,j}(u)}
\]

となる。ここで C_{G,j}(u) は、誘導辺数jの支配集合Rを走る \(u^{e-j-|V\setminus R|}\) の和で、**非負整数係数多項式**である。

従って、最短からの終局長の差と欠番の集合は**全q>=4で完全に一致**する。実現可能な差は0からe-1までに含まれ、両端は常に実現する。各差の配置数はq-3の次数高々eの非負整数係数多項式であり、e+1個のq値から厳密補間できる。qを増やせば各差の配置数は非減少で、総数は厳密増加する。

**偶奇法則：** qが偶数なら全極大配置総数は常に偶数。qが奇数なら、その偶奇は \(1+\#\{G\text{の極大独立集合}\}\) の偶奇である。q=5でK2の総数は5（奇数）、K3は18（偶数）。証明には、任意の有限グラフの支配集合の個数が奇数という対合恒等式を用いる。係数ごとのmod2合同式も成立する。

[全称証明](../../experiments/graph-star-q-spectrum-20261102/proof.md)と[独立検証器](../../experiments/graph-star-q-spectrum-20261102/verify.py)を保存。n<=5の全1,094グラフを調べ、うち1,855条件で禁止超辺から極大安全集合を直接完全列挙して不一致0。有限列挙と全称証明は区別する。**標準のn×n全格子盤や任意の幾何点集合のq不変性は主張しない。**
