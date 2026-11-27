---
id: K1348
title: "W_24 s=7 のドデカッド 3 層 — 9/10/11-部分集合の Grundy は 2/1/0"
kind: proposition
status: proved
topics: [grundy, geometry]
aliases:
- three dodecad layers of the W_24 s=7 Grundy spectrum
- G(k)=2,1,0 for dodecad k-subsets (k=9,10,11)
relations:
- type: related
  target: K1346
  note: ドデカッド 9-/11-部分集合の G=2/G=0 層（全数検証）
- type: related
  target: K1347
  note: 極大 13-キャップの 11-部分集合 66/12 分割
- type: related
  target: K1342
  note: W_24 s=7 のサイズ別分解（サイズ 10 は G=0 1,700,160 / G=1 170,016）
artifacts:
- path: research/experiments/w24-s7-dodecad-20261127/fullcheck.c
  role: solver
  note: 全数検証（9/11-部分集合 + 10-部分集合版 fullcheck10.c）
- path: research/experiments/w24-s7-dodecad-20261127/fullcheck10.c
  role: solver
  note: 10-部分集合の全数検証
- path: research/experiments/w24-s7-dodecad-20261127/results.txt
  role: data
  note: 全数検証の結果
scope: W_24 s=7 におけるドデカッド（Golay 重み 12 語、2,576 個）の 9-/10-/11-部分集合の Grundy と、サイズ別分解との集合一致。
evidence: ドデカッド 2,576 個の k-部分集合（k=9,10,11）を全数 DP で計算。9-部分集合 566,720 個はすべて G=2、10-部分集合 170,016 個はすべて G=1、11-部分集合 30,912 個はすべて G=0。各 k で G 層の総数（K1342: サイズ 9 G=2 566,720、サイズ 10 G=1 170,016、サイズ 11 G=0 30,912）と一致するので、**G 層はそれぞれドデカッドの k-部分集合全体と集合一致**。個数は 2,576×C(12,9)=566,720、2,576×C(12,10)=170,016、2,576×C(12,11)=30,912。パターンは k=9,10,11 で G=(11−k) mod 3 = 2,1,0。
---

# ドデカッド 3 層

| k | 個数 | Grundy | G 層総数 |
|---:|---:|---:|---:|
| 9 | 566,720 | **2** | 566,720 |
| 10 | 170,016 | **1** | 170,016 |
| 11 | 30,912 | **0** | 30,912 |
| 12 | 2,576 | 0（極大・終端） | — |

- k=9,10,11 で **G = (11−k) mod 3 = 2, 1, 0**。
- 各 k の G 層は**ドデカッドの k-部分集合全体**と集合一致（個数と全数検証）。
- ドデカッド自身（k=12）は極大キャップで G=0（終端）。
