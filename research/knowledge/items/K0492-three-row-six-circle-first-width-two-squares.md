---
id: K0492
title: 等間隔三行の6点円の最初の可能幅と二平方和による円数公式
kind: proposition
status: proved
topics:
- geometry
- rectangles
- variants
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 6点共円・共線禁止の対象定義
artifacts:
- path: research/experiments/fixed-width/reports/q36-three-row-onset-two-squares-20261020.md
  role: proof
  note: 三行の弦長二階差による全称証明と二平方和への4対1対応
- path: research/experiments/fixed-width/scripts/q36_three_row_onset_independent_20261020.cpp
  role: verifier
  note: 三行の三点から直接円を作る独立整数幾何完全列挙
- path: research/experiments/fixed-width/scripts/q36_three_row_onset_arithmetic_20261020.py
  role: verifier
  note: 弦長整数方程式を用いた別方式の完全計数
- path: research/experiments/fixed-width/output/q36_three_row_onset_audit_20261020.csv
  role: data
  note: h=1..60、m=2h+1と2h+2の120盤の独立一致結果
scope: 正整数h,mの整数格子{0,...,m−1}×{0,h,2h}における6点共円の存在と個数
---

すべての正整数 h,m で、三行格子の6点円の個数 C_h(m) は
m≤2h+1 なら0、m=2h+2 なら厳密に r₂(4h+1)/4。
従って最小幅が下界 2h+2 に一致する必要十分条件は
4h+1 が二平方和であること。

全称性は水平弦長 d_i に対する
d_0²−2d_1²+d_2²=−8h² と d_1≥2h+1、
等号時の正奇数解 d_0²+d_2²=8h+2、
および二平方和表現との4対1対応から証明される。

C++整数円方程式とPython弦長式の独立した完全列挙で
h=1..60の120盤が一致した。有限監査と数学的全称証明を区別する。
K0070の標準h=1のゲーム安定化長 M_{3,6}=9 とは異なる量。
下界を達成しない場合の最小幅一般式は主張しない。
