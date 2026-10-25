---
id: K0565
title: 二値超立方体の六点切片の高次座標型係数と四項指数補正
kind: proposition
status: proved
topics: [geometry, variants, statistics]
aliases: []
relations:
- type: depends_on
  target: K0561
  note: 座標型計数とアフィン包による切片判定を利用
artifacts:
- path: research/experiments/binary-cube-six-high-patterns-20261025/proof.md
  role: proof
  note: 33型以上の障害完全分類・包除原理・漸近式の証明
- path: research/experiments/binary-cube-six-high-patterns-20261025/verify.py
  role: verifier
  note: 120障害集合の完全包除と独立メビウス反転による全係数照合
- path: research/experiments/binary-cube-six-high-patterns-20261025/direct_check.py
  role: verifier
  note: 有理数行列消去による58例の独立標本検算
scope: 二値超立方体の6頂点超平面切片。座標型数33以上の全係数、dが無限大に向かう際の指数補正、およびd=4..7の厳密有限計数。
evidence: 大きさ32超の障害を支持数3・5の120集合に全称分類し、交差集合2806個を2方式の整数完全計数で検証。58例の独立有理数検算。
---

# 六点超平面切片の高次係数

既存K0561の g_{q,k}, E_{d,q} の定義を用いる。**全ての整数33<=k<=64**で

$$
\boxed{g_{6,k}=\binom{64}{k}-60\binom{48}{k}
+390\binom{40}{k}+900\binom{36}{k}+255\binom{34}{k}.}
$$

さらに、d→∞ で

$$
\boxed{E_{d,6}=\binom{2^d}{6}-\frac1{12}48^d
+\frac{13}{24}40^d+\frac54 36^d+\frac{17}{48}34^d
+O(32^d).}
$$

**全称性の根拠**：座標型を32種類より多く許す追加頂点のアフィン係数は、単位ベクトルを除き、支持数3の (1,1,-1) または支持数5の (1,1,1,-1,-1) に限られる。それぞれ60集合で、計120集合の交差を32型より大きい範囲で完全に数えた。2,806個の交差集合の包除係数を、逐次包除と包含順序のメビウス反転の独立2方式で一致確認した。

**証拠の境界**：上の g_{6,k} は有限完全計数に帰着した全称定理。E_{d,6} は漸近式であって、有限dでの厳密な等式ではない。k<=32 の係数は未確定。追加の58例は有理数計算による独立標本検算であり、完全性の根拠ではない。

詳細：[全称証明](../../experiments/binary-cube-six-high-patterns-20261025/proof.md)、[完全計数器](../../experiments/binary-cube-six-high-patterns-20261025/verify.py)、[独立有理数検算](../../experiments/binary-cube-six-high-patterns-20261025/direct_check.py)。

## 有限完全列挙による6点切片の4〜7次元（追加）

原点固定の全6点候補を完全列挙し、整数行基本変形と素数1009上の独立計算を照合した結果、**d=4,5,6,7に限り**次の値を厳密に決定した。

| d | 原点を含む有効な6点集合 N_{d,6} | E_{d,6} | v_2(E_{d,6}) |
|---:|---:|---:|---:|
| 4 | 15 | **40** | 3 |
| 5 | 225 | **1,200** | 4 |
| 6 | 19,362 | **206,528** | 6 |
| 7 | 2,244,606 | **47,884,928** | 7 |

K0567の恒等式 `6E_{d,6}=2^d N_{d,6}` を使用。d=4..6は原点以外の5頂点の直接完全列挙と座標型多重集合の重み付き完全列挙が一致し、d=7は後者の全12,620,256多重集合を整数・有限体の2方式で検査した。有限体1009による判定は、必要な6次以下の0/1小行列式が絶対値216以下であることから有理数上の判定と厳密に一致する。

これは**有限次元の完全計算**であって、全次元の6点切片閉形式ではない。d=6,7では一般可除性下界 `v_2(E_{d,6})>=d-1` が鋭くなく、d=4,5では鋭い。d>=8は未確定。

[完全計数・証拠境界・再現手順](../../experiments/binary-cube-six-census-20261025/results.md) / [独立検証器](../../experiments/binary-cube-six-census-20261025/q6_census.cpp)。
