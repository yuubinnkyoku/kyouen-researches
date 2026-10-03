---
id: K0243
title: 固定方向の主項係数は方向高さの三乗で減衰する
kind: proposition
status: proved
topics:
- geometry
aliases:
- B472
relations: []
artifacts:
- path: research/verification/round4-collinear-asymptotic.md
  role: proof
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B472の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round4_collinear_asymptotic.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round4_collinear_asymptotic.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票08](verification/batch-08.md)。有限範囲の次数フィットは動機にとどめる。D_nを共線四点数、C_nを非共線共円四点数とする。'
evidence: 原文監査 SUPPORTED / general_proof
---

# 固定方向の主項係数は方向高さの三乗で減衰する

対象命題: 固定方向の主項係数は方向高さの三乗で減衰する。 n→∞の方向別寄与をn^5で割った係数は、方向の比率に依存する有界関数をH(v)^3で割った形になる。

適用文脈: 起点: [個票08](verification/batch-08.md)。有限範囲の次数フィットは動機にとどめる。D_nを共線四点数、C_nを非共線共円四点数とする。

現在の結論: 原始方向高さH、r=min(|a|,|b|)/Hに対する主項係数は(5−3r)/(120H^3)。方向数と係数の収束を分ける。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
