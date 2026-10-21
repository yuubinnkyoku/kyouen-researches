---
id: K0481
title: 不等間隔三列三行q=4は全正整数間隔で全9初手が勝ち
kind: proposition
status: proved
topics:
- geometry
- rectangles
- variants
- grundy
aliases: []
relations:
- type: depends_on
  target: K0002
  note: 完全指摘・通常プレイのGrundy定義
artifacts:
- path: research/experiments/fixed-width/reports/three-row-q4-all-spacing-20261017.md
  role: proof
  note: 126個の共円4点組の整数多項式分類と8有限ゲームへの全称帰着
- path: research/experiments/fixed-width/scripts/three_row_q4_all_spacing_20261017.py
  role: verifier
  note: 純Python有理多項式証明検査・9-bit完全再帰・独立行列式検証
- path: research/experiments/fixed-width/output/three_row_q4_all_spacing_20261017.txt
  role: data
  note: 8分類の全安全局面と4096盤の独立照合
- path: research/experiments/knowledge-audit-20261021/README.md
  role: log
  note: 証明の論理監査・再実行範囲・判定
scope: 正整数a,b,dの三列x=0,a,a+b、三行y=0,d,2d、q=4完全指摘通常プレイ
solution:
  board: 不等間隔3列×3行・q=4
  level: strong
  outcome: first-player-win
  classification:
  - root
  - first-moves
  - all-safe-win-loss
  - all-safe-grundy
  coverage: 全正整数a,b,d・全安全局面（8種類の禁止集合型へ帰着）
  conditions: 完全指摘・通常プレイ、列位置0,a,a+b、行位置0,d,2d
  verification:
  - mathematical-proof
  - exhaustive-enumeration
  - independent-enumeration
  certificate: 126組の行列式の全称符号分類と8種類の9-bit mex完全再帰
  independent_check: 4096盤の整数行列式による独立4点組照合
  note: 空盤g=1、9通りの初手後g=0
evidence: '2026-10-21監査。126多項式の符号分類と全条件交差、8有限ゲームへの帰着を確認。全局面mex・4096独立数値盤を再検査。 監査記録: research/experiments/knowledge-audit-20261021/README.md。'
---


任意の正整数 `a,b,d` に対し、三列 `0,a,a+b`・三行 `0,d,2d` のq=4完全指摘通常プレイ共円ゲームは、空盤Grundy値が**1**、9通りすべての初手後のGrundy値が**0**となる。先手は任意の点に初手を置いて勝てる。

4点共円判定の126個の行列式は、恒等零9個、六つの算術条件で零になる21個、正整数領域で非零96個に分類できる。算術条件の真偽は全偽・六つの単独真・三つ同時真の8通りに限られる。各場合について9-bit全安全局面をmex再帰で完全列挙して証明。独立に4096種類の整数盤を行列式で検証した。4行以上への一般化は主張しない。
