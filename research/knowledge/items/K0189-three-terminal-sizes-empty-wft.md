---
id: K0189
title: T*(S)が3種類でもWFT(S)は空
kind: proposition
status: computed
topics:
- strategy-length
- grundy
aliases:
- B334
relations:
- type: depends_on
  target: K0049
  note: ''
artifacts:
- path: research/verification/round25-forced-length-holes.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B334の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round25_forced_verified.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round25_forced_n6.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round25_forced_lengths.cpp
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票02・T*とWFT](verification/batch-02.md)。勝敗維持の協調的到達可能性と、相手に逆らわれても手数を強制できることを区別する。'
evidence: 原文監査 SUPPORTED / finite_witness_and_minimum_board_proof
---

# T*(S)が3種類でもWFT(S)は空

対象命題: T*(S)が3種類でもWFT(S)は空。 勝ちは保証できるが、終局手数の選択を相手に一部握られていて、一つも固定できない局面がある。

適用文脈: 起点: [個票02・T*とWFT](verification/batch-02.md)。勝敗維持の協調的到達可能性と、相手に逆らわれても手数を強制できることを区別する。

現在の結論: n6三石N局面でT*={6,8,10}、WFT=∅。固定長AND/ORでも照合。三つの到達長のどれも勝者が事前保証できない。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
