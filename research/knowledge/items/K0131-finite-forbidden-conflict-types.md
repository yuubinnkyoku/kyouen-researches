---
id: K0131
title: 実現できる競合グラフには有限の小さい禁止型がある
kind: proposition
status: proved
topics:
- residual-games
- reconfiguration
aliases:
- B070
relations:
- type: depends_on
  target: K0108
  note: ''
artifacts:
- path: research/verification/round18-competition-stars.md
  role: proof
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-2026-09-27.md
  role: source
  note: B070の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round18_local_geometry.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round18_local_geometry.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 本文の原文量化と現在の採用境界
evidence: 原文監査 SUPPORTED / general_proof_and_infinite_construction
---

# 実現できる競合グラフには有限の小さい禁止型がある

対象命題: 実現できる競合グラフには有限の小さい禁止型がある。 固定占有石数kについて、任意のnから得られるP(S)すべてに共通する、三角形の有無だけではない誘導部分グラフ制約が存在する。

現在の結論: 固定kのクリーク分割辺の和。全kで誘導星の禁止と鋭い整数実現。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
