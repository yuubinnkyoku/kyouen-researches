---
id: K0476
title: 3本の平行直線・各4候補点で6点円は最大3本、達成可能
kind: proposition
status: needs-review
topics:
- geometry
- variants
- grundy
aliases: []
relations:
- type: depends_on
  target: K0001
  note: q点版の安全配置と禁止集合の定義を使用
artifacts:
- path: research/experiments/geometry/reports/three-parallel-four-points-q6-sharp-20261018.md
  role: proof
  note: 全称上界・4本排除・実数座標達成例の証明
- path: research/experiments/geometry/scripts/three_parallel_four_q6_audit.py
  role: verifier
  note: 行構造21種類の記号的排除と有限Grundy全局面計算
- path: research/experiments/geometry/scripts/three_parallel_four_q6_independent.cpp
  role: verifier
  note: 独立C++による達成例とGrundy計算
- path: research/experiments/geometry/output/three_parallel_four_q6_audit.json
  role: data
  note: Python監査結果
- path: research/experiments/geometry/output/three_parallel_four_q6_independent.txt
  role: data
  note: C++監査結果
evidence: 2026-10-20添付統合。元資料では proved または computed と報告（個別の元statusは保存ZIPを参照）。本項目の全量化範囲に対する証明・計算の再監査は未完了。有限検証の実行範囲は統合実験のVALIDATION.mdを参照。
---


> 統合監査: 以下は取込元の主張・報告。全称証明・完全列挙の監査が未完了のため、現在の採用状態は needs-review。本文中の「証明」「一致」は元資料での報告を表す。


# 3本の平行直線・各4候補点で6点円は最大3本、達成可能

平面上の任意の3本の異なる平行直線に、それぞれ高々4個の相異なる実座標の候補点を置く。これらの候補点を6個含む異なる円は**高々3本**であり、実際に3本の例がある。6点を含む直線は存在しないので、q=6の禁止6点集合も高々3個である。

さらに各行高々k候補点（k=1,2,3,4）の最大本数は順に0,1,1,3である。k=3では2円が各行で少なくとも1点を共有して計3交点となり不可能。

証明は円の交点数が高々2という事実からF≤4を導き、等号F=4を各行の円所属多重グラフ（4-cycleまたは二重完全マッチング）と円の根の和から全場合排除する。有限列挙による外挿ではなく**全実座標についての数学的証明**。

達成例：行y=0,1,2のx座標を順に {±4,±√18}, {±√15,±√14}, {±√12,±√10} とすると、x²+y²=16、x²+y²+y=16、x²+y²+2y=18 の3円がそれぞれ6候補点を含む。

この特定の12点ゲームについてのみ、4096部分集合の有限完全列挙で安全局面3915個、空盤Grundy値0、極大安全集合は9石8個と10石24個と計算し、独立したPython/C++で一致した。**任意の配置のGrundy分類ではない。** 標準整数格子上で3本達成可能かも未確認。

**登録状況：** K番号は作業時の仮番号。mainへ反映できた場合に番号衝突を確認し、knowledge生成物を再生成して全検査を行うこと。
