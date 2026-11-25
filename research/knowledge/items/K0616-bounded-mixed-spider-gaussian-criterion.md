---
id: K0616
title: 有界混合枝長の蜘蛛木における正規極限の必要十分条件と葉による二峰消滅
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants]
aliases: []
relations:
- type: depends_on
  target: K0602
  note: 任意グラフのq点整数平面実現と極大配置の削除集合分類
- type: depends_on
  target: K0614
  note: 任意枝長の中心状態別母関数と総数不等式
- type: generalizes
  target: K0615
  note: 長さ2・3の混合を、葉を含む有界枝長と全qへ拡張
artifacts:
- path: research/experiments/bounded-mixed-spider-20261102/proof.md
  role: proof
  note: 混合枝長の厳密母関数・全変動距離・正規極限の必要十分条件
- path: research/experiments/bounded-mixed-spider-20261102/verify.py
  role: verifier
  note: グラフ削除177条件、禁止超辺15条件84304部分集合、部門不等式60条件の独立照合
scope: K0602の整数平面q点共円共線実現。固定L>=2、固定q>=4、長さ1..Lの混合蜘蛛木、長さ2の枝数n2→∞、他の枝数任意。極大配置一様分布。標準格子盤・無作為着手順は対象外。
evidence: 中心状態別の全称計数、全変動距離評価、Lindeberg中心極限定理、二峰混合による必要性、有限独立完全列挙。
---

# 葉を少しずつ増やすだけでも、長さ2蜘蛛木の二峰混合は消える

長さℓ=1..Lの枝をn_ℓ本持つ蜘蛛木をK0602で整数平面の禁止q点共円・共線ゲームに実現する。r=q−3、E=Σℓn_ℓ、d=Σn_ℓ、最短極大石数s=2+rE。K0614の枝多項式F_ℓ,G_ℓ,J_ℓにより、**任意の有限n_ℓ**で

\[
P(u)=u^s\prod F_\ell(u)^{n_\ell}
+u^{s+d-1}\left(\prod G_\ell(u)^{n_\ell}-\prod J_\ell(u)^{n_\ell}\right)
+u^{s+E-1}
\]

が厳密に成立する。中心残存部門の独立枝変数の和をSとすると、A=∏F_ℓ(1)^{n_ℓ}、B=∏G_ℓ(1)^{n_ℓ}に対し、極大配置一様の終局石数Hは

\[
\boxed{d_{\rm TV}(\mathcal L(H-s),\mathcal L(S))\le2B/A.}
\]

各枝のSへの平均・分散の和をM,Vとする。**n_2→∞、Lとq固定**ならV→∞であり、次が必要十分である。

\[
\boxed{\frac{H-s-M}{\sqrt V}\Rightarrow N(0,1)
\iff\left(q\ge5\ \text{または}\ \sum_{\ell\ne2}n_\ell\to\infty\right).}
\]

特にq=4では、長さ3以上の枝だけでなく**長さ1の葉でも**二峰混合を消せる。長さ1の枝k本と長さ2の枝n本の場合、k固定でn→∞なら

\[
\boxed{\frac{H-s}{n}\Rightarrow
\frac{2^k}{2^k+1}\delta_{1/3}
+\frac1{2^k+1}\delta_1.}
\]

一方、k→∞なら、kがnよりどれほど遅く増えても正規極限に変わる。証明の鍵は、F_1(1)=r+1>G_1(1)=1、F_2(1)=r²+r+1、G_2(1)=r+2、ℓ>=3ではF_ℓ(1)>G_ℓ(1)であり、**q=4・長さ2だけが部門総数で同率**となることにある。

[全称証明](../../experiments/bounded-mixed-spider-20261102/proof.md)と[独立検証器](../../experiments/bounded-mixed-spider-20261102/verify.py)を参照。グラフ削除177条件、禁止超辺直接列挙15条件・84,304部分集合で不一致0。無限族の結論は有限列挙からの推測ではない。標準11×11全盤の勝敗は述べない。