---
id: K0276
title: H-denseはn≤10の記述を越える独立確認が未完了
kind: proposition
status: conjectured
topics:
- first-moves
- statistics
aliases:
- H-dense
relations:
- type: depends_on
  target: K0043
  note: ''
- type: depends_on
  target: K0021
  note: ''
- type: depends_on
  target: K0105
  note: 11盤通常版はUNKNOWNで独立holdoutとして未完了
artifacts:
- path: night-research/H_DENSE_PREREG.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 標準q=4・完全指摘・通常プレイ。独立確認は空盤先手勝ちが完了証明されたn>10に限る。
---

# H-denseはn≤10の記述を越える独立確認が未完了

確認済み先手勝ち盤n1,2,3,6,9は全初手勝ち、n5だけ9/25で混在。H-denseは新しい先手勝ちn>10でも非全勝は事前に凍結した構造例外だけ、という候補で未証明。

n9完了前に部分データを見て着想したため独立holdoutではない。n10密度0は後手勝ちの定義的帰結で追認にならない。新盤の初手outcomeを見てから例外条件を定めないという凍結条件も根拠に残す。

対象は標準通常版である。misère 8×8の16/64という混在初手は別ゲームの結果で、本予想の反例ではない。標準通常版11×11はUNKNOWNなので、新しい独立確認にはならない。
