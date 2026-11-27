---
id: K1335
title: "AG(2,7) s=2 の Grundy — G=2 は極大 7-キャップに含まれる 5-キャップ全体（49,392 個）"
kind: computation
status: computed
topics: [grundy, geometry]
aliases:
- Grundy 2 positions in the AG(2,7) cap game
- five-caps inside complete 7-arcs of AG(2,7)
relations:
- type: related
  target: K1300
  note: s-パラメータ表の AG(2,7) s=2（Grundy 分布 {0:581,827, 1:477,505, 2:49,392}）
- type: related
  target: K1333
  note: PG(2,9) の 6-キャップ G=2 の類似（極大 7-キャップ拡大が鍵）
- type: related
  target: K1298
  note: 局所パリティと Grundy の関係
artifacts:
- path: research/experiments/pg2q7-cap-game-20261125/output/grundy_ag2q7_s2.txt
  role: data
  note: AG(2,7) s=2 のサイズ別・Grundy 分布
- path: research/experiments/s-parameter-kyouen-20261125/output/board_ag2q7.txt
  role: data
  note: AG(2,7) 盤（49 点・56 円）
scope: AG(2,7)（49 点、56 直線（円）のアフィン平面）のキャップ・ゲーム s=2 の Grundy 値と、極大 7-キャップ（complete 7-arc）の構造。
evidence: AG(2,7) s=2 の国勢調査データ（grundy_ag2q7_s2.txt）は 7-キャップ 51,744 個・極大 7-キャップ 2,352 個、Grundy 2 が 49,392 個（すべてサイズ 5）。極大 7-キャップの 5-部分集合を列挙すると 2,352×21 = 49,392 個で**すべて相異なる**（重複 0）。代表 {0,1,7,9,19} の完全 DP は Grundy 2、極大拡大 {6,7}（混在パリティ）。G=2 の個数 49,392 がこれらの 5-部分集合の個数と一致するので、**G=2 の位置は極大 7-キャップに含まれる 5-キャップ全体**（49,392 個）。
---

# AG(2,7) s=2 の G=2 位置

- AG(2,7) の 7-キャップは 51,744 個、うち極大 7-キャップ（complete 7-arc）は 2,352 個。
- 極大 7-キャップの 5-部分集合は 2,352 × 21 = **49,392 個で、すべて相異なる**。
- 代表 {0,1,7,9,19} の完全 DP: **Grundy 2**、極大拡大 {6,7}（混在パリティ）。
- Grundy 2 はすべてサイズ 5 で 49,392 個 → **G=2 はまさに「極大 7-キャップに含まれる 5-キャップ」全体**。
- G=0/1 の内訳: 極大 7-キャップ自身など偶数極大のみの位置は 0、その他は 1。
