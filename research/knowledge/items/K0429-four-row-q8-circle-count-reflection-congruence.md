---
id: K0429
title: 4行8点円数は反射対称性から法2・法4で決まる
kind: proposition
status: proved
topics: [geometry, rectangles, variants]
aliases: []
relations: []
artifacts:
- path: research/experiments/fixed-width/reports/q48-reflection-mod4-20261015.md
  role: proof
  note: 上下反射作用と円数合同式の全称証明
- path: research/experiments/fixed-width/scripts/q48_reflection_mod4_20261015.py
  role: verifier
  note: 円の二通りの整数構成によるm=1..100の有限照合
- path: research/experiments/fixed-width/output/q48_reflection_mod4_audit_20261015.txt
  role: data
  note: 有限監査の出力
scope: 標準4行・幅mの盤内に全て含まれる各行2点の8点円。任意の整数m≥1。
evidence: C8(m) ≡ max(0,m-3) (mod 2)。奇数mでは法4でも同じ合同式。偶数mでは C8(m) ≡ max(0,m-3)+2N(m) (mod 4)、N(m)は非局所弦長型を上下反転で同一視した円の型数。
---

上下反射 `y↦3-y` の固定円は局所弦長型 `(1,3,3,1)` だけで、その水平移動数は `max(0,m-3)`。他の円は反射で二つずつ対になるので法2の式を得る。各非局所型の最大弦長は奇数であり、その反射対の寄与 `2(m-D)` は奇数mなら4の倍数、偶数mなら法4で2となる。これにより法4の式が従う。

`N(m)` の明示公式や非局所型の完全分類は主張しない。有限計算は証明の代替ではない。
