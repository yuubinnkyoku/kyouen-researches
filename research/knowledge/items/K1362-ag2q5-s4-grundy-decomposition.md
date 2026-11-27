---
id: K1362
title: "AG(2,5) s=4 の Grundy サイズ別完全分解 — 全 16,249,926 局面、最大 G=3"
kind: computation
status: computed
topics: [grundy, geometry]
aliases:
- size-by-size Grundy table of the AG(2,5) s=4 game
- largest s=4 decomposition computed (16M positions)
relations:
- type: related
  target: K1361
  note: PG(2,5) s=3 のサイズ別分解（K1361）（同程度の規模）
- type: related
  target: K1358
  note: 極大パリティ × 最大 Grundy 表
- type: related
  target: K1300
  note: s-パラメータ盤の系列
artifacts:
- path: research/experiments/ag2q5-s4-20261128/output/gsize_ag2q5_s4.txt
  role: data
  note: エンジン出力（SIZE/GRUNDY/GSIZE 行）
- path: research/experiments/ag2q5-s4-20261128/output/ag2q5_s4_gsize.json
  role: data
  note: サイズ別 Grundy 分布の JSON
- path: research/experiments/pg2q7-cap-game-20261125/scripts/grundy_s_stats.c
  role: solver
  note: s パラメータ付き Grundy 計算器（GSIZE 出力）
- path: research/experiments/ag2q5-s4-20261128/README.md
  role: log
  note: 結果と再現手順
scope: AG(2,5)（25 点、30 直線、各 5 点）の s=4 共演ゲーム全 16,249,926 局面の Grundy 値のサイズ別完全分解。
evidence: grundy_s_stats を board_ag2q5.txt s=4 で実行し GSIZE 行を取得。サイズ別の和は SIZE 行、Grundy 別合計は GRUNDY 行 {0:7,967,001, 1:7,919,925, 2:159,000, 3:204,000} と完全一致（総数 16,249,926 = SAFE）。k=0..10 は偶数 G0・奇数 G1 のパリティ則。k=11 で G3 72,000、k=12 で G2 72,000、k=13 で G2 6,000+G3 132,000、k=14 で G2 81,000、k=15 で G1、k=16 は全 28,375 が G0（極大）。極大サイズは 14 (1,500), 15 (6,600), 16 (28,375)。
---

# AG(2,5) s=4 のサイズ別 Grundy 完全分解

| k | 個数 | 極大 | G 分布 |
|---:|---:|---:|---|
| 0 | 1 | 0 | G0: 1 |
| 1 | 25 | 0 | G1: 25 |
| 2 | 300 | 0 | G0: 300 |
| 3 | 2,300 | 0 | G1: 2,300 |
| 4 | 12,650 | 0 | G0: 12,650 |
| 5 | 53,100 | 0 | G1: 53,100 |
| 6 | 176,500 | 0 | G0: 176,500 |
| 7 | 475,000 | 0 | G1: 475,000 |
| 8 | 1,047,375 | 0 | G0: 1,047,375 |
| 9 | 1,898,000 | 0 | G1: 1,898,000 |
| 10 | 2,809,700 | 0 | G0: 2,809,700 |
| 11 | 3,340,500 | 0 | G1: 3,268,500 / G3: 72,000 |
| 12 | 3,089,000 | 0 | G0: 3,010,000 / G1: 7,000 / G2: 72,000 |
| 13 | 2,103,000 | 0 | G0: 7,000 / G1: 1,958,000 / G2: 6,000 / G3: 132,000 |
| 14 | 961,500 | 1,500 | G0: 868,500 / G1: 12,000 / G2: 81,000 |
| 15 | 252,600 | 6,600 | G0: 6,600 / G1: 246,000 |
| 16 | 28,375 | 28,375 | G0: 28,375 |

- 合計: G0 7,967,001 / G1 7,919,925 / G2 159,000 / **G3 204,000**（全 16,249,926 = SAFE）。
- **k=0..10 はパリティ則**（偶数 G0、奇数 G1）。k=11 以降で混在。
- 極大サイズ 14（1,500）・15（6,600）・16（28,375）。
- 最大 Grundy **3**（s=4 の計算済み盤で初）。
