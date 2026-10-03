---
id: K0142
title: 既存最大配置に外周を足すだけでは次の最大へ届かない
kind: proposition
status: computed
topics:
- maximum-safe
- geometry
aliases:
- B087
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/verification/round58-original-maximum-extension-obstruction.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-2026-09-27.md
  role: source
  note: B087の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 原文の指定有限盤・証人範囲
evidence: 原文監査 SUPPORTED / complete_maximum_catalogue_embedding_obstruction
---

# 既存最大配置に外周を足すだけでは次の最大へ届かない

対象命題: 既存最大配置に外周を足すだけでは次の最大へ届かない。 すべてのn×n最大配置の平行移動埋め込みについて、n+1盤の最大配置への拡張が不可能なnがある。

現在の結論: 7×7最高層全16配置の8×8への全64埋込み・3200空点追加は全て禁止。一方8×8安全15石は存在し、既存14石を保った一点拡張では次の最大へ届かない。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
