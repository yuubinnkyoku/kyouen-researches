---
id: K0133
title: 点ごとの被覆重複には二次上限がある
kind: proposition
status: proved
topics:
- maximal-safe
- geometry
aliases:
- B072
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round45-cover-gap-and-sharp-overlap.md
  role: proof
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-2026-09-27.md
  role: source
  note: B072の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round45_cover_verified.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 本文の原文量化と現在の採用境界
evidence: 原文監査 SUPPORTED / general_geometric_proof_and_sharpness_certificates
---

# 点ごとの被覆重複には二次上限がある

対象命題: 点ごとの被覆重複には二次上限がある。 `b_S(p)≤floor(|S|(|S|−1)/6)`。B071が成立した場合の数量化候補であり、独立した経験則として扱わない。

現在の結論: 三点族の線形性と点対計数、異なる曲線の交点数で全盤証明。k≥4の改善上限−1、六石等号、二空点交差の最小石数6も検算。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
