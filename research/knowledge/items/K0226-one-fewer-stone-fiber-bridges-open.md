---
id: K0226
title: 一石少ない中間配置を許すと同一残局族を少数の橋で結べる
kind: question
status: open
topics:
- residual-games
- reconfiguration
aliases:
- B448
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
  note: B448の原文・定義（現在の結論は採用報告を優先）
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
evidence: 原文監査 PARTIAL / general_four_stone_bridge_proof
---

# 一石少ない中間配置を許すと同一残局族を少数の橋で結べる

未確定の命題: 一石少ない中間配置を許すと同一残局族を少数の橋で結べる。 端点ではL,Rを保ち、中間は別残局を許したG_{k−1}上で、各成分間の接続に共通する小さい橋の型がある。

適用文脈: 起点: [個票03・B057](verification/batch-03.md)。ここでは同じk・同じラベル付きL・同じ極小残余族Rを持つ集合を一つの族とする。Rが空の場合でもLを省略しない。

現在の結論: 安全四石対は、常に安全な三石層のJohnsonグラフを経由して接続できる。k≥5を含む原文全体は未証明。

採用境界: 任意の安全四石配置対は常に安全な三石層のJohnsonグラフを通って結べる。k≥5の原文全体は未証明。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
