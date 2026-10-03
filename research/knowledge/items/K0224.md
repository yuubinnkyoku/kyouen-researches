---
id: K0224
title: 非空で連結なRを持つ族も分裂する
kind: proposition
status: computed
topics:
- residual-games
- reconfiguration
aliases:
- B444
relations:
- type: depends_on
  target: K0108
  note: ''
artifacts:
- path: research/verification/round42-exact-residual-family-audit.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B444の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round42_families_verified.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round42_families_audit.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票03・B057](verification/batch-03.md)。ここでは同じk・同じラベル付きL・同じ極小残余族Rを持つ集合を一つの族とする。Rが空の場合でもLを省略しない。'
evidence: 原文監査 SUPPORTED / complete_exact_family_witness
---

# 非空で連結なRを持つ族も分裂する

対象命題: 非空で連結なRを持つ族も分裂する。 退化残局を除いても、同じ未来ゲームを異なる過去の配置が実現する。

適用文脈: 起点: [個票03・B057](verification/batch-03.md)。ここでは同じk・同じラベル付きL・同じ極小残余族Rを持つ集合を一つの族とする。Rが空の場合でもLを省略しない。

現在の結論: 非空連結Rの分裂、同一族別成分で最大一石解除数8対7、厳密抽象同型40集合の四成分分裂を検算。B446旧反証を訂正。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
