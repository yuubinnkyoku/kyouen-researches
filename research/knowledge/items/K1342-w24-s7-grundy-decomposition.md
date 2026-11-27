---
id: K1342
title: "W_24 s=7 の Grundy のサイズ別完全分解 — G=2 はサイズ 9 と 11 に集中"
kind: computation
status: computed
topics: [grundy, geometry]
aliases:
- size-by-size Grundy table of the W_24 s=7 game
- W_24 dodecad game Grundy decomposition
relations:
- type: related
  target: K1293
  note: W_24 s スペクトル（s=7 のみ混在、Grundy 2 が 2,606,912）
- type: related
  target: K1341
  note: W_22 s=5 のサイズ別分解（設計ボードの類似）
- type: related
  target: K1339
  note: AG(2,5) s=3 のサイズ別分解
artifacts:
- path: research/experiments/design-kyouen-witt-20261125/output/grundy_w24_s7_gsize.txt
  role: data
  note: 本ラウンドで再計算した GSIZE 分解
- path: research/experiments/design-kyouen-witt-20261125/output/grundy_w24_s7.txt
  role: data
  note: 既存の SIZE/GRUNDY 行（照合済み）
- path: research/experiments/pg2q7-cap-game-20261125/scripts/grundy_s_stats.c
  role: solver
  note: s パラメータ付き Grundy 計算器（GSIZE 出力）
scope: W_24（S(5,8,24)、24 点・759 オクタッド）の s=7 共演ゲーム全 7,932,035 局面の Grundy 値のサイズ別分解。
evidence: grundy_s_stats を board_w24.txt s=7 で再実行し GSIZE 行を得た。サイズ別の和は既存 SIZE 行と一致し、Grundy 別合計は GRUNDY 行 {0:3,662,291, 1:1,662,832, 2:2,606,912} と完全一致、総数 7,932,035 = SAFE。サイズ 12 の G=0 1,020,096 は極大 12-キャップ（ドデカッド 2,576 を含む）、G=1 373,520 は非極大。
---

# W_24 s=7 のサイズ別 Grundy 分解

| k | 個数 | G=0 | G=1 | G=2 |
|---:|---:|---:|---:|---:|
| 0 | 1 | 1 | | |
| 1 | 24 | | 24 | |
| 2 | 276 | 276 | | |
| 3 | 2,024 | | 2,024 | |
| 4 | 10,626 | 10,626 | | |
| 5 | 42,504 | | 42,504 | |
| 6 | 134,596 | 134,596 | | |
| 7 | 346,104 | | 346,104 | |
| 8 | 734,712 | 734,712 | | |
| 9 | 1,295,360 | | 728,640 | 566,720 |
| 10 | 1,870,176 | 1,700,160 | 170,016 | |
| 11 | 2,071,104 | 30,912 | | 2,040,192 |
| 12 | 1,393,616 | 1,020,096 | 373,520 | |
| 13 | 30,912 | 30,912 | | |

- 合計: G=0 3,662,291 / G=1 1,662,832 / G=2 2,606,912
  （全 7,932,035 = SAFE、既存 GRUNDY 行と一致）。
- サイズ 0–8 は **G=0（偶数）/ G=1（奇数）** のパリティ則。
- **G=2 はサイズ 9（566,720）と 11（2,040,192）のみ**（どちらも奇数サイズ）。
- サイズ 10 は G=0/1、サイズ 11 は G=0/2（G=1 なし）、サイズ 12 は G=0（極大）/ G=1（非極大）。
- 空局面の Grundy は 0。
