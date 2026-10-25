---
id: K0557
title: 二値超立方体の密度1/4超平面切片は高々5座標型・異なる頂点切片は4C(d,2)+16C(d,3)+92C(d,4)+80C(d,5)個
kind: proposition
status: proved
topics: [geometry, variants, statistics]
aliases: []
relations:
- type: depends_on
  target: K0556
  note: 1/4を超える切片と非等絶対値係数の上界との境界を精密化する
artifacts:
- path: research/experiments/binary-cube-quarter-sections-20261025/proof.md
  role: proof
  note: 任意実係数の支持数制限・完全分類・頂点切片の重複を除いた全称計数証明
- path: research/experiments/binary-cube-quarter-sections-20261025/verify_integer_weights.py
  role: verifier
  note: 正整数重み1..8、支持2..9の全24301重み多重集合と全切片を独立DP照合
- path: research/experiments/binary-cube-quarter-sections-20261025/verify_vertex_sections.cpp
  role: verifier
  note: 符号付き整数法線±1..±4、支持2..5の直接頂点列挙による切片集合数検証
- path: research/experiments/binary-cube-quarter-sections-20261025/results.md
  role: data
  note: 二方式の検証範囲・実測結果・全称公式の数値
scope: d>=2の{0,1}^dにおいてちょうど2^(d-2)頂点を含む実アフィン超平面。超平面そのものは無限個となり得るため、計数対象は異なる頂点交点集合。
evidence: 任意の実係数に対する条件付き二座標単射・部分和の単調増加・有限支持の組合せ分類による全称証明。整数係数有限列挙2方式は独立照合。
---

# 密度ちょうど1/4の切片の全称分類と計数

$d\ge2$、$V_d=\{0,1\}^d$ とする。実アフィン超平面 $H$ が
$|H\cap V_d|=2^{d-2}$ を満たすなら、法線の非零座標数 $k$ は **$2\le k\le5$**。
$k=5$ の場合は座標反転・並べ替え・非零定数倍を除いて、唯一

$$x_1+x_2+x_3+x_4+2x_5=3$$

である。$k=2,3,4$ の全型は[全称証明](../../experiments/binary-cube-quarter-sections-20261025/proof.md)に列挙した。

超平面は同じ頂点切片を共有し得る。**異なる頂点集合**
$H\cap V_d$ の総数は、全 $d\ge2$ で

$$
\boxed{Q_d=4\binom d2+16\binom d3+92\binom d4+80\binom d5}.
$$

存在しない二項係数は0とする。$d=2,3,4,5,6,7,8$ で
$Q_d=4,28,180,740,2240,5544,11928$。

支持数別の異なる切片は $k=2,3,4,5$ の順に **4,16,92,80** 種類
（指定した $k$ 座標上）。これらは互いに重複しない。

**注意**：これは超平面の個数ではない。$d\ge2$ では
$x_1+t x_2=0$（$t>0$）が無限個の異なる超平面を与えるが、
頂点切片はすべて $\{x_1=x_2=0\}$ と同じである。
1/4より大きい切片を扱う[K0556](K0556-binary-hypercube-superquarter-hyperplane-spectrum.md)との重要な違いである。

任意実係数についての結論は[数学的証明](../../experiments/binary-cube-quarter-sections-20261025/proof.md)による。
[Python検査](../../experiments/binary-cube-quarter-sections-20261025/verify_integer_weights.py)と
[C++検査](../../experiments/binary-cube-quarter-sections-20261025/verify_vertex_sections.cpp)は
有界整数係数の有限完全列挙であり、実係数全体の証明の代用ではない。
ゲームの勝敗・Grundy値や、1/4未満の切片は対象外。
