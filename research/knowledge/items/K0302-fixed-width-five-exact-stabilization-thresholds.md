---
id: K0302
title: 固定幅の真の満容量安定化長5件は24,12,16,13,11
kind: proposition
status: proved
topics:
- rectangles
- variants
- grundy
aliases: []
relations:
- type: generalizes
  target: K0071
  note: M_{3,5}=12を含む
- type: generalizes
  target: K0077
  note: M_{4,8}=11を含む
artifacts:
- path: research/q34-exact-threshold.md
  role: proof
  note: M_{3,4}=24
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/q35-exact-threshold.md
  role: proof
  note: M_{3,5}=12
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/q48-q6-exact-threshold.md
  role: proof
  note: M_{4,6}=16
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/q48-nearby-q7-threshold.md
  role: proof
  note: M_{4,7}=13
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/q48-exact-threshold.md
  role: proof
  note: M_{4,8}=11
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
---

# 固定幅の真の満容量安定化長5件は24,12,16,13,11

標準整数長方形盤のq点共線・共円禁止版で、
M_{3,4}=24、M_{3,5}=12、M_{4,6}=16、M_{4,7}=13、M_{4,8}=11
がそれぞれ厳密に確定した。

各閾値は直前長さの不足極大証人による下界と、一般末尾証明＋有限完全排除による上界を一致させている。閾値以降は全極大が行容量まで埋まり、全安全局面のGrundy値は残り手数の偶奇だけで決まる。
