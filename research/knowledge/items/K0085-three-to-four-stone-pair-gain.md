---
id: K0085
title: 3→4石ではpair gainはunique gainに一致、4石以降は一般に過大計数
kind: proposition
status: proved
topics:
- geometry
- search-methods
aliases: []
relations:
- type: depends_on
  target: K0001
  note: ''
artifacts:
- path: docs/9X9_TWO_STONE_PROBE_RESEARCH_NOTES.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 3→4石ではpair gainはunique gainに一致、4石以降は一般に過大計数

安全3石親{a,b,c}へ合法vを追加すると、親三ペア由来の補完集合は互いに素。共通完成点があれば円/直線の一意性から親+v自体が禁止四点となり矛盾する。

9×9全85320親・6538352合法追加で0反例。4石以降は既危険点の再計数と新規補完間の重複がある。正しいunique_gainは新規危険和集合から既危険集合を除いたpopcount。
