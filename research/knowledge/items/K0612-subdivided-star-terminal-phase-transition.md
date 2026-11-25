---
id: K0612
title: 細分星型共円ゲームの終局母関数と禁止4点・5点間の確率相転移
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants]
aliases: []
relations:
- type: depends_on
  target: K0602
  note: 任意q点版の整数共円実現と削除集合による極大配置分類を使用
artifacts:
- path: research/experiments/spider-graph-star-20261101/proof.md
  role: proof
  note: 全d・全qの母関数の組合せ論的全称証明とq4二峰混合・q5以上の正規極限
- path: research/experiments/spider-graph-star-20261101/verify.py
  role: verifier
  note: 28条件の頂点集合直接照合、9条件・1608000局面の禁止超辺直接完全列挙
scope: 任意d>=1・q>=4、d本の長さ2の枝を持つ細分星S_dのK0602整数平面実現。極大配置一様分布。全格子盤・ランダム着手順は対象外。
evidence: 中心残存・削除による削除集合の全称分類と二項分布の極限定理。独立全列挙28+9条件、不一致0。
---

# 細分星ではq=4だけ二峰混合、q>=5では正規極限

中心から長さ2の枝がd本出る木S_dを取り、K0602の整数共円実現を行う。r=q-3>=1、全点数N=2+2(r+1)d、最短極大石数s=N-2dとする。**全てのd>=1,q>=4に対して**極大配置の石数別母関数は

\[
\boxed{P_{d,r}(u)=u^s(r(r+1)+u)^d+((r+2)^d-1)u^{s+d-1}+u^{s+2d-1}.}
\]

したがって極大配置総数は (r²+r+1)^d+(r+2)^d。d>=3 なら終局石数は s,...,s+d および s+2d-1 の d+2 種類で、間に d-2 個の欠番がある。

全極大配置から一様に選んだ石数をHとし、A=r²+r+1、p=1/Aとすると、**有限dでも**

\[
d_{TV}(\mathcal L(H-s),\mathrm{Bin}(d,p))\le\frac{(r+2)^d}{A^d+(r+2)^d}.
\]

q>=5 なら A>r+2 なので右辺は指数的に0となり、(H-s-dp)/sqrt(dp(1-p)) は標準正規分布に収束する。一方**q=4では正規極限ではなく**

\[
\boxed{(H-s)/d\Longrightarrow\tfrac12\delta_{1/3}+\tfrac12\delta_1.}
\]

これは連結な木の終局長分布に関する、禁止点数を4から5へ変えるだけで起きる鋭い相転移である。K0611の星の二点終局分布とも異なる。中心を残す枝族と削除する枝族の重みを独立に数えた全称証明は proof.md、28条件の頂点全列挙と9条件・計1,608,000局面の禁止超辺直接列挙による独立照合は verify.py にある。全格子盤の勝敗や標準11×11の解決は主張しない。
