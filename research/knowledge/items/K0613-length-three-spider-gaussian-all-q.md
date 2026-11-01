---
id: K0613
title: 長さ3の枝を持つ星型共円構成の厳密母関数と全q正規極限
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants]
aliases: []
relations:
- type: depends_on
  target: K0602
  note: 任意グラフの整数平面実現と極大配置の削除集合分類
artifacts:
- path: research/experiments/spider-length-three-20261102/proof.md
  role: proof
  note: 任意dとqの閉形式の全称証明と全変動距離評価・正規極限
- path: research/experiments/spider-length-three-20261102/verify.py
  role: verifier
  note: 20条件の頂点削除集合直接列挙、7条件2263296部分集合の禁止超辺直接列挙
scope: 任意d>=1、q>=4の長さ3の枝d本を持つ木のK0602整数平面実現。正規極限はq固定、d→∞、極大配置一様分布。標準格子盤・無作為着手順は対象外。
evidence: 中心頂点の採否と枝の状態の全称分類による数学的証明、二項分布への指数的全変動距離評価。27条件の独立完全列挙と99整数検査。
---

# 長さ3の枝なら禁止4点版でも単一の正規極限になる

中心から長さ3の枝がd本伸びる木をK0602により整数平面の禁止q点共円・共線ゲームに実現する。r=q−3>=1、点数N=2+3(r+1)d、最短極大石数s=N−3dとすると、**全d>=1、q>=4について**石数別極大配置母関数は

\[
\boxed{P_{d,r}(u)=u^s(r+1)^d(r^2+2u)^d+u^{s+d-1}\bigl((u+(r+1)^2)^d-(r+1)^d\bigr)+u^{s+3d-1}.}
\]

A=(r+1)(r²+2)、B=(r+1)²+1、p=2/(r²+2) とする。一様な極大配置の石数Hについて

\[
\boxed{d_{TV}(\mathcal L(H-s),\operatorname{Bin}(d,p))\le (B/A)^d,\quad A-B=r^3>0.}
\]

したがって**任意の固定q>=4**で

\[
\boxed{(H-s-dp)/\sqrt{dp(1-p)}\Longrightarrow N(0,1).}
\]

特にq=4ならp=2/3、誤差は(5/6)^d以下。K0612の長さ2の枝ではq=4で二峰混合極限だったが、長さ3の枝ではq=4でも正規極限が成立する。中心頂点を残す場合の枝ごとの独立性と、削除する場合の総重みが指数的に小さいことが理由である。

全称証明は[proof.md](../../experiments/spider-length-three-20261102/proof.md)、閉形式から独立した頂点削除集合20条件・禁止超辺の全局面7条件（計2,263,296部分集合）の直接照合は[verify.py](../../experiments/spider-length-three-20261102/verify.py)にある。これは自由な整数点配置で極大配置を一様に選んだときの結果であり、標準11×11盤の勝敗や無作為着手順の終局長を述べない。
