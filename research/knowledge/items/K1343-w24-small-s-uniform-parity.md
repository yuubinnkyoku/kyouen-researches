---
id: K1343
title: "W_24 の s=1..6 はサイズごとに Grundy 一定 — パリティ則と s=7 での混在開始"
kind: computation
status: computed
topics: [grundy, geometry]
aliases:
- W_24 small-s size-uniform Grundy
- parity rules for the W_24 cap spectrum
relations:
- type: related
  target: K1293
  note: W_24 s スペクトル（s=7 のみ混在）
- type: related
  target: K1342
  note: W_24 s=7 のサイズ別分解（G=2 はサイズ 9 と 11）
artifacts:
- path: research/experiments/design-kyouen-witt-20261125/output/grundy_w24_s1.txt
  role: data
  note: 同様に s=1..6 の SIZE 行（grundy0 列から G0/G1 を導出）
- path: research/experiments/design-kyouen-witt-20261125/output/grundy_w24_s6.txt
  role: data
  note: s=6 の SIZE 行
- path: research/experiments/design-kyouen-witt-20261125/output/grundy_w24_s7_gsize.txt
  role: data
  note: s=7 の GSIZE（比較用）
scope: W_24（24 点、759 オクタッド）の s=1..6 共演ゲームのサイズ別 Grundy（全サイズで一様）と、s=7 で混在が始まることの確認。
evidence: 各 s の SIZE 行（count, maximal, grundy0）から G0 = grundy0、G1 = count − grundy0 を計算し、GRUNDY 行と照合。s=1: G=(k+1) mod 2（0→1, 1→0）。s=2,4,5,6: G = k mod 2（全サイズ一様）。s=3: G=(k+1) mod 2。s=7 のみ G=2 がサイズ 9（566,720）と 11（2,040,192）に現れ、サイズ 9 以降で一様性が破れる（K1342）。全 s で G0/G1 の合計は GRUNDY 行と一致。
---

# W_24 の s=1..6 はサイズごとに Grundy 一定

各セルは `G0/G1`（サイズ k の G=0 個数 / G=1 個数）。

| s | サイズ数 | サイズ別 G0/G1 | 合計 G0 / G1 |
|---:|---:|---|---|
| 1 | 2 | 0:0/1, 1:24/0 | 24 / 1 |
| 2 | 3 | 0:1/0, 1:0/24, 2:276/0 | 277 / 24 |
| 3 | 4 | 0:0/1, 1:24/0, 2:0/276, 3:2024/0 | 2,048 / 277 |
| 4 | 5 | 0:1/0, 1:0/24, 2:276/0, 3:0/2024, 4:10626/0 | 10,903 / 2,048 |
| 5 | 7 | 0:1/0, 1:0/24, 2:276/0, 3:0/2024, 4:10626/0, 5:0/42504, 6:113344/0 | 124,247 / 44,552 |
| 6 | 13 | 0:1/0, 1:0/24, 2:276/0, 3:0/2024, 4:10626/0, 5:0/42504, 6:134596/0, 7:0/340032, 8:637560/0, 9:0/566720, 10:170016/0, 11:0/30912, 12:2576/0 | 955,651 / 982,216 |

- **s=1〜6 はすべてのサイズで Grundy が一様**（同じサイズの全局面が同じ値）。
- 規則:
  - s=2, 4, 5, 6: `G(k) = k mod 2`（偶数 0、奇数 1）。
  - s=1, 3: `G(k) = (k+1) mod 2`（偶数 1、奇数 0）。
- **s=7 で初めて混在**（G=2 がサイズ 9・11、K1342）。
- ドデカッド（サイズ 12、2,576 個）は s=6 で G=0（極大、終端）。
