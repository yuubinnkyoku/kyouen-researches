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
scope: 二値超立方体の6頂点超平面切片。座標型数33以上の全係数と、dが無限大に向かう際の指数補正。
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
