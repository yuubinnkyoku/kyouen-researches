---
id: K0313
title: K_11≥21かつK_12≥22の明示安全極大構成がある
kind: proposition
status: computed
topics: [maximum-safe, maximal-safe, geometry]
aliases: []
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/experiments/saturation/reports/saturation-20261003-extra.md
  role: source
  note: 21・22・24石構成と外周被覆
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/experiments/saturation/output/saturation_20261003_extra_verified.json
  role: data
  note: 全四点安全性と全空点阻害証人
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/experiments/saturation/scripts/saturation_20261003_extra_verify.py
  role: verifier
  note: 独立整数行列式検証
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
---

# K_11≥21かつK_12≥22の明示安全極大構成がある

11×11に21石、12×12に22石の安全極大配置を明示構成し、全四点と全空点の禁止証人を独立検査した。従ってK_11≥21、K_12≥22。

12盤22石配置は外側1層52点も全て塞ぐため、平行移動すると14盤でも22石のまま極大。外側2層目の合法2点を追加して平行移動すると16盤の24石安全極大配置も得られる。
