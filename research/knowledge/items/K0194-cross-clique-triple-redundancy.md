---
id: K0194
title: 完全グラフ成分をまたぐ三点制約は冗長か値不変
kind: proposition
status: refuted
topics:
- residual-games
- reconfiguration
aliases:
- B345
relations:
- type: depends_on
  target: K0108
  note: ''
artifacts:
- path: research/verification/round38-b345-sole-triple-clique-counterexample.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B345の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round38_b345_verified.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round38_b345_n5_search.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round38_b345_search.cpp
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票03・B051〜B058](verification/batch-03.md)、[個票04・B064〜B068](verification/batch-04.md)。孤立点だけによる退化例は除いて考える。'
evidence: 原文監査 REFUTED / sole_minimal_triple_counterexample_and_minimum_legal_size
---

# 完全グラフ成分をまたぐ三点制約は冗長か値不変

否定された命題: 完全グラフ成分をまたぐ三点制約は冗長か値不変。 P(S)がクリークの直和のとき、極小な三点制約を加えてもgが変わらない。成分のxorだけで済む境界の候補。

適用文脈: 起点: [個票03・B051〜B058](verification/batch-03.md)、[個票04・B064〜B068](verification/batch-04.md)。孤立点だけによる退化例は除いて考える。

現在の結論: 5×5の残余は一二点辺+一三点辺。P=K2+K1+K1で、唯一の三点辺によりg1対3。非退化の最小合法点数4。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
