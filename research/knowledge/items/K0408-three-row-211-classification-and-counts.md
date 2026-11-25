---
id: K0408
title: 3水平行盤の2+1+1共円四点組の分類と厳密計数
kind: proposition
status: proved
topics:
- geometry
- statistics
- rectangles
aliases: []
relations: []
artifacts:
- path: research/experiments/geometry/reports/three-row-211-pell-20261011.md
  role: proof
  note: 3行分類・Pell族・3×m総数
- path: research/experiments/geometry/scripts/verify_three_row_211_20261011.py
  role: verifier
  note: 3行盤独立検査
- path: research/experiments/geometry/output/three_row_211_audit_20261011.txt
  role: data
  note: 3行盤監査
- path: research/experiments/geometry/reports/three-line-211-binary-forms-20261011.md
  role: proof
  note: 任意三行間隔の二次形式分類
- path: research/experiments/geometry/scripts/verify_three_line_211.py
  role: verifier
  note: 三行型行列式検査
- path: research/experiments/geometry/output/three_line_211_audit_20261011.txt
  role: data
  note: 任意三行監査
scope: 整数格子3水平行盤の全2+1+1型共円四点組
evidence: 中央・外側二次形式の必要十分分類、有限和の全称証明、独立検査。
---

標準整数格子の3水平行で二点行の位置に応じて2+1+1型共円四点組を分類する。中央行の弦間隔d、上下隔たりhでは完成点が `X²+Y²=2d²−8h²` に対応する。外側二点行では `2X²−Y²=d²+8h²` が必要十分条件。

これらの整数解に盤幅m内の平行移動数を重み付けして、3×mの各型および全禁止四点組数を厳密な有限和で表す。中央型は二平方和公式、外側型はPell再帰による無限の有限幅証人を持つ。

全称分類・有限和の証明が主根拠で、整数行列式による有限盤検査は独立監査。Grundy値・勝敗は導かない。
