---
id: K0192
title: 残余三点制約が一つでも、それを外すと必勝手が全交換される
kind: proposition
status: computed
topics:
- residual-games
- reconfiguration
aliases:
- B343
relations:
- type: depends_on
  target: K0108
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round33-b343-single-triple-switch.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B343の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round33_b343_verified.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round33_b343_n6_sole.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round33_b343_search.cpp
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票03・B051〜B058](../../log/claim-audit/batch-03.md)、[個票04・B064〜B068](../../log/claim-audit/batch-04.md)。孤立点だけによる退化例は除いて考える。'
evidence: 原文監査 SUPPORTED / finite_witness_with_sole_triple_and_full_certificate
---

# 残余三点制約が一つでも、それを外すと必勝手が全交換される

対象命題: 残余三点制約が一つでも、それを外すと必勝手が全交換される。 両版ともNだが、Pへ行く合法手集合が互いに素になる。

適用文脈: 起点: [個票03・B051〜B058](../../log/claim-audit/batch-03.md)、[個票04・B064〜B068](../../log/claim-audit/batch-04.md)。孤立点だけによる退化例は除いて考える。

現在の結論: 6×6で残余三点辺がちょうど一つ。単独解除でg1→3、勝ち手{14}→{15,19}が互いに素。全256拡張の独立mex一致。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
