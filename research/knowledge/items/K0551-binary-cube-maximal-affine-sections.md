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

**根拠の区別**：上の最大安全石数は任意の \(d\ge1\) についての数学的証明。\(d\le7\) の全ての \(t-1\) 点削除候補の完全列挙と、\(d=3,4\) の全 \(q\) 点組の独立アフィン階数検査は照合にすぎない。最小極大石数は以下の全称定理で決定し、Grundy値・勝敗は四次元まで有限強解決した。

[詳細な全称証明](../../experiments/binary-cube-affine-sections-20261024/proof.md)、[検算結果](../../experiments/binary-cube-affine-sections-20261024/results.md)、[横断集合の完全列挙器](../../experiments/binary-cube-affine-sections-20261024/verify_maximal_hyperplane_transversal.py)、[独立アフィン階数検査器](../../experiments/binary-cube-affine-sections-20261024/verify_maximal_hyperplane_rank.cpp)。


## 高密度共超平面禁止版の最小極大配置（全称定理）

上と同じ \(q=2^{d-1}\) 点共超平面禁止版について、任意の \(d\ge1\) で

$$
\boxed{s_d^{\mathrm{flat}}=2^d-d-1,\qquad
\#\{\text{最小極大安全配置}\}=2^{d-1}d!}.
$$

最小極大安全配置 \(S\) の補集合 \(V_d\setminus S\) は、**二値超立方体の対頂点を結ぶ最短辺路の \(d+1\) 頂点集合に限る**。逆も成立する。

証明の核心は、極大安全配置の補集合が包含極小な禁止超平面の横断集合であること。各横断点には、その点だけを含む禁止超平面が存在する。残りの横断点はその二値補集合に対応する別の実アフィン超平面上に載るため、各点を他から分離するアフィン関数が得られる。よって横断集合はアフィン独立で、高々 \(d+1\) 点。等号の場合には、座標列を補数同値で割った空間で各点の必須性を辺として表すと、全座標を一度ずつ使う単一巡回路になり、対頂点間の最短辺路に限る。個数は始点 \(2^d\) 通りと座標反転順序 \(d!\) 通りを逆順の重複2で割る。

既存の最大安全石数の定理と合わせ、**極大安全石数の両端**が全次元で決まる：

$$
\boxed{2^d-d-1\ \le |S|_{\mathrm{terminal}}\le\
2^d-1-\lceil\log_2(d+1)\rceil}.
$$

この不等式は全ての中間石数の極大配置が存在するという意味ではない。\(d\le5\) ではPythonとC++の独立完全列挙で最小横断集合の分布を照合し、サイズ \(d+1\) の横断集合と最短辺路の集合が一致した。

## 高密度版の有限強解決（d=4,q=8）

四次元二値超立方体の8点共超平面禁止版では、全65536部分集合のうち**61719局面が安全**。極大局面は11石192個、12石560個。通常版とmisère版のGrundy値の組 \((g,h)\) は

- \((0,1)\)：29367局面
- \((1,0)\)：30720局面
- \((2,2)\)：1632局面

だけである。従って**全安全局面で0と1の交換則が成立**し、空盤は \((g,h)=(0,1)\)、通常版後手必勝・misère版先手必勝。全16初手後は \((1,0)\)。

Pythonの座標・対角面方式と、C++の全8点組アフィン階数方式による独立した有限完全列挙が一致した。\(d=3,q=4\) の159安全局面も再計算し、既存K0530の交換則反例25局面と一致した。

**証拠の境界**：\(s_d^{\mathrm{flat}}\) と最小極大配置の分類・個数は全称数学的証明。\(d=4\) のGrundy値は有限完全列挙であり、\(d\ge5\) の勝敗や交換則は未決定。

[全称証明と有限強解決の説明](../../experiments/binary-cube-affine-sections-20261024/proof.md)、[検算結果](../../experiments/binary-cube-affine-sections-20261024/results.md)。

## 高密度版の全終局石数と最大終局配置数（全称定理）

$d\ge1$, $t_d=1+\lceil\log_2(d+1)\rceil$ とする。$q=2^{d-1}$ 点共超平面禁止版で、極大安全配置の石数は**穴なく**

$$
\boxed{2^d-d-1,\;2^d-d,\;\ldots,\;2^d-t_d}
$$

の全整数に一致する。さらに最大安全石数 $K_d^{\mathrm{flat}}=2^d-t_d$ を達成する配置数は

$$
\boxed{A_d=\frac{2^d}{t_d!}\prod_{j=0}^{d-1}(2^{t_d-1}-1-j)
=\frac{2^d d!}{t_d!}\binom{2^{t_d-1}-1}{d}.}
$$

$d=3,4,5,6,7,8$ の順に $A_d=8,560,3360,13440,26880,553512960$。証明は包含極小横断集合の鎖状構成と、正規化した二値座標列の単射計数による。**全次元での数学的証明**であり、$d\le5$ の全極小横断集合の完全列挙および $d\le12$ の各石数での明示構成・私有禁止面の検査は独立照合に限る。$d\ge5$ のGrundy値は未解決。

[証明（定理8）](../../experiments/binary-cube-affine-sections-20261024/proof.md)・[結果](../../experiments/binary-cube-affine-sections-20261024/results.md)・[検証器](../../experiments/binary-cube-affine-sections-20261024/verify_maximal_hyperplane_transversal.py)。


## 五次元高密度版の交換則に対する最初の反例（有限完全列挙）

$d=5,q=16$ の高密度共超平面禁止版では、四次元版で成立した通常・misèreのGrundy値の0↔1交換則は**全局面では成立しない**。25石の安全局面
$$
S=\{0,1\}^5\setminus\{0,1,2,7,13,24,28\}
$$
で、通常値とmisère補助値はともに $\boxed{(g,h)=(0,0)}$。未占有点への6合法手はいずれも子の値が $(2,2)$、残る1手は違法である（頂点番号は二進座標）。

一方、**全安全局面のうち未占有点が6点以下なら交換則が成立**する。これは最小横断集合サイズ4からの短い全称帰納証明による。よって25石が最初の反例層。未占有7点の全 $\binom{32}{7}$ 候補を有限完全列挙すると、安全局面3,025,376個のうち不一致は**34,560個**、すべて $(0,0)$。五次元立方体の座標反転・置換で13軌道（1920点軌道8個、3840点軌道5個）に分かれる。

禁止面の直接生成と、五頂点組の整数アフィン階数から禁止超平面を独立復元する方式が、全件数と証人の合法手で一致した。**五次元全局面の強解決や六次元以上の交換則は未確定**。詳細は[命題9の証明](../../experiments/binary-cube-affine-sections-20261024/proof.md)、[有限結果](../../experiments/binary-cube-affine-sections-20261024/results.md)、[直接方式](../../experiments/binary-cube-affine-sections-20261024/verify_d5_dense_swap_faces.cpp)、[独立整数階数方式](../../experiments/binary-cube-affine-sections-20261024/verify_d5_dense_swap_rank.cpp)。


## 高密度版の交換則は全ての d≥5 で破れる（全称定理）

五次元の反例を任意の高次元へ持ち上げられる。任意の整数 $d\ge5$ に対し、$q=2^{d-1}$ 点共超平面禁止版には **通常Grundy値とmisère補助値がともに0** の安全局面が存在する：

$$
\boxed{g(S_d)=h(S_d)=0,\qquad |S_d|=2^d-d-2.}
$$

具体的に、$A=\{1,2,6,7,9,11,16\}\subset\{0,1\}^5$、$n=d-5$ として、未占有点を

$$
T_d=\{(x,0^n):x\in A\}\cup\{(3,e_j):1\le j\le n\}
$$

と取ればよい。$d=5$ は既存の反例軌道の一つ。$d\ge6$ では追加点がすべて合法手で除去不能となり、残る7点のうち合法な部分集合が**全次元で同じ25局面**になることを全称証明した。根の6合法手の値は $(3,3)$ が4手、$(2,2)$ が2手なので、両者のmexは0。

これは四次元の全局面交換則を五次元以上へ一般化できないという**全次元の反証**であり、五次元以上の空盤勝敗・全安全局面の強解決ではない。証明・25局面の表は[定理10](../../experiments/binary-cube-affine-sections-20261024/proof.md)、[結果表](../../experiments/binary-cube-affine-sections-20261024/results.md)。[Python検証器](../../experiments/binary-cube-affine-sections-20261024/verify_dense_swap_all_dimensions.py)と[独立C++検証器](../../experiments/binary-cube-affine-sections-20261024/verify_dense_swap_direct.cpp)で $d=5,6,7,8,9,10,12,15,25$ を照合した。
