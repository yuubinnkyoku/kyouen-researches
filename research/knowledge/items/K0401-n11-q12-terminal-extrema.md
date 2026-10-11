---
id: K0401
title: 11×11・q=12の極大安全配置の石数範囲103〜114
kind: proposition
status: proved
topics:
- maximum-safe
- maximal-safe
- variants
- strategy-length
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 共円・共線q点禁止版の安全配置を使用
artifacts:
- path: research/experiments/geometry/reports/n11-q12-terminal-extremes-20261012.md
  role: proof
  note: 半整数中心による完全列挙と横断集合の両端値の証明
- path: research/experiments/geometry/scripts/verify_n11_q12_terminal_extremes_20261012.py
  role: verifier
  note: 独立2方式による21円列挙、210通りの19円部分集合の排除、両端証人
- path: research/experiments/geometry/output/n11-q12-terminal-extremes-20261012.txt
  role: data
  note: 検証器の実行結果
---

# 11×11・q=12の極大安全配置の最小石数103と最大石数114

標準11×11整数格子の**q=12版**では、極大安全配置の石数は103以上114以下で、両端とも実現する。これは標準q=4版のs_11・K_11の値ではない。

12点を通る円は21本だけで、12点を通る直線や13点以上を通る曲線はない。q>max(w,m)のときに限って成立する円中心の半整数性から441中心を有限完全列挙し、全三点組による独立な整数円生成と一致した。

安全集合の補集合は21円の横断集合。点次数最大3から最小横断集合サイズは7以上、7点の包含極小証人がある。19点以上の包含極小横断集合は、私有円19本がそれぞれ排他的点を持つ必要があるが、19本の選択210通りすべてでこの必要条件が破れる。18点の包含極小証人があるため、最小・最大極大安全サイズは121−18=103、121−7=114。

証拠は有限完全列挙と数学的帰着であり、11×11・q=12に限定される。空盤勝敗、全Grundy、103〜114の中間極大サイズの実現性は未解決。
