# 文献調査（第4回）：反転平面の定義の確認

2026-11-20。`finite-field-kyouen-20261120` の第62部。
Wikipedia の Möbius plane の記事で反転平面の定義を確認した。

## 1. 確認できた定義

### 反転平面（Möbius plane）の公理

Wikipedia（Möbius plane）から：

> An incidence structure 𝔐 = (𝒫, 𝒵, ∈) with point set 𝒫 and cycle set 𝒵 is a
> Möbius plane if:
> - **(A1)** For any three points A, B, C there is exactly one cycle z
>   containing A, B, C.
> - **(A2)** For any cycle z, any point P ∈ z and Q ∉ z there exists exactly one
>   cycle z' with P, Q ∈ z' and z ∩ z' = {P} (touching).

**これは我々が使っている 3-(q²+1, q+1, 1) 設計の定義と一致する。**

### 重要な記述：任意の三点が一意に円を定める

> "For any set of three points A,B,C there is exactly one cycle z which contains
> A,B,C."

**これが我々の「全三点ブロック性が恒真」の根拠である。**
反転平面の公理 (A1) そのものである。

### 空間模型

> "The classical real Möbius plane can be considered as the geometry of circles
> on the unit sphere."

球面上の円として実現できる。これは我々の「放物面上の cap」の見方と整合する。

### 有限 Möbius 平面

記事には "Finite Möbius planes and block designs" の節があるが、
内容は取得できなかった（truncated）。

## 2. 我々の結果との整合性

| 我々の主張 | 文献の裏付け |
|---|---|
| 反転平面は 3-(q²+1, q+1, 1) 設計 | (A1) そのもの |
| 任意の三点が一意に円を定める | (A1) そのもの |
| 各円は q+1 点 | 設計のパラメータ |
| 二円は高々2点で交わる | (A2) の touching の議論から |

**我々の基礎的な理解は文献と一致している。**

## 3. arc の定義について

Wikipedia の記事には arc の定義は見つからなかった。
"Finite Möbius planes and block designs" の節に含まれている可能性があるが、
取得できなかった。

## 4. Sonnino の (q+5)-arc との不整合（未解決）

前項で見つけた不整合：

- Sonnino は奇数の q に対して (q+5)-arc を構成
- 我々の K（各円と高々3点）は q+5 より小さい

**この不整合は未解決である。** 考えられる説明：
1. Sonnino の arc の定義が「各円と高々3点」ではない
2. "inversive plane Ad(q)" が標準的でない
3. 検索結果の要約を誤解している

## 5. 意義

- 反転平面の公理 (A1) が「任意の三点が一意に円を定める」ことを確認した。
- これは我々の「全三点ブロック性が恒真」の根拠であり、文献と整合する。
- 空間模型（球面上の円）は我々の「放物面上の cap」の見方と整合する。
- arc の定義は未確認。

## 6. 限界

- Wikipedia の記事は "Finite Möbius planes and block designs" の節が取得できなかった。
- arc の定義を一次資料で確認できていない。
- Sonnino の不整合は未解決。

## 7. 参考文献

- Wikipedia, "Möbius plane"
  https://en.wikipedia.org/wiki/M%C3%B6bius_plane
- A. Sonnino, "Large k-arcs in inversive planes of odd order",
  Journal of Geometry 66 (1999), 187-191.
