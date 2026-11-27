---
id: K1341
title: "W_22 s=5 の Grundy のサイズ別完全分解 — 前半はパリティ、8 以降に G=3"
kind: computation
status: computed
topics: [grundy, geometry]
aliases:
- size-by-size Grundy table of the W_22 s=5 game
- Witt design W_22 blocking-game Grundy decomposition
relations:
- type: related
  target: K1293
  note: W_24 s スペクトルと設計ボード（W_22 s=5 は最大 11/12/15 の混在）
- type: related
  target: K1300
  note: s-パラメータ表の W_22 s=5（Grundy {0:784,412, 1:949,829, 2:332,640, 3:101,640}）
- type: related
  target: K1339
  note: AG(2,5) s=3 のサイズ別分解（s=3 の類似）
artifacts:
- path: research/experiments/s-parameter-kyouen-20261125/output/stats_w22_s5.txt
  role: data
  note: W_22 s=5 の SIZE/GRUNDY/GSIZE 行
scope: W_22（22 点、77 ブロック）の s=5 共演ゲーム（各ブロックと高々 5 点で交わる安全集合）の全 2,168,521 局面の Grundy 値のサイズ別分解。
evidence: stats_w22_s5.txt の GSIZE 行（サイズ, Grundy 値, 個数）を集計。サイズ別の和は SIZE 行と一致し、Grundy 別合計は GRUNDY 行 {0:784,412, 1:949,829, 2:332,640, 3:101,640} と完全一致、総数 2,168,521 = SAFE。空局面の Grundy は 1（ROOT 1 0）。
---

# W_22 s=5 のサイズ別 Grundy 分解

| k | 個数 | G=0 | G=1 | G=2 | G=3 |
|---:|---:|---:|---:|---:|---:|
| 0 | 1 | | 1 | | |
| 1 | 22 | 22 | | | |
| 2 | 231 | | 231 | | |
| 3 | 1,540 | 1,540 | | | |
| 4 | 7,315 | | 7,315 | | |
| 5 | 26,334 | 26,334 | | | |
| 6 | 74,536 | | 74,536 | | |
| 7 | 169,312 | 169,312 | | | |
| 8 | 310,530 | | 282,810 | | 27,720 |
| 9 | 454,300 | 337,260 | 6,160 | 110,880 | |
| 10 | 508,816 | 22,792 | 412,104 | | 73,920 |
| 11 | 396,816 | 167,664 | 7,392 | 221,760 | |
| 12 | 176,176 | 22,176 | 154,000 | | |
| 13 | 36,960 | 36,960 | | | |
| 14 | 5,280 | | 5,280 | | |
| 15 | 352 | 352 | | | |

- 合計: G=0 784,412 / G=1 949,829 / G=2 332,640 / G=3 101,640
  （全 2,168,521 = SAFE、既存 GRUNDY 行と一致）。
- **サイズ 0–7 は G = (k が偶数なら 1、奇数なら 0)** というパリティ則。
- サイズ 8 以降でパリティ則が破れ、**G=3 がサイズ 8（27,720）と 10（73,920）**に現れる。
- 空局面の Grundy は 1。
