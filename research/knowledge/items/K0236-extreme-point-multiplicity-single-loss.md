---
id: K0236
title: 1点だけ失えるかは上下左右の極値点の重複度で決まる
kind: proposition
status: proved
topics:
- geometry
aliases:
- B463
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
  note: B463の原文・定義（現在の結論は採用報告を優先）
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

# 1点だけ失えるかは上下左右の極値点の重複度で決まる

対象命題: 1点だけ失えるかは上下左右の極値点の重複度で決まる。 完全円から正方形窓でm−1点を得られる条件を、4方向の端点個数と外接矩形の余裕で必要十分に記述できる。

適用文脈: 起点: [個票07・点数スペクトルと境界切断](verification/batch-07.md)。円Cの完全な格子点集合を固定し、整数座標の軸平行正方形窓に入る点数の集合をA(C)とする。

現在の結論: 完全円から一点だけを窓外にするには、その点が上下左右の少なくとも一つで唯一の極値点であることが必要十分。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
