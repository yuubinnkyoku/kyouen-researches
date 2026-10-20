---
id: K0119
title: 後手勝ち正方形盤のJ_nは連結
kind: question
status: open
topics:
- residual-games
- first-moves
aliases:
- B016
relations:
- type: depends_on
  target: K0108
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round28-seven-board-original-verdicts.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-2026-09-27.md
  role: source
  note: B016の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round28_n7_audited.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round28_n7_layers.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round28_n7_independent.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: この節のJ_nは、盤点を頂点、`g({p,q})=0` を辺とするグラフ。初手勝ちの頂点が孤立点になること自体は再帰定義からの帰結なので候補に数えない。
evidence: 原文監査 PARTIAL / finite_complete_classification
---

# 後手勝ち正方形盤のJ_nは連結

未確定の命題: 後手勝ち正方形盤のJ_nは連結。 初手への勝ち応答が盤の別々の領域に分裂せず、一つの大域的ネットワークになる。

適用文脈: この節のJ_nは、盤点を頂点、`g({p,q})=0` を辺とするグラフ。初手勝ちの頂点が孤立点になること自体は再帰定義からの帰結なので候補に数えない。

現在の結論: n7のJは49頂点552辺で連結、n4も連結。全ての後手勝ち盤への一般証明はない。

採用境界: 7×7までの一石・飽和・J・空盤WFTを完全検査したが、原文の無界全称は未証明。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。

## 2026-10-17 bounded advance

New finite evidence: BFS connectivity of non-isolated J_n part for n=1..7: n=4 (16 vertices, 84 edges) connected; n=7 (49 vertices, 552 edges) connected; n=5 non-isolated part (16 vertices, 20 edges) connected with 9 isolated winning first moves. F-win all-first-move-winning boards have empty J_n (n=1,2,3,6,9). n=6 empty J inferred from 36/36 winning first moves.

Scope clarification: finite evidence n<=7 only; n=8,n=10 S-win untested; universal claim unproved. Status remains open (question kind).

統合監査（2026-10-20）: 上記2026-10-17の追記はローカル研究時点の報告であり、今回すべての探索・測定を再実行したものではない。再検証の範囲は `research/experiments/local-main-integration-20261020/README.md` に記す。既存の未解決性・量化の限界を維持する。
