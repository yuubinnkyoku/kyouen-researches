---
id: K0117
title: J_5の非孤立部分は二部グラフ
kind: proposition
status: refuted
topics:
- residual-games
- first-moves
aliases:
- B014
relations:
- type: depends_on
  target: K0108
  note: ''
artifacts:
- path: research/verification/round27-fixed-response-audit.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-2026-09-27.md
  role: source
  note: B014の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round27_pairing_verified.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round27_pairing_audited.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round27_response_graphs.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: この節のJ_nは、盤点を頂点、`g({p,q})=0` を辺とするグラフ。初手勝ちの頂点が孤立点になること自体は再帰定義からの帰結なので候補に数えない。
evidence: 原文監査 REFUTED / finite_complete_classification
---

# J_5の非孤立部分は二部グラフ

否定された命題: J_5の非孤立部分は二部グラフ。 市松色そのものとは異なる二分が必要かもしれない。成立すれば「負け初手への返し」を二群間の応答として説明できる。

適用文脈: この節のJ_nは、盤点を頂点、`g({p,q})=0` を辺とするグラフ。初手勝ちの頂点が孤立点になること自体は再帰定義からの帰結なので候補に数えない。

現在の結論: 非孤立部分は五サイクルを持ち、二部ではない。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
