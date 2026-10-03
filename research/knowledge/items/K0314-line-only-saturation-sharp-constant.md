---
id: K0314
title: line-only版の最小極大サイズは主係数(3π²/8)^(1/3)でn^(2/3)以上
kind: proposition
status: proved
topics: [maximal-safe, geometry, variants]
aliases: []
relations:
- type: supports
  target: K0106
  note: 標準版の指数下界と同じ2/3をより鋭いline-only計数で支える
artifacts:
- path: research/saturation-20261003.md
  role: proof
  note: 原始方向容量による直線被覆上界
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/verification/scripts/check_saturation_20261003.py
  role: verifier
  note: 容量計数の独立検算
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
---

# line-only版の最小極大サイズは主係数(3π²/8)^(1/3)でn^(2/3)以上

4共線のみを禁止する版では、原始方向殻dに4φ(d)方向あることと方向別容量を使い、直線被覆数を

I_line(S) ≤ (4/(π√6)+o(1)) n k^(3/2)

まで改善できる。従って最小極大サイズは

s_n^line ≥ ((3π²/8)^(1/3)-o(1)) n^(2/3)

である。円も禁止する標準版にはこの主定数をそのまま適用しない。
