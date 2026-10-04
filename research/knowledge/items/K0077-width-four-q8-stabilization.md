---
id: K0077
title: 4×m・q=8の真の満容量安定化長はM_{4,8}=11
kind: proposition
status: proved
topics: [rectangles, variants, grundy]
aliases: []
relations:
- type: depends_on
  target: K0024
  note: ''
- type: depends_on
  target: K0072
  note: q=2w境界の整数格子構造を使う
artifacts:
- path: research/experiments/fixed-width/reports/q48-exact-threshold.md
  role: proof
  note: M_{4,8}=11の一般上界・有限排除・m=10証人
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/experiments/fixed-width/output/q48_exact_threshold.json
  role: data
  note: 円型分類とm=11,12完全排除
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/experiments/fixed-width/scripts/q48_exact_threshold.py
  role: verifier
  note: 整数演算による再現器
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
solution:
  board: 4×m・q=8
  level: strong
  outcome: second-player-win
  classification: [root, first-moves, all-safe-win-loss, all-safe-grundy]
  coverage: m≥11の全安全局面
  conditions: q=8,w=4,m≥11
  verification: [mathematical-proof, exhaustive-enumeration]
  certificate: m≥13の一般計数＋m=11,12完全排除＋m=10不足極大証人
  independent_check: m=10証人を全三点曲線生成で独立検査
  note: g(S)=(28-|S|) mod 2
---

# 4×m・q=8の真の満容量安定化長はM_{4,8}=11

m≥13は8点円の局所形と一般計数で不足極大を排除し、m=11,12は全不足行部分集合とblocker選択の完全列挙で排除した。4×10には27石の極大安全集合があるため下界11も達成する。

従ってM_{4,8}=11で、全m≥11・全安全局面Sについてg(S)=(28-|S|) mod2。これでq=2w境界の残っていたw=4も閉じた。
