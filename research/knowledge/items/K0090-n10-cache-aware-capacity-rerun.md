---
id: K0090
title: 10×10 cache-aware below-root改善は容量再実行の固定12親で確認
kind: proposition
status: observed
topics:
- search-methods
- statistics
aliases: []
relations: []
artifacts:
- path: research/experiments/solver-benchmarks/reports/10X10_CACHE_AWARE_BELOW_ROOT_CONFIRMATION_V2_RESULT.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/solver-benchmarks/reports/10X10_CACHE_AWARE_BELOW_ROOT_CAPACITY_RERUN_RESULT.md
  role: source
  note: 容量上限を修正した凍結24/24実行とprimary判定
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 10×10 cache-aware below-root改善は容量再実行の固定12親で確認

C2固定12親の容量再実行は24/24 fresh process完了、失敗0、output auditとverifier PASS。R=blind visited/aware visitedの中央値1.170872>1、改善12/12で事前条件を満たした。C1も固定12親で中央値1.162010、改善12/12。対象cohort内の改善であり、全親・他盤への一般化は未成立。

容量再実行ではdy12..16のtable容量を1 bit増やし、探索順の意味は維持した。従前に完了した11ペアのRは完全一致し、rank7親[1,12,80]も両条件LOSSまで閉じた（aware 555114540、blind 669211681 visits）。従前のV2は22/24完了・2 TableFullでINCOMPLETEのまま保存する。欠損11ペアだけから完了判定した結果ではない。
