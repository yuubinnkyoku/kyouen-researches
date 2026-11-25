---
id: K1327
title: "PG(2,8) の全キャップの PGL(3,8) 軌道分類 — k=6 は 5 軌道、k=7,8,9 は 2 軌道"
kind: computation
status: computed
topics: [geometry, maximum-safe]
aliases:
- complete orbit classification of caps in PG(2,8)
- PG(2,8) cap orbits by size
relations:
- type: related
  target: K1324
  note: 極大キャップ（6 と 10）の軌道。6-キャップの 3 極大軌道は本分類の一部
- type: related
  target: K1326
  note: 9-キャップの 2 軌道（本分類の特別な場合）
- type: related
  target: K1323
  note: 円錐曲線レイヤー（conic k-部分集合は各 k 単一軌道）
- type: related
  target: K1300
  note: PG(2,8) のキャップ国勢調査（サイズ別個数）
artifacts:
- path: research/experiments/pg2q8-cap-game-20261125/report.md
  role: log
  note: 全キャップ軌道表を含む総括
- path: research/experiments/pg2q9-cap-game-20261125/scripts/orbit_bfs.c
  role: solver
  note: 128-bit マスクの軌道 BFS
- path: research/experiments/pg2q8-cap-game-20261125/output/orbits_all.txt
  role: data
  note: k 別の軌道サイズ・固定群・国勢調査との一致
- path: research/experiments/pg2q8-cap-game-20261125/output/starts78.txt
  role: data
  note: 非 conic 7-キャップ・8-キャップの開始マスク
scope: PG(2,8)（73 点、73 直線）上の全キャップ（k=1..10）と PGL(3,8) の作用。軌道分解と固定群の位数。
evidence: PGL(3,8) 生成元 8 個（K1324 の gens.txt）による 128-bit マスク軌道 BFS。conic 部分集合は K1323 の PGL(2,8) 軌道（各 k 単一）から。非 conic の 7-キャップ {12,16,18,22,54,66,69} の軌道 2,747,136 = 全 7-キャップ 3,924,480 − conic 1,177,344、非 conic 8-キャップ {12,16,18,22,40,54,66,69} の軌道 1,177,344 = 1,471,680 − 294,336、非極大非 conic 6-キャップ {1,10,12,59,62,65} の軌道 4,120,704 = 6,181,056 − 2,060,352（極大 6 の 3 軌道）。これらと国勢調査（K1300）の全サイズ個数が一致し、**k=1..5,10 は 1 軌道、k=6 は 5 軌道、k=7,8,9 は 2 軌道**。軌道サイズはすべて |PGL(3,8)| = 16,482,816 を割り切り、固定群は 225792/6272/294/24/4/6/14/56/504 など。付記として、極大 6-キャップの 3 類は secant 本数分布 {1:36,2:24,3:7} が一致し、この不変量では分離できない。
---

# PG(2,8) の全キャップの軌道分類

## 軌道表

| k | 軌道 | サイズ（固定群） |
|---:|---|---|
| 1 | 1 | 73 (225792) |
| 2 | 1 | 2,628 (6272) |
| 3 | 1 | 56,064 (294) |
| 4 | 1 | 686,784 (24) |
| 5 | 1 | 4,120,704 (4) |
| 6 | **5** | conic 2,747,136 (6)／非極大非 conic 4,120,704 (4)／極大 3×686,784 (24) |
| 7 | 2 | conic 1,177,344 (14)／非 conic 2,747,136 (6) |
| 8 | 2 | conic 294,336 (56)／非 conic 1,177,344 (14) |
| 9 | 2 | conic 32,704 (504)／非 conic 294,336 (56) |
| 10 | 1 | 32,704 (504) |

- 各サイズの合計は国勢調査（K1300）と一致（総計 19,550,350）。
- k=3,4,5 は全キャップが conic（任意の 5 点は一意な conic 上）。
- k=6 だけが 5 軌道：conic 6-部分集合、非極大非 conic、極大 3 類。
- k=7,8,9 は conic 部分集合と非 conic の 2 軌道ずつ。

## 方法

- conic 部分集合は K1323 の PGL(2,8) 軌道（各 k 単一）。
- 非 conic の k=6,7,8,9 は代表を 1 個取り、PGL(3,8) 生成元で軌道 BFS。
  軌道サイズが「全個数 − conic 個数」と一致することで単一軌道を確認。
