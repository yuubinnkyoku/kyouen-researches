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
artifacts:
- path: research/verification/round54-small-board-saturation-jump.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-2026-09-27.md
  role: source
  note: B097の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 本文の原文量化と現在の採用境界
evidence: 原文監査 PARTIAL / complete_finite_saturation_sequence
---

# s_nは単調増加する

未確定の命題: s_nは単調増加する。 `s_{n+1}≥s_n`。盤を広げると新しい小型の飽和機構が生じて逆転する、という可能性との境界を探す。

現在の結論: s1..9=[1,3,5,5,5,6,7,8,9]、s10∈[9,10]なのでn1..10の非減少性は確認。全nへは未証明。

採用境界: 完全値s1..s9=1,3,5,5,5,6,7,8,9、十盤八石全域除外でs10∈[9,10]。有限n1..10の単調性まで確認、全nの原文は未決。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
