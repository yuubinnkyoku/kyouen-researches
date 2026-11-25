---
id: K0606
title: グラフ星型共円構成の成分積公式とクリーク直和の鋭い集中閾値
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants]
aliases: []
relations:
- type: depends_on
  target: K0602
  note: 整数平面上のグラフ星型実現、極大配置母関数、最短配置数を使用
- type: generalizes
  target: K0605
  note: 支配集合恒等式を連結成分ごとに積へ分解し、クリーク直和の鋭い境界を決定
artifacts:
- path: research/experiments/graph-star-clique-components-20261101/proof.md
  role: proof
  note: 成分積公式、全終局多項式、必要十分な対数集中境界の全称証明
- path: research/experiments/graph-star-clique-components-20261101/verify.py
  role: verifier
  note: 支配集合直接列挙40条件、禁止超辺全局面列挙6条件、単一成分60条件
scope: K0602の整数平面グラフ星型q点共円・共線禁止構成。Gは孤立点のない任意の非連結グラフ、特にL個のK_hの直和(h>=3)。無限族の閾値は固定q>=5。標準全格子盤は対象外。
evidence: K0602とK0605からの厳密な成分分解と、完全グラフの重み付き支配集合の全称解析。整数完全列挙106条件。
---

# グラフ成分の積公式と最短極大配置の鋭い集中境界

禁止点数 q>=4、r=q-3 とする。K0602 の整数平面グラフ星型構成において、グラフ G が成分 G_1,...,G_L に分かれるなら、極大配置総数は

\[
\boxed{T(G;r)=1+\prod_{i=1}^L W(G_i;r)},\qquad
W(H;r)=\sum_{U\text{ は }H\text{ の支配集合}}r^{e_H(U)}.
\]

中心点 O は全成分で共有されるため、通常の独立なゲームの直和とは異なる。

特に G が L 個の完全グラフ K_h (h>=3) の互いに素な和なら、t=Lh、e=L\binom h2、N=1+t+re として

\[
\boxed{P(u)=u^{N-1}+u^{N-t}
\left(\sum_{j=1}^h\binom hj r^{\binom j2}u^{j-\binom j2}\right)^L}.
\]

ここから

\[
\boxed{T=1+\left(\sum_{j=1}^h\binom hj r^{\binom j2}\right)^L,\quad
M=r^{L\binom h2},\quad s=N-L\binom h2,\quad K=N-1}.
\]

固定 q>=5（r>=2）で h→∞、L=L(h)>=1 とし、\(\alpha_h=Lh\,r^{-(h-1)}=t\,r^{-(h-1)}\) とすると

\[
\boxed{\frac MT\to
\begin{cases}
1 & \alpha_h\to0,\\
e^{-c} & \alpha_h\to c\in(0,\infty),\\
0 & \alpha_h\to\infty.
\end{cases}}
\]

最初と最後の極限については逆も成立する。従って集中の**必要十分条件**は \(h-1-\log_r t\to+\infty\)。K0602の一般十分条件に現れた係数2が、この無限族では鋭く1まで下がる。

q=4（r=1）では \(M/T=1/[1+(2^h-1)^L]\) で、hまたはLが無限大になれば非集中。

具体例 q=5、G=K_3⊔K_3 は N=19、禁止五点集合6本で、\(P(u)=64u^{13}+144u^{14}+81u^{15}+u^{18}\)。最短13石64通り、極大配置総数290通り。16・17石は欠番となる。

全称証明はproof.md、独立有限検証はverify.pyを参照。標準11×11全盤の勝敗やs_11を決定するものではない。
