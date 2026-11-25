---
id: K0042
title: 7×7のGrundy飽和開始層はσ_7=4
kind: proposition
status: proved
topics:
- grundy
aliases:
- B022
relations:
- type: depends_on
  target: K0005
  note: ''
- type: depends_on
  target: K0041
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round28-seven-board-original-verdicts.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 7×7のGrundy飽和開始層はσ_7=4

石数0〜14の最大Grundy列は `[0, 1, 5, 7, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]`。K_7=14なので初めて天井14−kに達するのはk=4。証人 `mask=9044480` のg=10。

全盤σ≤4の仮説や8×8の開始層をこの一盤から証明しない。Round28の二方式全数照合が有限結論の根拠。
