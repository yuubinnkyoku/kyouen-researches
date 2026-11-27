---
id: K1368
title: "PG(2,7) s=3 完全Grundyスペクトラム (2錐法)"
date: 2026-11-27
status: published
type: experiment-result
scope: finite
tags: [pg2q7, s3, grundy-spectrum, two-cone, complete-enumeration]
related: [K1356, K1361, K1298, K1365]
verdict: "finite-complete"
---

# K1368: PG(2,7) s=3 のサイズ別Grundy完全スペクトラム

PG(2,7) (57点・57直線・各直線8点・F7) の s=3 共演ゲーム
(安全 = 各直線 ≤3点・通常プレイ・mex) の全安全局面の
サイズ別Grundy分布の**初測定** (有限完全・全列挙+恒等式)。

## 方法

2錐法 (K1353 単錐法の s=3 拡張・本測定で新規):
錐A (固定非共線3点組Fを含む全安全集合・75,876,952局面) と
錐B (固定共線3点組F'を含む全安全集合・52,197,741局面) を
ディスク列挙+radix sort+ボトムアップmex DP で完全計算し、

N_m(g)·C(m,3) = 26,068·D_m(g) + 3,192·D'_m(g)

(N3nc=26,068, N3c=57·C(8,3)=3,192) で合成。
m≤2 と空盤は鎖として直接計算。

## 主結果

- 総安全局面 15,387,092,450 (m=0..15)。最大安全サイズ 15 (N_15=78,204)。
- Grundy 範囲 0..6。g(∅)=1。m=4 全局面 G=2。m=9 の30%が G=5。
  m≥13 は G∈{0,1} に収束。
- 極大 N_m^max (m=9,11,12,13,14,15) =
  26,068 / 20,176,632 / 335,964,384 / 180,182,016 / 6,569,136 / 78,204。
- 完全表は kit の output/combined_fset0.json。

## 検証

整除性全(m,g)・解析アンカー m=3,4,5・F不変性 (fset再走全表一致)・
決定性 (byte同一)・独立Python層再現 (m≤7両錐)・tamper電池5種・
較正 (K1356/K1361 全セル一致)。詳細は kit README と完了log。

## 未解決・接続

- N_9^max = 26,068 = N3nc の数値一致の構造的説明 (偶然の可能性を含む)。
- K1365 補集合双対 (極大安全 ↔ 極小t-fold blocking) による
  PG(2,7) blocking set 数との相互照合。
- AG(2,7) s=3 (隣接盤) は未着手。
- 11×11 標準盤・root verdict は不消費 (全時点 UNKNOWN)。

## kit

research/experiments/pg2q7-s3-twocone-spectrum-20261127/
