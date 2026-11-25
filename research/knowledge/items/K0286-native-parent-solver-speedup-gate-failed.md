---
id: K0286
title: 10k root-orderとstaged V3のnative親solver加速は凍結gate失敗
kind: proposition
status: observed
topics:
- search-methods
- statistics
- verification
aliases: []
relations:
- type: verifies
  target: K0285
  note: 分類成功から加速への外挿を親solverで確認し失敗
artifacts:
- path: research/experiments/solver-benchmarks/reports/10X10_V2_10K_PARENT_SOLVER_BENCHMARK_REPORT.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/solver-benchmarks/reports/10X10_AB_STAGED_V3_ROOT_ORDER_RESULT.md
  role: source
  note: 別16親のprobe込み凍結gate
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: results/10x10/ab-staged-v3-root/aggregate_summary.json
  role: data
  note: V3各主要gate
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/solver-benchmarks/reports/10X10_PARENT_BENCHMARK_MECHANISM_REFINEMENT.md
  role: source
  note: 九つのsingle-child費用差による説明訂正
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 10k root-orderとstaged V3のnative親solver加速は凍結gate失敗

V2十二親ではprobe込みB/A visited中央値1.84・改善2/12・aggregate1.49でprimary FAIL、勝敗一致12/12。exact-only中央値も1.70で、独立childのfile-order desk中央値.85をnative共有memo加速と解釈できない。

別staged V3十六親の勝敗一致16/16、probe込みaggregate.908は改善したが中央値1.367・改善7/16（必要13）・worst3.289でconfirmatory performance FAIL。exact-onlyaggregate.698を主要判定へ差替えない。

機構再検討ではV2九親が両条件root child一つだけを入り、その差は別root間memo汚染でなく選んだLOSS証明の費用差（中央値1.7911）。共有memo干渉一語で全失敗を説明しない。
