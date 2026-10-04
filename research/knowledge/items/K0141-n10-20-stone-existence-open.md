---
id: K0141
title: 10×10では20石まで届くか
kind: question
status: open
topics:
- maximum-safe
- geometry
aliases:
- B082
relations:
- type: depends_on
  target: K0026
  note: ''
- type: depends_on
  target: K0035
  note: 現行の全域上下界19≤K_10≤23
- type: depends_on
  target: K0316
  note: 完全局所排除は20石存在問題の一部だけを制限する
artifacts:
- path: research/experiments/original-claims/reports/round57-nineteen-stone-ten-board-bound.md
  role: source
  note: 19石証人と一般上界23
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/saturation/reports/saturation-20261003-extra.md
  role: source
  note: 複数19石極大と20石への局所非存在
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/experiments/saturation/output/saturation_20261003_extra_exact_results.json
  role: data
  note: 約8.42億節点の3完全探索結果
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: B082の原文監査
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 安全20石の存在（K_10≥20）を問う。旧B082の等号K_10=20にはさらに全域上界20が必要。
evidence: 19≤K_10≤23。既知19石近傍とほぼ安全20点集合Uの広い近傍に安全20石なし。
---

# 10×10では20石まで届くか

安全19石は複数系統で存在し、一般上界は23。20石の存在は未決着。

本項の存在問題はK_10≥20である。旧alias B082の等号K_10=20まで確定するには、20石証人に加えて全域上界20も必要である。

ある19石極大Tと10点以上を共有する安全20石は存在せず、ほぼ安全な20点集合Uについても|S∩U|≥10を満たす安全集合の最大サイズは19と完全計算された。20石が存在するならこれらの核から大規模な交換が必要だが、局所排除をK_10≤19へ拡張してはいけない。
