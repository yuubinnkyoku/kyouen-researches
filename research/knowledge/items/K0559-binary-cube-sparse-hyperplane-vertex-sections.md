---
id: K0559
title: 二値超立方体の1・2・3・4点超平面頂点切片数の全次元公式
kind: proposition
status: proved
topics: [geometry, variants, statistics]
aliases: []
relations:
- type: depends_on
  target: K0551
  note: 3点の別証明、および4点切片を2・3平坦に分けた全称計数
artifacts:
- path: research/experiments/binary-cube-sparse-hyperplane-sections-20261025/proof.md
  role: proof
  note: 任意次元の1・2・3・4点切片公式、三点の座標型分類、4点のアフィン包による分割
- path: research/experiments/binary-cube-sparse-hyperplane-sections-20261025/verify_affine_planes.py
  role: verifier
  note: d=2..6の全三点組を整数Cramer則で検査する独立有限完全列挙
- path: research/experiments/binary-cube-sparse-hyperplane-sections-20261025/verify_four_sections.cpp
  role: verifier
  note: d=3..6の全4点組を整数行列式で調べる独立有限完全列挙
- path: research/experiments/binary-cube-sparse-hyperplane-sections-20261025/results.md
  role: data
  note: 全三点組・全四点組のアフィン包交点数分布と公式値の比較
scope: 全整数d>=1の二値超立方体で、実アフィン超平面との交点がちょうど1・2・3・4頂点となる異なる非空頂点集合の個数。超平面自体は数えない。
evidence: アフィン包からの超平面選択、三点の座標型の包除原理、四点の2・3平坦分割とK0551の全称平坦計数による数学的証明。三点d=2..6・四点d=3..6の整数完全列挙は独立照合。
---

# 1・2・3・4点の疎な超平面頂点切片

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

## 4点切片の全称計数

さらに、$d\ge3$ について

$$
\boxed{
E_{d,4}=\frac{16^d-12\cdot12^d+30\cdot10^d-35\cdot8^d
+27\cdot6^d-16\cdot4^d+5\cdot2^d}{24}.
}
$$

$d=1,2$ では $E_{d,4}=0$。$d=3,4,5,6,7,8$ の順に **12, 180, 4560, 123536, 3014592, 66345280** である。

任意の4点切片のアフィン包は次元2または3で、交点はちょうどその4頂点となる。逆に、頂点4個で張られ、交点がちょうど4点となる真のアフィン平坦は、頂点を追加せず実超平面に拡張できる。K0551で全次元計数済みの4点2平坦と4点3平坦を足せば

$$
E_{d,4}=2^{d-2}\left\{\begin{matrix}d+1\\3\end{matrix}\right\}
+H^{(3)}_{d,4}
$$

となり、表示した指数公式が従う。これは**全称数学的証明**である。独立した整数Cramer則による全4点組の直接完全列挙で $d=3..6$ を照合した。詳細は[証明（定理2）](../../experiments/binary-cube-sparse-hyperplane-sections-20261025/proof.md)、[C++検証器](../../experiments/binary-cube-sparse-hyperplane-sections-20261025/verify_four_sections.cpp)、[結果](../../experiments/binary-cube-sparse-hyperplane-sections-20261025/results.md)。

**限界**：これらは異なる頂点切片の個数であり、実超平面そのものの個数、共超平面の禁止$q$点組の総数、ゲームの勝敗・Grundy値ではない。$q\ge5$ の疎な切片は分類していない。有限検算を無界次元の証明として用いていない。
