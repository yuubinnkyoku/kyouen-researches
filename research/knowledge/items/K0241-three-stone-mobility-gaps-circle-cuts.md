---
id: K0241
title: 三石後の合法手数の欠落は少数の円切断型で説明できる
kind: proposition
status: proved
topics:
- geometry
aliases:
- B470
relations: []
artifacts:
- path: research/verification/round4-circle-windows.md
  role: proof
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B470の原文・定義（現在の結論は採用報告を優先）
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
evidence: 原文監査 SUPPORTED / general_reduction_and_finite_exhaustion
---

# 三石後の合法手数の欠落は少数の円切断型で説明できる

対象命題: 三石後の合法手数の欠落は少数の円切断型で説明できる。 n≤12の補完数スペクトルの穴を、それぞれ新しい全列挙でなく共通の窓切断補題から導ける。

適用文脈: 起点: [個票07・点数スペクトルと境界切断](verification/batch-07.md)。円Cの完全な格子点集合を固定し、整数座標の軸平行正方形窓に入る点数の集合をA(C)とする。

現在の結論: 候補縮約を証明しn≤12を整数全走査。11点の最初の盤は11×11。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
