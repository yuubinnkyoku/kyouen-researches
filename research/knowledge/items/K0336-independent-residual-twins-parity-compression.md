---
id: K0336
title: 同一linkの独立双子点は正の偶奇数へ減らしてもGrundy数が一致する
kind: proposition
status: proved
topics:
- residual-games
- grundy
- search-methods
aliases: []
relations:
- type: depends_on
  target: K0108
  note: 全極小残余hypergraphによる継続ゲームの表現。Pグラフだけでは足りない
- type: depends_on
  target: K0002
  note: 通常プレイのmexと分離成分のxor
artifacts:
- path: research/experiments/n11-residual-twins/reports/twin-parity.md
  role: proof
  note: 外部点数の帰納法による任意有限rankの全称証明と必要条件の反例
- path: research/experiments/n11-residual-twins/scripts/twin_core.py
  role: solver
  note: 全link判定、正の偶奇圧縮、残余mex、独立な占有subset mex
- path: research/experiments/n11-residual-twins/scripts/sample_residual_twins.cpp
  role: solver
  note: 共有128-bit geometryを再利用したn4..11のbounded greedy snapshot生成
- path: research/experiments/n11-residual-twins/scripts/verify_twins.py
  role: verifier
  note: m≤5の全clutter監査と、保存格子証人の全L・最小R・Grundy再検査
- path: research/experiments/n11-residual-twins/output/geometry-samples.json
  role: data
  note: seed20261005、各盤200軌跡のlate snapshot頻度と存在証人。全局面列挙ではない
- path: research/experiments/n11-residual-twins/output/verified.json
  role: data
  note: 7020clutterの全検査、72圧縮例のmex一致、各盤保存証人の独立監査
scope: 任意有限点集合・任意rankの禁止hyperedgeを避ける一点追加通常プレイ。現在合法な点の包含極小残余辺について全linkが同じ非空classを同じ正の偶奇数まで減らす。misère・終局手数・Pグラフのみの判定は含まない。
evidence: 外部点数の帰納法による全称証明。別占有subset DPによる小clutter完全検査、Python geometryによるn4..11の存在証人監査。
---

# 同一linkの独立双子点の正の偶奇圧縮

現在合法点Vと極小残余禁止辺Fの通常ゲームで、点vの全linkを
`L_v={e\{v}:e∈F,v∈e}` とする。同じlinkを持つclass Xの大きさk>0を、
同じ正の偶奇の最小数（奇数なら1、偶数なら2）へ減らし、消した点を含む
辺を削除してもGrundy数は変わらない。任意有限rank・任意有限点集合で成立する。

同じlinkの相異なる点は同じ辺に入らない。Xを一つ打つと残るk−1点は全て
孤立し、kに依存しない外部ゲームとのxorになる。外部手はXを全て禁止するか、
Xの同一linkを保ったまま外部点を減らす。外部点数の帰納法とmexで全称証明する。
通常プレイの他ゲームとの直和でも等価だが、ゲーム木同型や終局手数の一致ではない。

偶数非孤立classをゼロまたは一つへ減らすことは不正。二葉starは元g=2に対し
一葉・無葉のいずれもg=1。全hypergraph linkを使う必要があり、Pグラフだけの
判定は三点辺一つのg=0を一頂点のg=1へ誤って変えてしまう。

m≤5の全7020clutterを列挙し、圧縮できる72（非孤立59）で元・圧縮後の
直接subset mexと残余mexが一致した。この有限検査を全称証明の代わりにはしない。

実格子ではn4..11の保存終盤証人をPythonの別geometry/coreで検査した。
n11の14石証人は `L={0,2,10,13,100}`、
`R={{0,10},{2,10},{10,100}}` で、X={0,2,100}を一つへ圧縮できる。
直接mexで元も圧縮後もg=0、同一残余solverのmemoは16→4状態だった。

seed固定200本のn11 greedy軌跡のlate snapshot822回では、圧縮可能23回、
非孤立圧縮可能9回を観測した。重複を許す選択標本であり全局面の比率ではない。
小終盤の状態数節約からs5・空盤df-pnの速度改善は主張しない。全R構築コストと
実探索profileでの有効性は未検証。11×11空盤勝敗は引き続きUNKNOWN。
