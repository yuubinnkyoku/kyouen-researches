---
id: K0607
title: グラフ星型共円ゲームの臨界窓における終局長のポアソン極限
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants]
aliases: []
relations:
- type: depends_on
  target: K0604
  note: 完全二部グラフの終局多項式と一様誤差評価
- type: depends_on
  target: K0606
  note: 完全グラフ直和の成分積公式と欠損項の漸近評価
artifacts:
- path: research/experiments/graph-star-poisson-20261101/proof.md
  role: proof
  note: 二つの臨界窓で主要族を分類し全変動収束を証明
- path: research/experiments/graph-star-poisson-20261101/verify.py
  role: verifier
  note: 禁止超辺直接完全列挙9条件と整数式照合483条件
scope: K0602の整数平面グラフ星型q点共円・共線禁止構成。固定q>=5、完全二部グラフまたは完全グラフ直和の臨界窓。極大配置の一様分布。標準全格子盤は対象外。
evidence: K0604・K0606の全称公式と誤差評価から主要族を抽出し、二項分布のポアソン極限を証明。禁止超辺直接列挙と整数照合で独立検査。
---

# 最短極大配置の割合から終局長の分布へ

q>=5、r=q-3 を固定し、K0602 の整数平面グラフ星型共円構成の極大安全配置を**一様に選ぶ**。最短終局石数を s、選んだ配置の石数を H とする。

**完全二部グラフ** G=K_{a,b}、2<=a<=b、b→∞、b/r^a→c∈(0,∞) なら、任意の固定 k>=0 に対して

\[
\boxed{\Pr\{H=s+(a-1)k\}\to e^{-c}c^k/k!.}
\]

中心点と a 側全頂点を含み、b 側から k 頂点を省いた主要族は正確に \(\binom bk r^{a(b-k)}\) 通りで、その主要族全体の割合が1に収束する。

**完全グラフ直和** G=K_h の L 個の直和、h→∞、Lh/r^{h-1}→c∈(0,∞) なら

\[
\boxed{\Pr\{H=s+(h-2)k\}\to e^{-c}c^k/k!.}
\]

中心点を含み、k 個の成分だけで1頂点を省き、他の成分では全頂点を残す主要族は \(\binom Lk h^k r^{L\binom h2-k(h-1)}\) 通り。その主要族全体の割合が1に収束する。

両族で欠損個数の分布は**全変動距離**で Poisson(c) に収束する。K0604・K0606 の最短割合 e^{-c} を、各固定 k の終局長へ強化した。証明と独立検査は artifacts 参照。

石数の刻み自体が増大するので、H-s 自体の固定尺度でのポアソン極限ではない。標準11×11全盤の結果でも、ランダムな着手過程の結果でもない。


## 有限誤差評価と正規極限（2026-11-01追補）

臨界窓の極限だけでなく、任意の有限パラメータに対する**二項分布への全変動距離上界**も証明した。厳密な証明と独立の有理数照合は既存 artifacts の proof.md・verify.py に追記している。

完全二部グラフ K_{a,b}（2<=a<=b、r>=2）では、x=r^{-a}、p=x/(1+x)、\(X=(H-s)/(a-1)\) とおくと、

\[
\boxed{d_{TV}(\mathcal L(X),\mathrm{Bin}(b,p))
\le \frac{(b+2)(3/4)^b+x^b}{(1+x)^b-x^b}+p^b.}
\]

さらに右辺に \(3bx^2\) を足せば Poisson(bx) への全変動距離上界になる。b→∞ で \(bp\to\infty\) なら、主要族外の確率が0に収束するため

\[
\boxed{(X-bp)/\sqrt{bp(1-p)}\Rightarrow N(0,1).}
\]

これは固定aでbを増やす場合も含む。

L 個の完全グラフ K_h（h>=3、r>=2）では、E=binom(h,2)、a=h r^{-(h-1)}、p=a/(1+a)、\(\eta_*=2^h r^{-(2h-3)}\)、\(Y=(H-s)/(h-2)\) とすると、

\[
\boxed{d_{TV}(\mathcal L(Y),\mathrm{Bin}(L,p))
\le r^{-LE}+\left(1+\frac{\eta_*}{1+a}\right)^L-1.}
\]

右辺に \(3La^2\) を足せば Poisson(La) への全変動距離上界となる。h→∞、Lp→∞、\(L\eta_*\to0\) の下では、\((Y-Lp)/\sqrt{Lp(1-p)}\Rightarrow N(0,1)\) も成立する。

有限検証は二部グラフ387条件、完全グラフ直和264条件の厳密有理数不等式、および両族の終局多項式から独立に求めた全分布の照合で行った。これらの有限検証は全称証明の代用ではない。標準格子全盤・ランダム着手列には適用しない。
