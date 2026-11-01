---
id: K0603
title: グラフ星型共円ゲームの疎グラフ終局分布とサイクルの厳密漸化式
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants]
aliases: []
relations:
- type: depends_on
  target: K0602
  note: グラフ星型の整数幾何実現・極小横断集合の母関数・最短極大個数を利用
artifacts:
- path: research/experiments/graph-star-sparse-cycles-20261101/proof.md
  role: proof
  note: 最大次数による指数的上界とサイクルの転送行列・特性多項式の全称証明
- path: research/experiments/graph-star-sparse-cycles-20261101/verify.py
  role: verifier
  note: サイクル36条件・直接極小横断集合6条件・一般グラフ792条件の独立整数照合
scope: K0602の整数平面グラフ星型q点共円・共線禁止構成。任意q>=4、最小次数2以上の有限単純グラフ、特に任意t>=4のサイクル。標準正方形全盤は対象外。
evidence: 独立集合による極小横断集合の重み付き下界、転送行列の全称恒等式、Perron-Frobenius定理による漸近解析。有限完全列挙は別途実施。
---

# 疎グラフでは最短極大配置への集中が起こらない

K0602のグラフ星型構成で、q>=4、r=q-3、Gの頂点数t、辺数e、最小次数δ>=2、最大次数Δとする。全極大安全配置数をT、最短極大配置数をMとすると、K0602よりM=r^eである。

**全称上界**

\[
\boxed{\frac{M}{T}\le(1+r^{-\Delta})^{-\lceil t/(\Delta+1)\rceil}.}
\]

従ってqとΔを固定し、tを無限に増やすどのグラフ族でも、最短極大配置の割合は指数的に0へ収束する。これはK0602の密なグラフでの割合1への収束と対照的である。Δがtとともに増える場合にも上の不等式自体は成立する。

**サイクルの厳密式**

G=C_t (t>=4) のとき、4状態行列

\[
B_r=\begin{pmatrix}r&1&0&0\\0&0&1&1\\r&1&0&0\\0&0&1&0\end{pmatrix}
\]

により

\[
\boxed{T_t(r)=1+Z_t(r),\quad Z_t(r)=\operatorname{tr}(B_r^t),\quad M_t(r)=r^t.}
\]

初期値はZ_1=r、Z_2=r^2+2、Z_3=r^3+3r+3で、t>=4について

\[
\boxed{Z_t=rZ_{t-1}+Z_{t-2}+Z_{t-3}.}
\]

λ_rをx^3-rx^2-x-1=0の最大実根とすると、λ_r>rかつ

\[
\boxed{\frac{M_t(r)}{T_t(r)}\sim(r/\lambda_r)^t.}
\]

例えばq=5 (r=2) では、C4の最短配置16通り／全43通り、C5は32通り／全108通り。λ_2は約2.546818で、割合は(2/2.546818)^tに漸近する。

証明と独立検証はartifacts参照。全称定理は有限実験からの外挿ではない。標準11×11全盤の最短極大石数や勝敗は導かない。
