---
id: K0106
title: 最小極大サイズの漸近指数には一般下界2/3がある
kind: proposition
status: proved
topics:
- maximal-safe
- geometry
aliases: []
relations:
- type: depends_on
  target: K0026
  note: ''
- type: supports
  target: K0147
  note: 本文の証明・証人が原文に与える帰結
- type: supports
  target: K0148
  note: 本文の証明・証人が原文に与える帰結
artifacts:
- path: research/verification/round52-general-saturation-exponent-lower-bound.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 最小極大サイズの漸近指数には一般下界2/3がある

任意のε>0に対し十分大きいnでs_n>n^(2/3−ε)、従ってliminf log(s_n)/log(n)≥2/3。安全k石からの直線被覆はO(n k^(3/2))、三格子点が定める真円の全格子点数は一様にn^o(1)。極大性の必要条件n²−k≤n[(2√2/3)k^(3/2)+(4/3)k]+C(k,3)R(n)から従う。

真円の整数係数を平方完成してN≤224(n−1)^6、r₂(N)≤4τ(N)を使う。これは全盤の下界で、s_n=o(n)やs_n=n^(2/3+o(1))の対応上界は未証明。
