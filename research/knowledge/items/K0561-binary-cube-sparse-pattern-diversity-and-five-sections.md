---
id: K0561
title: 二値超立方体の疎なq点切片の座標型閾値・第二指数項と5点切片の有限値
kind: proposition
status: proved
topics: [geometry, variants, statistics]
aliases: []
relations:
- type: depends_on
  target: K0559
  note: アフィン包に追加頂点がない集合を超平面切片へ拡張する補題、および3・4点公式との独立照合
artifacts:
- path: research/experiments/binary-cube-sparse-patterns-20261025/proof.md
  role: proof
  note: 任意固定qの鋭い座標型障害上界、最大障害型数、有限係数公式、第二指数項の全称証明
- path: research/experiments/binary-cube-sparse-patterns-20261025/support_enumerator.cpp
  role: verifier
  note: q3・4の全型集合、q5の型集合サイズ8以下を完全列挙する有限体上の厳密階数検査
- path: research/experiments/binary-cube-sparse-patterns-20261025/direct_integer_check.cpp
  role: verifier
  note: q5・d5/6の全5点組を整数の分数なし消去で独立に直接検査
- path: research/experiments/binary-cube-sparse-patterns-20261025/aggregate.py
  role: verifier
  note: 型集合数からのStirling数集計と既存q3・q4公式の回帰
- path: research/experiments/binary-cube-sparse-patterns-20261025/results.md
  role: data
  note: q5・d5..8の厳密有限値、独立整数検算、二素数による型集合全件照合
scope: 固定整数q>=3と全d>=qの二値超立方体の実超平面頂点切片。q5の具体的な有限値はd=5..8のみ。
evidence: 座標型と二非零係数の4通り判定による全称数学的証明。q3・q4の全型集合、q5のk<=8の型集合の有限完全列挙と、d5・d6の独立整数全5点組列挙で照合。
---

# 疎な超平面切片の座標型の鋭い閾値と5点切片

$V_d=\{0,1\}^d$、$E_{d,q}=\#\{H\cap V_d: H\text{ は実アフィン超平面},\ |H\cap V_d|=q\}$ とする。同じ頂点集合を与える異なる超平面は重複して数えない。

## 全称定理（全ての固定q）

$q\ge3$ 個の相異なる二値頂点を並べ、各座標に現れる $q$ ビット縦パターンの**異なる種類数**を $k$ とする。

$$
\boxed{k>3\cdot2^{q-2}\ \Longrightarrow\
\text{そのq頂点のアフィン包には追加二値頂点がない。}}
$$

閾値は最良であり、$k=3\cdot2^{q-2}$ で追加頂点を持つ最大障害型集合は、ちょうど $3\binom q3$ 種類ある。追加頂点は $z=x^{(i)}+x^{(j)}-x^{(k)}$ の型で生じる。

固定 $q$ について、$q$ 行が相異なり、そのアフィン包が二値頂点をちょうど $q$ 個含むような $k$ 元縦パターン集合の個数を $g_{q,k}$ と定める。全 $d\ge q$ で

$$
\boxed{E_{d,q}=\frac1{q!}\sum_{k=0}^{2^q}g_{q,k}\,k!\left\{\begin{matrix}d\\k\end{matrix}\right\}.}
$$

従って固定 $q$ では $E_{d,q}$ は $d\ge q$ で有限個の $j^d$ の有理係数線形結合になる。特に

$$
g_{q,k}=\binom{2^q}{k}\ (k>3\cdot2^{q-2}),\qquad
g_{q,3\cdot2^{q-2}}=\binom{2^q}{3\cdot2^{q-2}}-3\binom q3.
$$

さらに第二指数項まで全称的に確定した：

$$
\boxed{
E_{d,q}=\binom{2^d}{q}
-\frac{3\binom q3}{q!}\bigl(3\cdot2^{q-2}\bigr)^d
+O_q\bigl((3\cdot2^{q-2}-1)^d\bigr)
\quad(d\to\infty).
}
$$

特に $q=5$ は $E_{d,5}=\binom{2^d}{5}-24^d/4+O(23^d)$。これは漸近式であって全 $d$ の二項厳密公式ではない。


## 高次型係数の追加決定（5点版）

$q=5$ の座標型集合について、未確定だった係数のうち **$17\le k\le23$ を厳密に決定**した。$k>n$ のとき $\binom nk=0$ と約束すれば、既知の高次係数も含めて

$
\boxed{g_{5,k}=\binom{32}{k}-30\binom{24}{k}
+140\binom{20}{k}+135\binom{18}{k}
\qquad(17\le k\le32).}
$

従って5点切片の漸近式は次まで改善される。

$
\boxed{E_{d,5}=\binom{2^d}{5}-\frac14\,24^d
+\frac76\,20^d+\frac98\,18^d+O(16^d).}
$

非自明なアフィン係数で17型以上を許すものは、添字置換を除き $(1,1,-1,0,0)$（24型）と $(1,1,1,-1,-1)$（20型）だけであることを数学的に証明。これら40集合の2・3・4重交差を整数演算で完全検査し、包除原理で係数を得た。計算した交差表と検証器は既存の [証明](../../experiments/binary-cube-sparse-patterns-20261025/proof.md)・[結果](../../experiments/binary-cube-sparse-patterns-20261025/results.md)・aggregate.py に追記した。**$g_{5,9},\ldots,g_{5,16}$ はなお未確定**であり、全次元の短い厳密公式ではない。

## 5点切片の新しい厳密有限値

| d | E(d,5) | 根拠 |
|---:|---:|---|
| 5 | **2,592** | 型集合完全列挙、全201,376組の独立整数検査 |
| 6 | **256,704** | 型集合完全列挙、全7,624,512組の独立整数検査 |
| 7 | **18,778,368** | 型集合 $k\le7$ の完全列挙と全称集計式 |
| 8 | **1,133,185,536** | 型集合 $k\le8$ の完全列挙と全称集計式 |

$d=5$ は3平坦由来480・4平坦由来2112、$d=6$ は3平坦由来20160・4平坦由来236544。3平坦由来はK0551の全称式と一致する。

また、直接列挙していない大きな型集合についても**数学的証明**により $g_{5,24}=10,518,270$、$g_{5,k}=\binom{32}{k}$（$k\ge25$）と確定する。

[全称証明](../../experiments/binary-cube-sparse-patterns-20261025/proof.md)・[検算表と再現手順](../../experiments/binary-cube-sparse-patterns-20261025/results.md)。

**根拠と限界**：鋭い閾値・固定$q$係数公式・第二指数項は任意$q\ge3$の数学的証明。$d=5..8$ の5点数は有限完全列挙。$g_{5,9},\ldots,g_{5,16}$ は未確定であり、5点切片の全次元の簡潔な閉形式を得たとは主張しない。ゲームの勝敗・Grundy値や共超平面禁止5点組の総数は対象外。
