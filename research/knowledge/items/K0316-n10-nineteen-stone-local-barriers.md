---
id: K0316
title: 10×10の既知19石近傍には安全20石が存在しない大きな局所障壁がある
kind: computation
status: computed
topics: [maximum-safe, reconfiguration, geometry]
aliases: []
relations:
- type: supports
  target: K0141
  note: 20石存在問題への局所的な否定結果
artifacts:
- path: research/saturation-20261003-extra.md
  role: source
  note: 3つの完全局所探索と19石K4族
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/verification/scripts/saturation_20261003_extra_exact_results.json
  role: data
  note: 完走節点数と不存在結果
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/verification/scripts/saturation_20261003_extra_union_neighborhood.cpp
  role: solver
  note: Uとの共通点を固定した完全探索
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
---

# 10×10の既知19石近傍には安全20石が存在しない大きな局所障壁がある

ある19石極大Tと10点以上を共有する安全20石は存在しない。ほぼ安全な20点集合Uについても、|S∩U|≥10を満たす安全集合の最大サイズは19。3探索は合計約8.42億節点を完全に処理した。

Uの唯一の禁止四点組Qから1点だけ除いた4つの19石極大は、一石交換で互いに移れるK4を作る。この局所障壁はK_10≤19という全域上界ではない。
