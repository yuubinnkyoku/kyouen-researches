---
id: K0559
title: 二値超立方体の1・2・3点超平面頂点切片数の全次元公式
kind: proposition
status: proved
topics: [geometry, variants, statistics]
aliases: []
relations:
- type: depends_on
  target: K0551
  note: 3点が張る2平坦の最大4点性と4点2平坦の全称計数による別証明
artifacts:
- path: research/experiments/binary-cube-sparse-hyperplane-sections-20261025/proof.md
  role: proof
  note: 任意次元の1・2・3点切片公式、三点の座標型分類、二つの独立な全称導出
- path: research/experiments/binary-cube-sparse-hyperplane-sections-20261025/verify_affine_planes.py
  role: verifier
  note: d=2..6の全三点組を整数Cramer則で検査する独立有限完全列挙
- path: research/experiments/binary-cube-sparse-hyperplane-sections-20261025/results.md
  role: data
  note: 全三点組の平坦交点数分布と公式値の比較
scope: 全整数d>=1の二値超立方体で、実アフィン超平面との交点がちょうど1・2・3頂点となる異なる非空頂点集合の個数。超平面自体は数えない。
evidence: アフィン包からの超平面選択、座標の少数派型の包除原理、およびK0551の最大4点2平坦計数による全称数学的証明。d=2..6の整数完全列挙は独立照合。
---

# 1・2・3点の疎な超平面頂点切片

$V_d=\{0,1\}^d$ とし、$H$ を実アフィン超平面とする。
異なる集合 $H\cap V_d$ のうち、ちょうど $q$ 点を持つものの数を $E_{d,q}$ とする。超平面自体の個数ではない。

全 $d\ge1$ について

$$
\boxed{E_{d,1}=2^d,\qquad
E_{d,3}=\frac{8^d-3\cdot6^d+3\cdot4^d-2^d}{6}.}
$$

また $d\ge2$ では

$$
\boxed{E_{d,2}=\binom{2^d}{2}},
$$

ただし $E_{1,2}=0$ である。$d<3$ では $E_{d,3}=0$。

三点切片の必要十分条件は、三点の各点が、残り二点と異なる値を取る座標を**少なくとも一つずつ**持つことである。これは二値立方体のアフィン包に第四頂点が入らない条件と一致する。

$d=3,4,5,6,7,8$ の $E_{d,3}$ は順に **8, 160, 2080, 22400, 217728, 1989120**。$d=2..6$ の全三点組を整数演算で直接調べ、公式と一致した。

既存[K0551](K0551-binary-cube-maximal-affine-sections.md)の2平坦計数から、独立に

$$
E_{d,3}=\binom{2^d}{3}
-4\cdot2^{d-2}\left\{\begin{matrix}d+1\\3\end{matrix}\right\}
\qquad(d\ge2)
$$

とも導ける。中括弧は第二種スターリング数。二つの全称証明と有限検算の詳細は[証明](../../experiments/binary-cube-sparse-hyperplane-sections-20261025/proof.md)を参照。

**限界**：この公式は頂点切片の数であり、実超平面の個数、共超平面の禁止$q$点組の総数、ゲームの勝敗・Grundy値ではない。$q\ge4$ の疎な切片は分類していない。有限検算を無界次元の証明として用いていない。
