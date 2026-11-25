# 2026-11-23 文献調査：反転平面の弧（上界は未発表、我々の結果は新規）

サブエージェントに web 調査を依頼した結果のまとめ（全文は届いた報告に基づく）。

## 用語の確認

反転平面 `M(q)` の「弧（arc / k-arc）」＝**どの4点も同一円上にない k 点集合**。
Sonnino 1999 の要旨原文：
> "An arc of size k (briefly: a k-arc) in an inversive plane is defined as a set consisting of
> k points no four of which lie on the same circle."

（zbMATH のレビューに「no three」と書いたものがあるが、これは誤り。）

## 下界（文献の最良）

**A. Sonnino, "Large k-arcs in inversive planes of odd order", J. Geom. 66 (1999) 187–191**
（DOI 10.1007/BF01225681）
- 要旨原文："An infinite family of large k-arcs in the inversive plane M(q) over a finite field
  GF(q), with q ≡ 1 (mod 3), q ≥ 71 or q ∈ {17,23,27,29,41,47,49,53,59} is constructed."
- 本文スニペット："we shall construct a family of ½(q+5)-arcs in the inversive plane M(q) with q odd.
  These arcs turn out to be complete for q > 71 or q ∈ {17,23,27,29,41,47,53,59}."
- したがって **`K(q) ≥ (q+5)/2`（q 奇数）** が文献の記録。
  仮定（`q ≡ 1 mod 3` vs 全奇数）は要旨と本文で食い違っており**未確定**（flag）。
- zbMATH レビューには `1/3(q+5)` と書いたものがあるが誤植（(q+5)/3 は q=17,23,… で整数でない）。

**後年の Hadnagy–Sonnino, Discrete Math. 255 (2002) 181–188** は
素数位数で **≈(p+17)/4** の complete arc を構成するもので、`(q+5)/2` より**小さい**。
よって `(q+5)/2` が現在の文献最良で、我々の検証済み下界（q=13..49 で +1〜+5）は改善になっている。

## 上界：**文献に存在しない**

zbMATH（レビュー全文）・OpenAlex・Crossref・Springer・ScienceDirect・arXiv・EuDML を検索した限り、
**反転平面の弧の上界（`k ≤ q`, `q+1`, `q+2` など）を述べた論文はない**（奇数・偶数を問わず）。
唯一の材料は**ambient な PG(3,q) の理論**：

- J. W. P. Hirschfeld & L. Storme, "The packing problem in statistics, coding theory and finite
  projective spaces: update 2001", Table 3.1：`q` 奇数 `> 3` で `m(3,q) = q+1` かつ
  `(q+1)`-アークは normal rational curve（Segre 1955）。`q = 2^h ≥ 8` でも `m(3,q) = q+1`。
- ここで PG(3,q) の「n-arc」＝どの4点も同一平面上にない集合（＝我々の Q⁻ 上の弧の ambient 版）
  なので、ただちに **`K(q) ≤ q+1`（q 奇数 > 3、および q = 2^h ≥ 8）**。
  これは K1252 の一段目（射影上界から q+1）と同じ結論を文献から与える。

⇒ **`K(q) ≤ q`（q 奇数, q≥9）は文献にない**。K1252 の結果は新規と考えられる。

## 偶数 q：文献に何もない

Sonnino の一連の論文はすべて奇数位数。偶数位数（Miquelian および Suzuki–Tits ovoid 由来）に
ついては構成も上界も小さい q のデータも見つからず。背景：偶数位数の反転平面はすべて egglike
（Dembowski 1964）。

## 小さい q の厳密値：表もない

印刷された表は存在しない。文献にあるのは構成からの下界
（`K(3)≥4, K(5)≥5, K(7)≥6, K(9)≥7`）だけ。→ 我々の `K(3..9)` の厳密値は新規。

## MDS 対応

PG(3,q) 側の古典的対応は既知：Storme–Thas, J. Combin. Theory Ser. A 62 (1993) 139–154
"It is well known that k-arcs in PG(n,q) and linear MDS codes of dimension n+1 and length k
over GF(q) are equivalent objects."
**我々の「Q⁻ 上の弧＝楕円二次曲面上に列を持つ MDS 符号の最大長」という制限版の同定は
文献に見当たらない**（K1250 の新規性の根拠）。

## 調査で確認できなかったこと

- Sonnino 1999 と Hadnagy–Sonnino 2002 の全文（有料）。要旨・レビュー・索引 PDF の断片のみ。
- `(q+5)/2` 構成の適用範囲が全奇数 q か `q ≡ 1 (mod 3)` か。

## 反映先

- K1251（文献節の拡充、下界の位置づけ、我々の改善の明示）
- K1252（「先行研究の可能性」節を「文献には上界がない」に更新）
