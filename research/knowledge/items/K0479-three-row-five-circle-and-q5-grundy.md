---
id: K0479
title: 不等間隔三列・三行の5点円本数とq=5全安全局面Grundyを完全分類
kind: proposition
status: needs-review
topics:
- geometry
- rectangles
- variants
- grundy
aliases: []
relations: []
artifacts:
- path: research/experiments/fixed-width/reports/three-row-five-circle-and-q5-grundy-20261017.md
  role: proof
  note: 任意の正整数間隔の全称分類と有限mex表
- path: research/experiments/fixed-width/scripts/three_row_five_circle_classification_20261017.py
  role: verifier
  note: 4096盤の独立整数行列式列挙と全安全局面9-bit再帰
- path: research/experiments/fixed-width/output/three_row_five_circle_classification_20261017.txt
  role: data
  note: 4096盤と代表3盤の独立照合結果
scope: 三列x=0,a,a+b・三行y=0,d,2d、正整数a,b,d、q=5完全指摘通常プレイ
evidence: 2026-10-20添付統合。元資料では proved または computed と報告（個別の元statusは保存ZIPを参照）。本項目の全量化範囲に対する証明・計算の再監査は未完了。有限検証の実行範囲は統合実験のVALIDATION.mdを参照。
---


> 統合監査: 以下は取込元の主張・報告。全称証明・完全列挙の監査が未完了のため、現在の採用状態は needs-review。本文中の「証明」「一致」は元資料での報告を表す。


三列三行の盤上5点円の本数は

\[
N_5=\mathbf1_{a(a+b)=d^2}+\mathbf1_{b(a+b)=d^2}+2\mathbf1_{ab=2d^2}.
\]

三条件は互いに排他的で6点円は存在しない。N5=0,1,2の場合の空盤Grundy値は順に1,0,1。N5=0または1では全安全局面のGrundy値はそれぞれ(9-|S|) mod 2、(8-|S|) mod 2。N5=2では二つの5点禁則の共通2点・各固有3点・自由1点の占有数で全局面を縮約し、82状態の厳密mex表によって強解決する。最大Grundy値は3。

円の本数の式は、二点列の共通縦中心と第三列の円条件による任意の正整数間隔の全称証明。ゲームは全82個数状態のmex再帰で証明。独立した9-bit全安全局面再帰と4096盤の円行列式列挙で検証。一般の盤長や固定幅の真の安定化長を主張しない。

## 追補：全局面nimber分布と極大集合

5点円の本数が0,1,2の順に、全安全局面のGrundy値の度数（g=0,1,2,3）は
`(256,256,0,0)`, `(248,248,0,0)`, `(160,160,81,81)`。極大安全集合の石数別個数はそれぞれ `{9:1}`, `{8:5}`, `{7:9,8:2}`。二つの5点円の場合、共通2点・各固有3点・自由1点に分割し、有限状態のmex値を二項係数で重み付けした厳密集計である。極大配置数には共通点・固有点の選択による独立の組合せ証明がある。9-bit全局面の直接mex・極大性検査とも一致。
