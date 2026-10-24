---
id: K0554
title: 二値超立方体の第2位の超平面切片は3座標型・4座標型だけで全次元8C(d+1,4)個
kind: proposition
status: proved
topics: [geometry, variants, statistics]
aliases: []
relations:
- type: depends_on
  target: K0551
  note: 最大超平面切片の分類・個数とd=4の6点切片の既知結果に整合
artifacts:
- path: research/experiments/binary-cube-hyperplane-second-sections-20261025/proof.md
  role: proof
  note: Spernerの反鎖評価と等号分類による全次元証明
- path: research/experiments/binary-cube-hyperplane-second-sections-20261025/verify_d5.cpp
  role: verifier
  note: 五次元の全201376個の5点組から整数行列式で独立に超平面を列挙
- path: research/experiments/binary-cube-hyperplane-second-sections-20261025/results.md
  role: data
  note: d=3..8の公式値とd=5の独立有限完全列挙結果
scope: d>=3の二値超立方体における実アフィン超平面の交点数3*2^(d-3)の全分類・計数、および共超平面q点組の総数
evidence: Sperner定理の等号条件による全称数学的証明。五次元は整数4x4小行列式で全5点組を独立完全列挙し照合。
---

# 二値超立方体の第2位の超平面切片

$d\ge3$、$V_d=\{0,1\}^d$ とし、$q=3\cdot2^{d-3}$ と置く。実アフィン超平面 $H$ と $V_d$ の交点がちょうど $q$ 点となる超平面の個数は

$$
\boxed{H_d(q)=8\binom{d+1}{4}}.
$$

**分類**：非零係数が3個で絶対値が等しく、符号反転後の座標和が1または2となる超平面、あるいは非零係数が4個で絶対値が等しく、符号反転後の座標和が2となる超平面に限る。各支持集合から8個ずつ得られる。

さらに、同じ実超平面上に載る相異なる $q$ 頂点組の総数は

$$
\boxed{F_d(q)=d(d+1)\binom{2^{d-1}}{3\cdot2^{d-3}}
+8\binom{d+1}{4}}.
$$

$q>2^{d-2}$ なので各 $q$ 点組は超平面を一意に決め、重複計数はない。$d=4$ では6点切片40個、禁止6点組600個でK0551の定理12と一致。$d=5$ では**12点切片120個、禁止12点組54,720個**となる。

**証拠の区別**：Sperner定理による全次元の数学的証明。[全称証明](../../experiments/binary-cube-hyperplane-second-sections-20261025/proof.md)と[結果表](../../experiments/binary-cube-hyperplane-second-sections-20261025/results.md)を参照。五次元の[独立C++全数検査](../../experiments/binary-cube-hyperplane-second-sections-20261025/verify_d5.cpp)は201,376個の5点組を走査し、12点切片の80+40個と16点切片の10+20個を確認したが、全次元の証明の代用ではない。より小さい交点数の全分類や、$q$ 点共超平面禁止ゲームのGrundy値・空盤勝敗は主張しない。
