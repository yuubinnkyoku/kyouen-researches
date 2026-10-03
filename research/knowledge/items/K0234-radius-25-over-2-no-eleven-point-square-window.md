---
id: K0234
title: 半径二乗25/2の12点円は、正方形窓で11点だけを残せない
kind: proposition
status: proved
topics:
- geometry
aliases:
- B461
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
  note: B461の原文・定義（現在の結論は採用報告を優先）
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
evidence: 原文監査 SUPPORTED / general_proof
---

# 半径二乗25/2の12点円は、正方形窓で11点だけを残せない

対象命題: 半径二乗25/2の12点円は、正方形窓で11点だけを残せない。 一般の11点円の不存在ではなく、この具体的な族の切断制約に絞る。

適用文脈: 起点: [個票07・点数スペクトルと境界切断](verification/batch-07.md)。円Cの完全な格子点集合を固定し、整数座標の軸平行正方形窓に入る点数の集合をA(C)とする。

現在の結論: 半径二乗25/2の完全十二点円の整数正方形窓スペクトルに11はない。盤内十点と十二点の同半径族を混同しない。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
