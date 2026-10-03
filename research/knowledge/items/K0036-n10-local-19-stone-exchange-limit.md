---
id: K0036
title: 特定19石証人から九石交換以内では安全20石に届かない
kind: proposition
status: computed
topics:
- maximum-safe
aliases: []
relations:
- type: depends_on
  target: K0035
  note: ''
artifacts:
- path: research/verification/round59-60-final-ten-board-search.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round60_final_verified.json
  role: data
  note: 完了半径と保守的再開境界
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 特定19石証人から九石交換以内では安全20石に届かない

K0035の固定19石Sから除去半径1..9を完全探索。半径9の全C(19,9)=92378条件も完了した。安全20石Tがあるなら|S∩T|≤9、少なくとも十石の入替が必要。

半径10は22085削除集合まで完了、次の枝で中断した。全盤20石不存在でも半径10完了でもない。一般20石探索へ範囲を拡大しない。
