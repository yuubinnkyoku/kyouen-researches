---
id: K0608
title: サイクル型グラフ星共円ゲームの終局長母関数と正規極限
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants]
aliases: []
relations:
- type: depends_on
  target: K0602
  note: 任意q点の整数幾何実現と極大配置分類を使用
- type: generalizes
  target: K0603
  note: サイクルの極大配置総数の漸化式を石数別母関数に強化
artifacts:
- path: research/experiments/cycle-terminal-gaussian-20261101/proof.md
  role: proof
  note: 石数別転送行列、漸化式、平均分散の明示定数と正規極限の全称証明
- path: research/experiments/cycle-terminal-gaussian-20261101/verify.py
  role: verifier
  note: 36条件の円環・行列・漸化式照合と6条件608768局面の超辺直接完全列挙
scope: 任意固定q>=4、任意t>=4のサイクルC_tからK0602で整数平面上に構成したq点共円・共線禁止ゲーム。極大安全配置の一様分布。標準全格子盤は対象外。
evidence: 4状態行列の特性多項式とCayley-Hamiltonによる全称母関数、Perron-Frobeniusと解析的固有値による正規極限の数学的証明。有限独立検査は別途実施。
---

# サイクル型構成の終局長は、平均・分散が線形で正規分布へ近づく

K0602の整数点実現で、グラフをC_t（t>=4）、禁止点数をq>=4、r=q-3とする。全点数N=1+(r+1)t、最短極大石数s=1+rt、最大安全石数K=(r+1)t。

極大安全配置を石数ごとに数えた多項式は、Q_1=ru、Q_2=r²u²+2u³、Q_3=r³u³+3(r+1)u⁴、および

\[
Q_t=ruQ_{t-1}+u^3Q_{t-2}+u^4Q_{t-3}\quad(t\ge4)
\]

から、任意のt>=4,r>=1で

\[
\boxed{P_{t,r}(u)=u^{(r+1)t}+u^{1+(r-1)t}Q_t(u)}
\]

と厳密に求まる。これはK0603の極大配置**総数**の式を、終局石数別の分布へ強化する。

さらにλをλ³−rλ²−λ−1=0の最大実根として

\[
\alpha_r=r+\frac1{\lambda^2-\lambda+2},\qquad
\beta_r=\frac{\lambda(\lambda-1)^2(\lambda^2+\lambda+1)}{(\lambda+1)(\lambda^2-\lambda+2)^3}>0
\]

と置く。全極大配置から一様に選んだ終局石数H_tは、rを固定しt→∞で

\[
\boxed{\mathbb EH_t=1+\alpha_rt+o(1),\quad
\operatorname{Var}(H_t)=\beta_rt+o(1),\quad
\frac{H_t-1-\alpha_rt}{\sqrt{\beta_rt}}\Rightarrow N(0,1).}
\]

実際、q=5ではα≈2.168365330907、β≈0.082267978419であり、C_6の極大配置母関数は

\[
64u^{13}+144u^{14}+63u^{15}+2u^{16}+u^{18}.
\]

無界の結論は転送行列の数学的証明による。36条件の円環二値列・転送行列・漸化式の照合と、6条件・608768局面の禁止超辺直接完全列挙、12条件の有限モーメント照合は不一致0。詳細はartifacts参照。

これは**一様に選んだ極大配置**の分布であって、無作為な合法着手列の分布や最適戦略の結果ではない。また自由な整数点配置の定理であり、標準11×11全盤の勝敗には直接適用しない。
