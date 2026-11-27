---
id: K1366
title: "PG(2,4) s=4 の極大数 = 最小ブロッキング集合の個数 — 双対性の厳密確認"
kind: proposition
status: proved
topics: [maximum-safe, geometry]
aliases:
- maximal safe sets of PG(2,4) s=4 as complements of minimal blocking sets
- second confirmation of the blocking duality
relations:
- type: related
  target: K1365
  note: 補集合双対性（本項目はその PG(2,4) s=4 での厳密確認）
- type: related
  target: K1340
  note: PG(2,4) s=4 の極大数 {16:21, 14:360, 13:10,080, 12:280}
artifacts:
- path: research/experiments/pg2q4-blocking-duality-20261128/output/minimal_blocking.json
  role: data
  note: PG(2,4) の最小ブロッキング集合のサイズ別個数
- path: research/experiments/projective-blocking-kyouen-20261125/output/board_pg2q4.txt
  role: data
  note: PG(2,4) 盤
scope: PG(2,4)（21 点、21 直線、各 5 点）における最小ブロッキング集合の全数列挙と、s=4 ゲームの極大安全集合の個数との一致。
evidence: PG(2,4) の全 2^21 = 2,097,152 部分集合を走査し、ブロッキング集合（全直線と交わる）とその極小性（1 点除去でブロッキングでなくなる）を判定した。最小ブロッキング集合のサイズ別個数は 5 が 21、7 が 360、8 が 10,080、9 が 280（合計 10,741）。補集合双対性（K1365）より s=4 の極大安全集合のサイズは 21−5=16, 21−7=14, 21−8=13, 21−9=12 で、個数はそれぞれ 21, 360, 10,080, 280。これは K1340 の極大数 {16:21, 14:360, 13:10,080, 12:280} と完全に一致する。サイズ 5 の最小ブロッキングは 21 本の直線（Bose–Burton の下限 q+√q+1=7 より、非直線の最小は 7）。
---

# PG(2,4) s=4 の極大数 = 最小ブロッキング集合の個数

| 最小ブロッキングのサイズ | 個数 | 対応する極大安全集合のサイズ | 個数（K1340） |
|---:|---:|---:|---:|
| 5 | 21 | 16 | 21 |
| 7 | 360 | 14 | 360 |
| 8 | 10,080 | 13 | 10,080 |
| 9 | 280 | 12 | 280 |

- 全 2²¹ 部分集合の走査で、最小ブロッキング集合の個数を全数確定（合計 10,741）。
- 補集合双対性（K1365）が **PG(2,4) s=4 で厳密に成立**することを、
  独立に計算した両辺の一致で確認。
- サイズ 5 の最小ブロッキングは 21 本の直線。非直線の最小サイズは 7
  （Bose–Burton の下限 q+√q+1 = 7）。
