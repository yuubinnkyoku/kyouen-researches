---
id: K0288
title: certified witness順位と真のfirst LOSS順位は別、座標joinにも検査が必要
kind: method
status: active
topics:
- provenance
- verification
- search-methods
aliases: []
relations:
- type: depends_on
  target: K0080
  note: ''
artifacts:
- path: docs/THREE_STONE_PROBE_HOLDOUT_V2_EVAL_AUDIT.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: docs/THREE_STONE_PROBE_HOLDOUT_V2_LABEL_SEMANTICS_AUDIT.md
  role: source
  note: 元設計source-label mismatch
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: docs/THREE_STONE_PROBE_HOLDOUT_V2_PRE_RUN_RECEIPT.md
  role: manifest
  note: 1161childの元凍結cohort
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# certified witness順位と真のfirst LOSS順位は別、座標joinにも検査が必要

WIN親のHAS_EXACT_LOSS_CHILDは一つの証人を与えるだけで、唯一または順序最初のLOSSとは限らない。親[4,9,33]の既知batch0には[2,4,9,33]と[4,5,9,33]の少なくとも二LOSS。witness rankはfirst LOSS rankの上界。

未完PROBE集合のmemo順位を比較するなら両baselineで同じunresolved集合を使い、exact WIN除外とprobe完了を分離する。旧source child[0,13,60,68]は入力親[0,6,31]を文字通り含まず、別frameのcanonical childを直接label joinできない。元1161child設計はこの意味不一致で評価BLOCKEDと記録。別clean V2の1136child結果へ同じラベルを無条件に移さない。
