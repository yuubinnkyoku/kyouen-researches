---
id: K0054
title: 共線四点組数D_nの主項はn^5、次項は負のn^4 log n
kind: proposition
status: proved
topics:
- geometry
aliases:
- B141
relations:
- type: depends_on
  target: K0001
  note: ''
- type: refutes
  target: K0055
  note: 共線Θ(n^6)という旧漸近主張を否定
artifacts:
- path: research/verification/round4-collinear-asymptotic.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/ROUND4-B141-VERIFICATION.md
  role: verifier
  note: 方向別恒等式・定数の独立再計算
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round4_collinear_asymptotic.json
  role: data
  note: 整数・有理数の有限検算
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 共線四点組数D_nの主項はn^5、次項は負のn^4 log n

D_n=7ζ(2)/(60ζ(3)) n^5−3/(4ζ(2)) n^4 log n+O(n^4)。原始整数方向別の重複なし恒等式と一様誤差による全称証明。B141の旧REFUTEDは誤読で、現在は成立済み。

有限nで比率が増減することを漸近反証に使わない。非共線共円C_nの証明とは別。
