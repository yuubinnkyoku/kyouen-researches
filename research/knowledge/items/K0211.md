---
id: K0211
title: 8石極大の被覆は二本の三点直線と少数の円へ圧縮できる
kind: proposition
status: refuted
topics:
- maximal-safe
- geometry
aliases:
- B376
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/verification/round10-small-saturation.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B376の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round10_small_saturation.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round10_small_saturation.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票05・新しい8×8の8石証人](verification/batch-05.md)。s_8=8はまだ仮定せず、「安全な8石極大集合」の族を対象にする。'
evidence: 原文監査 REFUTED / finite_exhaustion
---

# 8石極大の被覆は二本の三点直線と少数の円へ圧縮できる

否定された命題: 8石極大の被覆は二本の三点直線と少数の円へ圧縮できる。 全56三つ組を使わず、12本以下の円・直線で全空点を覆う例がある。

適用文脈: 起点: [個票05・新しい8×8の8石証人](verification/batch-05.md)。s_8=8はまだ仮定せず、「安全な8石極大集合」の族を対象にする。

現在の結論: 8×8全408安全八石極大は全空点被覆に13曲線以上必要。貪欲set coverの値を最小本数の下界には使っていない。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
