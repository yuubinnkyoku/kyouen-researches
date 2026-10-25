---
id: K0556
title: 二値超立方体の1/4超超平面切片は等絶対値係数のみ・密度は4種類・35/128の個数は128C(d+1,8)
kind: proposition
status: proved
topics: [geometry, variants, statistics]
aliases: []
relations:
- type: generalizes
  target: K0554
  note: 3/8密度の超平面切片分類と個数を含み、1/4超の全密度を決定
- type: generalizes
  target: K0555
  note: 5/16密度の超平面切片分類と個数を含み、非等絶対値係数の一様上界を与える
artifacts:
- path: research/experiments/binary-cube-superquarter-sections-20261025/proof.md
  role: proof
  note: 非等絶対値係数の1/4上界・全密度分類・一般q点組計数の全称数学的証明
- path: research/experiments/binary-cube-superquarter-sections-20261025/verify_direct_normals.cpp
  role: verifier
  note: d=7,8の係数-2..2の全原始法線と切片を整数DPで直接列挙
- path: research/experiments/binary-cube-superquarter-sections-20261025/verify_weight_patterns.py
  role: verifier
  note: 支持1..8・正整数重み1..10の43757組を別方式で有限完全検査
- path: research/experiments/binary-cube-superquarter-sections-20261025/results.md
  role: data
  note: 有界係数独立検査の結果とd=7..10の厳密公式値
scope: d>=1の二値超立方体における交点密度1/4超の実アフィン超平面の全分類・計数。d>=7では全整数q>2^(d-2)の共超平面q点組の総数も決定。
evidence: 任意実係数に対する二座標条件付けの数学的証明と二項係数の分類。d=7,8の有界整数法線直接列挙および43757正整数重み列の独立有限照合。
---

# 1/4超の超平面切片は4密度のみ

$d\ge1$、$V_d=\{0,1\}^d$ とする。実アフィン超平面 $H$ が
$|H\cap V_d|>2^{d-2}$ を満たすなら、方程式 $\sum_i a_ix_i=b$ の
**非零係数の絶対値はすべて等しい**。異なる絶対値 $u,v>0$ が二つあれば、
残りの座標を固定したときの二座標の左辺4値 $c,c+u,c+v,c+u+v$ は
相異なるため、交点は高々 $2^{d-2}$ 点となるからである。

従って座標反転後に $\sum_{i=1}^k y_i=r$ となり、
密度は $2^{-k}\binom kr$。$k\ge9$ では中央二項係数の密度が
$\binom94/2^9<1/4$ 以下なので、$k\le8$。
$1/4$ 超の密度は**ちょうど4種類**で、各超平面の個数は

$$
\begin{array}{c|c|c}
\text{密度}&\text{支持座標数}&\text{超平面数}\\\hline
1/2&1,2&d(d+1)\\
3/8&3,4&8\binom{d+1}{4}\\
5/16&5,6&32\binom{d+1}{6}\\
35/128&7,8&\boxed{128\binom{d+1}{8}}
\end{array}
$$

となる。存在しない支持の二項係数は0とする。
最後の35/128密度は $d\ge7$ で初めて現れ、
$d=7,8,9,10$ の超平面数はそれぞれ **128, 1152, 5760, 21120**。

さらに $d\ge7$、$m=2^{d-7}$、整数 $2^{d-2}<q\le2^{d-1}$ について、
同一実超平面に載る相異なる $q$ 頂点組の個数は

$$
\boxed{\begin{aligned}
F_d(q)={}&d(d+1)\binom{64m}{q}
+8\binom{d+1}{4}\binom{48m}{q}\\
&+32\binom{d+1}{6}\binom{40m}{q}
+128\binom{d+1}{8}\binom{35m}{q}.
\end{aligned}}
$$

$q>2^{d-2}$ 点組は超平面を一意に決めるので重複計数はない。
二項係数は $q>n$ の場合0とする。

**証拠の境界**：[全称証明](../../experiments/binary-cube-superquarter-sections-20261025/proof.md)
は任意実係数・任意次元を扱う。
[直接整数法線検査](../../experiments/binary-cube-superquarter-sections-20261025/verify_direct_normals.cpp)と
[別方式の正係数検査](../../experiments/binary-cube-superquarter-sections-20261025/verify_weight_patterns.py)
は有界係数の有限照合に限る。ゲームのGrundy値・勝敗や1/4未満の切片は未分類。密度ちょうど1/4の頂点切片は[K0557](K0557-binary-hypercube-quarter-vertex-sections.md)で全次元分類済み（超平面自体の個数ではない）。
