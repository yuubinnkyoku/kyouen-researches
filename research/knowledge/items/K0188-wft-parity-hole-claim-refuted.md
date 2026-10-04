---
id: K0188
title: WFT(S)の同じ偶奇の穴はない
kind: proposition
status: refuted
topics:
- strategy-length
- grundy
aliases:
- B333
relations:
- type: depends_on
  target: K0049
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round25-forced-length-holes.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B333の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round25_forced_verified.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round25_forced_n6.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round25_forced_lengths.cpp
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票02・T*とWFT](../../log/claim-audit/batch-02.md)。勝敗維持の協調的到達可能性と、相手に逆らわれても手数を強制できることを区別する。'
evidence: 原文監査 REFUTED / finite_counterexample_and_minimum_board_proof
---

# WFT(S)の同じ偶奇の穴はない

否定された命題: WFT(S)の同じ偶奇の穴はない。 tとt+4以上を強制できるなら、その間の同じ偶奇の手数もすべて強制できる。

適用文脈: 起点: [個票02・T*とWFT](../../log/claim-audit/batch-02.md)。勝敗維持の協調的到達可能性と、相手に逆らわれても手数を強制できることを区別する。

現在の結論: n6にWFT={7,11}の局面があり9が欠ける。T*とWFTを同じ定義にしない。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
