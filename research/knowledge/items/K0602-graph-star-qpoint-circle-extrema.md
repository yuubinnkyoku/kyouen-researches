---
id: K0602
title: 任意q点版のグラフ星型共円実現・全母関数・最短極大配置の次数公式
kind: proposition
status: proved
topics: [geometry, maximal-safe, maximum-safe, residual-games, statistics, variants, strategy-length]
aliases: []
relations:
- type: generalizes
  target: K0601
  note: q=4の任意グラフ星型共円実現を全q>=4へ拡張し、最短極大の閉公式と個数も決定
artifacts:
- path: research/experiments/graph-star-qpoint-20261101/proof.md
  role: proof
  note: 無界q・無界グラフの整数幾何構成、全安全・極大母関数、最短極大個数の全称証明とq5十点座標
- path: research/experiments/graph-star-qpoint-20261101/verify.py
  role: verifier
  note: 1181グラフ・4395216部分集合、q5十点の全252五点組・1024局面を独立完全検査
scope: 任意整数q>=4と任意の辺を持つ有限単純グラフから構成する整数平面上のq点共円・共線禁止ゲーム。標準全格子盤は対象外。
evidence: 有理円上の有限除外構成と極小横断集合分類による無界の数学的証明。q4..7の1181ゲーム・4395216部分集合と11×11内q5十点の252五点組・1024局面の完全列挙で不一致0。
---

# 任意q点版のグラフ星型共円ゲームを全称分類

任意q>=4、辺を少なくとも一つ持つ有限単純グラフG=(V,E)を取り、t=|V|、e=|E|、r=q−3、N=1+t+reとする。整数平面上にN点を配置し、禁止q点組を各辺abに対応する {O,V_a,V_b,P_ab,1,...,P_ab,r} のみとすることができる。

X⊆Vの誘導辺数をe(X)、D(G)={X⊆V: 各v∈XがV\Xに隣接点を持つ}とすると、全安全配置母関数と極大安全配置母関数は

\[
\boxed{A(u)=(1+u)^{N-1}+u\sum_{X\subseteq V}u^{|X|}\bigl((1+u)^r-u^r\bigr)^{e(X)}(1+u)^{r(e-e(X))}}
\]

\[
\boxed{P(u)=u^{N-1}+\sum_{X\in D(G)}r^{e(V\setminus X)}u^{N-|X|-e(V\setminus X)}}.
\]

最短極大石数と最大安全石数はグラフの接続形状に依存せず

\[
\boxed{s=N-e=1+t+(q-4)e,\quad K=N-1}.
\]

次数1の頂点のうち非葉に隣接する数をℓ、孤立辺成分の数をhとすれば、最短極大配置の個数は

\[
\boxed{M_{\min}=r^{e-\ell-h}(r+1)^\ell(r+2)^h+\mathbf1_{e=1}}.
\]

q=4ではs=t+1であり、K0601の極値を任意のグラフへ強化する。q>=5の完全グラフ族ではs/N→(q−4)/(q−3)。

11×11格子内の10点でq=5、G=K3を実現し、禁止五点円は正確に3本、極大母関数は **8u^7+9u^8+u^9**。全252五点組と全1024局面を検査した。さらにq=4..7の1181グラフ・4395216部分集合で全公式を独立照合し、不一致0。無界の結論は幾何的構成と横断集合分類の数学的証明によるもので、標準11×11全盤の勝敗を示すものではない。
