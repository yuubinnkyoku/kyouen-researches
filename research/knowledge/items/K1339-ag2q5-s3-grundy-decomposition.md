---
id: K1339
title: "AG(2,5) s=3 の Grundy のサイズ別完全分解 — G=4 までの全分布"
kind: computation
status: computed
topics: [grundy, geometry]
aliases:
- size-by-size Grundy table of the AG(2,5) s=3 game
- AG(2,5) blocking-game Grundy decomposition
relations:
- type: related
  target: K1300
  note: s-パラメータ表の AG(2,5) s=3（Grundy {0:402,925, 1:323,901, 2:227,000, 3:358,000, 4:54,000}）
- type: related
  target: K1338
  note: AG(2,7) s=2 のサイズ別分解（s=2 の類似）
- type: related
  target: K1298
  note: 局所パリティ定理（s=2 の 0/1 構造との対比）
artifacts:
- path: research/experiments/s-parameter-kyouen-20261125/output/stats_ag2q5_s3.txt
  role: data
  note: AG(2,5) s=3 の SIZE/GRUNDY/GSIZE 行
- path: research/experiments/s-parameter-kyouen-20261125/output/board_ag2q5.txt
  role: data
  note: AG(2,5) 盤（25 点・30 直線）
scope: AG(2,5)（25 点、30 直線）の s=3 共演ゲーム（各直線と高々 3 点で交わる安全集合）の全 1,365,826 局面の Grundy 値のサイズ別分解。
evidence: stats_ag2q5_s3.txt の GSIZE 行（サイズ, Grundy 値, 個数）を集計。サイズ別の和は SIZE 行と一致し、Grundy 別合計は GRUNDY 行 {0:402,925, 1:323,901, 2:227,000, 3:358,000, 4:54,000} と完全一致、総数 1,365,826 = SAFE。空局面の Grundy は 1（ROOT 1 1）。
---

# AG(2,5) s=3 のサイズ別 Grundy 分解

| k | 個数 | G=0 | G=1 | G=2 | G=3 | G=4 |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1 | | 1 | | | |
| 1 | 25 | 25 | | | | |
| 2 | 300 | | 300 | | | |
| 3 | 2,300 | 2,300 | | | | |
| 4 | 12,500 | | 12,500 | | | |
| 5 | 50,100 | 50,100 | | | | |
| 6 | 148,000 | | 16,000 | 26,000 | 106,000 | |
| 7 | 310,000 | 140,000 | 56,000 | 60,000 | | **54,000** |
| 8 | 421,500 | 48,000 | 88,500 | 33,000 | 252,000 | |
| 9 | 315,500 | 125,500 | 82,000 | 108,000 | | |
| 10 | 96,600 | 28,000 | 68,600 | | | |
| 11 | 9,000 | 9,000 | | | | |

- 合計: G=0 402,925 / G=1 323,901 / G=2 227,000 / G=3 358,000 / G=4 54,000
  （全 1,365,826 = SAFE、既存の GRUNDY 行と一致）。
- **G=4 はサイズ 7 のみ**（54,000 個）。G=3 はサイズ 6（106,000）と 8（252,000）に集中。
- サイズ 0–5 は 0/1 のみ、サイズ 6 以降で 2 以上が現れる（s=3 の複雑さ）。
- 空局面の Grundy は 1。
