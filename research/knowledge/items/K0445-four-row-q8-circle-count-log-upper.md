---
id: K0445
title: 四行8点円の総数は O(m² log m) 以下
kind: proposition
status: needs-review
topics:
- geometry
- rectangles
- variants
aliases: []
relations:
- type: depends_on
  target: K0073
  note: 四行円の水平弦長平方の二階差分条件を使用
artifacts:
- path: research/experiments/fixed-width/reports/q48-circle-count-upper-log-20261015.md
  role: proof
  note: 二平方和表示数の積とガウス整数の最大公約数による全称上界
- path: research/experiments/fixed-width/scripts/q48_circle_upper_log_audit_20261015.py
  role: verifier
  note: 格子点直接列挙・約数公式・弦長列挙の有限独立監査
- path: research/experiments/fixed-width/output/q48_circle_upper_log_audit_20261015.txt
  role: data
  note: 監査結果
scope: 標準整数格子の四連続行に各行二点ずつを持つ8点円。m列盤内の8点集合の総数。任意の整数m≥1。
evidence: 2026-10-20添付統合。元資料では proved または computed と報告（個別の元statusは保存ZIPを参照）。本項目の全量化範囲に対する証明・計算の再監査は未完了。有限検証の実行範囲は統合実験のVALIDATION.mdを参照。
---


> 統合監査: 以下は取込元の主張・報告。全称証明・完全列挙の監査が未完了のため、現在の採用状態は needs-review。本文中の「証明」「一致」は元資料での報告を表す。


標準の4行m列盤内に各行2点ずつを持つ円の8点集合の個数を `C8(m)` とすると、

`C8(m) ≤ 162m(m+1)(1+floor(log2(m+1))) = O(m² log m)`。

弦長の奇数性と二階差分 `−8` から、第二行の弦長 `b` について
`a²+c²=2(b−2)(b+2)`。奇数 `b` では二因子が互いに素なので、
二平方和表示数 `r2` を用いると型数は
`T(m)≤(1/4)Σ_{3≤b<m, b odd}r2(b−2)r2(b+2)`。
Cauchy–Schwarz とガウス整数の最大公約数による初等的な計数から
`Σ_{n≤X}r2(n)²=O(X log X)` を証明し、各型の横移動数高々 `m` を掛ける。

この上界は**無界の全称定理**であり、計算実験による外挿ではない。
`C8(m)=Ω(m log m)` の既知Pell族下界と真の次数が一致するかは未解決。
付属の監査は `m≤300` の有限範囲であり、全称証明の根拠は報告書の代数・計数論証にある。
