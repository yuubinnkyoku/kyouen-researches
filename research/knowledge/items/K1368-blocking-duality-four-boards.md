---
id: K1368
title: "極大数 = 最小ブロッキング集合の個数 — 4 盤での双対性確認と総括"
kind: proposition
status: proved
topics: [maximum-safe, geometry, statistics]
aliases:
- four-board confirmation of the complement blocking duality
- summary of maximal-safe vs minimal-blocking counts
relations:
- type: related
  target: K1365
  note: 補集合双対性の命題
- type: related
  target: K1367
  note: AG(2,4) s=3 の確認
- type: related
  target: K1366
  note: PG(2,4) s=4 の確認
- type: related
  target: K1364
  note: AG(2,5) s=4 の確認
- type: related
  target: K1356
  note: PG(2,3) s=3 の完全スペクトル（極大数 7:234, 9:13）
artifacts:
- path: research/experiments/pg2q3-blocking-duality-20261128/output/minimal_blocking.json
  role: data
  note: PG(2,3) の最小ブロッキング集合のサイズ別個数
- path: research/experiments/ag2q4-blocking-duality-20261128/output/minimal_blocking.json
  role: data
  note: AG(2,4) の最小ブロッキング集合
- path: research/experiments/pg2q4-blocking-duality-20261128/output/minimal_blocking.json
  role: data
  note: PG(2,4) の最小ブロッキング集合
- path: research/experiments/ag2q5-s4-20261128/output/ag2q5_s4_gsize.json
  role: data
  note: AG(2,5) s=4 の極大数
scope: 直線サイズ l の 4 盤（AG(2,4) s=3、PG(2,3) s=3、PG(2,4) s=4、AG(2,5) s=4）における最小ブロッキング集合の全数と、s = l−1 ゲームの極大安全集合の全数の一致。
evidence: 補集合双対性（K1365）より、s = l−1 のとき安全集合の補集合は通常のブロッキング集合、極大安全集合の補集合は極小ブロッキング集合。4 盤で両辺を独立に全数計算した。AG(2,4) s=3 は最小ブロッキング 7 が 1,120・8 が 120、極大安全 9 が 1,120・8 が 120（K1340, K1367）。PG(2,3) s=3 は最小ブロッキング 4 が 13・6 が 234、極大安全 9 が 13・7 が 234（K1356）。PG(2,4) s=4 は最小ブロッキング 5 が 21・7 が 360・8 が 10,080・9 が 280、極大安全 16 が 21・14 が 360・13 が 10,080・12 が 280（K1340, K1366）。AG(2,5) s=4 は最小ブロッキング 9 が 28,375・10 が 6,600・11 が 1,500、極大安全 16 が 28,375・15 が 6,600・14 が 1,500（K1364）。極大安全の総数はそれぞれ 1,240・247・10,741・36,475 で最小ブロッキングの総数と一致。
---

# 極大数 = 最小ブロッキング集合の個数（4 盤での確認）

s = l−1（l は直線サイズ）のとき、補集合双対性（K1365）より

```
極大安全集合のサイズ m の個数 = 最小ブロッキング集合のサイズ (N−m) の個数
```

| 盤 | l | s | 最小ブロッキング（サイズ: 個数） | 極大安全（サイズ: 個数） |
|---|---:|---:|---|---|
| AG(2,4) | 4 | 3 | 7: 1,120 / 8: 120 | 9: 1,120 / 8: 120 |
| PG(2,3) | 4 | 3 | 4: 13 / 6: 234 | 9: 13 / 7: 234 |
| PG(2,4) | 5 | 4 | 5: 21 / 7: 360 / 8: 10,080 / 9: 280 | 16: 21 / 14: 360 / 13: 10,080 / 12: 280 |
| AG(2,5) | 5 | 4 | 9: 28,375 / 10: 6,600 / 11: 1,500 | 16: 28,375 / 15: 6,600 / 14: 1,500 |

- 極大安全の総数（1,240 / 247 / 10,741 / 36,475）が最小ブロッキングの総数と完全一致。
- 最小ブロッキングの最小サイズは l（直線）で、非直線の最小サイズは
  AG(2,4) で 7、PG(2,3) で 6、PG(2,4) で 7、AG(2,5) で 9（Bose–Burton 系の下界と整合）。
- 4 盤すべてで s = l−1 のケースを独立計算で確認。
