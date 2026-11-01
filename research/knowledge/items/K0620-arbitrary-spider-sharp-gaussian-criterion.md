---
id: K0620
title: 禁止4点蜘蛛木で長さ2の枝が増大する場合の無制限混合枝長・正規極限必要十分条件
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants]
aliases: []
relations:
- type: depends_on
  target: K0602
  note: グラフ型禁止4点ゲームの自由な整数平面実現
- type: depends_on
  target: K0614
  note: 枝多項式F・G・Jと中心状態による厳密分解
- type: generalizes
  target: K0617
  note: 最大枝長の制限付き必要十分条件を含む
- type: generalizes
  target: K0618
  note: 巨大枝1本の二乗臨界尺度と混合極限を含む
- type: depends_on
  target: K0619
  note: 中心残存部門の全枝長一様中心極限定理
artifacts:
- path: research/experiments/arbitrary-spider-sharp-clt-20261102/proof.md
  role: proof
  note: 全枝長無制限の必要十分条件と有限二部門母関数・臨界混合の全称証明
- path: research/experiments/arbitrary-spider-sharp-clt-20261102/verify.py
  role: verifier
  note: 独立枝語・状態遷移・グラフ頂点削除全列挙と有限モーメント検査
scope: K0602の自由な整数平面点集合に実現するq=4の蜘蛛木。長さ2の枝数n2→∞、それ以外の枝数・長さは任意の三角配列。極大配置一様分布。標準格子盤・無作為着手順は対象外。
evidence: K0614の厳密二部門分解、K0617の一様比、K0618・K0619の解析的転送行列による全称証明。有限独立完全列挙は補助監査。
---

# 非臨界枝の本数と総長の合成条件で正規極限を完全判定

禁止4点版の蜘蛛木で長さ2の枝を n=n₂→∞ 本持ち、それ以外の枝の本数を K、総長を L とする。

\[
K=\sum_{\ell\ne2}n_\ell,\qquad L=\sum_{\ell\ne2}\ell n_\ell.
\]

極大配置一様の終局石数をH、最短石数をs=2+Σℓnℓ、中心残存枝の独立和の平均・分散をM,Vとすると、**枝長の上限なし**で

\[
\boxed{\frac{H-s-M}{\sqrt V}\Rightarrow N(0,1)
\quad\Longleftrightarrow\quad K+L/n^2\to\infty.}
\]

これはK0617の枝長制限を除き、K0618の巨大枝1本の二乗尺度も含む**必要十分条件**である。K→∞なら枝長によらず正規極限となり、Kが有界でも L≫n² なら二つの終局長の峰が合流する。Kが有界かつL=O(n²)となる部分列があれば正規極限にはならない。KとL/n²のどちらが大きいかが交互に変わる場合も、この和の発散で正確に判定できる。

Kが有界でL/n²→c∈(0,∞)、中心削除と中心残存の配置数比R→ρ>0なら、極限は

\[
\frac1{1+\rho}N(0,1)+\frac\rho{1+\rho}
N\left(\frac2{3\sqrt{\beta c}},1\right),\qquad
\beta\approx0.063803198448.
\]

特に固定k本の非臨界枝が全て長さ→∞ならρ=(λ−1)^k（λはx³−x²−x−1=0の正実根）。L/n²→0かつK有界では、第二の峰が標準化後に+∞へ逃げる。

[全称証明](../../experiments/arbitrary-spider-sharp-clt-20261102/proof.md)では、有限の正確な母関数と転送行列の一様漸近評価から両方向を証明する。[独立検証器](../../experiments/arbitrary-spider-sharp-clt-20261102/verify.py)は有限枝語・グラフの直接列挙を照合する。有限計算から無界定理を外挿したものではない。

標準11×11全盤の勝敗には適用しない。
