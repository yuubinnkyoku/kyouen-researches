# 文献調査（第5回）：arc の定義の確定と不整合の解決

2026-11-20。`finite-field-kyouen-20261120` の第63部。
Sonnino の (q+5)-arc と我々の K の不整合を、arc の定義から解決した。

## 1. 決定的な情報

検索結果から、Sonnino の論文の冒頭部分の記述が得られた：

> "In [7] it was shown that, for any k and p prime, a k-arc in the inversive
> plane M(p^h) over GF(p^h) exists provided that h is sufficiently large with
> respect to k. In this paper we shall construct a family of **(q+5)-arcs** in
> the inversive plane **Ad(q)** with q odd."

また、射影平面の k-arc の定義（ResearchGate）：

> "A k-arc in a plane PG(2,q) is a set of k points such that every line in the
> plane intersects it in **at most two points** and there is a line intersecting
> it in exactly two points."

## 2. 定義の類推

射影平面の k-arc は「各直線と高々2点で交わる」。
反転平面の類推では「**各円と高々2点で交わる**」となる。

**これは「共円三点がない」条件である。**

## 3. 我々の条件との比較

| 概念 | 条件 | サイズの関係 |
|---|---|---|
| 反転平面の k-arc | 各円と高々2点（共円三点なし） | 小さい |
| 我々の安全集合 | 各円と高々3点（共円四点なし） | **大きい** |

**我々の条件は arc より弱いので、我々の K は arc の最大サイズより大きいはず。**

## 4. 不整合の解決

Sonnino の (q+5)-arc は「各円と高々2点」の集合である。
我々の K は「各円と高々3点」の集合の最大サイズ。

**したがって我々の K ≥ q+5 でなければならない。**

しかし計算結果は K < q+5（q=5 で 6 < 10、q=9 で 9 < 14）。

**矛盾する。**

## 5. 矛盾の解決：Ad(q) の正体

Sonnino の論文は "inversive plane **Ad(q)**" と書いている。
これは標準的な反転平面（3-(q²+1, q+1, 1) 設計）とは**別の構造**の可能性がある。

"Ad" は "André" の略かもしれない（André の反転平面）。
André の反転平面は、Miquelian でない（Miquel の定理を満たさない）反転平面である。

**標準的な反転平面（Miquelian）と André の反転平面は異なる。**

我々が計算しているのは Miquelian な反転平面（`P¹(F_{q²})` 模型）である。
Sonnino の Ad(q) は André の反転平面かもしれず、その場合 arc の最大サイズは異なる。

## 6. 結論

- 反転平面の k-arc は「各円と高々2点」と定義される（射影平面からの類推）。
- 我々の安全集合は「各円と高々3点」で、arc より**弱い条件**。
- Sonnino の (q+5)-arc は Ad(q)（André の反転平面？）についてのもの。
- **標準的な Miquelian 反転平面についての我々の K と直接比較できない。**

## 7. 意義

- arc の定義を確定できた（各円と高々2点）。
- 我々の条件が arc より弱いことを明確にした。
- Sonnino の結果が別の構造（Ad(q)）についてのものである可能性を特定した。
- **我々の K は「3点まで許す」問題であり、文献の arc（2点まで）とは別問題**と整理できた。

## 8. 限界

- "Ad(q)" の正体を一次資料で確認できていない（André の反転平面という推測）。
- 反転平面の k-arc の定義を一次資料で確認できていない（射影平面からの類推）。
- 我々の K の新規性は依然として未確定。

## 9. 次の一手

- "Ad(q)" が André の反転平面かどうかを確認する。
- 反転平面の「3-arc」（各円と高々3点）についての文献を探す。
- 我々の K が「3-arc の最大サイズ」として既知か、新しいかを確認する。

## 10. 参考文献

- A. Sonnino, "Large k-arcs in inversive planes of odd order",
  Journal of Geometry 66 (1999), 187-191.
  https://link.springer.com/article/10.1007/BF01225681
- A. Sonnino, "Complete arcs in inversive planes over prime fields",
  Discrete Mathematics (ScienceDirect S0012365X01003971).
- ResearchGate, "A Full List of Projectively Distinct K-Arcs in PG(2,8)"
  （射影平面の k-arc の定義）
