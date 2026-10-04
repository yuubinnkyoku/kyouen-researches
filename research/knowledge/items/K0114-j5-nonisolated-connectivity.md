---
id: K0114
title: 5×5のJ_5の非孤立部分は連結
kind: proposition
status: computed
topics:
- residual-games
- first-moves
aliases:
- B011
relations:
- type: depends_on
  target: K0108
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round27-fixed-response-audit.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-2026-09-27.md
  role: source
  note: B011の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round27_pairing_verified.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round27_pairing_audited.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round27_response_graphs.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: この節のJ_nは、盤点を頂点、`g({p,q})=0` を辺とするグラフ。初手勝ちの頂点が孤立点になること自体は再帰定義からの帰結なので候補に数えない。
evidence: 原文監査 SUPPORTED / finite_complete_classification_and_witness
---

# 5×5のJ_5の非孤立部分は連結

対象命題: 5×5のJ_5の非孤立部分は連結。 20本のPペアは独立した局所罠の寄せ集めではなく、一つの応答構造を作っている可能性。

適用文脈: この節のJ_nは、盤点を頂点、`g({p,q})=0` を辺とするグラフ。初手勝ちの頂点が孤立点になること自体は再帰定義からの帰結なので候補に数えない。

現在の結論: J5の非孤立16点・全20辺を再構成すると連結。残る九点は孤立。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
