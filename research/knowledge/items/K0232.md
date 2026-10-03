---
id: K0232
title: q≥3の円は境界に切られても点数を一つずつ変えやすい
kind: question
status: open
topics:
- geometry
aliases:
- B457
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
  note: B457の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round4_circle_windows.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round4_circle_windows.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票07・B131〜B137](verification/batch-07.md)。分母に対する単調性は捨てる。半径が同じだが片側が0点という退化比較も除き、双方4格子点以上の円を主に扱う。'
evidence: 原文監査 PARTIAL / partial_general_spectrum_result
---

# q≥3の円は境界に切られても点数を一つずつ変えやすい

未確定の命題: q≥3の円は境界に切られても点数を一つずつ変えやすい。 同じ完全円上点数で比べ、格子正方形の平行移動によって得られる盤内点数の種類がq≤2より多い。

適用文脈: 起点: [個票07・B131〜B137](verification/batch-07.md)。分母に対する単調性は捨てる。半径が同じだが片側が0点という退化比較も除き、双方4格子点以上の円を主に扱う。

現在の結論: 全サイズ和集合と固定窓の穴に一般結果。原文の同点数での統計比較は未完了。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
