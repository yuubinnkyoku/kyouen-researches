---
id: K0253
title: 残り最大手数が3以下ならPのランダム勝率は1/2以下
kind: proposition
status: refuted
topics:
- statistics
- grundy
aliases:
- B506
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
  note: B506の原文・定義（現在の結論は採用報告を優先）
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

# 残り最大手数が3以下ならPのランダム勝率は1/2以下

否定された命題: 残り最大手数が3以下ならPのランダム勝率は1/2以下。 0.5超えの戦略的錯覚には、少なくとも4手以上先の相互作用が必要になる。

適用文脈: p_rand(S)を、両者が一様合法手で打つ場合の手番側勝率とする。前回の有限証人はNで約0.09、Pで約0.56。これを無限族の証明とは扱わない。

現在の結論: 4×4の真の残り最大手数h3のP証人でランダム勝率76/135>1/2。合法点数をhの代わりに使わない。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
