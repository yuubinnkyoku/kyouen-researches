---
id: K0083
title: R内4石のΣdとLOSS分離、二石順位の旧記述は訂正済み
kind: proposition
status: observed
topics:
- statistics
aliases:
- F-E
- F-AF
relations: []
artifacts:
- path: research/archive/hypothesis-ledgers/findings.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: scripts/analysis/f_e_exact_label_test.py
  role: verifier
  note: 固定R全70状態の整数幾何と厳密記述検定
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# R内4石のΣdとLOSS分離、二石順位の旧記述は訂正済み

固定Rの4石全70局面でLOSS12、WIN58、Σd平均8732.833対8285.276、AUC0.759339。重なるsubsetの固定有限記述で、label-randomization p=0.00157331は母集団一般化の有意性ではない。

F-Eの「二石LOSS2個はΣd最小の二つ」はF-AF全28ペア照合で偽（5位と26位）。序盤の低Σd→LOSSという説明全体を強い一般則として採用しない。
