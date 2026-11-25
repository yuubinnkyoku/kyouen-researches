---
id: K0190
title: 空盤で強制できる終局長はT*の中央値
kind: question
status: open
topics:
- strategy-length
- grundy
aliases:
- B335
relations:
- type: depends_on
  target: K0049
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
- path: research/archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B335の原文・定義（現在の結論は採用報告を優先）
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
scope: '起点: [個票02・T*とWFT](../../log/claim-audit/batch-02.md)。勝敗維持の協調的到達可能性と、相手に逆らわれても手数を強制できることを区別する。'
evidence: 原文監査 PARTIAL / finite_complete_classification
---

# 空盤で強制できる終局長はT*の中央値

未確定の命題: 空盤で強制できる終局長はT*の中央値。 WFT(∅)が単元のとき、その値はT*(∅)を昇順に並べた中央の値に一致する。偶数個なら中央二値のいずれかとする。

適用文脈: 起点: [個票02・T*とWFT](../../log/claim-audit/batch-02.md)。勝敗維持の協調的到達可能性と、相手に逆らわれても手数を強制できることを区別する。

現在の結論: n≤6の空盤WFT単元とT*中央値は一致、n7はWFT空で条件外。全盤一般には未証明。

採用境界: 7×7までの一石・飽和・J・空盤WFTを完全検査したが、原文の無界全称は未証明。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。

## 2026-10-17 bounded advance

New finite evidence: empty-board K0190 holds for n=1..6 (WFT singleton equals median of T*). n=7 has empty WFT, antecedent false. Generalization to arbitrary positions is false: 8 violations among n=6 5-stone positions with T*={6,8,10}, WFT={6}.

Scope clarification: K0190 is an empty-board-only claim; arbitrary-position median extension refuted.

Next steps: test n>=8 empty boards. Status remains open.

## 2026-10-17 bounded advance (round 4)

New finite evidence: median relation tested on non-empty n=7 positions with k<=3 (19,650 stored positions; 10,799 singleton-WFT). Violations: 0. Breakdown: k=1 49 stored/21 singleton/0 violations; k=2 1,176/14/0; k=3 18,424/10,764/0. Primary and independent layer files identical for k<=3. 857 singleton positions have even |T*|, all satisfy central-value condition. Empty board (k=0) has T*={8,10,12,14}, WFT empty, so antecedent false.

Scope clarification: no violations within tested bound only; positions with >=4 stones not tested at per-state resolution. Does not establish K0190 for all n=7 positions. Broader arbitrary-position extension remains refuted by 8 five-stone 6x6 positions. Empty-board status unaffected (n=7 WFT empty). K0190 remains open.

Next steps: per-state T*/WFT data for higher layers or general proof. Status remains open.

統合監査（2026-10-20）: 上記2026-10-17の追記はローカル研究時点の報告であり、今回すべての探索・測定を再実行したものではない。再検証の範囲は `research/experiments/local-main-integration-20261020/README.md` に記す。既存の未解決性・量化の限界を維持する。
