---
id: K1356
title: "PG(2,3) s=3 の完全 Grundy スペクトル — G=(k+1) mod 2、全 4,330 局面"
kind: proposition
status: proved
topics: [grundy, geometry]
aliases:
- complete Grundy spectrum of the PG(2,3) s=3 game
- smallest projective-plane s=3 spectrum
relations:
- type: related
  target: K1353
  note: 錐＋枠二重数え上げ法（複数軌道の合算）
- type: related
  target: K1355
  note: PG(2,4) s=3 の完全スペクトル（同型の結果）
- type: related
  target: K1352
  note: PG(2,9) s=2 の完全分類
artifacts:
- path: research/experiments/pg2q3-s3-20261128/output/pg2q3_s3_spectrum.json
  role: data
  note: サイズ別 Grundy スペクトル
- path: research/experiments/pg2q3-s3-20261128/scripts/cone_pg2q3_s3.py
  role: solver
  note: 三角形・一直線 3-キャップの 2 錐＋二重数え上げ
- path: research/experiments/pg2q3-s3-20261128/independent/REPORT.md
  role: log
  note: 独立検証（132/132 PASS、全 2^13 部分集合の完全 DP、極大 7 の注意）
- path: research/experiments/pg2q3-s3-20261128/README.md
  role: log
  note: 結果と再現手順
scope: PG(2,3)（13 点、13 直線、各 4 点）の s=3 共演ゲーム全 4,330 局面の Grundy 値のサイズ別完全スペクトル。
evidence: 3-キャップは 2 軌道（三角形 234・一直線 52）で両方 G=0。三角形 F={0,1,4} の錐 260 局面と一直線 3-キャップ {0,1,2} の錐 214 局面で完全 DP。PGL(3,3) の三角形・一直線 3-部分集合への推移性より `234·T_m(g) + 52·U_m(g) = C(m,3)·N_m(g)`。k=0,1,2 は mex 連鎖（3-キャップ全 G=0 → 2-キャップ G=1 → 1-キャップ G=0 → 空 G=1）。結果は k=0..9 で G = 1,0,1,0,1,0,1,0,1,0、個数 1, 13, 78, 286, 702, 1,170, 1,248, 702, 117, 13。合計 4,330（G0 2,184 / G1 2,146）。最大安全サイズ 9。**独立検証（132/132 PASS）** では、2^13 全部分集合の完全 DP で全数一致。**注意点** として、極大安全集合は 247 個（サイズ 7 が 234、サイズ 9 が 13）で、最大サイズ 9 は最大値にすぎない（サイズ 7 の終端 234 個は三角形 T とその 3 辺上の 4 点 Q(T) の和; 補集合は Pasch 6-集合）。G(7)=0 は終端 0 と非終端 mex{1}=0 の両方から成り立つ。**パリティによる説明** として、極大サイズは 7 と 9 でいずれも奇数なので、局所系（K1298）より全局面で `G=(9−k) mod 2=(k+1) mod 2` が従う（終端 7 も p=7 で同じ値）。
---

# PG(2,3) s=3 の完全 Grundy スペクトル

| k | 個数 | G |
|---:|---:|---:|
| 0 | 1 | 1 |
| 1 | 13 | 0 |
| 2 | 78 | 1 |
| 3 | 286 | 0 |
| 4 | 702 | 1 |
| 5 | 1,170 | 0 |
| 6 | 1,248 | 1 |
| 7 | 702 | 0 |
| 8 | 117 | 1 |
| 9 | 13 | 0 |

- 全 4,330 局面（G0 2,184 / G1 2,146）。最大安全サイズ 9。
- **G(k) = (k+1) mod 2**（k=0..9）。
- 3-キャップは 2 軌道（三角形 234・一直線 52）だが両方 G=0。
- **注意**: 極大安全集合は 247 個（サイズ 7 が 234、サイズ 9 が 13）。最大サイズ 9 は
  最大値であり、すべての極大集合がサイズ 9 ではない（ゲーム長は固定でない）。
  サイズ 7 の終端 234 個は三角形 T と Q(T)（T の 3 辺上の 4 点）の和で、
  非終端の 468 個は 2 手（G=1 の 8-キャップへ）を持つが mex{1}=0。
- 二重数え上げは両軌道を合算: `234·T_m + 52·U_m = C(m,3)·N_m`。
