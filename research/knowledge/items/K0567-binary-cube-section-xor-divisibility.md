---
id: K0567
title: 二値超立方体の座標反転軌道による切片数の2進可除性と3・5点切片の厳密合同則
kind: proposition
status: proved
topics: [geometry, variants, statistics]
aliases: []
relations:
- type: depends_on
  target: K0559
  note: 3点切片の全次元指数公式から正確な2進付値を導出
- type: depends_on
  target: K0561
  note: 5点切片の全次元指数公式とアフィン包の切片延長補題を使用
artifacts:
- path: research/experiments/binary-cube-xor-orbits-20261025/proof.md
  role: proof
  note: 全qの軌道可除性、原点固定計数、3・5点切片の2進合同則の全称証明
- path: research/experiments/binary-cube-xor-orbits-20261025/verify_rooted.cpp
  role: verifier
  note: d=5,6の原点を含む全5点組の独立有限体完全列挙
- path: research/experiments/binary-cube-xor-orbits-20261025/verify_congruences.py
  role: verifier
  note: 既存指数公式によるd<=64の厳密整数検算と偶数qの有限値回帰
scope: 全次元dと全qの二値超立方体における座標反転不変q点集合族。特に超平面切片E_{d,q}とq=3,5の2進付値。
evidence: 座標反転群の軌道安定化群定理と二重計数による全称証明。3点・5点の追加合同則は既存全次元厳密公式を法8・16で評価。d=5,6の独立原点固定全列挙とd<=64の整数検算。
---

# 座標反転で得られる全qの可除性

`V_d={0,1}^d` とし、`E_{d,q}` は `q` 頂点をちょうど含む実アフィン超平面切片の**異なる頂点集合**の数とする（K0561）。

**全称定理：** 座標反転 `x -> x xor t` で不変な任意の `q` 点集合族 `F` について

$$
\boxed{2^{\max(0,d-v_2(q))}\mid |F|.}
$$

従って超平面切片数も

$$
\boxed{2^{\max(0,d-v_2(q))}\mid E_{d,q}.}
$$

特に `q` が奇数なら `2^d | E_{d,q}`。これは全称的な**算術的必要条件**であり、各 `E_{d,q}` の値自体を求める式ではない。

**原点固定計数：** `F` に属する集合のうち原点 `0^d` を含むものを `N_{d,q}` 個とすると、全 `q` について

$$
\boxed{q|F|=2^d N_{d,q}.}
$$

奇数 `q` なら `q\mid N_{d,q}`。原点を含む候補だけを列挙して全切片数を復元でき、独立した整数性検査にもなる。

## 3点・5点のより強い合同則

既存K0559の3点切片公式から、**全 `d>=3`** で

$$
\boxed{
v_2(E_{d,3})=
\begin{cases}
d& d\text{ が奇数},\\
d+1& d\text{ が偶数}.
\end{cases}}
$$

既存K0561の5点切片公式から、**全 `d>=5`** で

$$
\boxed{
\frac{E_{d,5}}{2^d}\equiv
\begin{cases}
1\pmod 2&d\equiv1,2\pmod4,\\
0\pmod 2&d\equiv0,3\pmod4.
\end{cases}}
$$

従って5点では `d≡1,2 (mod4)` の場合に一般可除性が**ちょうど鋭く**、残る剰余類ではもう一段階2で割れる。


## 偶数点数 q=2,4 での可除性の鋭さ

既存K0559の全次元閉形式を使うと、**全 d>=2** で

$
\boxed{v_2(E_{d,2})=d-1}
$

が成立する。また、**全 d>=3** で

$
\boxed{v_2(E_{d,4})=
\begin{cases}
d-1 & d\text{ が奇数},\\
d-2 & d\text{ が偶数}.
\end{cases}}
$

したがって座標反転軌道からの一般下界 d-v_2(q) は、q=2 では全 d>=2、q=4 では偶数 d>=4 で**ちょうど鋭い**。一方 q=4 で奇数 d の場合は追加の2因子が必ず現れる。

q=2 は E_{d,2}=2^{d-1}(2^d-1) による。q=4 では既存K0559の公式から 24E_{d,4}/2^d を作り、法8で評価する。偶数底の寄与は d>=3 で消え、残りは 30*5^d+27*3^d+5 となる。これは奇数 d で4、偶数 d で6に合同であり、正確な2進付値が従う。

この証明は既存の全次元閉形式に依存する**全称証明**であり、d=3..5の独立アフィン階数完全列挙とd=3..64の整数検算は補助的な検証である。検証コードは既存の verify_congruences.py に追加した。

## 独立検算

有限体101上の直接アフィン階数検査で、原点を含む全5点集合を調べた。

| d | 原点を含む全5点候補 | 追加二値頂点のない候補 | 復元したE_{d,5} |
|---:|---:|---:|---:|
| 5 | 31,465 | 405 | 2,592 |
| 6 | 595,665 | 20,055 | 256,704 |

2方式の独立性：この直接検査はK0561の指数係数・包除原理を使用しない。別の `verify_congruences.py` は既存の厳密指数公式から `d<=64` の合同則を整数演算で検算した。

**根拠と限界：** 可除性・原点固定式・合同則は全称数学的証明。表は有限完全列挙、`d<=64` の検査は回帰である。一般の偶数 `q` に対して可除性の下界が常に鋭いとは主張しない。標準整数格子の共円ゲームへの同一群作用は主張しない。

[全称証明](../../experiments/binary-cube-xor-orbits-20261025/proof.md)・[原点固定検証器](../../experiments/binary-cube-xor-orbits-20261025/verify_rooted.cpp)・[合同則検算](../../experiments/binary-cube-xor-orbits-20261025/verify_congruences.py)。
