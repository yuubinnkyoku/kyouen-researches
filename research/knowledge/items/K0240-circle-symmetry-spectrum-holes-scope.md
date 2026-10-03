---
id: K0240
title: 高い対称性を持つ円ほど点数スペクトルの穴が多い
kind: proposition
status: scope-unclear
topics:
- geometry
aliases:
- B468
relations: []
artifacts:
- path: research/verification/round4-circle-windows.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B468の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round4_circle_windows.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round4_circle_windows.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票07・点数スペクトルと境界切断](verification/batch-07.md)。円Cの完全な格子点集合を固定し、整数座標の軸平行正方形窓に入る点数の集合をA(C)とする。'
evidence: 原文監査 SCOPE_UNCLEAR / counterexample_to_monotonic_reading
---

# 高い対称性を持つ円ほど点数スペクトルの穴が多い

対象命題: 高い対称性を持つ円ほど点数スペクトルの穴が多い。 完全点数・外接矩形幅をそろえ、円上点集合の格子対称性が大きい族ほどA(C)が疎になる。

適用文脈: 起点: [個票07・点数スペクトルと境界切断](verification/batch-07.md)。円Cの完全な格子点集合を固定し、整数座標の軸平行正方形窓に入る点数の集合をA(C)とする。

現在の結論: 同完全点数・同スパンでも対称性→穴数の単調性には反例。統計的傾向という読みには母集団指定が必要。

採用境界: 同完全点数・同スパンで単調性の反例。統計傾向には追加の母集団指定が必要。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
