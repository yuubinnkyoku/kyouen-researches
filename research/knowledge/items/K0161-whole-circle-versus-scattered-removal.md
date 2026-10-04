---
id: K0161
title: 円一つの禁止解除が、同数のばらばらな解除より強く効く
kind: proposition
status: computed
topics:
- variants
aliases:
- B252
relations: []
artifacts:
- path: research/experiments/original-claims/reports/round22-b252-one-circle-versus-scattered.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-2026-09-27.md
  role: source
  note: B252の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round22_b252_verified.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round22_b252_n4_all_geometry.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round22_b252_n4_all_scan.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: この節では盤点を固定して禁止4点族だけを変える。標準版での局面ラベルをそのまま流用しない。
evidence: 原文監査 SUPPORTED / finite_witness
---

# 円一つの禁止解除が、同数のばらばらな解除より強く効く

対象命題: 円一つの禁止解除が、同数のばらばらな解除より強く効く。 同じ数の四点禁止を外しても、同一円にまとまった解除でだけ勝者が変わる例がある。

適用文脈: この節では盤点を固定して禁止4点族だけを変える。標準版での局面ラベルをそのまま流用しない。

現在の結論: 4×4中央八点円の全70禁止四点を解除するとg0→1。同数の散在した70解除では勝者保存。これは存在比較で、どんな円がどんな散在解除より強いという全称ではない。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
