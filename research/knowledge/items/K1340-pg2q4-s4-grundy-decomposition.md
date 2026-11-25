---
id: K1340
title: "PG(2,4) s=4 の Grundy のサイズ別完全分解 — G=3 までの全分布"
kind: computation
status: computed
topics: [grundy, geometry]
aliases:
- size-by-size Grundy table of the PG(2,4) s=4 game
- PG(2,4) blocking-game Grundy decomposition
relations:
- type: related
  target: K1300
  note: s-パラメータ表の PG(2,4) s=4（Grundy {0:402,633, 1:381,983, 2:262,920, 3:186,480}）
- type: related
  target: K1339
  note: AG(2,5) s=3 のサイズ別分解（s=3 の類似）
artifacts:
- path: research/experiments/s-parameter-kyouen-20261125/output/stats_pg2q4_s4.txt
  role: data
  note: PG(2,4) s=4 の SIZE/GRUNDY/GSIZE 行
- path: research/experiments/s-parameter-kyouen-20261125/output/board_pg2q4.txt
  role: data
  note: PG(2,4) 盤（21 点・21 直線）
scope: PG(2,4)（21 点、21 直線）の s=4 共演ゲーム（各直線と高々 4 点で交わる安全集合）の全 1,234,016 局面の Grundy 値のサイズ別分解。
evidence: stats_pg2q4_s4.txt の GSIZE 行（サイズ, Grundy 値, 個数）を集計。サイズ別の和は SIZE 行と一致し、Grundy 別合計は GRUNDY 行 {0:402,633, 1:381,983, 2:262,920, 3:186,480} と完全一致、総数 1,234,016 = SAFE。空局面の Grundy は 0（ROOT 0 1）。
---

# PG(2,4) s=4 のサイズ別 Grundy 分解

| k | 個数 | G=0 | G=1 | G=2 | G=3 |
|---:|---:|---:|---:|---:|---:|
| 0 | 1 | 1 | | | |
| 1 | 21 | | 21 | | |
| 2 | 210 | 210 | | | |
| 3 | 1,330 | | 1,330 | | |
| 4 | 5,985 | 5,985 | | | |
| 5 | 20,328 | | 1,008 | 9,240 | 10,080 |
| 6 | 53,928 | 17,808 | 32,760 | 3,360 | |
| 7 | 113,760 | 33,960 | 4,200 | | 75,600 |
| 8 | 191,730 | 17,850 | 108,360 | 65,520 | |
| 9 | 255,920 | 171,640 | 33,880 | | 50,400 |
| 10 | 263,508 | 18,228 | 114,240 | 131,040 | |
| 11 | 198,408 | 105,840 | 38,808 | 3,360 | 50,400 |
| 12 | 98,770 | 18,130 | 30,240 | 50,400 | |
| 13 | 26,880 | 10,080 | 16,800 | | |
| 14 | 2,880 | 2,880 | | | |
| 15 | 336 | | 336 | | |
| 16 | 21 | 21 | | | |

- 合計: G=0 402,633 / G=1 381,983 / G=2 262,920 / G=3 186,480
  （全 1,234,016 = SAFE、既存 GRUNDY 行と一致）。
- **G=3 はサイズ 5, 7, 9, 11 に現れる**（10,080 / 75,600 / 50,400 / 50,400）。
- サイズ 0–4 は 0/1 のみ、サイズ 5 以降に G=2/3 が現れる。
- 空局面の Grundy は 0。
