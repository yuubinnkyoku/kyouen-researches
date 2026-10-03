---
id: K0208
title: 被覆重複が大きいのに一石で大量解除できる
kind: proposition
status: computed
topics:
- maximal-safe
- geometry
aliases:
- B367
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/verification/round29-fault-witness-audit.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B367の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round29_fault_witnesses.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round29_fault_witnesses.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 安全極大Sに対し、元から空だった点を一つでも合法に戻すために必要な最小石除去数をρ(S)とする。除去した場所そのものを再着手可能と数えない。
evidence: 原文監査 SUPPORTED / finite_witness
---

# 被覆重複が大きいのに一石で大量解除できる

対象命題: 被覆重複が大きいのに一石で大量解除できる。 min b≥2の極大Sに、取り除くと盤の空点の正の割合が合法になる一つの石がある。

適用文脈: 安全極大Sに対し、元から空だった点を一つでも合法に戻すために必要な最小石除去数をρ(S)とする。除去した場所そのものを再着手可能と数えない。

現在の結論: 独立幾何で原文の故障耐性・解除割合・最大集合不要石の具体的証人を照合。旧決着の監査。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
