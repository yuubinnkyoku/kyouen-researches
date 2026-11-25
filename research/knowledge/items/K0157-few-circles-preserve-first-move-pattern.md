---
id: K0157
title: 少数の円だけで標準版の初手分類を再現できる
kind: proposition
status: computed
topics:
- variants
aliases:
- B224
relations: []
artifacts:
- path: research/experiments/original-claims/reports/round21-b224-ten-curves.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-2026-09-27.md
  role: source
  note: B224の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round21_b224_verified.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round21_b224_witness.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round21_b224_search.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: この節だけは派生ゲーム。標準ルールでの結論と混ぜない。円のみ版は4共線を許すが、4点が非退化円上にある場合は禁止する。
evidence: 原文監査 SUPPORTED / finite_witness
---

# 少数の円だけで標準版の初手分類を再現できる

対象命題: 少数の円だけで標準版の初手分類を再現できる。 小盤n≥4で、円・直線を一部選んだ禁止族が、全標準禁止族と同じW_nを持つ。

適用文脈: この節だけは派生ゲーム。標準ルールでの結論と混ぜない。円のみ版は4共線を許すが、4点が非退化円上にある場合は禁止する。

現在の結論: 5×5で真円四本・直線六本の計十曲線を残すと、勝ち初手九点を完全保存する。全曲線削除後の自明な空の勝ち集合ではなく、標準の非空分類を保持。最小本数とは主張しない。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
