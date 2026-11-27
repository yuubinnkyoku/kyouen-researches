---
id: K1361
title: "PG(2,5) s=3 の Grundy サイズ別完全分解 — G=4 はサイズ 7 のみ"
kind: computation
status: computed
topics: [grundy, geometry]
aliases:
- size-by-size Grundy table of the PG(2,5) s=3 game
- largest s=3 decomposition (7,906,892 positions)
relations:
- type: related
  target: K1300
  note: PG(2,5) s=3 の Grundy 分布（G=4 186,000）
- type: related
  target: K1357
  note: s=3 盤の極大パリティ × Grundy 表（極大 9,10,11 混在、最大 4）
- type: related
  target: K1358
  note: 全 s 盤の最大 Grundy 表
artifacts:
- path: research/experiments/pg2q5-s3-20261128/output/gsize_pg2q5_s3.txt
  role: data
  note: エンジン出力（SIZE/GRUNDY/GSIZE 行）
- path: research/experiments/pg2q5-s3-20261128/output/pg2q5_s3_gsize.json
  role: data
  note: サイズ別 Grundy 分布の JSON
- path: research/experiments/pg2q7-cap-game-20261125/scripts/grundy_s_stats.c
  role: solver
  note: s パラメータ付き Grundy 計算器（GSIZE 出力）
- path: research/experiments/pg2q5-s3-20261128/independent/REPORT.md
  role: log
  note: 独立検証（3 実装一致・24/24 PASS）
- path: research/experiments/pg2q5-s3-20261128/README.md
  role: log
  note: 結果と再現手順
scope: PG(2,5)（31 点、31 直線、各 6 点）の s=3 共演ゲーム全 7,906,892 局面の Grundy 値のサイズ別完全分解。
evidence: grundy_s_stats を board_pg2q5.txt s=3 で実行し GSIZE 行を取得。サイズ別の和は SIZE 行、Grundy 別合計は GRUNDY 行 {0:2,056,726, 1:2,083,666, 2:1,519,000, 3:2,061,500, 4:186,000} と完全一致（総数 7,906,892）。結果は k=0..11 の G 分布で 0:G1; 1:G0; 2:G1; 3:G0; 4:G2 31,000; 5:G0 111,600+G1 46,500; 6:G0 15,500+G1 3,100+G2 186,000+G3 387,500; 7:G0 480,500+G1 697,500+G2 186,000+G4 186,000; 8:G0 465,000+G1 232,500+G2 186,000+G3 1,674,000; 9:G0 666,500+G1 620,000+G2 930,000; 10:G0 248,000+G1 483,600; 11:G0 65,100。最大 Grundy 4 はサイズ 7 のみ。極大サイズ 9,10,11 の混在と整合。**独立検証（24/24 PASS）** では、公開エンジン再実行は主张ファイルと**バイト単位で一致**、独立 C 実装・完全 Python DP の 3 実装が 46 行すべて一致（7,906,892 局面）。全 31,000 個の 4-キャップが G=2、G=4 はサイズ 7 のみ、極大 9/10/11、root G=1・misère 1 を確認。
---

# PG(2,5) s=3 のサイズ別 Grundy 完全分解

| k | 個数 | 極大 | G 分布 |
|---:|---:|---:|---|
| 0 | 1 | 0 | G1: 1 |
| 1 | 31 | 0 | G0: 31 |
| 2 | 465 | 0 | G1: 465 |
| 3 | 4,495 | 0 | G0: 4,495 |
| 4 | 31,000 | 0 | **G2: 31,000** |
| 5 | 158,100 | 0 | G0: 111,600 / G1: 46,500 |
| 6 | 592,100 | 0 | G0: 15,500 / G1: 3,100 / G2: 186,000 / G3: 387,500 |
| 7 | 1,550,000 | 0 | G0: 480,500 / G1: 697,500 / G2: 186,000 / **G4: 186,000** |
| 8 | 2,557,500 | 0 | G0: 465,000 / G1: 232,500 / G2: 186,000 / G3: 1,674,000 |
| 9 | 2,216,500 | 93,000 | G0: 666,500 / G1: 620,000 / G2: 930,000 |
| 10 | 731,600 | 248,000 | G0: 248,000 / G1: 483,600 |
| 11 | 65,100 | 65,100 | G0: 65,100 |

- 合計: G0 2,056,726 / G1 2,083,666 / G2 1,519,000 / G3 2,061,500 / **G4 186,000**
  （全 7,906,892 = SAFE、既存 GRUNDY 行と一致）。
- **最大 Grundy 4 はサイズ 7 のみ**（186,000 個）。
- 4-キャップはすべて **G=2**（31,000 個）。
- 極大サイズは 9,10,11（混在）で、K1357/1358 の「混在 ⇒ 最大 2 以上」と整合。
