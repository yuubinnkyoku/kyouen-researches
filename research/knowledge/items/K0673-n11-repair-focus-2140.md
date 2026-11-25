---
id: K0673
title: 2091計画の崩壊証人focus_s6を除く修復三証人交換で2140類へ（条件付き計画の再構築）
kind: computation
status: computed
topics: [square-outcomes, certificates, verification]
aliases: []
relations:
- type: depends_on
  target: K0672
  note: focus_s6手番WIN確定により証人候補から除外
- type: depends_on
  target: K0003
  note: 条件付き証明義務と確定勝敗の区別
- type: supersedes
  target: K0670
  note: 修復済み46証人集合（2,140類）が崩壊した2091計画（2,091類）を置き換える
artifacts:
- path: research/experiments/n11-central-19-cover-20261031/output/repair_focus_neighborhood.json
  role: data
  note: 修復列挙の機械可読出力（focus除去有効交換16,043、最良2,140類と交換内訳）
- path: research/experiments/n11-central-19-cover-20261031/audit_central49_2091_repair_focus_neighborhood.py
  role: verifier
  note: focus_s6を除外集合に追加し、focus除去交換の最小フロンティアを記録する近傍全数監査
- path: research/log/2026-11-06-n11-repair-focus-neighborhood.md
  role: log
  note: 修復列挙の経緯
scope: 標準11x11完全指摘・通常プレイの2091基準46証人集合に対する1回三証人交換（focus_s6除去を必須とする条件付き修復）。六石LOSS・二石root・空盤勝敗は含まない。
evidence: >-
  K0672により46証人のfocus_s6は手番WINと確定した。2091基準集合から三証人交換の全数列挙（15,180三つ組×15マッチング=227,700候補総数、313,905候補組合せ、283,635幾何的有効）をfocus_s6除外の条件で再監査した。有効交換278,364の中からfocus_s6を含む除去交換は16,043を数え、その最小フロンティアは2,140類であった。最良交換は除去3件（00000000000000203800002000002000、00000000000000203800440000000000、focus_s6）に追加3件（00000000000000203800040000000040、00000000000000203800400000002000、0000000000000080100a102000000000）であり、94/94被覆を維持する。改善交換は0件であり、2091基準自体は局所最適のままである。outcomesは従来どおりUNKNOWN。
---

# focus 除外の修復：2,140類

K0672 により focus_s6（`00000000000000203808000000000040`）は手番 WIN と確定し、K0670（2091 計画）は LOSS 証人構造として崩壊した。

修復として、focus_s6 を証人候補から除外した条件で三証人交換近傍の全数列挙を再実行した。有効交換 16,043 のうち focus_s6 除去を含むものの最小フロンティアは **2,140 類** であった（除去3件・追加3件、内訳は証憑 JSON 参照）。46 証人・94/94 被覆を維持する。

**条件付き計画であり、勝敗の主張ではない。** 修復後も六石 LOSS・二石 root・空盤勝敗は UNKNOWN。破壊した 2091 計画の幾何的数値（2,091 類・局所最適）は残るが、計画としての意義は失われ、本項目がその現行版となる。

## 2026-11-06 追記：K0674 により修復計画の前提も崩壊

K0673 の修復済み46証人の実検証（全2,140類確定・全件独立監査）により、46証人全員が手番WIN、LOSS は0件と確定した（K0674）。修復計画の前提（46証人が LOSS 候補）も崩壊し、本項目は LOSS 証人構造として無効となった。outcomes は従来どおり UNKNOWN。
