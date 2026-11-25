---
id: K0610
title: 完全グラフ花束型共円ゲームの極大配置母関数と正規極限
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants]
aliases: []
relations:
- type: depends_on
  target: K0602
  note: グラフ星型の整数共円実現と極大配置の支配集合分類を使用
artifacts:
- path: research/experiments/clique-bouquet-gaussian-20261101/proof.md
  role: proof
  note: 花弁ごとの厳密母関数・全変動誤差・正規極限の全称証明
- path: research/experiments/clique-bouquet-gaussian-20261101/verify.py
  role: verifier
  note: 52条件の支配集合列挙と9条件605312局面の禁止超辺直接完全列挙
scope: 任意k>=2,L>=1,q>=4の完全グラフ花束B_{k,L}をK0602で整数平面に実現した共円・共線禁止ゲーム。正規極限はk,q固定、L→∞、極大配置一様分布。標準全格子盤は対象外。
evidence: 共通頂点の採否で花弁が独立になることから厳密母関数を全称証明し、指数誤差と独立同分布の中心極限定理を適用。61条件の独立整数完全照合で不一致0。
---

# 共通頂点を持つ完全グラフの花束でも終局長は正規分布へ近づく

1つの共通頂点に L 個の完全グラフ K_{k+1}（各花弁は k 頂点）を貼り合わせる。k>=2, L>=1, r=q-3>=1, E=k(k+1)/2, N=2+(k+rE)L, s=N-EL とする。

\[
A(u)=\sum_{j=0}^k\binom kj r^{j(j+1)/2}u^{E-k-j(j-1)/2},\quad
B(u)=\sum_{j=1}^k\binom kj r^{j(j-1)/2}u^{E-k+j-j(j-1)/2}.
\]

**任意の整数パラメータについての厳密公式**は

\[
\boxed{P(u)=u^s A(u)^L+u^{s-1}B(u)^L+u^{N-1}.}
\]

最短極大配置は r^(EL) 通り、全極大配置は A(1)^L+B(1)^L+1 通り。k,r 固定、L→∞ では A(1)>B(1) なので、極大配置の石数 H は s と L 個の独立同分布整数値変数 Y_i の和で全変動距離 ≤(B(1)^L+1)/(A(1)^L+B(1)^L+1) だけ近似できる。Y_i の確率母関数は A(u)/A(1)。

μ=A'(1)/A(1), σ²=A''(1)/A(1)+μ-μ²>0 とすれば、

\[
\boxed{\mathbb EH=s+\mu L+o(1),\quad\operatorname{Var}(H)=\sigma^2L+o(1),\quad
(H-s-\mu L)/(\sigma\sqrt L)\Rightarrow N(0,1).}
\]

特に三角形花束 k=2 では A=r³+(2r+1)u, B=(r+2)u² で、q=4 でも最短割合 1/(4^L+3^L+1)→0、一方で終局石数は二項分布から正規極限を持つ。q=5,L=2 の母関数は 64u^12+80u^13+25u^14+16u^15+u^17。

無界の主張は共通頂点による場合分けと独立同分布の数学的証明による。独立検証器で52条件のグラフ直接列挙と9条件605312局面の禁止超辺直接列挙を照合し、不一致0。これは連結で最大次数が増大するグラフ族の結果であり、標準11×11盤の勝敗や無作為着手列の分布ではない。
