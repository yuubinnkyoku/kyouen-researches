---
id: K0374
title: 11×11 reply27の難S5局面を全90 S6子WINで確定
kind: computation
status: computed
topics: [square-outcomes, search-methods, certificates, verification]
aliases: []
relations:
- type: depends_on
  target: K0002
  note: 先手固定視点の奇数ANDと偶数ORの完全境界規則
- type: depends_on
  target: K0355
  note: reply27の現行S4/S5証明境界
- type: depends_on
  target: K0372
  note: solver-trusted raw葉と独立な上位境界の証拠区分
artifacts:
- path: research/experiments/n11-s6-universal-closure-20261011/README.md
  role: source
  note: 対象S5、S6全子探索、計算量、正しい極性、残課題
- path: research/experiments/n11-s6-universal-closure-20261011/scripts/audit.py
  role: verifier
  note: 全90合法S6子・raw exact・cache隔離・S4/S5伝播の独立監査
- path: research/experiments/n11-s6-universal-closure-20261011/output/audit.json
  role: manifest
  note: 生のS6 solver出力、全source hash、証明frontier
- path: research/experiments/n11-s6-universal-closure-20261011/output/s6-win-complete.csv
  role: data
  note: 全90canonical S6 WIN葉と直接rawへの参照
- path: research/experiments/n11-s6-universal-closure-20261011/output/s5-universal-witness.json
  role: data
  note: S5 ANDの全子WIN証拠
scope: 11×11標準通常版のS5一局面と、そのS4親二classのみ。S6 90葉は直接solver-trusted exactであり、terminal-only独立minimax未完成。
---

# S5 direct UNKNOWNをS6全子WINで解決

S5 `(1188950301626859520,603979776)` は、従来の15M-node直接探索でUNKNOWNだった。独立整数幾何で90個のcanonical合法S6子を完全列挙し、1M/2Mの探索と5局面の15M再探索によって**90/90 exact WIN、UNKNOWN0**が得られた。全S6試行29,794,287 nodes。

元の先手固定視点で石数5はAND層なので、完全なS6子集合がすべてWINならS5はWIN。このS5を合法子として持つS4 `(1188950301626859520,536870912)` と `(1188950301776805888,0)` はOR層なので、ともにWINへ確定した。全3,384 S4はLOSS31 / WIN274 / UNKNOWN3079となった。

別途2局面の直接S5 LOSSをcold replay・記憶共有実行の両方で確認し、現行cacheは5,752行（WIN159、LOSS5,593）、conflict0。119第三手被覆117、残り `{100,108}`、追加class最小1、有理LP双対1は不変。

独立検査したのは、各S6 raw葉のcanonical・安全性・合法手数・完全な親子集合と、その上位AND/OR伝播である。90葉それ自体を終局まで独立再証明したわけではないので、**solver-trusted exact** と **terminal-only minimax証明** は区別する。
