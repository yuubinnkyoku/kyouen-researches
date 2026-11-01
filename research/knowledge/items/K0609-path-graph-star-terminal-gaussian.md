---
id: K0609
title: 道グラフ型共円ゲームの終局長母関数と正規極限
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants]
aliases: []
relations:
- type: depends_on
  target: K0602
  note: 任意q点の整数幾何実現と極大配置・最短極大個数の分類を使用
- type: depends_on
  target: K0608
  note: 同じ転送行列の固有値と平均・分散係数を利用し、道の境界条件に拡張
artifacts:
- path: research/experiments/path-terminal-gaussian-20261101/proof.md
  role: proof
  note: 道の境界条件つき母関数・3項漸化式・正規極限の全称証明
- path: research/experiments/path-terminal-gaussian-20261101/verify.py
  role: verifier
  note: 88比較の独立方式照合と11条件171632局面の禁止超辺直接完全列挙
scope: 任意t>=2の道P_tと任意q>=4に対するK0602の整数平面グラフ星型q点共円・共線禁止構成。正規極限はq固定・t無限大で極大配置を一様に選ぶ場合。標準正方形全盤は対象外。
evidence: 境界条件つき4状態転送行列・Cayley-Hamilton・Perron-Frobeniusと解析的固有値による数学的証明。44条件88比較および11条件171632局面の独立有限完全列挙で不一致0。
---

# 道グラフでも終局長の正規極限が成立する

K0602の整数点構成でグラフを道 \(P_t\)（\(t\ge2\)）、禁止点数を \(q\ge4\)、\(r=q-3\) とする。全点数 \(N=1+t+r(t-1)\)、最短極大石数 \(s=N-(t-1)\)、最大安全石数 \(K=N-1\)。

\[
S_2=(r+2)u^3,\quad S_3=(r+1)^2u^4+u^5,\quad
S_4=r(r+1)^2u^5+(2r+3)u^6,
\]
\[
\boxed{S_t=ruS_{t-1}+u^3S_{t-2}+u^4S_{t-3}\quad(t\ge5)}
\]

とおけば、全極大安全配置の石数別母関数は

\[
\boxed{P_{t,r}(u)=u^{N-1}+u^{N-2t}S_t(u)}.
\]

最短極大配置数は \(t\ge3\) で \(r^{t-3}(r+1)^2\)、\(t=2\) では \(r+3=q\)。例えば禁止5点版の \(P_5\) では

\[
\boxed{P_{5,2}(u)=36u^{10}+27u^{11}+u^{12}+u^{13}}.
\]

さらに \(r\) 固定、\(t\to\infty\) で全極大配置から一様に選んだ終局石数 \(H_t\) について、\(\lambda\) を \(\lambda^3-r\lambda^2-\lambda-1=0\) の最大実根とし

\[
\alpha_r=r+\frac1{\lambda^2-\lambda+2},\quad
\beta_r=\frac{\lambda(\lambda-1)^2(\lambda^2+\lambda+1)}{(\lambda+1)(\lambda^2-\lambda+2)^3}>0
\]

とすると、

\[
\boxed{\mathbb EH_t=\alpha_rt+O(1),\quad
\operatorname{Var}(H_t)=\beta_rt+O(1),\quad
\frac{H_t-\alpha_rt}{\sqrt{\beta_rt}}\Rightarrow N(0,1).}
\]

**サイクル型K0608と同じ線形係数を持つが、端点の影響で定数項は異なる。** 境界条件つき転送行列とその正の最大固有値を用いた無界の数学的証明であり、有限実験からの外挿ではない。独立検証では44条件88比較、11条件171632局面の禁止超辺直接完全列挙で不一致0。詳細はartifacts参照。

これは自由な整数点配置の一様な極大配置分布についての結果であり、無作為な着手順や最適戦略、標準11×11全盤の勝敗を述べるものではない。
