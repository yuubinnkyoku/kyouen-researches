---
id: K0163
title: 最大配置の分類を完全保存しても勝者は変わる
kind: proposition
status: computed
topics:
- variants
aliases:
- B255
relations: []
artifacts:
- path: research/experiments/original-claims/reports/round20-b255-maximum-preserving-flip.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-2026-09-27.md
  role: source
  note: B255の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round20_b255_verified.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round20_b255_n5.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round20_b255_n5.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: この節では盤点を固定して禁止4点族だけを変える。標準版での局面ラベルをそのまま流用しない。
evidence: 原文監査 SUPPORTED / finite_witness_and_minimum_board_proof
---

# 最大配置の分類を完全保存しても勝者は変わる

対象命題: 最大配置の分類を完全保存しても勝者は変わる。 Q_nを削ったゲームで最大サイズ・全最大配置族が標準版と一致するのに、空盤勝者が反転する。

適用文脈: この節では盤点を固定して禁止4点族だけを変える。標準版での局面ラベルをそのまま流用しない。

現在の結論: 5×5で19禁止四点を外し、最大サイズ9と全100最大安全配置を完全保存しつつ空盤g1→0。n≤4では不可能、最小正方形盤5。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
