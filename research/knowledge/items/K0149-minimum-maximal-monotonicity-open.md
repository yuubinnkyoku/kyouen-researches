---
id: K0149
title: s_nは単調増加する
kind: question
status: open
topics:
- maximal-safe
- geometry
aliases:
- B097
relations:
- type: depends_on
  target: K0026
  note: ''
- type: depends_on
  target: K0312
  note: 11盤の境界は単調性を証明も反証もしない
artifacts:
- path: research/experiments/original-claims/reports/round54-small-board-saturation-jump.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-2026-09-27.md
  role: source
  note: B097の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/saturation/reports/saturation-20261003.md
  role: source
  note: 8≤s_11≤10。n=10から11への非減少性はこの区間では決まらない
scope: 標準q=4のs_nの全nにわたる非減少性。
evidence: 原文監査 PARTIAL / complete_finite_saturation_sequence
---

# s_nは単調増加する

標準正方形盤で全nについてs_{n+1}≥s_nかは未証明。

s_1..s_9=[1,3,5,5,5,6,7,8,9]、9≤s_10≤10なのでn=1..10の有限系列は非減少と確認できる。最新の11盤は8≤s_11≤10であり、n=10から11への大小関係は未確定。

11盤の10石極大やn=11..15のn−1石構成は存在上界であって最小性の証明ではない。盤の包含だけからs_nの単調性を推論しない。
