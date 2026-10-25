---
id: K0563
title: 3×3二係数二次形式版207禁止族型のハイパーグラフ同型類は46
kind: proposition
status: computed
topics: [variants, geometry, grundy, verification]
aliases: []
relations:
- type: depends_on
  target: K0518
  note: 3×3二係数版の31直線・175交点・207禁止族型の完全分類
artifacts:
- path: research/experiments/quadratic-pencil-isomorphism-20261023/README.md
  role: proof
  note: 同型の定義、2方式の分類方法、結果と限界
- path: research/experiments/quadratic-pencil-isomorphism-20261023/isomorphism.py
  role: solver
  note: 禁止族の再生成、不変量bucket＋全探索同型判定、canonical form、自己同型計数
- path: research/experiments/quadratic-pencil-isomorphism-20261023/isomorphism-results.json
  role: data
  note: 全46類の代表・所属型・証人置換・自己同型位数・代表プロファイル
- path: research/log/2026-10-23-quadratic-pencil-isomorphism.md
  role: log
  note: 候補03の実行記録と残課題
scope: 3×3盤の二係数二次形式版 det[x²+λy²+μxy,x,y,1]=0（K0518）の全207禁止族型。同型は9点ラベルの置換による禁止族の一致
evidence: 禁止族を整数行列式の2経路で再生成しK0518の公開値と全照合した後、同型判定を全探索backtrackingと色精密化canonical formの2方式で実行して分割の一致を確認。全同型に証人置換を保存し直接代入で再検査
---

# 207型は46同型類に縮む

K0518 の3×3二係数分類で得た207禁止族型は、9点の置換による
ハイパーグラフ同型で **46類** に縮む。類サイズ分布は
`1:7類, 2:13類, 4:16類, 8:4類, 10:1類, 12:4類, 20:1類`。
generic は単独類、直線型31件は8類、交点型175件は37類で、
直線型と交点型が混ざる類はない。最大類は辺数4・空盤 `g=1` の交点型20件。

単独類は generic、直線 `λ=1`・`μ=0`・`λ=0`、交点 `(λ,μ)=(1,0)`・`(-1,0)`・`(0,0)` の7件。

Grundyプロファイル（安全局面数・空盤値・初手値多重集合・Grundy頻度・終局分布）は
各類上で一定だが、相異なるプロファイルは45種しかない。
代表 `(1/3,-1/6)` の類（12件）と代表 `(1/3,-2/3)` の類（8件）は、
辺数4・安全局面416・空盤 `g=1`・初手値すべて0・終局分布 `{6:2, 7:9}`・
Grundy頻度 `{0:192, 1:192, 2:16, 3:16}` まで完全に一致しながら、
自己同型位数が 4 と 8 で異なり同型ではない。
よってプロファイル全体の一致からも同型は結論できない。

有限完全計算の結果であり、一般定理ではない。係数平面上の反射・反転などの
変換がこれらの同型をどこまで説明するかは未解決（log の候補06・07）。
4×4二係数版や他の盤への外挿もしない。
