---
id: K0312
title: 11×11の最小極大サイズは8≤s_11≤10
kind: proposition
status: computed
topics:
- maximal-safe
- geometry
aliases: []
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/experiments/saturation/reports/saturation-20261003.md
  role: source
  note: 10石極大証人と6・7石全域排除
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/experiments/saturation/output/saturation_20261003_exact_results.json
  role: data
  note: 11盤7石排除の完了計数
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/experiments/saturation/scripts/saturation_20261003_verify.py
  role: verifier
  note: 証人と幾何の独立検査
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
---

# 11×11の最小極大サイズは8≤s_11≤10

11×11に安全な10石極大配置が存在する。6石・7石極大は完全探索で全域排除され、7石排除の完了記録は1,501,466,264節点。

独立Python監査は座標証人・禁止幾何・完了フラグ・節点集計の整合性を検査する。15億節点の探索木を別実装で再探索したという意味ではない。

したがって8≤s_11≤10。8石または9石極大の存在は未確定で、探索の未発見を非存在として扱わない。
