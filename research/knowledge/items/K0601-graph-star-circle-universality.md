---
id: K0601
title: 任意単純グラフの星型禁止四点組を整数共円実現し全安全・極大母関数を決定
kind: proposition
status: proved
topics: [geometry, maximal-safe, maximum-safe, residual-games, statistics, variants, strategy-length]
aliases: []
relations:
- type: generalizes
  target: K0599
  note: 完全二部グラフの円交差構成を任意有限単純グラフへ拡張
- type: depends_on
  target: K0600
  note: 既存の完全二部グラフ族との漸近比較
artifacts:
- path: research/experiments/graph-star-circle-20261101/proof.md
  role: proof
  note: 任意単純グラフの有理円構成・整数化、母関数の全称証明、完全グラフ族の鋭い極値
- path: research/experiments/graph-star-circle-20261101/verify.py
  role: verifier
  note: 1094ラベル付きグラフ・3802800部分集合、11×11内のK3七点の幾何判定と全局面列挙
scope: 辺を少なくとも一つ持つ任意有限単純グラフに対応する整数平面上の有限点配置。共円または共線の4点禁止。標準11×11全盤の勝敗は対象外。
evidence: 無界グラフの有理円による幾何実現と極小横断集合分類の数学的証明。1094グラフ・3802800部分集合の完全照合、K3整数座標の35四点組と128部分集合の独立検算。
---

# 任意単純グラフを整数共円ゲームの禁止四点組として実現

任意の辺を持つ有限単純グラフ G=(V,E) に対し、N=1+|V|+|E| 個の相異なる整数点 O,V_v,P_e を置き、禁止四点組をちょうど {O,V_v,V_w,P_{vw}}（{v,w}∈E）にできる。K0599の完全二部グラフの場合を、非二部グラフを含む全単純グラフに一般化した。

e(X) を G[X] の辺数、D(G)={X⊆V: 各v∈XはV\Xに隣接点を持つ} とすると、全安全集合と極大安全集合の石数別母関数はそれぞれ

\[
\boxed{A_G(u)=(1+u)^{N-1}+u\sum_{X\subseteq V}u^{|X|}(1+u)^{|E|-e(X)}}
\]

\[
\boxed{P_G(u)=u^{N-1}+\sum_{X\in D(G)}u^{N-|X|-e(V\setminus X)}}.
\]

最大安全石数は K=N−1、最小極大石数は s=N−max_{X∈D(G)}(|X|+e(V\X))。無界の全称証明は有理円の有限除外構成と包含極小横断集合の必要十分条件による。

特に完全グラフ K_t（t≥3）では、N=1+t+binom(t,2)、極大配置総数は 2^t、最短・最長極大配置は各一つで

\[
\boxed{s=t+1,\qquad K=N-1,\qquad s/\sqrt N\to\sqrt2.}
\]

これは任意整数点配置におけるK0600の s≈2√N より小さい係数を与える。11×11格子内のK_3七点構成では禁止円が正確に3本、終局長母関数は u^4+6u^5+u^6。

独立検証では1,094個の全ラベル付き非空グラフ（頂点2〜5）・3,802,800部分集合を点別完全列挙し、11×11内の七点の全35四点組と128部分集合も検査した。不一致0。標準11×11の全121点盤の勝敗、標準s_nの漸近は未解決のまま。
