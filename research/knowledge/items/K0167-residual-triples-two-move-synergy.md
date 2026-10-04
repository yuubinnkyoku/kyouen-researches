---
id: K0167
title: 二手相乗作用を少数の残余三点制約で表せる
kind: proposition
status: proved
topics:
- geometry
aliases:
- B266
relations: []
artifacts:
- path: research/experiments/original-claims/reports/round18-pair-synergy.md
  role: proof
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-2026-09-27.md
  role: source
  note: B266の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round18_local_geometry.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round18_local_geometry.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 合法pについて `u_S(p)=|L(S)\({p}∪L(S+p))|` を新たに禁止する合法点数とする。
evidence: 原文監査 SUPPORTED / general_proof_and_infinite_construction
---

# 二手相乗作用を少数の残余三点制約で表せる

対象命題: 二手相乗作用を少数の残余三点制約で表せる。 `S+p+q`で初めて禁止される点の構造を、Sの石1個とp,qの組が作る円束へ分け、局所的な上限を出せる。

適用文脈: 合法pについて `u_S(p)=|L(S)\({p}∪L(S+p))|` を新たに禁止する合法点数とする。

現在の結論: 二手相乗を石ごとの一般化円へ分解し、無界の利得を整数格子で実現。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
