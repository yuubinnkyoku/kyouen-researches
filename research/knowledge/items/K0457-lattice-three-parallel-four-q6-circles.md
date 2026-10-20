---
id: K0457
title: 3本の平行直線に各4整数点で6点円3本を実現できる
kind: proposition
status: needs-review
topics:
- geometry
- variants
- rectangles
aliases: []
relations: []
artifacts:
- path: research/experiments/geometry/reports/lattice-three-circles-q6-20261018.md
  role: proof
  note: 8通りの水平弦の完全分類による存在・排他証明
- path: research/experiments/geometry/scripts/lattice_three_circles_q6.py
  role: verifier
  note: 有理数円係数による全候補検査と有限Grundy計算
- path: research/experiments/geometry/scripts/lattice_three_circles_q6_independent.cpp
  role: verifier
  note: 独立した整数行列式検査とGrundy計算
- path: research/experiments/geometry/output/lattice_three_circles_q6.json
  role: data
  note: Pythonの有限完全列挙結果
- path: research/experiments/geometry/output/lattice_three_circles_q6_independent.txt
  role: data
  note: C++の独立検算結果
evidence: 2026-10-20添付統合。元資料では proved または computed と報告（個別の元statusは保存ZIPを参照）。本項目の全量化範囲に対する証明・計算の再監査は未完了。有限検証の実行範囲は統合実験のVALIDATION.mdを参照。
---


> 統合監査: 以下は取込元の主張・報告。全称証明・完全列挙の監査が未完了のため、現在の採用状態は needs-review。本文中の「証明」「一致」は元資料での報告を表す。


# 3本の平行直線に各4整数点で6点円3本を実現できる

整数格子上の水平線 `y=0,1,3` にそれぞれ `{-2,0,1,3}`, `{-2,-1,2,3}`, `{-3,0,1,4}` を選ぶと、6点を通る異なる円は正確に3本である。平行移動により8×4整数格子に含まれる。任意の実数座標の3平行線×各4点で円は高々3本という一般上界を、整数座標でも達成する明示例となる。

全称的な主張はこの明示構成の存在と円3本の完全性である。各行の2根の和が共通であることを使うと、3行に共通の二点和は1だけ。候補8通りは `t3-3t1+2t0=-24` により正確に3通りへ絞られる。詳細は証明資料を参照。

この特定の12点上の6点禁止ゲームの有限完全列挙では、安全局面3915、空盤Grundy値0、極大配置は9石8個・10石24個。これは任意配置に対するGrundy定理ではない。標準3×4全点盤とも区別する。

**限界：** 8×4という包囲格子が最小かどうかは未確定。一般3円配置のゲーム分類も未確定。
