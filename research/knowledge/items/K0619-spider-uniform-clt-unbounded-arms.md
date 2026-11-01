---
id: K0619
title: 禁止4点蜘蛛木の無界混合枝長に対する一様中心極限定理と正規極限の十分条件
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants]
aliases: []
relations:
- type: depends_on
  target: K0602
  note: 任意グラフの自由な整数平面点集合への禁止4点実現
- type: depends_on
  target: K0614
  note: 任意枝長の中心状態別の厳密母関数
- type: depends_on
  target: K0617
  note: 全枝長に一様な中心削除部門の比17/20
- type: depends_on
  target: K0618
  note: 枝語の転送行列と正の漸近分散係数
artifacts:
- path: research/experiments/spider-uniform-clt-20261102/proof.md
  role: proof
  note: 解析的転送行列の一様累積量評価と全変動距離による全称証明
- path: research/experiments/spider-uniform-clt-20261102/verify.py
  role: verifier
  note: 二値語・頂点削除直接全列挙・300枝長の分散と比の独立有限検査
scope: K0602の整数平面実現によるq=4の蜘蛛木。枝数と最大枝長に制限を置かない三角配列。極大配置の一様分布であり、着手順一様・標準11×11盤は対象外。
evidence: K0618の解析的最大固有値を用いた全枝長一様の三次累積量評価と正の分散下界、K0617の全変動距離評価。有限独立照合は補助証拠。
---

# 枝長の上限なしでも中心残存部門は正規極限になる

禁止4点版の蜘蛛木で、長さ \(\ell\) の枝を \(n_\ell\) 本置く。枝数・枝長・その比率はすべて変動してよい。\(E=\sum_{\ell\ge1}\ell n_\ell\)、\(s=2+E\) とする。中心残存枝母関数 \(F_\ell(u)\)（K0614）から独立変数 \(Y_{\ell,i}\) を定め、\(S=\sum Y_{\ell,i}\)、\(M=\mathbb ES\)、\(V=\operatorname{Var}S\)、\(D=\sum_{\ell\ge2}\ell n_\ell\)、\(K=\sum_{\ell\ne2}n_\ell\) とする。

**一様中心極限定理。** ある絶対定数 \(0<c<C<\infty\) が存在して、全ての有限枝長の組について \(cD\le V\le CD\) が成立する。したがって \(D\to\infty\) なら

\[
\boxed{\frac{S-M}{\sqrt V}\Rightarrow N(0,1)}
\]

であり、枝長の最大値に制限はない。

**共円ゲームの終局長への移行。** 極大安全配置を一様に選んだ終局石数を \(H\) とすると、K0617の全変動距離評価は枝長に依存せず

\[
d_{\mathrm{TV}}(\mathcal L(H-s),\mathcal L(S))
\le\min\{1,2(17/20)^K\}.
\]

よって

\[
\boxed{D\to\infty\ \text{かつ}\ K\to\infty
\quad\Longrightarrow\quad
\frac{H-s-M}{\sqrt V}\Rightarrow N(0,1).}
\]

特に \(n_2\to\infty\) の場合、K0617の正規極限の**十分条件** \(K\to\infty\) は \(L_{\max}=o(\sqrt{n_2})\) という制限を一切必要としない。ただし必要条件への拡張は**誤り**であり、K0618の巨大枝1本の反例がある。

証明は[全称証明](../../experiments/spider-uniform-clt-20261102/proof.md)、有限独立照合は[検証器](../../experiments/spider-uniform-clt-20261102/verify.py)を参照。有限計算から正規極限を推測したのではなく、転送行列の解析的な固有値から一様な三次誤差を導いた。標準11×11全盤の勝敗は対象外。
