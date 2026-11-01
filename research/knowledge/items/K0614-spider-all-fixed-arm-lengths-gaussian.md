---
id: K0614
title: 任意固定枝長の星型共円構成の母関数と正規極限の完全分類
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants]
aliases: []
relations:
- type: depends_on
  target: K0602
  note: 任意q点版の整数平面実現と極大配置の削除集合分類
- type: generalizes
  target: K0612
  note: 長さ2の臨界二峰混合とq>=5正規極限を含む
- type: generalizes
  target: K0613
  note: 長さ3の全q正規極限を含む
artifacts:
- path: research/experiments/spider-all-arm-lengths-20261102/proof.md
  role: proof
  note: 任意枝長の母関数と枝長別正規極限の全称証明
- path: research/experiments/spider-all-arm-lengths-20261102/verify.py
  role: verifier
  note: 頂点削除集合92条件と禁止超辺10条件1497344部分集合の独立完全照合
scope: K0602の整数平面実現による中心から等長ℓ>=1の枝d本の蜘蛛木、任意d>=1、q>=4。正規極限は枝長ℓとqを固定しd→∞、極大配置一様分布。標準格子盤は対象外。
evidence: 枝二値語の全称分類、中心残存語への単射と0011...1による厳密優越、指数的全変動距離評価、独立同分布の中心極限定理。有限独立完全照合102条件。
---

# 固定枝長の星型共円構成の正規極限は、長さ2・禁止4点版だけが臨界例

中心から長さℓの枝をd本出す木をK0602で整数平面の禁止q点共円・共線ゲームに実現する。r=q−3>=1、N=2+(r+1)ℓd、最短極大石数s=N−ℓdとする。

枝の許容二値語から計算される非負係数多項式F_{ℓ,r},G_{ℓ,r},J_{ℓ,r}を用いると、**全てのℓ,d>=1、q>=4について**終局石数別母関数は

\[
\boxed{P(u)=u^sF(u)^d+u^{s+d-1}(G(u)^d-J(u)^d)+u^{s+\ell d-1}.}
\]

ℓ>=3では、A=F(1)、B=G(1)に対し**全r>=1でA−B>=r^{ℓ−3}>0**。F(u)/Aが定める非退化な非負整数値変数Yと、独立同分布のY_1,...,Y_dを用いると

\[
\boxed{d_{TV}(\mathcal L(H_d-s),\mathcal L(\sum_iY_i))\le(B/A)^d.}
\]

従って**固定ℓ>=3の全てのq>=4**で終局長は中心化・標準化後に標準正規分布へ収束する。ℓ=2でもq>=5なら同じ結論が成立するが、ℓ=2・q=4だけはK0612の二峰混合。ℓ=1はK0611の二点分布で非退化な正規極限を持たない。これは全ての固定枝長の完全分類である。

新しい明示例としてℓ=4、q=4ではF=2+8u+u²、G=4+5u、J=2+u。よってYの平均10/11、分散32/121、全変動距離の誤差は(9/11)^d以下。

[全称証明](../../experiments/spider-all-arm-lengths-20261102/proof.md)と[独立検証器](../../experiments/spider-all-arm-lengths-20261102/verify.py)を参照。92条件の頂点集合完全列挙と10条件・1,497,344部分集合の禁止超辺直接完全列挙で不一致0。無界命題は数学的証明であり、有限実験の外挿ではない。標準11×11全盤の勝敗や無作為着手順の終局分布を述べない。
