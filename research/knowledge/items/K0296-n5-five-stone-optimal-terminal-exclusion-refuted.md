---
id: K0296
title: 5×5の全勝敗維持対局では五石で終わらないという説明は偽
kind: proposition
status: refuted
topics:
- strategy-length
- maximal-safe
aliases:
- F-Y
relations:
- type: depends_on
  target: K0295
  note: ''
artifacts:
- path: research/archive/hypothesis-ledgers/findings.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round25_forced_n5.json
  role: data
  note: Tstar_bits672とWFT_bits128
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 5×5の全勝敗維持対局では五石で終わらないという説明は偽

旧F-Yの「五石極大があるのに最適終局にない」「全勝敗維持対局の終局は七または九」という読みは、独立全状態計算の空盤T*={5,7,9}により否定される。固定witness証明書戦略の{7,9}という表自体は有効。

旧記録は固定証明戦略を全最適対局と呼んだため境界を失った。修正したT*とWFTの全範囲は別項目から参照する。五石終局が勝者に事前保証できるという主張にはしない。
