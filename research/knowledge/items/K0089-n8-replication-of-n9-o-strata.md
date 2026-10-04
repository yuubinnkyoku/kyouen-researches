---
id: K0089
title: 9×9 O0-only正方向の構造仮説は8×8全censusへ再現しなかった
kind: proposition
status: observed
topics:
- statistics
- verification
aliases: []
relations:
- type: verifies
  target: K0088
  note: O0-only仮説の他盤確認。失敗を明示
artifacts:
- path: research/experiments/8x8-replication/reports/8X8_O_STRATUM_REPLICATION_RESULT.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/solver-benchmarks/output/8x8-o-primary-summary.json
  role: data
  note: 凍結primary endpoint
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/solver-benchmarks/output/8x8-o-solve-manifest.json
  role: manifest
  note: 848rootの完了と失敗0
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 9×9 O0-only正方向の構造仮説は8×8全censusへ再現しなかった

8×8凍結O0-only165、overlap155、O1-only102。848/848必要roots完了、O0-only Δ−0.0424、overlap−0.0129、主contrast−0.0295で、凍結成功条件Δ>0かつgap≥0.05はFAIL。

共有親interactionは全155で厳密0。O1-only+0.0882はsecondary記述で新しいprimaryへ差替えない。全8×8安全局面のcensusではなく、固定O strata母集団のcensusである。
