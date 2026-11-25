# 文献調査（第2回）：Sonnino の (q+5)-arc と我々の K の比較

2026-11-20。`finite-field-kyouen-20261120` の第60部。
反転平面の arc についての文献調査を深め、重要な情報を得た。

## 1. 見つかった主要文献

### Sonnino, "Large k-arcs in inversive planes of odd order"

- Journal of Geometry, Volume 66, pages 187-191 (1999)
- 著者：Angelo Sonnino（Università della Basilicata）
- 検索結果の要約から読み取れた内容：
  - 「[7] で、任意の k と素数 p について、k-arc が inversive plane M(p^h) に
    存在することが示された（h が k に対して十分大きければ）」
  - 「本論文では、奇数の q に対して inversive plane Ad(q) における
    **(q+5)-arc の族**を構成する」

### Sonnino, "Complete arcs in inversive planes over prime fields"

- 素数位数 p の反転平面で arc を構成し、p が十分大きければ complete であることを示す。

## 2. 我々の K との比較

Sonnino の構成は **(q+5)-arc**、つまりサイズ `q+5` の arc が存在するというもの。

我々の計算結果（反転平面の最大安全サイズ）：

| q | 我々の K | q+5 |
|---:|---:|---:|
| 3 | 5 | 8 |
| 4 | 5 | 9 |
| 5 | 6 | 10 |
| 7 | 6 | 12 |
| 8 | 7 | 13 |
| 9 | 9 | 14 |
| 11 | 9 | 16 |
| 13 | 10 | 18 |

**我々の K は q+5 よりずっと小さい。**

## 3. 重大な不整合の可能性

もし Sonnino の (q+5)-arc が「どの円とも3点以下で交わる集合」なら、
我々の K ≥ q+5 となるはずだが、計算結果は K < q+5。

**考えられる説明**：

1. **arc の定義が異なる**：Sonnino の "arc" は「どの円とも3点以下」ではなく、
   別の条件（例えば「どの3点も同一円上にない」= 3点が一意に円を定めることの否定、
   つまり「共円三点がない」）かもしれない。

2. **我々の計算が誤っている**：可能性は低い（完全探索で検証済み）。

3. **"inversive plane Ad(q)" が標準的な反転平面と異なる**：別の構造かもしれない。

## 4. 定義の確認が必要

反転平面の文脈での "k-arc" の標準的な定義は：

> **k-arc**：どの円も高々2点で交わる k 点集合

もしそうなら、これは「共円三点がない」条件であり、我々の「共円四点がない」より**強い**。
その場合、k-arc のサイズは我々の K より小さくなるはずで、`q+5` は矛盾する。

一方、我々の条件（共円四点がない）に対応するのは **3-arc** かもしれない。

**この定義の違いを確認しないと、文献との比較はできない。**

## 5. 現時点の結論

- Sonnino の (q+5)-arc と我々の K は**直接比較できない**（arc の定義が未確認）。
- 我々の K の系列（5,5,6,6,7,9,9,10）が既知の結果と一致するかは**未確定**。
- 定義の確認が最優先課題。

## 6. 限界

- Springer の有料論文に直接アクセスできず、要約のみから推測している。
- arc の定義を一次資料で確認できていない。
- 我々の K の新規性は主張できない。

## 7. 次の一手

- 反転平面の arc の標準的定義を、アクセス可能な資料
  （arXiv、Handbook of Combinatorial Designs の抜粋、講義ノート）で確認する。
- 特に「k-arc」「3-arc」「cap」の区別を明確にする。
- 定義を確認した上で、我々の K と既知の結果を照合する。

## 8. 参考文献

- A. Sonnino, "Large k-arcs in inversive planes of odd order",
  Journal of Geometry 66 (1999), 187-191.
  https://link.springer.com/article/10.1007/BF01225681
- A. Sonnino, "Complete arcs in inversive planes over prime fields".
- A. Sonnino, "k-archi nei piani di Benz", Note Mat. 15 (1995), 111-119.
- A. Sonnino, "Linear collineation groups preserving an arc in a Möbius plane",
  Proceedings of the 16th British Combinatorial Conference, London 1997.
