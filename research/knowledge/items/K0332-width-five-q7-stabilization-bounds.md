---
id: K0332
title: 5×m・q=7の満容量安定化長は19以上200以下
kind: proposition
status: proved
topics: [rectangles, variants, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0318
  note: 一般上界200を使用
artifacts:
- path: research/experiments/fixed-width-frontier-20261005/reports/q57-bounds-and-encoding.md
  role: proof
  note: 下界証人・一般上界・完全円生成・未完probeの区別
- path: research/experiments/fixed-width-frontier-20261005/output/q57_independent_witness.json
  role: data
  note: 5×18の29石安全極大証人と全61空点のblocker
- path: research/experiments/fixed-width-frontier-20261005/scripts/q57_witness_check.py
  role: verifier
  note: 全三点曲線生成による独立安全性・極大性検査
- path: research/experiments/fixed-width-frontier-20261005/scripts/q57_geometry.cpp
  role: solver
  note: 片根と接点を含む7/8点円の完全生成
---

# 5×m・q=7の満容量安定化長は19以上200以下

標準五行整数格子の7点共円・共線禁止版について19≤M_{5,7}≤200。
5×18には行占有数(5,6,6,6,6)の29石安全極大配置が存在するため下界19。
上界200はK0318の一般曲線充填定理を代入した数学的上界である。

下界証人は盤内全三点から生成した整数円・直線で独立に安全性を確認し、
全61空点が追加不能であることを具体的blocker付きで確認した。
短時間SATのUNKNOWNや未監査UNSATはこの不等式の根拠に含めない。
M_{5,7}の厳密値、全m≥19での満容量化は未解決である。
