---
id: K0617
title: 禁止4点版の無界混合枝長蜘蛛木における正規極限の鋭い非臨界枝数条件
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants]
aliases: []
relations:
- type: depends_on
  target: K0602
  note: 任意グラフの整数平面q点実現と極大配置の削除集合分類
- type: depends_on
  target: K0614
  note: 任意有限枝長の中心状態別母関数
- type: depends_on
  target: K0616
  note: 混合蜘蛛木の部門分解と有界枝長での正規極限判定
artifacts:
- path: research/experiments/unbounded-spider-gaussian-20261102/proof.md
  role: proof
  note: 4状態遷移・鋭い一様比17/20・Lindebergと二峰残存による全称証明
- path: research/experiments/unbounded-spider-gaussian-20261102/verify.py
  role: verifier
  note: 枝長150の厳密漸化式・15語計数・混合405条件685204頂点部分集合の独立照合
scope: K0602の整数平面実現による禁止4点版q=4、長さ2の枝数n2→∞、最大枝長Lmax=o(sqrt(n2))、その他の枝数と長さは任意に変動。極大配置一様分布。標準格子盤・無作為着手順は対象外。
evidence: 枝語の4状態遷移に基づく全称3項漸化式と鋭い17/20上界、三角配列Lindeberg中心極限定理、第二部門の正の質量による必要性、有限独立完全列挙。
---

# 枝長の上限が増えても、非臨界枝が無限本なら正規極限

禁止4点版の蜘蛛木で、長さ2の枝数を n=n_2→∞、長さ2以外の枝の総数を K=Σ_{ℓ≠2}n_ℓ、最大枝長を L_max とする。**L_max=o(√n)** の条件のもと、極大配置を一様に選んだ終局石数 H、最短石数 s、中心残存枝の独立和から求める平均 M・分散 V に対して

\[
\boxed{\frac{H-s-M}{\sqrt V}\Rightarrow N(0,1)
\quad\Longleftrightarrow\quad K\to\infty.}
\]

これはK0616の**禁止4点版について**枝長の固定上限を外した定理である。例えば最大枝長が n^{1/3} 程度まで増えても、長さ2以外の枝が無限本あれば正規極限になる。最大枝長が √n と同程度以上の場合は本定理の対象外。

鍵となるのは、中心を残す枝の総数 A_ℓ と中心を削除する枝の総数 B_ℓ が、q=4では3項和漸化式を満たし、

\[
\boxed{A_\ell-B_\ell=A_{\ell-3}\ (\ell\ge3),\qquad
\sup_{\ell\ne2}B_\ell/A_\ell=17/20}
\]

となること。上限17/20は枝長5で達成される**鋭い定数**である。中心残存部門の独立枝和 S との全変動距離は、全ての有限枝長の組について

\[
\boxed{d_{TV}(\mathcal L(H-s),\mathcal L(S))
\le\min\{1,2(17/20)^K\}.}
\]

一方Kが有界な部分列では中心削除部門が正の質量を持ち続け、標準化後に+∞へ逃げる。従って正規極限の必要性も示せる。

[全称証明](../../experiments/unbounded-spider-gaussian-20261102/proof.md)と[独立検証器](../../experiments/unbounded-spider-gaussian-20261102/verify.py)を参照。枝長1〜150の厳密整数計数、枝長1〜15の独立語列挙、混合405条件・計685,204グラフ頂点部分集合を照合し不一致0。無限族の結論は数学的証明によるもので、有限計算の外挿ではない。標準11×11全盤の勝敗を主張しない。
