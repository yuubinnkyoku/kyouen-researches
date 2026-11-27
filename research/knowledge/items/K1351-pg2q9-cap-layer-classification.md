---
id: K1351
title: "PG(2,9) のサイズ 5–10 層の Grundy 分類 — 局所パリティによる説明"
kind: computation
status: computed
topics: [grundy, geometry]
aliases:
- layer classification of PG(2,9) caps
- Grundy by size and maximality in PG(2,9)
relations:
- type: related
  target: K1333
  note: k=6 の 0/2 混在と G=2 個数 14,152,320（証明済み）
- type: related
  target: K1331
  note: PG(2,9) のキャップ構造（サイズ別 conic/極大分解）
- type: related
  target: K1305
  note: 5-キャップ 2 軌道・すべて G=1
- type: related
  target: K1298
  note: 局所パリティ定理（極大拡大が一様パリティなら G=(p−|S|) mod 2）
artifacts:
- path: research/experiments/pg2q9-cap-game-20261125/output/census_pg2q9.txt
  role: data
  note: サイズ別キャップ数・極大数
- path: research/experiments/pg2q9-cap-game-20261125/output/conic_layer.json
  role: data
  note: conic k-キャップの個数
- path: research/experiments/pg2q9-cap-game-20261125/independent_layers/REPORT.md
  role: log
  note: 独立検証（全項目 PASS、88 サンプル DP・200 サンプル構造・算術）
scope: PG(2,9)（91 点、91 直線）の s=2 キャップ・ゲームのサイズ 5–10 層の Grundy 分類。
evidence: 極大キャップのサイズは 6, 7, 8, 10（K1300/K1331）。k=5 は全 14,859,936 が G=1（K1305、2 軌道とも）。k=6 は極大 707,616 が G=0、非極大のうち奇数 7-拡大を持つ 14,152,320 が G=2、残り 37,857,456 が G=0（K1333、証明済み）。k=7 は極大 2,021,760 が終端 G=0、非極大 49,533,120 は極大拡大が 8 か 10（偶数）なので局所系より G=1。k=8 は極大 5,307,120（終端 G=0）と conic 8-キャップ 2,653,560（10 へ拡大、偶数）の両方が G=0。k=9 は全 conic で 10 へ拡大（偶数）→ G=(10−9) mod 2=1。k=10 は conic で終端 G=0。
---

# PG(2,9) のサイズ 5–10 層の Grundy 分類

| k | 個数 | G=0 | G=1 | G=2 | 説明 |
|---:|---:|---:|---:|---:|---|
| 5 | 14,859,936 | 0 | **14,859,936** | 0 | conic 6-子（G=0）が必ず存在し、子は {0,2} のみ → mex{0}=mex{0,2}=1（K1305） |
| 6 | 52,009,776 | **37,857,456** | 0 | **14,152,320** | 極大 7-子と非極大 7-子 → mex{0,1}=2（K1333） |
| 7 | 51,554,880 | **2,021,760** | **49,533,120** | 0 | 極大は終端 0、非極大は 8/10（偶数）へ → G=1 |
| 8 | 7,960,680 | **7,960,680** | 0 | 0 | 極大 5,307,120（終端）と conic（10 へ、偶数）→ 0 |
| 9 | 589,680 | 0 | **589,680** | 0 | 全 conic → 10 へ（偶数）→ (10−9) mod 2=1 |
| 10 | 58,968 | **58,968** | 0 | 0 | conic・終端 |

- **k=8,9,10 はサイズだけでは決まらないが、極大性と局所系で完全に決まる**。
- k=7 は極大/非極大で 0/1 に分かれる。
- k=6 だけが 0/2 の混在（G=2 は 14,152,320、K1333）。
- k=5 はすべて 1（2 軌道とも、K1305）。独立検証（全項目 PASS）: 88 サンプルの完全 DP・200 サンプル構造・census/conic 再現・算術で確認。k=5 の G=1 は「conic 6-子（G=0）の存在」と「子が {0,2} のみ」から従う。
