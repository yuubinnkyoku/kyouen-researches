---
id: K0438
title: 任意有限整数点盤の指定安全局面の共円ゲーム勝敗判定はPSPACE完全
kind: proposition
status: needs-review
topics:
- geometry
- grundy
- residual-games
- variants
- search-methods
aliases: []
relations:
- type: depends_on
  target: K0348
  note: 任意グラフの円による整数点符号化と多項式ビット長
- type: depends_on
  target: K0108
  note: 残余禁止集合の継続ゲームへの対応
artifacts:
- path: research/experiments/game-structure/reports/node-kayles-pspace-20261019.md
  role: proof
  note: Node Kaylesとの全状態同型・PSPACE完全性・独立幾何構成の数学的証明
- path: research/experiments/game-structure/scripts/verify_node_kayles_reduction_20261019.py
  role: verifier
  note: 既存幾何構成の独立整数行列式監査と全残余状態Grundy照合
- path: research/experiments/game-structure/scripts/verify_graph_realization_20261019.py
  role: verifier
  note: 有理円逐次構成による別証明の有限監査
- path: research/experiments/game-structure/scripts/independent_p3_audit_20261019.cpp
  role: verifier
  note: 7点P3別構成の独立C++検算
- path: research/experiments/game-structure/output/node_kayles_pspace_20261019.json
  role: data
  note: 88グラフ・全9614四点組・749安全残余局面の照合結果
scope: 標準q=4・完全指摘・通常プレイ。二進整数座標で明示された任意有限点盤と指定安全占有集合を入力する勝敗判定。全正方形格子盤および空盤だけの勝敗判定を含まない。
evidence: 2026-10-20添付統合。元資料では proved または computed と報告（個別の元statusは保存ZIPを参照）。本項目の全量化範囲に対する証明・計算の再監査は未完了。有限検証の実行範囲は統合実験のVALIDATION.mdを参照。
---


> 統合監査: 以下は取込元の主張・報告。全称証明・完全列挙の監査が未完了のため、現在の採用状態は needs-review。本文中の「証明」「一致」は元資料での報告を表す。


# 指定安全局面の共円ゲーム勝敗判定はPSPACE完全

任意有限単純グラフGの頂点数をv、辺数をeとする。K0348の整数円符号化はv+e+1点の有限盤Bを作り、禁止四点は各辺uvについて{p,s_u,s_v,s_e}だけとなる。

安全占有集合S={p}∪{s_e:e∈E}からの残余禁止集合は正確にグラフGの辺集合であり、任意の安全継続局面のGrundy値までNode Kaylesに一致する。Node Kaylesの勝敗判定はPSPACE完全（Schaefer 1978）なので、幾何構成が多項式時間・多項式ビット長であることからPSPACE困難。全ゲーム長は高々|B|であり、各合法手は整数行列式で多項式空間判定できるのでPSPACE所属。従ってPSPACE完全。

全点に三共線がなく、禁止四点が全て共通点pを通る円という特殊形でも困難性が成立する。独立の有理円逐次構成ではv+2e点でも同じ全状態同型を証明できる。

n≤4の全76ラベル付きグラフとn=5の固定乱数12グラフについて、全9,614四点組と749安全残余局面を厳密検査した。これは一般証明の代用ではない。

**標準n×n盤全体の勝敗判定や空盤の計算量は、この定理からは確定しない。**
