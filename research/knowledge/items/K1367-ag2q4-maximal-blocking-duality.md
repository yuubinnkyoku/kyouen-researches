---
id: K1367
title: "AG(2,4) s=3 の極大数 = 最小ブロッキング集合の個数 — 双対性の第三確認"
kind: proposition
status: proved
topics: [maximum-safe, geometry]
aliases:
- maximal safe sets of AG(2,4) s=3 as complements of minimal blocking sets
- third confirmation of the blocking duality
relations:
- type: related
  target: K1365
  note: 補集合双対性（本項目はその AG(2,4) s=3 での厳密確認）
- type: related
  target: K1340
  note: AG(2,4) s=3 の極大数 {8:120, 9:1120}
- type: related
  target: K1366
  note: PG(2,4) s=4 での双対性確認
artifacts:
- path: research/experiments/ag2q4-blocking-duality-20261128/output/minimal_blocking.json
  role: data
  note: AG(2,4) の最小ブロッキング集合のサイズ別個数
- path: research/experiments/s-parameter-kyouen-20261125/output/board_ag2q4.txt
  role: data
  note: AG(2,4) 盤
scope: AG(2,4)（16 点、20 直線、各 4 点）における最小ブロッキング集合の全数列挙と、s=3 ゲームの極大安全集合の個数との一致。
evidence: AG(2,4) の全 2^16 = 65,536 部分集合を走査し、ブロッキング集合とその極小性を判定した。最小ブロッキング集合のサイズ別個数は 7 が 1,120、8 が 120（合計 1,240）。補集合双対性（K1365）より s=3 の極大安全集合のサイズは 16−7=9 と 16−8=8 で、個数は 1,120 と 120。これは K1340 の極大数 {8:120, 9:1120} と完全に一致する。最小ブロッキングの最小サイズ 7 は AG(2,q) の下界 q+√q+1 = 7（q=4）と一致する。
---

# AG(2,4) s=3 の極大数 = 最小ブロッキング集合の個数

| 最小ブロッキングのサイズ | 個数 | 対応する極大安全集合のサイズ | 個数（K1340） |
|---:|---:|---:|---:|
| 7 | 1,120 | 9 | 1,120 |
| 8 | 120 | 8 | 120 |

- 全 2¹⁶ = 65,536 部分集合の走査で、最小ブロッキング集合を全数確定（合計 1,240）。
- 補集合双対性（K1365）が **AG(2,4) s=3 で厳密に成立**することを、
  独立に計算した両辺の一致で確認（3 例目）。
- 最小ブロッキングの最小サイズ 7 は AG(2,q) の下界 q+√q+1 = 7 と一致。
