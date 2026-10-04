---
id: K0126
title: 四石以降で初めて現れる競合グラフの最小型がある
kind: proposition
status: proved
topics:
- residual-games
- reconfiguration
aliases:
- B063
relations:
- type: depends_on
  target: K0108
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round19-b063-stone-hierarchy.md
  role: proof
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-2026-09-27.md
  role: source
  note: B063の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round19_b063_hierarchy.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round19_b063_hierarchy.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 本文の原文量化と現在の採用境界
evidence: 原文監査 SUPPORTED / general_lower_bound_and_finite_witness
---

# 四石以降で初めて現れる競合グラフの最小型がある

対象命題: 四石以降で初めて現れる競合グラフの最小型がある。 ある固定グラフHは、どの盤の三石局面にも誘導部分グラフとして現れず、四石局面には現れる。石数による表現能力の階層を狙う。

現在の結論: 誘導K1,4は三石局面では不可能、四石で実現する。最小合法点数は五。石数と合法点数の最小性を分ける。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
