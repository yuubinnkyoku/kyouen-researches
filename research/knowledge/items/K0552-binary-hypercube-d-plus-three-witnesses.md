---
id: K0552
title: 六〜十次元二値超立方体の共超平面禁止版にd+3石の安全配置
kind: proposition
status: proved
topics: [variants, geometry, maximum-safe]
aliases: []
relations: []
artifacts:
- path: research/experiments/binary-cube-hyperplane-d-plus-three-20261024/proof.md
  role: proof
  note: 6次元の双対核証明、一般の余核判定補題、6〜10次元の有限証明書
- path: research/experiments/binary-cube-hyperplane-d-plus-three-20261024/verify_exact.py
  role: verifier
  note: Python整数Bareiss行列式による全最大小行列式の厳密検査
- path: research/experiments/binary-cube-hyperplane-d-plus-three-20261024/verify_mod.cpp
  role: verifier
  note: 独立した素数1009上の掃き出し法で全小行列式の非零性を確認
- path: research/experiments/binary-cube-hyperplane-d-plus-three-20261024/results.md
  role: data
  note: 6〜10次元の明示配置、検査対象数、整数行列式の範囲
scope: d=6,7,8,9,10の二値超立方体におけるd+1点共超平面禁止ゲームの最大安全石数の下界
evidence: 各次元でd+3頂点の明示証人を与え、全C(d+3,2)個の(d+1)次最大小行列式の非零を整数演算と独立な有限体演算で検査。6次元は双対核ベクトルでも証明
---

# 6〜10次元では既知の一般下界を1石改善

二値超立方体 $V_d=\{0,1\}^d$ で、相異なる $d+1$ 点が一つの実アフィン超平面に載ること（退化を含む）を禁止する。最大安全石数を $K_d$ とすると、各 $d\in\{6,7,8,9,10\}$ で

$$
\boxed{K_d\ge d+3}.
$$

したがってK0546の全次元構成下界 $K_d\ge d+2$ は、少なくともこれら5次元では鋭くない。特に $K_6\ge9$ は $K_d=d+2$ が全次元で成立するという可能性への厳密な反例である。

証人の各頂点は、整数 $x$ の第 $i$ ビット（$0\le i<d$）を第 $i$ 座標とする方法で表す。証人一覧は[結果表](../../experiments/binary-cube-hyperplane-d-plus-three-20261024/results.md)に記載した。全ての $d+1$ 点部分集合について、行を $(1,x_0,\ldots,x_{d-1})$ とする正方行列の行列式が非零である。従って任意の $d+1$ 点はアフィン独立で、禁則は一つも含まれない。

**証明の種類**：固定した5つの次元についての明示的・有限の厳密証明である。探索で見つけた証人の完全性（最大値の上界）は主張しない。$d\ge11$ に同じ改善が成立するかも未証明であり、Grundy値・空盤勝敗は扱わない。

さらに一般の $(d+3)\times(d+1)$ 増補座標行列について、左零空間の2本の基底ベクトルの座標対が互いに非比例であることと、全ての最大小行列式が非零であることが同値である。この双対判定補題と6次元の小さい整数証明書は[証明](../../experiments/binary-cube-hyperplane-d-plus-three-20261024/proof.md)に記録した。
