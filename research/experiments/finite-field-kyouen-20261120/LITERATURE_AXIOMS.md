# 文献調査（第6回）：反転平面の公理の完全確認

2026-11-20。`finite-field-kyouen-20261120` の第65部。
反転平面の公理を一次資料（チュートリアル）で確認し、我々の理解を完全に裏付けた。

## 1. 確認できた公理

出典：softmath.com の "Inversive Plane Geometry" チュートリアル

> An inversive plane is a geometry with three undefined notions: points,
> circles, and an incidence relation between points and circles, satisfying
> the following three axioms:
>
> **(I.1)** Through any three distinct points there is exactly one circle.
>
> **(I.2)** If P and Q are points, and C is a circle passing through P but not Q,
> then there is a unique circle C' passing through Q such that C ∩ C' = {P}.
>
> **(I.3)** There exist four points which do not lie on a common circle.

## 2. 我々の理解との照合

| 我々の主張 | 公理 | 整合 |
|---|---|---|
| 任意の三点が一意に円を定める | (I.1) | ✓ |
| 二円は高々2点で交わる | (I.2) の `C ∩ C' = {P}` | ✓ |
| 自明でない構造（4点が同一円上にない） | (I.3) | ✓ |

**すべての公理が我々の理解と一致する。**

## 3. 特に重要な点

### (I.1) が「全三点ブロック性」の根拠

前項で「任意の三点が同一円または同一直線上にある」が恒真だと結論したが、
これはまさに (I.1) である。

### (I.2) が「二円は高々2点で交わる」の根拠

層サイズ公式（k ≤ 5）の証明で使った「二円は高々2点で交わる」は (I.2) から従う。

### (I.3) が「自明でない」ことの保証

4点が同一円上にない点が存在するので、ゲームが自明にならない。

## 4. 空間模型の確認

> "A model of these axioms is provided by the points and circles lying on a
> sphere S in Euclidean 3-space."

球面上の円として実現できる。これは我々の「放物面上の cap」の見方と整合する。

また：

> "Another (obtained by stereographically projecting S onto a plane) is the
> extended Euclidean plane E = R² ∪ {∞}"

拡張ユークリッド平面（無限遠点を1つ加えたもの）も模型になる。
これは我々の「反転平面 = AG(2,q) + 無限遠点」の理解と整合する。

## 5. 有限模型について

> "Other models exist (in particular finite models) but we will be primarily
> concerned with the model E described above, called the real inversive plane."

有限模型の存在は言及されているが、詳細はこのチュートリアルにはない。

## 6. 意義

- 反転平面の公理 (I.1)(I.2)(I.3) を確認した。
- 我々が使ってきた性質（三点が一意に円を定める、二円は高々2点で交わる）が
  すべて公理から従うことを確認した。
- 空間模型（球面上の円、拡張ユークリッド平面）も我々の理解と整合する。
- **我々の基礎的な理解は文献と完全に整合している。**

## 7. 限界

- 有限反転平面の arc についての情報は得られなかった。
- 我々の K（3-arc の最大）が文献で扱われているかは依然として未確認。
- Sonnino の "arc" の定義も未確認。

## 8. 次の一手

- 有限反転平面の arc についての専門文献（Handbook of Combinatorial Designs など）
  を調査する。
- 我々の K 系列（5,5,6,6,7,9,9,10）を既知の系列と照合する。

## 9. 参考文献

- "Inversive Plane Geometry"（softmath.com チュートリアル）
  https://softmath.com/tutorials-3/cramer%E2%80%99s-rule/inversive-plane-geometry.html
- Wikipedia, "Möbius plane"
  https://en.wikipedia.org/wiki/M%C3%B6bius_plane
