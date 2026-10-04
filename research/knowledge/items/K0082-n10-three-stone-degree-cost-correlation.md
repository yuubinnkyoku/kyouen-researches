---
id: K0082
title: 10×10の3石探索コストとΣdの負相関は固定R内限定
kind: proposition
status: observed
topics:
- statistics
- search-methods
aliases:
- F-D
- H3
relations: []
artifacts:
- path: research/archive/hypothesis-ledgers/findings.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: scripts/analysis/cost_correlation.py
  role: verifier
  note: 独立探索visitedに限った相関計算
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 10×10の3石探索コストとΣdの負相関は固定R内限定

固定8石LOSSルートRの独立探索3石26局面でlog10(visited)とΣdの相関−0.786、4石では−0.045へ消える。合法手数94..97は小差で、探索コスト差を単独説明しない。

これは固定R・特定solver/profileでの観測。全3石の母集団、他盤、探索順変更への一般化は未確定。
