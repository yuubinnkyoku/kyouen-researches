---
id: K0165
title: 最小勝敗保持禁止族に共通する必須四点型がある
kind: proposition
status: scope-unclear
topics:
- variants
aliases:
- B258
relations: []
artifacts:
- path: research/verification/round23-b256-symmetric-minimum.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-2026-09-27.md
  role: source
  note: B258の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round23_minimum_family_verified.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round23_minimum_family.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: この節では盤点を固定して禁止4点族だけを変える。標準版での局面ラベルをそのまま流用しない。
evidence: 原文監査 SCOPE_UNCLEAR / general_result_with_quantifier_ambiguity
---

# 最小勝敗保持禁止族に共通する必須四点型がある

対象命題: 最小勝敗保持禁止族に共通する必須四点型がある。 同じ盤の異なる最小部分族のすべてに現れるD4四点型があり、それが勝敗の説明の核になる。

適用文脈: この節では盤点を固定して禁止4点族だけを変える。標準版での局面ラベルをそのまま流用しない。

現在の結論: 全n≥4共通の必須型はない。他方、存在量化にn2を含めれば唯一の四点組で自明に真。量化を指定しない原文全体は判定保留。

採用境界: 全n≥4に共通必須型なし。n=2を存在量化に含む読みは自明に真で、全体判定は保留。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
