---
id: K0251
title: 標準盤のP局面のランダム勝率は2/3以下
kind: proposition
status: refuted
topics:
- statistics
- grundy
aliases:
- B501
relations:
- type: depends_on
  target: K0002
  note: ''
artifacts:
- path: research/verification/round36-random-original-witness-audit.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B501の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round36_random_witnesses_verified.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round3_b502_pgrand_n6.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round36_random_witness_audit.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: p_rand(S)を、両者が一様合法手で打つ場合の手番側勝率とする。前回の有限証人はNで約0.09、Pで約0.56。これを無限族の証明とは扱わない。
evidence: 原文監査 REFUTED / exact_rational_finite_counterexamples
---

# 標準盤のP局面のランダム勝率は2/3以下

否定された命題: 標準盤のP局面のランダム勝率は2/3以下。 任意に1へ近づくという第1回の候補に対し、幾何に由来する非自明な上限を予想する。

適用文脈: p_rand(S)を、両者が一様合法手で打つ場合の手番側勝率とする。前回の有限証人はNで約0.09、Pで約0.56。これを無限族の証明とは扱わない。

現在の結論: 5×5のP証人で一様合法手のランダム勝率2383/3360>2/3。これは最適勝敗ではなくランダム再帰での手番側勝率。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
