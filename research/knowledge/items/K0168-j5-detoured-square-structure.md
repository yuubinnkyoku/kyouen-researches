---
id: K0168
title: J_5は四角形の各辺に長さ4の迂回路を添えたグラフ
kind: proposition
status: computed
topics:
- residual-games
- first-moves
aliases:
- B301
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
- path: research/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B301の原文・定義（現在の結論は採用報告を優先）
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
scope: '起点: [個票01・B011〜B020](verification/batch-01.md)。既知の連結性・完全マッチング・Aut=D4そのものは再提案しない。'
evidence: 原文監査 SUPPORTED / finite_complete_classification_and_witness
---

# J_5は四角形の各辺に長さ4の迂回路を添えたグラフ

対象命題: J_5は四角形の各辺に長さ4の迂回路を添えたグラフ。 非孤立部分の次数2頂点をすべて抑制すると、各辺が2重になった4サイクルになる。20辺の表を一つの形に圧縮する候補。

適用文脈: 起点: [個票01・B011〜B020](verification/batch-01.md)。既知の連結性・完全マッチング・Aut=D4そのものは再提案しない。

現在の結論: 四隅の四サイクルの各辺に長さ四の迂回路を添えたJ5。次数二頂点を抑制すると各辺二重の四サイクルになる。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
