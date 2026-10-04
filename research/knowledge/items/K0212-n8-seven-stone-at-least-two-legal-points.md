---
id: K0212
title: 安全7点集合では8×8に必ず2点以上の合法手が残る
kind: proposition
status: computed
topics:
- maximal-safe
- geometry
aliases:
- B377
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round10-small-saturation.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B377の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round10_small_saturation.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round10_small_saturation.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票05・新しい8×8の8石証人](../../log/claim-audit/batch-05.md)。s_8=8はまだ仮定せず、「安全な8石極大集合」の族を対象にする。'
evidence: 原文監査 SUPPORTED / finite_exhaustion_and_witness
---

# 安全7点集合では8×8に必ず2点以上の合法手が残る

対象命題: 安全7点集合では8×8に必ず2点以上の合法手が残る。 s_8≥8より強い被覆余裕の主張で、最小反例は「合法手がちょうど1点」の7石集合。

適用文脈: 起点: [個票05・新しい8×8の8石証人](../../log/claim-audit/batch-05.md)。s_8=8はまだ仮定せず、「安全な8石極大集合」の族を対象にする。

現在の結論: 8×8全安全七点集合には二点以上の合法手がある。一合法点という候補を縮約して排除した。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
