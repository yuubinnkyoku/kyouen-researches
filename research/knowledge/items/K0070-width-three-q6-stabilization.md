---
id: K0070
title: 3×m・q=6の真の満容量安定化長M_{3,6}=9
kind: proposition
status: proved
topics:
- rectangles
- variants
- grundy
aliases:
- F-BJ
- F-BK
relations:
- type: depends_on
  target: K0024
  note: ''
artifacts:
- path: research/experiments/fixed-width/reports/q-point-fixed-width.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/fixed-width/output/q_point_fixed_width.json
  role: data
  note: 有限長の検算
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/findings.md
  role: source
  note: M=9の専用完全列挙と3×8証人
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
solution:
  board: 3×m・q=6
  level: strong
  outcome: first-player-win
  classification:
  - root
  - first-moves
  - all-safe-win-loss
  - all-safe-grundy
  coverage: m≥9の全安全局面
  conditions: q=6,w=3,m≥9
  verification:
  - mathematical-proof
  - exhaustive-enumeration
  certificate: 解析証明＋有限排除
  independent_check: 下界証人と有限補完検査
  note: M_{3,6}=9、g=(15−|S|) mod2
---

# 3×m・q=6の真の満容量安定化長M_{3,6}=9

一般十分長さ385を解析で21へ改善し、m=9..20の不足極大を専用完全列挙で排除。3×8には14石極大があり下界9。従ってM_{3,6}=9、全m≥9で全極大15石・g(S)=(15−|S|) mod2。

旧F-BJのm≥21は同じ安定化問題の過去の上界としてこの項目へ統合し、別イベント項目にはしない。
