---
id: K0166
title: 一手ずつは弱いが二手そろうと大量に塞ぐ
kind: proposition
status: proved
topics:
- geometry
aliases:
- B261
relations: []
artifacts:
- path: research/verification/round18-pair-synergy.md
  role: proof
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-2026-09-27.md
  role: source
  note: B261の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round18_local_geometry.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round18_local_geometry.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 合法pについて `u_S(p)=|L(S)\({p}∪L(S+p))|` を新たに禁止する合法点数とする。
evidence: 原文監査 SUPPORTED / general_proof_and_infinite_construction
---

# 一手ずつは弱いが二手そろうと大量に塞ぐ

対象命題: 一手ずつは弱いが二手そろうと大量に塞ぐ。 p,qをどちらの順でも合法に置け、u_S(p),u_S(q)は定数以下なのに、二手後の新規禁止点数はnとともに無限に増える局面族がある。

適用文脈: 合法pについて `u_S(p)=|L(S)\({p}∪L(S+p))|` を新たに禁止する合法点数とする。

現在の結論: 二手相乗を石ごとの一般化円へ分解し、無界の利得を整数格子で実現。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
