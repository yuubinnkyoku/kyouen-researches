---
id: K0024
title: q点版固定幅盤の十分長さ定理
kind: proposition
status: proved
topics:
- rectangles
- grundy
- variants
aliases:
- F-BH
relations:
- type: depends_on
  target: K0002
  note: ''
- type: generalizes
  target: K0068
  note: q≥4の一般定理は標準q4定理を含む
artifacts:
- path: research/experiments/fixed-width/reports/q-point-fixed-width.md
  role: proof
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/fixed-width/scripts/q_point_fixed_width.py
  role: verifier
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/fixed-width/output/q_point_fixed_width.json
  role: data
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
solution:
  board: w×m・q点版
  level: strong
  outcome: conditional
  classification:
  - root
  - first-moves
  - all-safe-win-loss
  - all-safe-grundy
  coverage: 全安全局面
  conditions: q≥4,w固定,m≥T_{w,q}=min(A,B)
  verification:
  - mathematical-proof
  certificate: 一般証明。具体盤の巨大証明書は不要
  independent_check: 67盤の有限検算は支持資料
  note: 先手勝ち iff q偶数かつw奇数
---

# q点版固定幅盤の十分長さ定理

q≥4、w≥1とし、N=(q−1)(w−1)と置く。十分長さの二つの上界とその最小値は

```text
A = q−1 + 2{C(N,q−1)−(w−1)} + (q−2)C(N,q−2)
B = q−1 + 2{C(N,3)−(w−1)C(q−1,3)} + (q−2)C(N,2)
T = min(A,B)
```

である。m≥Tなら全極大集合は(q−1)w石、全安全局面でg(S)=((q−1)w−|S|) mod2。二項係数の範囲外は0とする。

各不足行で禁止交点数を上界評価し合法点が残ることを証明する。空盤先手勝ち iff q偶数かつw奇数。勝ち局面では任意合法手が勝ち手。Tは十分長さで最小安定化長Mとは限らない。
