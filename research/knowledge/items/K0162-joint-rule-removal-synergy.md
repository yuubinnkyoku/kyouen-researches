---
id: K0162
title: 各禁止を単独解除しても不変だが同時解除で反転する
kind: proposition
status: computed
topics:
- variants
aliases:
- B253
relations: []
artifacts:
- path: research/experiments/original-claims/reports/round19-rule-removal-audit.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-2026-09-27.md
  role: source
  note: B253の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round19_rule_certificates.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round19_rule_pair_lower.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round19_rule_certificates.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: この節では盤点を固定して禁止4点族だけを変える。標準版での局面ラベルをそのまま流用しない。
evidence: 原文監査 SUPPORTED / finite_witness_and_exhaustion
---

# 各禁止を単独解除しても不変だが同時解除で反転する

対象命題: 各禁止を単独解除しても不変だが同時解除で反転する。 Q_nの小さい部分族Eで、Eの真部分集合の解除では空盤勝者が変わらず、E全体の解除で初めて変わる。

適用文脈: この節では盤点を固定して禁止4点族だけを変える。標準版での局面ラベルをそのまま流用しない。

現在の結論: 全単独・全ペア解除を除外し、三組解除の全真部分族と真のmexを検算。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
