---
id: K1354
title: "AG(2,9) s=2 の Grundy 完全スペクトル — 錐法で最大 Grundy 3"
kind: computation
status: computed
topics: [grundy, geometry]
aliases:
- complete Grundy spectrum of the AG(2,9) cap game
- AG(2,9) s=2 with Grundy values 0..3
relations:
- type: related
  target: K1353
  note: 錐＋枠二重数え上げ法（本計算の手法）
- type: related
  target: K1300
  note: AG(2,q) s=2 の系列（q≤8 は最大 Grundy 2 以下）
- type: related
  target: K1352
  note: PG(2,9) s=2 の完全分類（最大 Grundy 2）との対比
artifacts:
- path: research/experiments/ag2q9-cap-game-20261128/output/board_ag2q9.txt
  role: data
  note: AG(2,9) 盤（81 点・90 直線）
- path: research/experiments/ag2q9-cap-game-20261128/scripts/cone_ag2q9.py
  role: solver
  note: 錐 DP ＋ 枠二重数え上げ
- path: research/experiments/ag2q9-cap-game-20261128/output/ag2q9_spectrum.json
  role: data
  note: サイズ別 Grundy 分布
- path: research/experiments/ag2q9-cap-game-20261128/README.md
  role: log
  note: 結果と再現手順
scope: AG(2,9)（81 点、90 直線）の s=2 キャップ・ゲーム全 63,277,282 局面の Grundy 値のサイズ別完全スペクトル。独立検証（全項目 PASS）では、盤の独立構築と添字一致、AGL(2,9) の三角形への単純推移（466,560 順序三角形）、錐の完全性（21,353 と別 DFS 一致）、14 クラス各 12 個のグローバルサンプル 168/168 一致、総数・mex 連鎖の再現。F のビット表記（{0,9,1}）は README の文字座標 (1,0),(0,1)（ビット {0,27,3}）と異なるが同じ AGL 軌道で分布は同一（検証で確認）。
evidence: 盤は GF(9) 上で構築し、全 3,240 点対が一意な直線上にあることを確認。3-キャップ F = ビット {0,9,1}（親盤の添字で (0,0),(i,0),(0,i)）の錐（21,353 局面）で完全 DP を行い、AGL(2,9) の三角形への推移性と Grundy 不変性から N_m(g)=N_3·T_m(g)/C(m,3)（N_3=77,760）で全サイズ分布を得た。k=0,1,2 は mex 連鎖。結果は k=3 全 G=1、k=4 全 G=0、k=5 は G=1 7,861,536 と G=3 466,560、k=6 は G=0 12,216,096 / G=1 77,760 / G=2 13,996,800、k=7 は G=0 2,566,080 / G=1 21,228,480、k=8 は G=0 3,353,400 / G=1 58,320、k=9 は G=0 6,480 / G=1 233,280、k=10 全 G=0。合計 63,277,282、G0 19,276,705 / G1 29,537,217 / G2 13,996,800 / G3 466,560。
---

# AG(2,9) s=2 の完全 Grundy スペクトル

| k | 個数 | Grundy 分布 |
|---:|---:|---|
| 0 | 1 | G0: 1 |
| 1 | 81 | G1: 81 |
| 2 | 3,240 | G0: 3,240 |
| 3 | 77,760 | G1: 77,760 |
| 4 | 1,108,080 | G0: 1,108,080 |
| 5 | 8,328,096 | G1: 7,861,536 / **G3: 466,560** |
| 6 | 26,290,656 | G0: 12,216,096 / G1: 77,760 / G2: 13,996,800 |
| 7 | 23,794,560 | G0: 2,566,080 / G1: 21,228,480 |
| 8 | 3,411,720 | G0: 3,353,400 / G1: 58,320 |
| 9 | 239,760 | G0: 6,480 / G1: 233,280 |
| 10 | 23,328 | G0: 23,328 |

- 全 63,277,282 局面: **G0 19,276,705 / G1 29,537,217 / G2 13,996,800 / G3 466,560**。
- **最大 Grundy は 3**（5-キャップの 466,560 個）。計算済みの s=2 の AG(2,q) 系列では
  q=8 まで最大 2 だったので、**q=9 で初めて 3 が現れる**。
- PG(2,9) s=2（最大 2）との対比で、アフィン盤の方が高い Grundy を持つ。
