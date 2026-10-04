---
id: K0181
title: J_nにある固定ペア分けは中盤では必ず破れる
kind: proposition
status: computed
topics:
- residual-games
- first-moves
aliases:
- B317
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
- path: research/archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B317の原文・定義（現在の結論は採用報告を優先）
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
evidence: 原文監査 SUPPORTED / finite_witness_and_exhaustive_certificates
---

# J_nにある固定ペア分けは中盤では必ず破れる

対象命題: J_nにある固定ペア分けは中盤では必ず破れる。 完全マッチングはあるが、そのどれを採っても、初手応答後に相手が合法手で固定応答を破れる後手勝ち盤がある。

適用文脈: 起点: [個票01](../../log/claim-audit/batch-01.md)。拠点自身への初手にも返せるよう、閉近傍による支配と全域支配を分ける。

現在の結論: 4×4全112212完全マッチングは固定応答が破れる。109704個は四手目、2508個は六手目。各合法prefixと違法応答を証明書へ保存し、逆順独立全列挙でも不足・余剰0。全部が四手目に失敗するとは言わない。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
