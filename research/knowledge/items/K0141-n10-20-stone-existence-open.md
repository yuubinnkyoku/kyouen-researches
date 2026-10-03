---
id: K0141
title: 10×10では20石まで届く
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
artifacts:
- path: research/verification/round57-nineteen-stone-ten-board-bound.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-2026-09-27.md
  role: source
  note: B082の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 本文の原文量化と現在の採用境界
evidence: 原文監査 PARTIAL / independent_nineteen_stone_extension_and_local_exclusion
---

# 10×10では20石まで届く

未確定の命題: 10×10では20石まで届く。 `K_10=20`。単純な `2n−1` の再現より、7×7と同種の上振れを予想する分岐。

現在の結論: 安全19石を独立全3876四点検算、一般上界23。特定19石から除去≤9の20石延長は全域なしだが、一般20石存在を決着させない。

採用境界: 公開九盤18石を移動して一点追加、全3876四点組で十盤19石安全。行内点対上界23。特定19石から除去9まで完全に20石なし、一般20石の不在や等号20は未証明。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
