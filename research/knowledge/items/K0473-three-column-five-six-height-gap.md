---
id: K0473
title: 三列異方格子の5点円と6点円の初出行数差は無界で初出円は2本と1本
kind: proposition
status: needs-review
topics:
- geometry
- rectangles
- variants
aliases: []
relations: []
artifacts:
- path: research/experiments/fixed-width/reports/three-column-unbounded-five-six-height-gap-20261017.md
  role: proof
  note: 任意の積条件 ab=d²k(k+1) に対する初出行数の全称証明
- path: research/experiments/fixed-width/scripts/verify_three_column_height_gap_20261017.py
  role: verifier
  note: 行列式列挙と弦長方程式列挙の独立照合
- path: research/experiments/fixed-width/output/three_column_height_gap_20261017.txt
  role: data
  note: 17組の有限完全照合記録
- path: research/experiments/fixed-width/scripts/verify_three_column_height_multiplicity_20261017.py
  role: verifier
  note: 二点と第三点から円係数を構成する独立完全列挙
- path: research/experiments/fixed-width/output/three_column_height_multiplicity_20261017.txt
  role: data
  note: 初出円の本数に関する17組の独立完全照合
evidence: 2026-10-20添付統合。元資料では proved または computed と報告（個別の元statusは保存ZIPを参照）。本項目の全量化範囲に対する証明・計算の再監査は未完了。有限検証の実行範囲は統合実験のVALIDATION.mdを参照。
---


> 統合監査: 以下は取込元の主張・報告。全称証明・完全列挙の監査が未完了のため、現在の採用状態は needs-review。本文中の「証明」「一致」は元資料での報告を表す。


# 三列異方格子の5点円と6点円の初出行数差は無界

正整数 $a,b,d,k$ が $ab=d^2k(k+1)$ を満たすとき、列位置 $0,a,a+b$、縦間隔 $d$ の有限三列格子について、5点円・6点円の初出行数は厳密に $H_5=k+2$, $H_6=2k+2$ である。

さらに初出の $m=k+2$ 行盤の5点円はちょうど2本、$m=2k+2$ 行盤の6点円はちょうど1本である。

したがって $H_6-H_5=k$ は無界であり、比 $H_6/H_5$ は2に近づく。二つの縦二点列から得る共通中心と弦長の二次恒等式を使って両下界を証明し、6点の明示的円構成で上界を達成する。17組の有限完全列挙を二方式で独立照合済み。初出円の本数も独立検証した。

一般の $a,b,d$ における初出行数の閉形式は主張しない。
