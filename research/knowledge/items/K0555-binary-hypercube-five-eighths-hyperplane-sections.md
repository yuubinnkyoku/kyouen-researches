---
id: K0555
title: 二値超立方体の最大超平面切片5/8密度は5座標型・6座標型だけで全次元32C(d+1,6)個
kind: proposition
status: proved
topics: [geometry, variants, statistics]
aliases: []
relations:
- type: depends_on
  target: K0554
  note: 3/4密度切片の分類・個数を禁止q点組の総数に利用
- type: depends_on
  target: K0551
  note: 最大1/2密度切片の分類・個数および平坦交点上界を利用
artifacts:
- path: research/experiments/binary-cube-hyperplane-five-eighths-20261025/proof.md
  role: proof
  note: Sperner・LYM等号条件と4座標5点不可能性による全次元分類・計数
- path: research/experiments/binary-cube-hyperplane-second-sections-20261025/verify_d5.cpp
  role: verifier
  note: 全201376個の五次元5点組を整数行列式で独立完全列挙（10点切片も検査）
- path: research/experiments/binary-cube-hyperplane-five-eighths-20261025/results.md
  role: data
  note: d=4..8の厳密公式値と五次元独立全数検査
scope: d>=4の二値超立方体における実アフィン超平面の交点数5*2^(d-4)の全分類・計数および共超平面q点組の総数
evidence: 全次元の反鎖・LYM等号条件による数学的証明。d=5は整数小行列式で全5点組を独立完全列挙し照合。
---

# 最大切片の5/8密度の全分類

$d\ge4$、$V_d=\{0,1\}^d$、$m=2^{d-4}$ とする。実アフィン超平面 $H$ が $|H\cap V_d|=5m$ を満たす必要十分条件は、座標反転後に、相異なる5座標の和が2または3、あるいは相異なる6座標の和が3となることである。

そのような超平面は

$$
\boxed{H_d(5m)=32\binom{d+1}{6}}
$$

個（$d=4$ では0個）。また、**同一実超平面に載る相異なる $q=5m$ 点組の総数**は

$$
\boxed{F_d(q)=32\binom{d+1}6+
8\binom{d+1}4\binom{6m}{5m}+
d(d+1)\binom{8m}{5m}}.
$$

$5m$ 以上の頂点を含む超平面切片は、$5m,6m,8m$ の3種類しかない。特に五次元では10点切片32個、禁止10点組248192個、六次元では20点切片224個、禁止20点組9486274784個。

**根拠の境界**：[全称証明](../../experiments/binary-cube-hyperplane-five-eighths-20261025/proof.md)は反鎖・Sperner・LYMの等号条件から任意の$d$に対して導く。[整数行列式による五次元全数検査](../../experiments/binary-cube-hyperplane-second-sections-20261025/verify_d5.cpp)と[結果表](../../experiments/binary-cube-hyperplane-five-eighths-20261025/results.md)は独立した有限照合。ゲームのGrundy値や勝敗、より小さい切片の全分布は未解決。
