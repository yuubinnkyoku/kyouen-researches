---
id: K0091
title: D9 one-shot memo read-maskは物理slot書換えでなく論理epochが必要
kind: proposition
status: proved
topics:
- search-methods
- provenance
aliases: []
relations: []
artifacts:
- path: research/experiments/solver-benchmarks/reports/10X10_D9_READ_MASK_REWRITE_SEMANTICS_CORRECTION.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/solver-benchmarks/reports/10X10_D9_READ_MASK_ACCESS_PATH_INVARIANT.md
  role: source
  note: 両read経路でのmask不変条件
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# D9 one-shot memo read-maskは物理slot書換えでなく論理epochが必要

RankCompactTable/RankFlat17の同一key同一outcome try_putは冪等no-opで、新generationを作らない。成功returnだけでmaskを退役すると未再計算でも事実を再開してしまう。

選択rankのepoch0をentry/child-prefetch両readでmaskし、対象状態の再計算完了とoutcome一致writeを明示的epoch1とする。slotbytesが同一でも実験sidecarで一度だけ退役する。これは必要な実装意味論で、未実施cohortの効果を証明しない。
