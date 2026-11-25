---
id: K0320
title: n=11..15にはn−1石の安全極大配置が存在する
kind: proposition
status: computed
topics: [maximal-safe, geometry]
aliases: []
relations:
- type: depends_on
  target: K0026
  note: ''
- type: supports
  target: K0147
  note: s_n<nとなる連続した有限範囲の明示例
artifacts:
- path: research/experiments/saturation/reports/saturation-20261003.md
  role: source
  note: 11〜15盤のn−1石極大座標
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/experiments/saturation/output/saturation_20261003_verified.json
  role: data
  note: 安全性と全空点の禁止証人
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/experiments/saturation/scripts/check_saturation_20261003.py
  role: verifier
  note: 明示構成の軽量再現検査
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
---

# n=11..15にはn−1石の安全極大配置が存在する

標準n×n盤について、n=11,12,13,14,15それぞれに
10,11,12,13,14石の安全極大配置を明示構成した。したがってこの有限範囲でs_n≤n−1。

各構成は全四点の整数行列式で安全性を確認し、全空点について既存三石との禁止四点組の証人を保存して極大性を確認している。

これは一般のs_n=o(n)を証明するものではないが、s_n=nという小盤パターンが11盤で破れ、その破れが15盤まで連続して明示される。
