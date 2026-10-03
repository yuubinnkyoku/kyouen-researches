---
id: K0071
title: 3×m・q=5は12≤M_{3,5}≤56、m=12..21とm≥56は強解決
kind: proposition
status: proved
topics:
- rectangles
- variants
- grundy
aliases:
- F-BL
relations:
- type: depends_on
  target: K0024
  note: ''
artifacts:
- path: research/q5-w3-stabilization.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
solution:
  board: 3×m・q=5
  level: strong
  outcome: second-player-win
  classification:
  - root
  - first-moves
  - all-safe-win-loss
  - all-safe-grundy
  coverage: m=12..21 またはm≥56の全安全局面
  conditions: q=5,w=3,m∈[12,21]またはm≥56
  verification:
  - mathematical-proof
  - exhaustive-enumeration
  certificate: 解析上界＋有限完全排除
  independent_check: 3×11下界証人検算
  note: 22..55は未確定、12≤M≤56
---

# 3×m・q=5は12≤M_{3,5}≤56、m=12..21とm≥56は強解決

不足行の被覆上界55からm≥56で全極大12石。3×11に11石極大がありM≥12。m=12..21は全不足極大の専用完全排除済みでg(S)=(12−|S|) mod2。

資料の「この5盤」は12..21の十盤と不整合な誤記として採用しない。m=22..55の不足極大再出現は未確定で、M=12と外挿しない。
