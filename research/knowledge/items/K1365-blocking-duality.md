---
id: K1365
title: "共演ゲームとブロッキング集合の双対性 — 補集合で s-ゲームは t-重ブロッキング問題になる"
kind: proposition
status: proved
topics: [grundy, geometry, maximum-safe]
aliases:
- complement duality between safe sets and blocking sets
- s-game as a t-fold blocking set problem
relations:
- type: related
  target: K1364
  note: AG(2,5) s=4 の極大数 1,500/6,600/28,375 は最小ブロッキング集合の個数と一致
- type: related
  target: K1353
  note: 錐法（極大構造の計算に使う）
- type: related
  target: K1298
  note: パリティ定理（極大集合のサイズ）
artifacts:
- path: research/experiments/ag2q5-s4-20261128/output/ag2q5_s4_gsize.json
  role: data
  note: AG(2,5) s=4 の極大数（14:1,500, 15:6,600, 16:28,375）
- path: research/experiments/ag2q5-s4-20261128/independent/count_complements.c
  role: solver
  note: 補集合（ブロッキング集合）の全数列挙
scope: AG(2,q) または PG(2,q) の共演ゲーム（s-パラメータ）と、補集合の t-重ブロッキング集合との双対性。
evidence: 盤の直線サイズを l（AG は q、PG は q+1）とし、S を安全集合、C = P∖S をその補集合とすると、|S∩L| ≤ s ⇔ |C∩L| ≥ l−s が全直線で成り立つ。よって S は s-ゲームの安全集合であることと、C が t = l−s 重ブロッキング集合（各直線と少なくとも t 点で交わる）であることが同値。包含順序が反転するので、S が極大安全集合であることと C が極小 t-重ブロッキング集合であることも同値。したがって l = q の AG(2,q) では t = q−s、l = q+1 の PG(2,q) では t = q+1−s。s = q−1（AG）または s = q（PG）で t = 1 の通常のブロッキング集合になる。AG(2,5) s=4（q=5, t=1）では、最小ブロッキング集合のサイズ 9, 10, 11 の個数 28,375 / 6,600 / 1,500 が、極大安全集合のサイズ 16, 15, 14 の個数と一致する（K1364 の独立検証で全数確認）。
---

# 共演ゲームとブロッキング集合の双対性

盤の直線サイズを l（AG(2,q) は q、PG(2,q) は q+1）、S を安全集合、C = P∖S とする。

```
|S ∩ L| ≤ s  (∀L)  ⟺  |C ∩ L| ≥ l − s  (∀L)
```

すなわち **s-ゲームの安全集合は、t = l−s 重ブロッキング集合の補集合**である。
包含が反転するので、

```
S が極大安全集合  ⟺  C が極小 t-重ブロッキング集合
```

- AG(2,q): t = q−s。s = q−1 で通常のブロッキング集合（t=1）。
- PG(2,q): t = q+1−s。s = q で通常のブロッキング集合（t=1）。

## 応用（AG(2,5) s=4）

- q=5, s=4 → t=1: 安全集合の補集合は通常のブロッキング集合。
- 極大安全集合のサイズ 16, 15, 14 の個数 28,375 / 6,600 / 1,500 は、
  最小ブロッキング集合のサイズ 9, 10, 11 の個数と一致（K1364 の独立検証）。
- 最大安全サイズ 16 は「サイズ 9 のブロッキング集合が存在する」ことと同値。

## 意義

- s-ゲームの極大構造を、ブロッキング集合の古典的問題に帰着できる。
- 極大集合の個数・サイズの計算を、ブロッキング集合の列挙として独立に検証できる
  （K1364 の検証で実際に使用）。
- パリティ定理（K1298）と組み合わせると、極大集合のサイズの偶奇が
  ブロッキング集合のサイズの偶奇に翻訳される。
