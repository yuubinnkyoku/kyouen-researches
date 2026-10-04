---
id: K0239
title: 円の窓点数スペクトルは円周上の点の座標順序で決まる
kind: proposition
status: proved
topics:
- geometry
aliases:
- B467
relations: []
artifacts:
- path: research/experiments/original-claims/reports/round4-circle-windows.md
  role: proof
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B467の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round4_circle_windows.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round4_circle_windows.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票07・点数スペクトルと境界切断](../../log/claim-audit/batch-07.md)。円Cの完全な格子点集合を固定し、整数座標の軸平行正方形窓に入る点数の集合をA(C)とする。'
evidence: 原文監査 SUPPORTED / general_proof
---

# 円の窓点数スペクトルは円周上の点の座標順序で決まる

対象命題: 円の窓点数スペクトルは円周上の点の座標順序で決まる。 半径・中心そのものを使わず、x順位・y順位と間隔の大小関係からA(C)を計算する有限組合せ型を作れる。

適用文脈: 起点: [個票07・点数スペクトルと境界切断](../../log/claim-audit/batch-07.md)。円Cの完全な格子点集合を固定し、整数座標の軸平行正方形窓に入る点数の集合をA(C)とする。

現在の結論: 完全円の可変サイズ整数窓のスペクトルと一点削除の必要十分条件。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
