---
id: K0229
title: 分母が2の冪の円は奇分母の円より最小収容盤が小さい
kind: proposition
status: refuted
topics:
- geometry
aliases:
- B454
relations: []
artifacts:
- path: research/experiments/original-claims/reports/round12-b454-counterexample.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B454の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round12_circle_bbox_w161_power2.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round12_circle_bbox_w64.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round12_circle_bbox_verification.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票07・B131〜B137](../../log/claim-audit/batch-07.md)。分母に対する単調性は捨てる。半径が同じだが片側が0点という退化比較も除き、双方4格子点以上の円を主に扱う。'
evidence: 原文監査 REFUTED / finite_counterexample_and_exhaustion
---

# 分母が2の冪の円は奇分母の円より最小収容盤が小さい

否定された命題: 分母が2の冪の円は奇分母の円より最小収容盤が小さい。 同じ格子点数mを初めて実現する円を選ぶと、q=2^aの族の最小軸平行幅が奇数q≥3の族以下になる。

適用文脈: 起点: [個票07・B131〜B137](../../log/claim-audit/batch-07.md)。分母に対する単調性は捨てる。半径が同じだが片側が0点という退化比較も除き、双方4格子点以上の円を主に扱う。

現在の結論: 11点円で奇分母q11のスパン161を達成。全二冪分母候補を除外し、奇分母が常に劣るという比較を反証。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
