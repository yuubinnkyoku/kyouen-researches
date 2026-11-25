---
id: K1330
title: "PG(2,8) の PΓL(3,8) キャップ軌道分類 — PGL の 17 軌道が 15 軌道に融合"
kind: computation
status: computed
topics: [geometry, maximum-safe]
aliases:
- PGammaL(3,8) cap orbits of PG(2,8)
- semilinear refinement of the cap orbit classification
relations:
- type: related
  target: K1327
  note: PGL(3,8) での全キャップ軌道分類（17 軌道）
- type: related
  target: K1329
  note: Frobenius が極大 6-キャップの 3 軌道を巡回置換し 1 軌道に融合
- type: related
  target: K1323
  note: conic 6-キャップの単一軌道
artifacts:
- path: research/experiments/pg2q8-cap-game-20261125/output/frob_caps.txt
  role: data
  note: conic 6-キャップ・非極大非 conic 6-キャップの Frobenius 像
- path: research/experiments/pg2q9-cap-game-20261125/scripts/orbit_bfs.c
  role: solver
  note: probe 付き軌道 BFS
- path: research/experiments/pg2q8-cap-game-20261125/output/orbits_all.txt
  role: data
  note: PGL 軌道サイズ（K1327）
scope: PG(2,8)（73 点、73 直線）上の全キャップ（k=1..10）と PΓL(3,8) = PGL(3,8) ⋊ C3 の作用。
evidence: PGL(3,8) の全キャップ軌道は K1327 の 17 軌道（k=1..5,10 は各 1、k=6 は 5、k=7,8,9 は各 2）。Frobenius φ(x,y,z)=(x²,y²,z²) について、conic 6-キャップ代表 {2,3,10,16,18,21} の φ 像 {2,5,10,12,18,23} は同じ conic 6-キャップ軌道（2,747,136）に属し、非極大非 conic 6-キャップ代表 {1,10,12,59,62,65} の φ 像 {1,10,14,29,32,33} は同じ非極大非 conic 軌道（4,120,704）に属する（probe 付き軌道 BFS で確認）。K1329 より極大 6-キャップの 3 軌道は φ で巡回置換され 1 軌道（2,060,352）に融合。他の融合が起きないのは、φ が conic 6-キャップ軌道と非極大非 conic 6-キャップ軌道をそれぞれ保存し（probe で確認）、極大 6-キャップの 3 軌道だけを巡回置換するからである（割り算だけでは不十分で、非極大+極大 3 軌道の和 6,181,056 は |PΓL|/8 で割り切れる）。よって **PΓL(3,8) の非空キャップ軌道は 15 個**（空を含めると 16 個。PGL は非空 17・空込み 18）で、k=1..5,10 は各 1、k=6 は 3、k=7,8,9 は各 2。
---

# PΓL(3,8) のキャップ軌道分類

## 結果

| k | PGL 軌道（K1327） | PΓL 軌道 |
|---:|---:|---:|
| 1 | 1 | 1 |
| 2 | 1 | 1 |
| 3 | 1 | 1 |
| 4 | 1 | 1 |
| 5 | 1 | 1 |
| 6 | 5 | **3**（conic／非極大非 conic／極大） |
| 7 | 2 | 2 |
| 8 | 2 | 2 |
| 9 | 2 | 2 |
| 10 | 1 | 1 |
| 合計 | 17 | **15** |

- 極大 6-キャップの 3 軌道（各 686,784）だけが Frobenius で融合し、
  1 軌道（2,060,352、固定群 24）になる。
- 他の軌道は Frobenius で不変（conic 6-キャップ、非極大非 conic 6-キャップを
  probe 付き軌道 BFS で確認）。他の融合は |PΓL| = 49,448,448 の割り算で不可能。
