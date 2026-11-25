---
id: K0237
title: 長方形窓なら実現する点数が正方形窓では実現しない
kind: proposition
status: refuted
topics:
- geometry
aliases:
- B464
relations: []
artifacts:
- path: research/experiments/original-claims/reports/round4-circle-windows.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B464の原文・定義（現在の結論は採用報告を優先）
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
evidence: 原文監査 REFUTED / general_impossibility
---

# 長方形窓なら実現する点数が正方形窓では実現しない

否定された命題: 長方形窓なら実現する点数が正方形窓では実現しない。 同じ円Cについて、窓の縦横比を変えるだけでA(C)の穴が埋まる例がある。

適用文脈: 起点: [個票07・点数スペクトルと境界切断](../../log/claim-audit/batch-07.md)。円Cの完全な格子点集合を固定し、整数座標の軸平行正方形窓に入る点数の集合をA(C)とする。

現在の結論: 完全格子円の長方形整数窓と正方形整数窓で実現点数のスペクトルは常に同じ。長方形だけの点数はない。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
