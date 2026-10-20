---
id: K0471
title: 三列異方格子では5点円初出を3行に固定して6点円初出を無界にできる
kind: proposition
status: needs-review
topics:
- geometry
- rectangles
- variants
aliases: []
relations: []
artifacts:
- path: research/experiments/fixed-width/reports/three-column-constant-five-unbounded-six-20261017.md
  role: proof
  note: 任意のt>=2に対する構成・合同式による下界・初出6点円の一意性
- path: research/experiments/fixed-width/scripts/verify_constant_five_unbounded_six_20261017.py
  role: verifier
  note: 弦長整数方程式と独立三点行列式による完全列挙
- path: research/experiments/fixed-width/output/constant_five_unbounded_six_20261017.txt
  role: data
  note: t=2..50の弦長検査とt=2..9の独立全円列挙
scope: 三列x=0,1,t²、縦間隔t、t>=2、円のみの初出行数
evidence: 2026-10-20添付統合。元資料では proved または computed と報告（個別の元statusは保存ZIPを参照）。本項目の全量化範囲に対する証明・計算の再監査は未完了。有限検証の実行範囲は統合実験のVALIDATION.mdを参照。
---


> 統合監査: 以下は取込元の主張・報告。全称証明・完全列挙の監査が未完了のため、現在の採用状態は needs-review。本文中の「証明」「一致」は元資料での報告を表す。


正整数t>=2の三列異方格子 x=0,1,t²、y=tj (0<=j<m) で、少なくともq点を通る円の最小行数をH_q(t)とする。このとき H_5(t)=3、H_6(t)=2t+1。初出m=2t+1の6点円はちょうど1本。従ってH5を固定してもH6-H5およびH6/H5は無界。

5点円と6点円の明示構成に加え、6点円の各列の行番号差D0,D1,D2が同じ偶奇を持ち、t²(D1²-D0²-4)=D2²-D0²-4を満たすことから、法4・法8の合同条件で下界を全称証明する。初出の一意性も同じ方程式で証明。独立有限検算は補助資料であって全称証明の代用ではない。

直線のq点禁止は含めないため、q点版ゲームの安定化長・Grundy数についての主張ではない。
