---
id: K0604
title: 完全二部グラフ型共円ゲームの終局多項式と最短極大配置集中の鋭い対数境界
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants]
aliases: []
relations:
- type: depends_on
  target: K0602
  note: 任意q点版の整数幾何実現と極小横断集合分類を利用
- type: generalizes
  target: K0599
  note: q=4の格子状円構成と同じ抽象K_{a,b}型の終局多項式を全q>=4に拡張
artifacts:
- path: research/experiments/graph-star-bipartite-threshold-20261101/proof.md
  role: proof
  note: 完全二部グラフの全母関数、鋭い対数閾値、指数的誤差評価の全称証明
- path: research/experiments/graph-star-bipartite-threshold-20261101/verify.py
  role: verifier
  note: 禁止辺からの全局面直接列挙6条件、頂点集合独立列挙100条件、厳密有理数誤差照合315条件
scope: K0602の整数平面グラフ星型構成にG=K_{a,b}, 2<=a<=bを適用。全q>=4、q>=5の固定qでb無限大の極限。標準全格子盤は対象外。
evidence: 極小横断集合の全称分類、二項恒等式と一様指数誤差上界の数学的証明。6盤373248部分集合、100組合せ条件、315厳密有理数条件の独立検証。
---

# 完全二部グラフでは最短極大配置の集中境界を厳密に決定できる

禁止点数q>=4、r=q−3、G=K_{a,b}（2<=a<=b）、N=1+a+b+rabとする。K0602により、この禁止構造を持つ整数平面の共円・共線ゲームを構成できる。

**極大安全配置の石数別母関数**

\[
\boxed{P(u)=u^{N-1}+u^{N-a}+u^{N-b}
+\sum_{i=1}^{a}\sum_{j=1}^{b}\binom ai\binom bj r^{ij}
u^{N-a-b+i+j-ij}.}
\]

極大配置総数T、最短極大配置数M、最短・最長石数は

\[
\boxed{T=3+\sum_{i=1}^{a}\sum_{j=1}^{b}\binom ai\binom bj r^{ij},\quad
M=r^{ab},\quad s=N-ab,\quad K=N-1.}
\]

**q=4（r=1）では** \(T=2^{a+b}-2^a-2^b+4\)。b→∞で最短極大配置の割合M/T→0。

**任意の固定q>=5（r>=2）では** 全整数2<=a<=bについて

\[
\boxed{\left|\frac{T}{r^{ab}}-(1+r^{-a})^b\right|\le(b+2)(3/4)^b.}
\]

従ってb→∞でz=b/r^aとおくと、z→0ならM/T→1、z→c∈(0,∞)ならM/T→e^(−c)、z→∞ならM/T→0。前後の極限の必要十分条件もそれぞれz→0とz→∞である。

つまり、**最小側の部の大きさaがlog_r(b)をどれだけ超えるか**が最短配置への集中を決める。K0602の一般十分条件（最小次数が約2log_r(t)を超える）を、この完全二部グラフ族では鋭い係数1まで改善し、臨界窓の極限割合も決定した。

例えばK_{7,128}、q=5ではb/r^a=1、最短配置の割合は約0.369312で、臨界極限e^(−1)に近い。K_{2,3}、q=5ではT=179、M=64。

証明はartifactsのproof.md、独立検証はverify.pyを参照。有限計算から無限族へ外挿していない。標準11×11全盤の勝敗や最短極大石数は未解決のままである。
