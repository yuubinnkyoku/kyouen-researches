---
id: K0551
title: 二値超立方体のk次元平坦の最大交点数とStirling数による全個数
kind: proposition
status: proved
topics: [geometry, variants, statistics]
aliases: []
relations:
- type: generalizes
  target: K0545
  note: K0545の共面四点数の全称公式を任意のアフィン次元kに拡張（同項目の四次元ゲーム強解決は対象外）
artifacts:
- path: research/experiments/binary-cube-affine-sections-20261024/proof.md
  role: proof
  note: 交点上界・等号分類・Stirling数公式と禁止集合数の全称証明
- path: research/experiments/binary-cube-affine-sections-20261024/verify.py
  role: verifier
  note: 有理数RREFによるd≤5のアフィン平坦の直接完全列挙
- path: research/experiments/binary-cube-affine-sections-20261024/results.md
  role: data
  note: d≤5の相異なる平坦数と等号達成数
scope: 全整数d≥1、0≤k≤dの二値超立方体と実k次元アフィン平坦
evidence: 任意次元の射影・アフィンBoolean関数の分類・第二種Stirling数による全称証明。d≤5の有理数完全列挙で独立照合
---

# 二値超立方体の最大交点アフィン平坦の全分類

任意の実k次元アフィン平坦Lについて、二値超立方体V_d={0,1}^dとの交点は最大2^k点である。等号を達成する平坦は、k個の自由二値変数t_iを使って各座標が0、1、t_i、1−t_iのいずれかで表され、各変数が少なくとも一度現れるものに限る。

等号達成平坦の個数は、第二種Stirling数を用いて

$$
\boxed{N_{d,k}=2^{d-k}\left\{\begin{matrix}d+1\\k+1\end{matrix}\right\}}
$$

である。漸化式は $N_{d+1,k}=2(k+1)N_{d,k}+N_{d,k-1}$。

k=2ではK0545の共面四点数 $2^{d-3}(3^d-2^{d+1}+1)$ に一致する。一般に、2^k点が同じk平坦に載る禁止ルールの禁止組数はN_{d,k}であり、q>2^k点を禁止する版は全盤面で制約が空となり、全安全局面の通常Grundy値は $(2^d-|S|)\bmod2$。

**証拠の範囲**：上界・等号分類・個数は全称数学的証明。d=2〜5の有限有理数列挙は独立照合であり、証明の代用ではない。k次元超平面禁止版のq≤2^kの一般的な勝敗や最大安全石数は主張しない。
