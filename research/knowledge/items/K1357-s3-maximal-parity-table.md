---
id: K1357
title: "s=3 盤の極大サイズのパリティと Grundy — 奇数一様の 2 盤は 2 値、混在 3 盤は最大 2/4"
kind: computation
status: computed
topics: [grundy, geometry]
aliases:
- parity of maximal safe sets vs Grundy values for s=3 boards
- s=3 board classification by maximal parity
relations:
- type: related
  target: K1298
  note: パリティ特性定理（極大パリティ一様 ⇔ Grundy 0/1、局所系 G=(p−k) mod 2）
- type: related
  target: K1355
  note: PG(2,4) s=3（極大 7,9 奇数一様、G=(k+1) mod 2）
- type: related
  target: K1356
  note: PG(2,3) s=3（極大 7,9 奇数一様、G=(k+1) mod 2）
- type: related
  target: K1300
  note: s-パラメータ表（AG(2,4), AG(2,5), PG(2,5) の s=3）
artifacts:
- path: research/experiments/s-parameter-kyouen-20261125/output/grundy_general.json
  role: data
  note: AG(2,4)/AG(2,5) s=3 の極大サイズと Grundy 分布
- path: research/experiments/s-parameter-kyouen-20261125/output/grundy_pg2q5_s3.txt
  role: data
  note: PG(2,5) s=3 の極大サイズと Grundy 分布
- path: research/experiments/pg2q3-s3-20261128/output/pg2q3_s3_spectrum.json
  role: data
  note: PG(2,3) s=3（K1356）
- path: research/experiments/pg2q4-s3-20261128/output/pg2q4_s3_spectrum.json
  role: data
  note: PG(2,4) s=3（K1355）
scope: 計算済みの s=3 共演ゲーム 5 盤（PG(2,3), PG(2,4), AG(2,4), AG(2,5), PG(2,5)）の極大安全集合のサイズ・パリティと Grundy 値の関係。
evidence: 極大サイズと Grundy 分布は各データファイルより: PG(2,3) は 7 (234), 9 (13) の奇数一様で Grundy {0,1}（K1356）; PG(2,4) は 7 (360), 9 (11,480) の奇数一様で {0,1}（K1355）; AG(2,4) は 8 (120), 9 (1,120) の混在で {0,1,2}（G=2 が 960）; AG(2,5) は 9,10,11 の混在で {0,1,2,3,4}; PG(2,5) は 9,10,11 の混在で {0,1,2,3,4}。奇数一様な 2 盤は局所系（K1298）より全局面で G=(9−k) mod 2=(k+1) mod 2; 混在盤は G≥2 を含み最大 2（AG(2,4)）または 4（AG(2,5), PG(2,5)）。
---

# s=3 盤の極大パリティと Grundy

| 盤 | 極大サイズ（個数） | パリティ | Grundy 値 | 最大 G |
|---|---|---|---|---:|
| PG(2,3) | 7 (234), 9 (13) | 奇数一様 | {0,1} | 1 |
| PG(2,4) | 7 (360), 9 (11,480) | 奇数一様 | {0,1} | 1 |
| AG(2,4) | 8 (120), 9 (1,120) | 混在 | {0,1,2} | 2 |
| AG(2,5) | 9, 10, 11 | 混在 | {0,1,2,3,4} | 4 |
| PG(2,5) | 9, 10, 11 | 混在 | {0,1,2,3,4} | 4 |

- **奇数一様な 2 盤**（PG(2,3), PG(2,4)）は局所系より `G=(k+1) mod 2`（全局面 2 値）。
- **混在盤**は G≥2 を含み、最大 2（AG(2,4)）または 4（AG(2,5), PG(2,5)）。
- パリティ特性定理（K1298）の「一様 ⇔ 0/1」と「混在 ⇒ 2 以上が存在」を、
  s=3 の 5 盤で具体的に確認した表。
