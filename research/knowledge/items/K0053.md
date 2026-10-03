---
id: K0053
title: D4点軌道内の共円性と軌道占有容量
kind: proposition
status: proved
topics:
- geometry
- maximum-safe
aliases: []
relations:
- type: depends_on
  target: K0001
  note: ''
artifacts:
- path: night-research/CYCLE31B_ORBIT_CIRCLES_ALL_N.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: night-research/CYCLE34_OCCUPANCY_LATTICE_CERTIFICATE.md
  role: proof
  note: 7×7骨格の有限占有vector排除
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# D4点軌道内の共円性と軌道占有容量

盤中心からの同じD4点軌道は同距離なので一円上。標準四点禁止では非退化な軌道占有は高々3という必要条件を得る。複数軌道の同円・共線四点も存在し、単一軌道容量だけでは安全性十分条件にならない。

7×7骨格の圧縮不等式や有限占有vector判定はこの必要条件を使うが、可能なvectorから安全配置存在を自動推測しない。
