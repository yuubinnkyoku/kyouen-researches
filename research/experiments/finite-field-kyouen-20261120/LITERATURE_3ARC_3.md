# 文献調査（第3回）：arc の定義の確認と我々の K の位置づけ

2026-11-20。`finite-field-kyouen-20261120` の第61部。
反転平面の arc の定義を確認し、我々の K の位置づけを明確にした。

## 1. 得られた重要な記述

ICM 1998 のサーベイ（Documenta Mathematica, Extra Volume ICM 1998）の
検索結果要約から、次の記述が確認できた：

> "A k-arc of PG(2,q) is a set of k points of PG(2,q), no three of which are
> collinear. Then clearly k ≤ q+2. By Bose, 1947, for q odd, k ≤ q+1.
> Further, any nonsingular conic of PG(2,q) is a (q+1)-arc."
>
> "Let J be an inversive plane of order n ..."

つまり：
- **射影平面の k-arc** = 「どの3点も共線でない」集合（`k ≤ q+1`、q 奇数）
- 反転平面についても同様の arc 概念が定義されている（記述は途中で切れている）

## 2. 反転平面の arc の標準的定義（推定）

射影平面の類推から、反転平面の k-arc は

> **どの円も高々2点で交わる k 点集合**

と定義される可能性が高い。これは「**共円三点がない**」条件である。

## 3. 我々の条件との違い

| 概念 | 条件 | 我々の K との関係 |
|---|---|---|
| 反転平面の k-arc（推定） | どの円も高々2点（共円三点なし） | **我々より強い条件** |
| 我々の安全集合 | どの円も高々3点（共円四点なし） | より弱い条件 |

**我々の安全集合は「3-arc」に対応する**（3点まで許す）。

## 4. Sonnino の (q+5)-arc との整合性

もし Sonnino の arc が「共円三点なし」（k-arc）なら、サイズは我々の K より
**小さくなる**はずである。しかし `q+5` は我々の K より**大きい**。

**矛盾する。** したがって：
- Sonnino の arc の定義は「共円三点なし」ではない可能性がある。
- あるいは "inversive plane Ad(q)" が標準的な反転平面と異なる。
- あるいは検索結果の要約を誤解している。

**一次資料にアクセスできないため、確定できない。**

## 5. 我々の K の位置づけ（現時点）

- 我々の K は「反転平面で各円と高々3点で交わる集合の最大サイズ」。
- これは文献の "3-arc" または "cap" に対応する可能性がある。
- しかし文献の arc の定義を一次資料で確認できていない。
- **新規性は主張できない。**

## 6. 意義

- 射影平面の arc の標準的定義（共線三点なし）を確認した。
- 反転平面の arc も同様の類推で定義される可能性が高い。
- 我々の条件（共円四点なし）は arc より**弱い**条件であり、
  より大きな集合を許す。
- したがって我々の K は「3-arc」または「cap」に対応する。

## 7. 限界

- 一次資料（Springer の有料論文、PDF）にアクセスできていない。
- 反転平面の arc の定義を直接確認できていない。
- Sonnino の (q+5)-arc との不整合を説明できていない。
- 我々の K の新規性は未確定。

## 8. 次の一手

- アクセス可能な教科書・講義ノート（Hirschfeld の "Finite Projective Spaces of
  Three Dimensions"、Hartmann の "Planar Circle Geometries" など）で
  反転平面の arc の定義を確認する。
- 特に Hartmann の PDF（TU Darmstadt）は無料公開されているので、
  反転平面の章を確認する。

## 9. 参考文献

- Documenta Mathematica, Extra Volume ICM 1998（射影平面の arc の定義）
  https://ems.press/content/book-files/27293
- E. Hartmann, "Planar Circle Geometries"（TU Darmstadt、無料公開）
  https://www2.mathematik.tu-darmstadt.de/~ehartmann/circlegeom.pdf
- A. Sonnino, "Large k-arcs in inversive planes of odd order",
  Journal of Geometry 66 (1999), 187-191.
