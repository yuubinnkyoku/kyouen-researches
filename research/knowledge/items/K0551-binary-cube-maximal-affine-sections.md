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

## 交点数の空白と密な禁止組の全称公式

最大交点数の直下には空白がある。任意の実 $k$ 平坦 $L$、$2\le k<d$ に対し、

$$
|L\cap V_d|=2^k\quad\text{または}\quad |L\cap V_d|\le3\cdot2^{k-2}.
$$

後者は $d\ge k+1$ で達成可能（座標 $t_1,\ldots,t_k,t_1+t_2$）。したがって $3\cdot2^{k-2}<q\le2^k$ のとき、同じ実 $k$ 平坦に載る相異なる $q$ 点組の総数は

$$
\boxed{F_{d,k,q}=2^{d-k}\left\{\begin{matrix}d+1\\k+1\end{matrix}\right\}\binom{2^k}{q}}.
$$

各 $q$ 点組は一意な $k$ 平坦を張るため重複しない。特に $k=3,q=7$ では $d=4$ に160組、$d=5$ に2080組。

五次元立方体の3平坦の交点数分布を有理数と有限体の独立完全列挙で確認すると、4点:3840、5点:480、6点:1200、8点:260。この分布から5石極大配置数を $480+1200\cdot6+260\cdot56=\boxed{22240}$ と再計数でき、K0546の全安全局面列挙と一致する。空白・禁止組公式は全称数学的証明、平坦分布と22240の照合は有限完全列挙である。

[証明](../../experiments/binary-cube-affine-sections-20261024/proof.md)、[有理数検証器](../../experiments/binary-cube-affine-sections-20261024/verify.py)、[有限体独立検証器](../../experiments/binary-cube-affine-sections-20261024/affine_gap_independent.cpp)、[結果表](../../experiments/binary-cube-affine-sections-20261024/results.md)。


## 最大交点数を禁止する共超平面版の最大安全石数（全称定理）

任意の \(d\ge1\) で、二値超立方体 \(\{0,1\}^d\) 上の**相異なる \(q=2^{d-1}\) 点が同じ実 \((d-1)\) 次元超平面に載ることを禁止する版**を考える。この版の最大安全石数は

$$
\boxed{K_d^{\mathrm{flat}}=2^d-1-\lceil\log_2(d+1)\rceil.}
$$

これは、K0546・K0552の \(d+1\) 点共超平面禁止版の \(K_d\) と**別の量**である。例えば \(d=3,4,5,6,7,8\) で \(K_d^{\mathrm{flat}}=5,12,28,60,124,251\)。

証明は最大交点平坦の分類から始まる。禁止集合は \(x_i=0,1\) と \(x_i=x_j,1-x_j\) の \(d(d+1)\) 個に限る。安全配置の補集合 \(T\) がすべての禁止集合を横切るには、\(T\) を行とする二値行列の \(d\) 列が、非定数かつ互いに等しくも補数でもない必要十分がある。\(t=|T|\) ならそのような列は最大 \(2^{t-1}-1\) 本なので \(t\ge1+\lceil\log_2(d+1)\rceil\)。逆に、第一行を全0とし、残る \(t-1\) 行で各列に相異なる非零二進表現を与えれば等号を達成する。

**根拠の区別**：上の最大安全石数は任意の \(d\ge1\) についての数学的証明。\(d\le7\) の全ての \(t-1\) 点削除候補の完全列挙と、\(d=3,4\) の全 \(q\) 点組の独立アフィン階数検査は照合にすぎない。勝敗・Grundy値・最小極大石数は未決定。

[詳細な全称証明](../../experiments/binary-cube-affine-sections-20261024/proof.md)、[検算結果](../../experiments/binary-cube-affine-sections-20261024/results.md)、[横断集合の完全列挙器](../../experiments/binary-cube-affine-sections-20261024/verify_maximal_hyperplane_transversal.py)、[独立アフィン階数検査器](../../experiments/binary-cube-affine-sections-20261024/verify_maximal_hyperplane_rank.cpp)。
