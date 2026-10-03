---
id: K0051
title: 7×7最大14石族は16配置・二つのD4相に完全分類される
kind: proposition
status: computed
topics:
- maximum-safe
- reconfiguration
aliases: []
relations:
- type: depends_on
  target: K0029
  note: ''
artifacts:
- path: night-research/FINAL_SELECTION_THEOREM.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: night-research/SELECTION_THEOREM_CHECKLIST.md
  role: manifest
  note: COMPLETE/SAMPLE区別と個別証拠
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: results/cycle8_verify.json
  role: data
  note: 有限族の独立補題検査
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 7×7最大14石族は16配置・二つのD4相に完全分類される

最大安全14石は16個、各8個のD4軌道二相。十点軌道順(0,0),(0,1),(0,2),(0,3),(1,1),(1,2),(1,3),(2,2),(2,3),(3,3)で占有数A=(2,3,2,0,1,3,2,0,0,1)、B=(3,1,2,1,1,3,1,0,2,0)。Aは中央あり角2、Bは中央なし角3。

最大族の相の定義と容量分解は有限全数に限定する。n=8のnode-cappedサンプルやn=6との比較を同じ完全分類として扱わない。
