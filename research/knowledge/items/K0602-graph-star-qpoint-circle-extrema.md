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


## 系：密なグラフでは最短極大配置が圧倒的多数を占める

上の全母関数を、点数の大きいグラフ族の**極大配置を一様に選ぶ確率**に適用する。グラフの頂点数を t、辺数を e、最小次数を δ≥2、r=q−3≥2 とすると、最短極大配置は正確に r^e 通り、極大配置の総数 T は

\[
\boxed{r^e\le T\le r^e+1+
\sum_{k=1}^{t}\binom tk r^{e-\lceil\delta k/2\rceil}
\le r^e\left(r^{-e}+(1+r^{-\delta/2})^t\right).}
\]

したがって t r^{-δ/2}→0 なら、**極大配置のうち最短石数 s=N−e を持つ割合 r^e/T→1**。例えば固定した q≥5 に対して δ>(2+ε)log_r t なら十分である。最短極大配置の「数」の定理であり、ゲームの最適戦略がその石数に誘導するとは主張しない。

特に完全グラフ K_t (t≥3) は整数共円配置として実現でき、N=1+t+r\binom t2 に対して、終局石数の母関数は

\[
\boxed{P_{K_t,q}(u)=u^{N-1}+
\sum_{j=1}^{t}\binom tj r^{\binom j2}
u^{N-t+j-\binom j2}.}
\]

異なる終局石数は正確に t 種類、最短と最長の間に存在しない石数は \(\binom t2-t+1=\binom{t-1}2\) 種類である。q=4 (r=1) では総数 T=2^t、最短極大配置は一つで割合 2^{-t}→0。一方 **任意の固定 q≥5 では最短割合が1へ収束**する。同じグラフの禁止点数を4から5に増やすだけで、典型的な極大配置の振る舞いが逆転する。なお、終局石数の種類数と欠番数は q に依存しない。

証明・有限独立照合は [proof.md](../../experiments/graph-star-qpoint-20261101/proof.md) と [verify.py](../../experiments/graph-star-qpoint-20261101/verify.py) に追記。これは K0602 の全母関数から導く新しい系であり、標準の全格子盤の極大配置分布ではない。
