---
id: K0084
title: R外4石36局面のΣd→LOSS方向は全幅memo再求解でも維持
kind: proposition
status: observed
topics:
- statistics
- verification
aliases:
- F-F
relations:
- type: supports
  target: K0083
  note: 固定R外でも4石方向が再現。一般定理ではない
artifacts:
- path: research/experiments/solver-benchmarks/reports/10X10_F_E_R_EXTERNAL_HOLDOUT_RESULT.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/solver-benchmarks/reports/10X10_F_E_R_EXTERNAL_HOLDOUT_MEMO_REVALIDATION.md
  role: verifier
  note: 全幅キーで36/36ラベルの独立再求解
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: results/10x10/f-e-r-external-holdout/holdout_summary.json
  role: data
  note: 凍結標本endpoint
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# R外4石36局面のΣd→LOSS方向は全幅memo再求解でも維持

事前凍結したR外safe canonical36局面（Σd三分位各12）でLOSS10/WIN26、低0/12・中4/12・高6/12、AUC0.811538、LOSS−WIN平均Σd差620.331。事前判定reversal_supported_outside_Rが成立。

旧FlatMemo81は10×10キー上位6bit切捨てを持ったため、36/36を全幅キーで再求解し全ラベル不変を確認した。層化標本なのでp値を非層化母集団有意性にしない。R外二〜三石の逆方向は未検証。
