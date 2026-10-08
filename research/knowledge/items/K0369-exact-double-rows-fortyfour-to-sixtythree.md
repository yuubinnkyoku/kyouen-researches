---
id: K0369
title: 標準整数格子44〜63行で円が二点ずつ通る行数の厳密最大値
kind: proposition
status: proved
topics:
- geometry
- rectangles
- variants
aliases: []
relations:
- type: depends_on
  target: K0072
  note: 標準整数格子の二重点行と独立行公式
artifacts:
- path: research/experiments/fixed-width/reports/exact-double-rows-44-63.md
  role: proof
  note: 数学的な上界と明示的な下界円
- path: research/experiments/fixed-width/scripts/verify_double_rows_44_63.py
  role: verifier
  note: 2独立方法の合同排除と20幅の明示的証人
---

連続する w 本の整数水平行において、一本の実円が異なる整数格子点2個ずつを含む行数の最大値 T(w) は、

- T(44)=T(45)=14
- T(46)=T(47)=15
- T(w)=16（48<=w<=63）

である。横方向の格子点は全整数にわたるものとする。

上界の証明：二重点行の番号差のgcdを g とすると g∈{1,2,3}。g=1,2 はmod9,11,19,23,7,49の平方剰余必要条件の完全排除に帰着する。g=3 はmod19の許容11行剰余上界と、少なくとも13種類の相異なる行剰余が必要なことの矛盾で排除する。すべての幅で下界を達成する円を明示し、整数判別式・円方程式の直接代入で照合した。全法のマスク集合は2方式で全一致を確認。有限候補の排除を無限個の円の全探索と混同しない。

帰結：標準q点版で q>w+T(w) なら全てのm>=1と全安全局面Sについて g(S)=(w min(m,q−1)−|S|) mod 2、真の安定化長M_(w,q)=q−1。特にw=63ならq>=80が十分。さらに任意のw=63a+r (0<=r<63) についてT(w)<=16a+T(r)。w>=64の個別厳密値は未確定。
