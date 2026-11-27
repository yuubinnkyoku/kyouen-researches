---
id: K1355
title: "PG(2,4) s=3 の完全 Grundy スペクトル — G=(k+1) mod 2、全 157,398 局面"
kind: proposition
status: proved
topics: [grundy, geometry]
aliases:
- complete Grundy spectrum of the PG(2,4) s=3 game
- PG(2,4) blocking game with two-valued Grundy
relations:
- type: related
  target: K1353
  note: 錐＋枠二重数え上げ法（本計算の手法）
- type: related
  target: K1340
  note: PG(2,4) s=4 のサイズ別分解（別の s）
- type: related
  target: K1352
  note: PG(2,9) s=2 の完全分類（同種の完全表）
artifacts:
- path: research/experiments/pg2q4-s3-20261128/output/pg2q4_s3_spectrum.json
  role: data
  note: サイズ別 Grundy スペクトル
- path: research/experiments/pg2q4-s3-20261128/scripts/cone_pg2q4_s3.py
  role: solver
  note: 三角形の錐＋枠二重数え上げ（および一直線 3-キャップの錐）
- path: research/experiments/pg2q4-s3-20261128/README.md
  role: log
  note: 結果と再現手順
scope: PG(2,4)（21 点、21 直線、各 5 点）の s=3 共演ゲーム全 157,398 局面の Grundy 値のサイズ別完全スペクトル。
evidence: 三角形 F={0,1,5}（非共線）の錐 5,038 局面で完全 DP。PGL(3,4) は三角形に推移的、サイズ ≥4 のキャップは三角形を含むので N_m(g)=N_3·T_m(g)/C(m,3)（N_3=1,120）。一直線 3-キャップ 210 個は別の錐（{0,1,2}、3,809 局面）で G=0。k=0,1,2 は mex 連鎖（3-キャップ全 G=0 → 2-キャップ G=1 → 1-キャップ G=0 → 空 G=1）。結果: k=0..9 で G = 1,0,1,0,1,0,1,0,1,0、個数 1, 21, 210, 1,330, 5,040, 16,128, 35,952, 50,976, 37,620, 10,120。合計 157,398（G0 78,575 / G1 78,823）。最大安全サイズ 9。
---

# PG(2,4) s=3 の完全 Grundy スペクトル

| k | 個数 | G |
|---:|---:|---:|
| 0 | 1 | 1 |
| 1 | 21 | 0 |
| 2 | 210 | 1 |
| 3 | 1,330 | 0 |
| 4 | 5,040 | 1 |
| 5 | 16,128 | 0 |
| 6 | 35,952 | 1 |
| 7 | 50,976 | 0 |
| 8 | 37,620 | 1 |
| 9 | 10,120 | 0 |

- 全 157,398 局面（G0 78,575 / G1 78,823）。最大安全サイズ 9。
- **G(k) = (k+1) mod 2**（k=0..9）。
- 3-キャップは 2 軌道（一直線 210 個・三角形 1,120 個）だが、両方 G=0。
- サイズ ≥4 のキャップは必ず三角形を含むため、三角形の錐で全数を得られる。
