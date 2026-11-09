---
id: K0713
title: 二値立方体の共面四点は一意な平行四辺形で三点から高々一通りに補完
kind: proposition
status: proved
topics: [variants, geometry, rectangles]
aliases: []
relations:
- type: depends_on
  target: K0545
  note: 共面四点数の公式と二値立方体の長方形構造
artifacts:
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/proof.md
  role: proof
  note: 単射な二座標射影による共面四点と平行四辺形の同値
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/triple-unique-completion.md
  role: proof
  note: 三点のxorによる一意補完と少数派条件の全称証明
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/pair-codegrees.md
  role: proof
  note: 二頂点共起数と一点次数の全称公式
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/verify_unique_completion.py
  role: verifier
  note: 整数アフィン小行列式によるd=2..6の全四点・三点・二点の照合
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/finite-audit.json
  role: data
  note: d=2..5における禁止四点数と補完可能三点数
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/finite-audit-d6.json
  role: data
  note: d=6における禁止四点数と全二点・三点の照合
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/constant-weight-layers.md
  role: proof
  note: 等重み層の禁止四点数の全称公式と重み2の場合の四角形禁止グラフへの帰着
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/verify_constant_weight.py
  role: verifier
  note: d=2..7の各重み層で対角和の全数列挙と計数式を照合
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/constant-weight-audit.json
  role: data
  note: 各次元・重みの禁止四点数
scope: 任意のd>=2に対する二値超立方体の相異なる頂点と実数アフィン共面四点。共面五点や平面共円ゲームには拡張しない。
evidence: 二座標射影による平行四辺形の全称証明と少数派座標による一意補完・共起数の組合せ証明。d=2..6の全四点を整数アフィン小行列式で検算。
---

# 二値立方体の共面四点と一意補完

任意の `d≥2` で、二値立方体 `{0,1}^d` の相異なる四頂点が同一アフィン2平面上にあることと、それらを適切に並べて `a+e=b+c` と表せることは同値。アフィン2平面への制限が単射となる二座標を選べば、四頂点は二値正方形の四隅に射影され、各座標のアフィン性から対角和が等しい。逆向きは平行四辺形である。

相異なる三頂点 `a,b,c` を含む共面四点集合は高々一つで、存在する場合の第四頂点は `a xor b xor c`。補完可能な条件は、三点が一致しない座標で少数派となる頂点が、高々二種類であること。共面四点禁止超グラフは、異なる二辺が三点を共有しない **3-線形な4一様超グラフ**である。

禁止四点数は `F(d)=(6^d−2·4^d+2^d)/8`、補完可能な三点数は `4F(d)=(6^d−2·4^d+2^d)/2`。さらに距離 `t` の相異なる二頂点を同時に含む禁止四点数は `2^(t−1)+2^(d−t)−2`、各頂点を含む禁止四点数は `(3^d−2^(d+1)+1)/2` である。

重み `k` の頂点に限った禁止四点数にも、互いに素な二つの偶数サイズの支持集合による全称計数式がある。特に重み2では `3·binom(d,4)` 個であり、頂点を `K_d` の辺と対応させると、禁止四点は四角形に対応する。各重み層の公式を `d=2..7` で別途全数列挙して照合した。

根拠は二座標射影・一意な対角線分割・座標支持集合の計数による**数学的全称証明**。独立検算として整数小行列式から `d=2,3,4,5,6` の全四点を分類し、全二点・三点について公式と条件を照合した。`d=6` では禁止四点4816個、補完可能な三点19264個となる。有限検算を全称証明の代わりにはしない。一般の格子上の共円四点では三点からの補完が複数存在し得る。
