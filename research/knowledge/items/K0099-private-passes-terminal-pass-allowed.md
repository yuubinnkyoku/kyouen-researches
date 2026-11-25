---
id: K0099
title: 終端パス可の有限私有パス版は残数差と通常gで勝敗・mexを分類
kind: proposition
status: proved
topics:
- variants
- grundy
aliases: []
relations:
- type: depends_on
  target: K0002
  note: ''
artifacts:
- path: research/experiments/structural-lemmas-2026-10-02/finite-passes.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/structural-lemmas-2026-10-02/checks/equal_pass_mex.json
  role: data
  note: 有限DAG704200比較
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 終端パス可の有限私有パス版は残数差と通常gで勝敗・mexを分類

通常終端でもパス可能な規約。手番側a、相手bでF(G,a,b)=g(G) if a=b、0 if a<b、2 if a=b+1 and g(G)=1、その他a>bは1。従って権利多い側が勝ち、同数なら通常値保存。

役割を交換する通常子(H,b,a)とパス子(G,b,a−1)の相対状態mexを高さ・権利総数で帰納する。私有パス付き直和に通常xor則を自動適用しない。
