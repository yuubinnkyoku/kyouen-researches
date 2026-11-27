---
id: K1346
title: "W_24 s=7 の G=2/G=0 層はドデカッドの 9-/11-部分集合 — 個数一致とサンプル検証"
kind: proposition
status: proved
topics: [grundy, geometry]
aliases:
- dodecad layers of the W_24 s=7 Grundy 2 positions
- 566720 = 2576*C(12,9) and 30912 = 2576*C(12,11)
relations:
- type: related
  target: K1342
  note: W_24 s=7 のサイズ別分解（G=2 566,720 はサイズ 9、G=0 30,912 はサイズ 11）
- type: related
  target: K1293
  note: ドデカッド 2,576（Golay 重み 12 語、サイズ 12 の極大キャップ）
- type: related
  target: K1343
  note: s≤6 のサイズ一様性
artifacts:
- path: research/experiments/witt-s-spectrum-20261125/independent_gsize/comparison_results.txt
  role: log
  note: 105/105 チェック PASS の独立検証（s=1..6 一様性・s=7 GSIZE）
- path: research/experiments/w24-s7-dodecad-20261127/README.md
  role: log
  note: ドデカッド仮説のサンプル検証（本ラウンド）
scope: W_24 s=7 の Grundy 2/0 層とドデカッド（Golay 重み 12 語）の関係。
evidence: ドデカッド 2,576 個（759 オクタッドの F2 張から再計算、重み分布 {0:1,8:759,12:2576,16:759,24:1}）の 9-部分集合は 566,720 個（すべて相異なる）で、s=7 のサイズ 9 の G=2 個数 566,720 と一致。11-部分集合は 30,912 個（相異なる）で、サイズ 11 の G=0 個数 30,912 と一致。サンプル検証では、ドデカッド 9-部分集合 5 個はすべて G=2、非ドデカッド 9-キャップ 5 個はすべて G=1、ドデカッド 11-部分集合 5 個はすべて G=0、非ドデカッド 11-キャップ 5 個はすべて G=2。**全数検証（fullcheck.c）** では 566,720 個の 9-部分集合すべてが G=2、30,912 個の 11-部分集合すべてが G=0（他の値なし）。G=2 の総数 566,720 と G=0（サイズ 11）の総数 30,912 がそれぞれと一致するので、**集合レベルで完全一致**。
---

# W_24 s=7 のドデカッド層

- ドデカッドは Golay コードの重み 12 語（2,576 個）で、W_24 s=6 のサイズ 12 極大キャップ。
- ドデカッドの 9-部分集合 566,720 個 = サイズ 9 の G=2 個数。
- ドデカッドの 11-部分集合 30,912 個 = サイズ 11 の G=0 個数。
- サンプル検証（各 5 個、完全 DP）:
  - ドデカッド 9-部分集合 → G=2、非ドデカッド 9-キャップ → G=1。
  - ドデカッド 11-部分集合 → G=0、非ドデカッド 11-キャップ → G=2。

## 注意

- 全数検証（fullcheck.c）で集合レベルの完全一致を確認: 9-部分集合はすべて G=2、11-部分集合はすべて G=0。
