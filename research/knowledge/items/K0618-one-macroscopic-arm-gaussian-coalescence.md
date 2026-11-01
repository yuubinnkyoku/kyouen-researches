---
id: K0618
title: 禁止4点蜘蛛木の一本の巨大枝による二峰合流と二乗臨界尺度
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants]
aliases: []
relations:
- type: depends_on
  target: K0602
  note: 任意グラフの整数平面禁止4点実現と極大配置分類
- type: depends_on
  target: K0614
  note: 任意枝長の中心状態別母関数
- type: depends_on
  target: K0617
  note: 無界枝長の比の一様評価と条件付き必要十分条件
artifacts:
- path: research/experiments/macroscopic-spider-arm-20261102/proof.md
  role: proof
  note: 重み付き4状態転送行列の最大固有値と二正規混合の全称証明
- path: research/experiments/macroscopic-spider-arm-20261102/verify.py
  role: verifier
  note: 独立二値語・グラフ削除全列挙・漸化式と長枝モーメントの照合
scope: K0602の整数平面実現による禁止4点版q=4。長さ2の枝n本と長さL(n)の枝1本、n→∞、L(n)→∞。極大配置一様分布。標準格子盤・着手順一様分布は対象外。
evidence: 重み付き4状態転送行列の最大固有値と特性関数による全称漸近証明。39語条件・18グラフ条件21168部分集合・長枝モーメントの独立検証。
---

# 一本の巨大枝だけで二峰が正規分布に合流する

禁止4点版の蜘蛛木で、長さ2の枝をn本、長さL=L(n)の枝を1本持たせる。n→∞、L→∞とし、極大配置を一様に選んだ終局石数をH、最短石数をs=2+2n+Lとする。中心残存部門の平均M・分散Vを使って Z=(H−s−M)/√V と標準化する。

λ≈1.839286755214を x³−x²−x−1=0 の正実根、β≈0.063803198448を枝語の漸近分散係数、θ=1−1/λ≈0.456310987308とする。このとき次の**厳密な漸近分類**が成立する。

- **L/n²→∞**：Z⇒N(0,1)。長さ2以外の枝はたった1本（K=1）でも正規極限になる。
- **L/n²→c∈(0,∞)**：Z⇒(1−θ)N(0,1)+θN(2/(3√(βc)),1)。
- **L/n²→0**：Zは緊密でない。正の重みθが標準化後に+∞へ逃げる。

したがってK0617の K→∞ 必要性は、その定理の **L_max=o(√n)** の仮定を外しては成立しない。具体的にはL=n³が反例である。一方、L=cn²では二つの正規峰が有限距離を保ち、正規分布にはならない。

全ての有限n,Lに対して、K0614の枝多項式を用いた終局長母関数は

\[
P_{n,L}(u)=u^s(2+u)^nF_L(u)+u^{s+n}(3^nG_L(u)-J_L(u))+u^{s+2n+L-1}
\]

と厳密に計算できる。無限族の結論は重み付き転送行列の最大固有値に基づく数学的証明であり、有限実験の外挿ではない。

[全称証明](../../experiments/macroscopic-spider-arm-20261102/proof.md)・[独立検証器](../../experiments/macroscopic-spider-arm-20261102/verify.py)。独立照合は39枝語条件、18グラフ条件・21,168部分集合、長さ150までの漸化式、長さ500までのモーメントを含み、不一致0件。標準11×11盤の勝敗は対象外。
