---
id: K0035
title: 10×10の最大安全サイズは19≤K_10≤23
kind: proposition
status: proved
topics:
- maximum-safe
aliases: []
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round57-nineteen-stone-ten-board-bound.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round57_nineteen_verified.json
  role: data
  note: 座標安全性と上下界の監査
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 10×10の最大安全サイズは19≤K_10≤23

19石の安全・極大証人 `[9, 15, 16, 18, 20, 22, 30, 36, 44, 58, 62, 65, 67, 70, 71, 87, 91, 93, 97]` を全3,876四点組で独立検算。点番号はx+10y。行内点対に基づく一般上界は23。

20石の存在・不在、最大性は未確定。十九石が極大であることは最大19を意味せず、最小極大の下界にもならない。
