---
id: K0480
title: 3行・共通5列の6点円は最大4本で等号は正方格子型に限る
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
  note: 6点版の円成立条件と盤面規則
artifacts:
- path: research/experiments/three-row-five-columns-20261019/reports/q6-five-common-columns-real-upper-bound.md
  role: proof
  note: 任意の実数横座標・行間隔に対する完全計数式と鋭い上界の証明
- path: research/experiments/three-row-five-columns-20261019/scripts/verify_three_rows_five_columns.py
  role: verifier
  note: 二点和による有限検証
- path: research/experiments/three-row-five-columns-20261019/scripts/verify_three_rows_five_columns.cpp
  role: verifier
  note: 円方程式への直接代入による独立検証
- path: research/experiments/three-row-five-columns-20261019/output/q6-five-common-columns-integer-audit.json
  role: data
  note: 22638配置の完全列挙集計
- path: research/experiments/knowledge-audit-20261021/README.md
  role: log
  note: 証明の論理監査・再実行範囲・判定
evidence: '2026-10-21監査。5列の全重複和条件と積差による円数上界・等号分類を確認。独立2方式の22638配置が一致。 監査記録: research/experiments/knowledge-audit-20261021/README.md。'
---


# 3行・共通5列の6点円は最大4本

相異なる実数 `x0<...<x4` と `a,b>0` から作る15点 `(xi,0),(xi,a),(xi,a+b)` において、相異なる6点を通る円は最大4本。等号が成立する必要十分条件は、`xi=x0+i*d` かつ `a=b=d>0`。

各二点和 `s` に2組の点対があるときの積差を `D_s` とすると、円の本数は `sum_s ([D_s=ab]+[D_s=a(a+b)]+[D_s=b(a+b)])`。これが任意の実数に対する完全計数式であり、円の水平断面・二次式の二階差分・5点の加法衝突分類から上界と等号条件を証明する。

横座標が非等差、または `a!=b` なら最大3本。整数横座標462通りと行間隔49通りの22,638配置について、二点和方式と独立した整数円方程式方式で完全照合し一致した。

**量化の限界:** 各行の横座標集合が共通である場合に限る。各行が独立の5点集合をもつ場合には拡張していない。有限監査を全称証明と混同しない。
