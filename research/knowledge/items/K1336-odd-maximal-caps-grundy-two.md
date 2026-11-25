---
id: K1336
title: "s=2 盤の G=2 位置 — 奇数極大キャップに含まれるキャップ（PG(2,9) 6-、AG(2,7) 5-、AG(2,5) 4-キャップ）"
kind: computation
status: computed
topics: [grundy, geometry]
aliases:
- Grundy 2 positions as caps inside odd maximal caps
- odd maximal extension pattern in s=2 cap games
relations:
- type: related
  target: K1333
  note: PG(2,9) の 6-キャップ G=2（14,152,320 個）
- type: related
  target: K1335
  note: AG(2,7) の 5-キャップ G=2（49,392 個）
- type: related
  target: K1298
  note: 局所パリティと Grundy の関係
- type: related
  target: K1300
  note: AG(2,5) s=2 の Grundy 分布（G=2 が 3,000 個）
artifacts:
- path: research/experiments/pg2q9-sixcap-20261126/results.txt
  role: data
  note: PG(2,9) の 14,152,320 個の 6-部分集合
- path: research/experiments/pg2q7-cap-game-20261125/output/grundy_ag2q7_s2.txt
  role: data
  note: AG(2,7) の G=2 49,392
- path: research/experiments/s-parameter-kyouen-20261125/output/board_ag2q5.txt
  role: data
  note: AG(2,5) 盤（25 点・30 直線）
scope: s=2 のキャップ・ゲーム（PG(2,9)、AG(2,7)、AG(2,5)）における Grundy 2 の位置の構造。
evidence: 3 盤で「G=2 の位置 = 奇数サイズの極大キャップに含まれる（より小さい）キャップ全体」が成り立つ。PG(2,9) は極大 7-キャップ 2,021,760 個の 6-部分集合 14,152,320 個（相異、K1333）が G=2。AG(2,7) は極大 7-キャップ 2,352 個の 5-部分集合 49,392 個（相異）が G=2 で、G=2 総数 49,392 と一致。AG(2,5) は極大 5-キャップ 600 個の 4-部分集合 3,000 個（相異）が G=2 で、G=2 総数 3,000 と一致。代表の完全 DP で G=2、極大拡大は奇数と偶数の混在（PG(2,9) 6: {7,8}、AG(2,7) 5: {6,7}、AG(2,5) 4: {5,6}）。
---

# s=2 盤の G=2 位置

| 盤 | 奇数極大キャップ | その部分キャップ | G=2 総数 |
|---|---|---:|---:|
| PG(2,9) | 7-キャップ 2,021,760 | 6-部分集合 **14,152,320** | 14,152,320 |
| AG(2,7) | 7-キャップ 2,352 | 5-部分集合 **49,392** | 49,392 |
| AG(2,5) | 5-キャップ 600 | 4-部分集合 **3,000** | 3,000 |

- 3 盤とも **G=2 の位置は「奇数サイズの極大キャップに含まれるキャップ」全体**で、
  個数が Grundy 分布の G=2 と完全一致。
- 代表の完全 DP: G=2、極大拡大は奇数・偶数の混在
  （{7,8}、{6,7}、{5,6}）。
- 偶数極大のみの位置は G=0（局所系 K1298）、それ以外は G=1。

## 注意

- 「奇数極大キャップに含まれる ⟹ G=2」は 3 盤での観察であり、一般の s=2 盤での
  証明はまだない（子の Grundy 値の混在が必要）。
