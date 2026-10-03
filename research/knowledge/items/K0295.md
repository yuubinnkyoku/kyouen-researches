---
id: K0295
title: 1〜7×7空盤の全勝敗維持終局T*と固定長保証WFTは区別される
kind: proposition
status: computed
topics:
- strategy-length
- grundy
aliases: []
relations:
- type: depends_on
  target: K0049
  note: ''
- type: verifies
  target: K0048
  note: 固定witness集合が全T*ではない境界を照合
- type: refutes
  target: K0296
  note: 独立全状態でT*に五石が含まれる
artifacts:
- path: research/verification/round25-forced-length-holes.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round25_forced_n5.json
  role: data
  note: 五盤rootのT*/WFT bitset
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round25_forced_n6.json
  role: data
  note: 六盤rootのT*/WFT
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round25_forced_verified.json
  role: data
  note: 小盤独立全状態と固定長AND/OR検査
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round28_n7_layers.json
  role: data
  note: 七盤rootのT*/WFT
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 1〜7×7空盤の全勝敗維持終局T*と固定長保証WFTは区別される

空盤のT*はn1..7で{1},{3},{5},{6},{5,7,9},{7,9,11},{8,10,12,14}。WFTは{1},{3},{5},{6},{7},{9},空集合。

特に5×5は最適勝敗を保ったまま五石終局へ到達できる（n5JSON root Tstar_bits672=2^5+2^7+2^9）。全経路から五石が欠けるわけではない。一方、勝者が相手の全選択に対し事前保証できるのは七石のみ。固定証明書witness戦略の{7,9}とも異なる。
