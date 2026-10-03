---
id: K0128
title: P(S)が空でも高nimberを持つ
kind: proposition
status: computed
topics:
- residual-games
- reconfiguration
aliases:
- B065
relations:
- type: depends_on
  target: K0108
  note: ''
artifacts:
- path: research/verification/round41-b065-pair-empty-grundy-five.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-2026-09-27.md
  role: source
  note: B065の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round41_b065_verified.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round41_audit.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 原文の指定有限盤・証人範囲
evidence: 原文監査 SUPPORTED / finite_witness_and_minimum_board_proof
---

# P(S)が空でも高nimberを持つ

対象命題: P(S)が空でも高nimberを持つ。 残余2点制約が一つもないのに `g(S)≥4` となる局面がある。目先の競合がなくても強いゲーム的分岐が生まれる候補。

現在の結論: 8×8でS=[0,1,5,10,17,37,48,50,59]、L=[9,38,39,43,47,62,63]。二点辺0、三点辺8・四点辺1、g=5で勝ち手62。全128拡張の四安全性実装・67安全mexの三実装が一致。n≤7全域除外と合わせ最小正方形盤8。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
