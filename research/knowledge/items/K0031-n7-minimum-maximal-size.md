---
id: K0031
title: 7×7の最小極大安全サイズs_7=7
kind: proposition
status: proved
topics:
- maximal-safe
aliases:
- F-AR
- F-BA
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/findings.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/exploration/fact_kmin_n7_safe.json
  role: data
  note: 安全証人と完了探索の記録
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 7×7の最小極大安全サイズs_7=7

安全で極大な証人[1,9,22,23,27,44,45]とk≤6の完全排除でs_7=7。点番号はx+7y。旧F-ARの不安全な証人は無効だが、命題そのものは安全な別証人で成立が確定している。

証人は全四点の安全性と全外点の禁止を別々に検査する。合法追加がないことだけで安全性を推測しない。
