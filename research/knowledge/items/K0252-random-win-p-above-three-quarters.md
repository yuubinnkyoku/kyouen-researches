---
id: K0252
title: P局面でランダム勝率3/4を超えられる
kind: proposition
status: computed
topics:
- statistics
- grundy
aliases:
- B502
relations:
- type: depends_on
  target: K0002
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round36-random-original-witness-audit.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B502の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round36_random_witnesses_verified.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round3_b502_pgrand_n6.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round36_random_witness_audit.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: p_rand(S)を、両者が一様合法手で打つ場合の手番側勝率とする。前回の有限証人はNで約0.09、Pで約0.56。これを無限族の証明とは扱わない。
evidence: 原文監査 SUPPORTED / exact_rational_finite_witness
---

# P局面でランダム勝率3/4を超えられる

対象命題: P局面でランダム勝率3/4を超えられる。 B501への明確な競合候補。小盤の約0.56の壁を大幅に越える構成を狙う。

適用文脈: p_rand(S)を、両者が一様合法手で打つ場合の手番側勝率とする。前回の有限証人はNで約0.09、Pで約0.56。これを無限族の証明とは扱わない。

現在の結論: 6×6 mask35652737はPだが一様合法手ランダム勝率5162/6615>3/4。全115安全拡張のg,p,hを独立整数幾何・Fraction再帰で検算。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
