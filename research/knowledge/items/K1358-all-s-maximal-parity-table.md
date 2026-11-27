---
id: K1358
title: "全 s 盤の極大パリティ × 最大 Grundy 表 — パリティ一様なら最大 1、混在なら 2 以上"
kind: computation
status: computed
topics: [grundy, statistics]
aliases:
- maximal parity vs maximum Grundy across computed boards
- cross-s Grundy ceiling table
relations:
- type: related
  target: K1357
  note: s=3 盤の同様の表
- type: related
  target: K1298
  note: パリティ特性定理（一様 ⇔ 0/1、混在 ⇒ ≥2）
- type: related
  target: K1354
  note: AG(2,9) s=2（極大 6-10 混在、最大 3）
- type: related
  target: K1300
  note: s-パラメータ表
artifacts:
- path: research/experiments/s-parameter-kyouen-20261125/output/grundy_general.json
  role: data
  note: AG(2,x) s=2/3、W_22 s=5、W_24 s=5/6 など
- path: research/experiments/ag2q9-cap-game-20261128/output/ag2q9_spectrum.json
  role: data
  note: AG(2,9) s=2（極大 6-10 混在、最大 G=3）
- path: research/experiments/pg2q9-cap-game-20261125/output/census_pg2q9.txt
  role: data
  note: PG(2,9) s=2 の極大
- path: research/experiments/design-kyouen-witt-20261125/output/grundy_w24_s7.txt
  role: data
  note: W_24 s=7（極大 12,13 混在、最大 2）
scope: 計算済みの共演ゲーム（s=2..7）における極大安全集合のサイズ・パリティと、Grundy 値の最大の関係の総括表。
evidence: 各盤のデータより極大サイズと Grundy 分布を整理。偶数または奇数一様の盤（PG(2,2)-PG(2,8), AG(2,8), W_24 s=5,6 など）は最大 Grundy 1（K1298 の十分条件）。混在盤は最大 2 以上で、PG(2,9) s=2 は 2、AG(2,5)/AG(2,7) s=2 は 2、AG(2,9) s=2 は 3（極大 6,7,8,9,10）、AG(2,4) s=3 は 2、AG(2,5)/PG(2,5) s=3 は 4（極大 9,10,11）、PG(2,4) s=4 は 3（極大 12,13,14,16）、W_22 s=5 は 3（極大 11,12,15）、W_24 s=7 は 2（極大 12,13）。最大 Grundy はパリティ一様性では 1/2 以上に分かれるが、混在盤の上限は盤依存（2,3,4）。
---

# 全 s 盤の極大パリティ × 最大 Grundy

| 盤 | s | 極大サイズ | パリティ | 最大 G |
|---|---:|---|---|---:|
| PG(2,9) | 2 | 6,7,8,10 | 混在 | 2 |
| AG(2,5) | 2 | 5,6 | 混在 | 2 |
| AG(2,7) | 2 | 6,7,8 | 混在 | 2 |
| AG(2,9) | 2 | 6,7,8,9,10 | 混在 | 3 |
| PG(2,3) | 3 | 7,9 | 奇数一様 | 1 |
| PG(2,4) | 3 | 7,9 | 奇数一様 | 1 |
| AG(2,4) | 3 | 8,9 | 混在 | 2 |
| AG(2,5) | 3 | 9,10,11 | 混在 | 4 |
| PG(2,5) | 3 | 9,10,11 | 混在 | 4 |
| PG(2,4) | 4 | 12,13,14,16 | 混在 | 3 |
| W_22 | 5 | 11,12,15 | 混在 | 3 |
| W_24 | 5 | 6 | 偶数一様 | 1 |
| W_24 | 6 | 12 | 偶数一様 | 1 |
| W_24 | 7 | 12,13 | 混在 | 2 |

- **パリティ一様な盤は最大 Grundy 1**（K1298 の十分条件）。
- **混在盤は最大 2 以上**（定理の必要性）。上限は盤依存（2, 3, 4）。
- 混在の「幅」（極大サイズの種類数）と最大 Grundy は単純比例しない
  （AG(2,4) s=3 は 8,9 で最大 2、AG(2,5) s=3 は 9,10,11 で最大 4）。
