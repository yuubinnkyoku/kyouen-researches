---
id: K0558
title: 二値超立方体の固定正密度超平面頂点切片数は次元の整数値多項式・密度1/4以上の明示式
kind: proposition
status: proved
topics: [geometry, variants, statistics]
aliases: []
relations:
- type: depends_on
  target: K0556
  note: 密度1/4超の具体係数を利用
- type: depends_on
  target: K0557
  note: 密度ちょうど1/4の具体係数を利用
artifacts:
- path: research/experiments/binary-cube-dense-section-polynomial-20261025/proof.md
  role: proof
  note: 任意固定正密度の有限支持・支持一意性・整数値多項式性と計算可能性の全称証明
- path: research/experiments/binary-cube-dense-section-polynomial-20261025/verify_affine_hulls.py
  role: verifier
  note: 法線に依存しないアフィン包の全頂点部分集合列挙で密度1/4以上の支持1..4の係数を独立照合
scope: 0<δ≤1/2を固定した任意のd≥1の二値超立方体で、実アフィン超平面と頂点集合の異なる非空交点集合のうち密度δ以上のものを数える。
evidence: Spernerの反鎖上界・切片自身からの支持一意復元・有理アフィン包の有限判定による全称証明。密度1/4の明示係数はK0556・K0557に依存し、支持1..4を独立有限完全列挙。
---

# 正密度の超平面頂点切片は有限支持・個数は次元多項式

$V_d=\{0,1\}^d$、$0<\delta\le1/2$ を固定する。
$|H\cap V_d|\ge\delta2^d$ を満たす実アフィン超平面 $H$ の
**異なる頂点切片集合**の数を $P_\delta(d)$ とする。

$$
K_\delta=\max\left\{k\ge1:
\frac{\binom{k}{\lfloor k/2\rfloor}}{2^k}\ge\delta\right\}.
$$

この値は有限であり、全次元 $d\ge1$ で

$$
\boxed{P_\delta(d)=\sum_{k=1}^{K_\delta}c_{\delta,k}\binom dk},
\qquad c_{\delta,k}\in\mathbb Z_{\ge0}.
$$

各係数は $k$ 次元二値立方体の頂点部分集合に対する**有限個の有理数階数判定**で厳密に求められる。
従って固定正密度での異なる切片集合数は、全次元で成立する整数値多項式である。

証明の要点は、同じ正重み部分和を与える割当が反鎖となるため支持座標数が $K_\delta$ 以下であること、
および非空切片の支持集合が「その方向の立方体辺を切片内に含まない座標」として一意に復元できることである。
[全称証明と有限判定法](../../experiments/binary-cube-dense-section-polynomial-20261025/proof.md)に詳述。

特に **密度1/4以上** の場合、既存の[K0556](K0556-binary-hypercube-superquarter-hyperplane-spectrum.md)と
[K0557](K0557-binary-hypercube-quarter-vertex-sections.md)の分類を統合すると

$$
\boxed{\begin{aligned}
P_{1/4}(d)={}&2\binom d1+6\binom d2+24\binom d3+100\binom d4\\
&+112\binom d5+32\binom d6+128\binom d7+128\binom d8.
\end{aligned}}
$$

$d=1,2,3,4,5,6,7,8,9,10$ では順に
**2, 10, 48, 240, 922, 2786, 7184, 16848, 37410, 80234**。
支持 $k\le4$ の係数 $2,6,24,100$ は
[アフィン包の独立完全列挙](../../experiments/binary-cube-dense-section-polynomial-20261025/verify_affine_hulls.py)
でも一致した。$k=5,6,7,8$ の係数は既存全称定理から導く。

**限界**：これは超平面そのものや共超平面$q$点組の個数ではない。
$\delta<1/4$ の係数は未計算であり、有限計算可能性のみを証明した。
$q$ 固定で $d\to\infty$ の場合は密度が0に近づくため本定理の固定密度仮定を満たさない。
