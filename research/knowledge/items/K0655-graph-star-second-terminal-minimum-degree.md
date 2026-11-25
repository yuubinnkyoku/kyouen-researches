---
id: K0655
title: グラフ星型共円ゲームの二番目に短い終局長は最小非葉次数で決まる
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants]
aliases: []
relations:
- type: depends_on
  target: K0602
  note: グラフ星型の整数共円構成と極大配置分類
- type: depends_on
  target: K0648
  note: 許容核の欠損公式と次数下界
artifacts:
- path: research/experiments/graph-star-second-terminal-degree-20261103/proof.md
  role: proof
  note: 二番目の終局長・欠番数・初出係数の全称証明
- path: research/experiments/graph-star-second-terminal-degree-20261103/verify.py
  role: verifier
  note: 支配集合の独立直接列挙8776条件と初出係数940条件の照合
scope: K0602の有限単純グラフG（孤立頂点可）、辺数e>=1、任意の整数q>=4。標準全格子盤は対象外。
evidence: K0648の許容核公式からの全称証明。8776条件の独立有限列挙は補助監査。
---

# 二番目に短い極大配置の石数は最小非葉次数だけで決まる

G の辺数を e>=1、q>=4、r=q-3、全点数を N=1+|V|+re、最短極大石数を s=N-e とする。H={v:deg(v)>=2} とおく。

**全称定理。** e>=2 のとき、二番目に短い（最短とは異なる）極大安全配置の石数は

\[
\boxed{s+\gamma(G)},\qquad
\gamma(G)=\begin{cases}
\min_{v\in H}(\deg(v)-1),&H\ne\varnothing,\\
e-1,&H=\varnothing.
\end{cases}
\]

したがって最短終局の直後には **ちょうど \(\gamma(G)-1\) 個の欠番** がある。この値は q に依存しない。e=1 では終局長は s の一種類だけである。

H が空なら G は孤立点と e 本の独立辺からなり、全母関数は
\[
\boxed{P_{G,q}(u)=(r+2)^e u^s+u^{s+e-1}.}
\]
e=1 では両項が同じ次数になる。

さらに \(H\ne\varnothing\) で \(\delta=\min_{v\in H}\deg(v)\ge3\) のとき、初めて現れる上側係数は **最小次数の頂点一個からの寄与だけ** で計算できる。L は高次数頂点に隣接する葉の数、h は孤立辺成分数、C=e-L-h、a_v は v に隣接する葉の数として、
\[
\boxed{
[u^{s+\delta-1}]P_{G,q}(u)
=\mathbf1_{e=\delta}
+(r+2)^h\sum_{\deg(v)=\delta}
r^{C+a_v-\delta}(r+1)^{L-a_v}.}
\]
各指数は非負。\(\delta=2\) の場合は、K0648の次数2頂点および次数2同士の辺の閉公式を使う。

例：星 K_{1,5} の終局長差は 0,4 だけで、差4の係数は q によらず2。K4 では最初の正の差が2で、その係数は \(4(q-3)^3\)。独立辺3本では差0と差2だけになる。

[全称証明](../../experiments/graph-star-second-terminal-degree-20261103/proof.md)と[独立検証器](../../experiments/graph-star-second-terminal-degree-20261103/verify.py)を保存。8776条件で次の終局長、940条件で初出係数を直接支配集合列挙と照合し不一致0。有限列挙は全称証明の代わりではない。

**適用範囲：** 任意の整数点集合や標準 n×n 全格子盤の最短終局 s_n、11×11空盤勝敗への主張ではない。
