---
id: K0067
title: 三点補完被覆による小さい極大集合の必要条件
kind: proposition
status: proved
topics:
- maximal-safe
- geometry
aliases:
- F-AX
- F-AY
- F-BE
relations:
- type: depends_on
  target: K0066
  note: ''
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/findings.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: scripts/analysis/fact_kmin_cover_bound.cpp
  role: solver
  note: 楽観的補完被覆上界と完全探索
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 三点補完被覆による小さい極大集合の必要条件

安全k集合が極大ならn²−k≤Σ_{T⊂S,|T|=3}|completion(T)|。10×10の最大補完数9より100−k≤9 C(k,3)が必要で、k≤5を排除する。

これは必要条件で、和集合重複を無視した上界。満たすことは存在証明にならない。後日の6,7,8石全域排除で現在のs_10下界は9へ進んでいる。
