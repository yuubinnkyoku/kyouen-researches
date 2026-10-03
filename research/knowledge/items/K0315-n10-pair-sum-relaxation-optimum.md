---
id: K0315
title: 10×10で行・列の点対和制約だけを課した緩和問題の最大値は23
kind: proposition
status: proved
topics: [maximum-safe, geometry]
aliases: []
relations:
- type: depends_on
  target: K0141
  note: K_10上界23をこの制約だけでは改善できないことを示す
artifacts:
- path: research/saturation-20261003.md
  role: proof
  note: 23点緩和証人と既知上界
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/verification/scripts/saturation_20261003_verified.json
  role: data
  note: 行列双方の点対和と違反四点の検査
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
---

# 10×10で行・列の点対和制約だけを課した緩和問題の最大値は23

各行・各列3石以下とし、同じ向きの行内・列内点対和が重複しないという必要条件を両方向に課しても、23点配置が存在する。既知の一方向上界23と一致するため、この緩和問題の最適値は23。

この23点集合は標準ゲームでは多数の禁止四点組を含み安全でない。従ってK_10≥23ではなく、K_10≤22を示すには別の幾何制約が必要だと分かる。
