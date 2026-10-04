---
id: K0177
title: J_4には二点の全域支配集合がある
kind: proposition
status: computed
topics:
- residual-games
- first-moves
aliases:
- B311
- B312
relations:
- type: depends_on
  target: K0108
  note: ''
artifacts:
- path: research/experiments/original-claims/output/round70_scope_catalogue_check.json
  role: data
  note: J4全84Pペア内の40全域支配・15型内8型を再検算
- path: research/experiments/original-claims/output/round5_jn_followup2.json
  role: data
  note: TD/非TDの共通近傍数の全分類
- path: research/experiments/original-claims/reports/round27-fixed-response-audit.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B311の原文・定義（現在の結論は採用報告を優先）
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
scope: '起点: [個票01](../../log/claim-audit/batch-01.md)。拠点自身への初手にも返せるよう、閉近傍による支配と全域支配を分ける。'
evidence: 原文監査 SUPPORTED / finite_complete_classification_and_witness
---

# J_4には二点の全域支配集合がある

対象命題: J_4には二点の全域支配集合がある。 盤のどの点にも、その二点の少なくとも一つが別の点として必勝応答になる。単なる支配数2から一段強める。

適用文脈: 起点: [個票01](../../log/claim-audit/batch-01.md)。拠点自身への初手にも返せるよう、閉近傍による支配と全域支配を分ける。

現在の結論: J4には全域支配ペアが40個ある。閉近傍による通常の支配ではない。

B312の分類も固定J4で完了。全84二石Pペアは15D4型、全域支配40ペアはそのうち8型であり、全域支配ペアは全てP。Pペア内の共通近傍数はTDで5（16ペア）または8（24ペア）、非TDでは4/6/7で完全分離する。全n版への外挿は含めない。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
