---
id: K1338
title: "AG(2,7) s=2 の Grundy のサイズ別完全分解 — 6-キャップの拡大パリティと 5-キャップの G=2"
kind: proposition
status: proved
topics: [grundy, geometry]
aliases:
- complete size-by-size Grundy decomposition of the AG(2,7) cap game
- AG(2,7) six-cap extension parity
relations:
- type: related
  target: K1335
  note: AG(2,7) の G=2 は極大 7-キャップの 5-部分集合 49,392 個
- type: related
  target: K1336
  note: 子に G=0 と G=1 が混在する位置が G=2（機構）
- type: related
  target: K1300
  note: s-パラメータ表の AG(2,7) s=2 の Grundy 分布
- type: related
  target: K1298
  note: 局所パリティ定理（極大拡大のパリティ一様なら G=(p−|S|) mod 2）
artifacts:
- path: research/experiments/pg2q7-cap-game-20261125/output/grundy_ag2q7_s2.txt
  role: data
  note: AG(2,7) s=2 のサイズ別・Grundy 分布
- path: research/experiments/s-parameter-kyouen-20261125/output/board_ag2q7.txt
  role: data
  note: AG(2,7) 盤（49 点・56 円）
scope: AG(2,7)（49 点、56 直線）の s=2 キャップ・ゲームの全サイズ・全 Grundy 値の分解。
evidence: 6-キャップ 460,992 個を極大拡大のパリティで分類すると、極大 271,656、8 のみに拡大 172,872、7 のみに拡大 16,464、7 と 8 の混在 0。局所系（K1298）より only8 は G=0、only7 は G=1。5-キャップ 444,528 個はすべて極大 6-子を持ち、G=2 は 7-拡大を持つ 5-キャップ（= 極大 7-キャップの 5-部分集合 49,392 個、K1335）に限る。サイズ別に集計すると G=0 が 1+1,176+127,596+271,656+172,872+2,352+6,174 = 581,827、G=1 が 49+16,464+395,136+16,464+49,392 = 477,505、G=2 が 49,392 で、既存の分布と完全一致（合計 1,108,724）。
---

# AG(2,7) s=2 の Grundy のサイズ別分解

| k | 個数 | G=0 | G=1 | G=2 |
|---:|---:|---:|---:|---:|
| 0 | 1 | 1 | | |
| 1 | 49 | | 49 | |
| 2 | 1,176 | 1,176 | | |
| 3 | 16,464 | | 16,464 | |
| 4 | 127,596 | 127,596 | | |
| 5 | 444,528 | | 395,136 | **49,392** |
| 6 | 460,992 | 444,528（極大 271,656 + only8 172,872） | 16,464（only7） | |
| 7 | 51,744 | 2,352（極大） | 49,392（非極大） | |
| 8 | 6,174 | 6,174（極大） | | |

- 合計: G=0 581,827、G=1 477,505、G=2 49,392、全体 1,108,724（既存分布と完全一致）。
- G=0/1 はサイズと極大拡大のパリティで決まり、G=2 は 5-キャップの 49,392 個のみ。
- 6-キャップに 7 と 8 の混在拡大は存在しない（全数）。
