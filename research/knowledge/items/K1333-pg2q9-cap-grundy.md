---
id: K1333
title: "PG(2,9) のキャップ Grundy — サイズと極大性による決定（k=7,8,9,10、k=6 は 0/2 混在）"
kind: computation
status: computed
topics: [geometry, grundy]
aliases:
- Grundy values of caps in PG(2,9)
- size and maximality determine cap Grundy in PG(2,9)
relations:
- type: related
  target: K1298
  note: パリティ特性定理と局所系（極大拡大のパリティ一様なら G=(p−|S|) mod 2）
- type: related
  target: K1331
  note: PG(2,9) のキャップ構造（サイズ別 conic/極大分解）
- type: related
  target: K1321
  note: conic k-キャップの Grundy（k=6..9）
- type: related
  target: K1305
  note: 5-キャップの Grundy=1
artifacts:
- path: research/log/2026-11-26-pg2q9-6cap-grundy.md
  role: log
  note: 6-キャップの局所パリティと 200 サンプル分布
- path: research/experiments/pg2q9-cap-game-20261125/output/board_pg2q9.txt
  role: data
  note: PG(2,9) 盤
- path: research/log/2026-11-26-pg2q9-cap-structure.md
  role: log
  note: キャップ構造（極大サイズの分布）
scope: PG(2,9)（91 点、91 直線）上のキャップの s=2 共演ゲーム（Grundy 値）。サイズ k=5..10。
evidence: 極大キャップのサイズは 6,7,8,10（K1300/K1331）。局所系（K1298）より、位置 S の極大拡大がすべて同じパリティ p なら G(S)=(p−|S|) mod 2。k=7: 極大なら終端 G=0、非極大なら極大拡大は 8-caps と 10-caps のみ（偶数）→ G=(0−7) mod 2=1。k=8: 極大なら 0、非極大なら 10-caps のみ（偶数）→ G=0。k=9: 全キャップが conic（K1321）で 10-cap へ延長 → G=(0−9) mod 2=1。k=10: 終端 G=0。k=5: 全て非極大で G=1（K1305/K1321）。k=6: 極大（707,616）は終端 G=0、非極大は極大拡大が {8,10}（偶数）なら G=0、{7,8}（混在）なら G=2（witness {0,1,10,20,32,39}、200 ランダムサンプルで G=0 154 / G=2 46、G=2 はすべて {7,8}）。よって **k=7,8,9,10 の Grundy はサイズと極大性で完全に決まり、k=6 だけが局所パリティに応じて 0/2 に分かれる**。
---

# PG(2,9) のキャップ Grundy

| k | 極大 | Grundy |
|---:|---|---|
| 5 | なし | 1 |
| 6 | あり | 極大: 0／非極大: 偶数極大のみなら 0、7-arc 拡大ありなら 2 |
| 7 | あり | 極大: 0／非極大: 1 |
| 8 | あり | すべて 0 |
| 9 | なし | すべて 1 |
| 10 | あり | すべて 0 |

- k=7,8,9,10 はサイズと極大性で完全に決まる（局所系 K1298）。
- k=6 のみ、極大拡大に 7-caps（奇数）が含まれるかで 0 と 2 に分かれる。
- ランダム 200 個の 6-キャップ: G=0 が 154、G=2 が 46（G=2 はすべて {7,8} の混在）。
