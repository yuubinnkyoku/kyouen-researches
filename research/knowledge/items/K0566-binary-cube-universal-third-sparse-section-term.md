---
id: K0566
title: 二値超立方体の任意q点切片における第三指数項の全称公式
kind: proposition
status: proved
topics: [geometry, variants, statistics]
aliases: []
relations:
- type: depends_on
  target: K0561
  note: 疎なq点切片・座標型係数の定義とアフィン包による判定を利用
artifacts:
- path: research/experiments/binary-cube-universal-third-term-20261025/proof.md
  role: proof
  note: 全qの障害支持数分類、包除原理、高々10座標への有限帰着
- path: research/experiments/binary-cube-universal-third-term-20261025/verify.py
  role: verifier
  note: 全A3三重交差・A3/B5交差・B5二重交差と四座標の一意性を完全列挙
- path: research/experiments/binary-cube-universal-third-term-20261025/independent_check.py
  role: verifier
  note: q=4,5,6の第三係数をビット集合とは独立の集合列挙で照合
scope: 固定整数q>=4、全d>=qの二値超立方体のちょうどq頂点の実超平面切片。全qの高次型係数と第三指数項。
evidence: 障害の全称支持数分類と最大10座標の有限完全列挙を組み合わせた数学的証明。q=4,5,6の既存独立公式と照合。
---

# 任意のqで第三指数項まで確定

K0561 の定義による E_{d,q}（同じ頂点集合を重複して数えない）と
g_{q,k} について、**任意の整数 q>=4** に対して

$$
\boxed{g_{q,k}=\binom{2^q}{k}
-3\binom q3\binom{3\cdot2^{q-2}}k
+\left(30\binom q4-10\binom q5\right)
\binom{5\cdot2^{q-3}}k
\quad(k>9\cdot2^{q-4}).}
$$

従って固定 q で d→∞ とすると

$$
\boxed{E_{d,q}=\binom{2^d}{q}
-\frac{3\binom q3}{q!}(3\cdot2^{q-2})^d
+\frac{30\binom q4-10\binom q5}{q!}(5\cdot2^{q-3})^d
+O_q((9\cdot2^{q-4})^d).}
$$

第三指数項の分子係数は q=4,5,6 でそれぞれ
30,140,390。既存 K0559・K0561・K0565 の特殊例と一致する。

**全称性の根拠**：9/16 より大きい許容縦パターン集合を持つ
非自明なアフィン係数は支持数3の (1,1,-1) と
支持数5の (1,1,1,-1,-1) のみ。
前者の二重交差で密度5/8となるものは
30*C(q,4) 個で、互いに異なる。
その他の三重交差・混合交差・後者の二重交差は
密度9/16以下となる。後半の境界は支持座標数最大10への
厳密な帰着と、全組合せの整数完全列挙で確定した。

**限界**：g の等式は表示した k の範囲でのみ厳密。
E の式は漸近式であり有限 d の完全閉形式ではない。
9/16 以下の型係数、ゲームの勝敗・Grundy値は未解決のまま。

[証明](../../experiments/binary-cube-universal-third-term-20261025/proof.md)・
[完全検証器](../../experiments/binary-cube-universal-third-term-20261025/verify.py)。
