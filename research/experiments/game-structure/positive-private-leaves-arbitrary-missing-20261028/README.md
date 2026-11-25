# 全クリーク頂点に私有葉がある分割グラフのGrundy統一公式（2026-10-28）

## 結論：欠損グラフは完全に任意

通常プレイの Node Kayles において、頂点集合がクリーク $C=\{c_0,\ldots,c_{k-1}\}$ と独立集合 $I$ に分かれ、各独立点のクリーク側近傍が **ちょうど1点または2点** の分割グラフ $G$ を考える。$c_i$ にのみ隣接する独立点の個数を $t_i$、$\{c_i,c_j\}$ に隣接する独立点の個数を $r_{ij}$ とする。

**定理（計算機援用全称証明）：** $k\ge3$、**すべての $t_i\ge1$**、任意の $r_{ij}\ge0$ に対して

$$
u=\left(\sum_i t_i+\sum_{i<j}r_{ij}\right)\bmod2,\qquad
z_i=\left(t_i+\sum_{j\ne i}r_{ij}\right)\bmod2,
$$

$$
\boxed{g(G)=
\begin{cases}
1\oplus u\oplus z_0 & z_0=\cdots=z_{k-1},\\
2+u & \text{それ以外}.
\end{cases}}
$$

が成立する。特に **$g(G)\le3$**。**欠損二点型の数・形・最大次数に制限はない。** $D=K_k$（二点型が全欠損）も含む。独立側に孤立点が別途ある場合、その個数の偶奇を最後に xor する。

**閾値 $k\ge3$ は鋭い。** $k=2,(t_0,t_1)=(1,1),r_{01}=1$ は5頂点で真の $g=3$、式の予測 $0$。$k=1,t_0=2$ でも式は破れる。

## 証明

### 1. 有限基底 $k=3,4$

同じ非空近傍を持つ独立点は [K0336](../../../knowledge/items/K0336-independent-residual-twins-parity-compression.md) の正の偶奇縮約で、個数を1（奇数）または2（偶数）へ厳密に縮約できる。よって全私有葉正の条件では $t_i\in\{1,2\}$、各二点型は $r_{ij}\in\{0,1,2\}$ だけで十分。

$k=3$ は $2^3 3^3=216$ 構成、$k=4$ は $2^4 3^6=11,664$ 構成を、予測式を再帰内に使わない厳密 mex で完全列挙した。不一致はどちらも0。

検証器 verify_quotient.cpp はクリークの生存集合 $S$ ごとに再帰し、非孤立独立点数の偶奇 $u(S)$ を数える。クリーク点 $i\in S$ を選んだ子値は $u(S)\oplus z_i$。近傍型 $B$ の独立点を選んだ子値は $g(S\setminus B)\oplus(u(S)\oplus u(S\setminus B)\oplus1)$。各 $S$ でこれらの mex を直接取るため、予想式を再帰内部に仮定していない。

別実装 verify_named.py は実際の名前付き頂点を個別に生成し、閉近傍削除を直接再帰する。$k=3$ 全216構成、$k=4$ の固定96構成、$k=2$ の反例2構成で一致。$k=4$ 全11,664件を第二実装で再計算したわけではない。

### 2. 帰納段階 $k\ge5$

$k=3,4$ を基底とし、$k\ge5$ で $3\le k'<k$ の定理を仮定する。

クリーク点 $i$ を選ぶとクリークは全消去され、独立点のみが残る。そのGrundy値は $u\oplus z_i$。

独立点 $x$ を選び、そのクリーク近傍 $B$（$|B|=1$ または2）を消去する。生存クリークは $C\setminus B$、そのサイズは $k-|B|\ge3$。**各生存クリーク点は元の私有葉を少なくとも1個保つ**。したがって帰納仮定が使える。元の $z_i$ は生存点について不変である（消えた点に接続していた二点型は新たな私有葉となる）。

親の独立点数の偶奇を $u$、子で非孤立な独立点数の偶奇を $u'$ とする。選んだ点を除き新たに孤立する独立点の偶奇は $\delta=u\oplus u'\oplus1$。帰納仮定と孤立点の xor 則から、独立点初手の子値は

$$
\begin{cases}
u\oplus s & \text{生存 }z_i\text{ が一様 }s,\\
u\oplus3 & \text{生存 }z_i\text{ が混在}
\end{cases}
$$

となる。

親の $z_i$ が全て同じ $s$ なら、すべての初手の子値は $u\oplus s$。よって $\operatorname{mex}\{u\oplus s\}=1\oplus u\oplus s$。

親の $z_i$ が混在するなら、クリーク初手で0と1の両方が現れる。**人数の多い側の $z$ 値を持つクリーク頂点を1個選び、その私有葉を打つ。** $k\ge5$ なのでその側は少なくとも3点、少ない側は少なくとも1点であり、1点を消しても生存 $z$ は混在する。この子値は $u\oplus3$。他の子値は一様の場合の0/1か、混在の場合の $u\oplus3$ に限られる。従って $\operatorname{mex}\{0,1,u\oplus3\}=2+u$。帰納法が閉じる。

## 実行・検証結果

    c++ -std=c++17 -O3 -Wall -Wextra -pedantic research/experiments/game-structure/positive-private-leaves-arbitrary-missing-20261028/verify_quotient.cpp -o /tmp/positive_leaves
    /tmp/positive_leaves
    python3 research/experiments/game-structure/positive-private-leaves-arbitrary-missing-20261028/verify_named.py

出力（2026-10-28）：

    k=1 total=2 bad=1 maxGrundy=2
    k=2 total=12 bad=2 maxGrundy=3
    k=3 total=216 bad=0 maxGrundy=3
    k=4 total=11664 bad=0 maxGrundy=3
    PASS exhaustive bases k=3,4; sharpness k=1,2
    PASS literal k=3: 216 cases
    PASS literal k=4: 96 cases
    PASS total literal cases: 312; two k=2 sharpness witnesses

**証拠水準：** 既存の正の偶奇縮約の全称定理、2つの有限基底の完全列挙、数学的帰納法による計算機援用全称証明。$k=4$ の独立再計算は標本のみ。これは抽象分割グラフの Node Kayles に関する結論であり、整数格子の共円ゲームに全構成が実現するとは主張しない。11×11空盤勝敗への直接的な結論もない。

## 位置づけと次の課題

従来の最大欠損次数3（$k\ge6$）、$D=K_5\sqcup H$（$k\ge7$）の定理は、**私有葉数が0でもよい**点で依然として重要。今回の定理は、欠損の形を全く制限しない代わりに、全クリーク点に私有葉を要求する別方向の拡張である。

次は「私有葉のない頂点を高々1個許す」場合の閾値、または子局面で正の私有葉が自動生成される欠損条件を調べる。knowledge正本への昇格は、生成物の再構築・整合性検査を実行できる段階で行う。
