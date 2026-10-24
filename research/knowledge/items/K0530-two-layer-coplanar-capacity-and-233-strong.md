---
id: K0530
title: 2×k×m・4点共面禁止版の全長容量・三石極大数と2×3×3の全局面
kind: proposition
status: proved
topics: [variants, geometry, maximum-safe, maximal-safe, grundy, first-moves]
aliases: []
relations:
- type: depends_on
  target: K0002
  note: 通常・misèreのGrundy定義
- type: generalizes
  target: K0527
  note: 2×2×mのK・sを含むが、全局面Grundy偶奇則は一般化しない
- type: generalizes
  target: K0526
  note: 2×2×2の容量と最小極大石数を含む
artifacts:
- path: research/experiments/coplanar-two-layer-all-widths-20261024/proof.md
  role: proof
  note: 全k,mの容量・三石極大数の数学的証明と2×3×3の完全列挙境界
- path: research/experiments/coplanar-two-layer-all-widths-20261024/verify.py
  role: verifier
  note: 3×3整数行列式と全安全局面mex
- path: research/experiments/coplanar-two-layer-all-widths-20261024/independent.cpp
  role: verifier
  note: 独立4×4行列式と全局面再帰
- path: research/experiments/coplanar-two-layer-all-widths-20261024/results.md
  role: data
  note: 4盤の独立一致結果と境界盤の局面分布
scope: 3次元2×k×m整数格子・4点共面禁止・全k,m≥1のK,s,三石極大数、2×3×3の全安全局面
solution:
  board: 2×3×3・4点共面禁止
  level: strong
  outcome: conditional
  classification: [root, first-moves, all-safe-win-loss, all-safe-grundy, safe-layers]
  coverage: 2×3×3の全6456安全局面。全k,mのK,s,三石極大数は数学的証明
  conditions: 通常は先手勝ち、misèreは後手勝ち。一般の2×k×mの空盤勝敗は未解決
  verification: [mathematical-proof, exhaustive-enumeration, independent-enumeration]
  certificate: 全k,mの容量・三石極大数の初等証明と2×3×3の全2^18部分集合検査
  independent_check: Python外積とC++4×4行列式展開で4盤の全局面集計が一致
  note: k,m≥3はK=6,s=3。2×3×3ではg(空)=1,h(空)=0、通常勝ち初手8個
---

# 2×k×mの4点共面禁止版

全整数k,m≥1について、Kは(1,1)で2、min(k,m)=1かつkm>1で3、min(k,m)=2で5、k,m≥3で6。最小極大石数sは(1,1)で2、(2,2)で4、それ以外は3。k,m≥2では三石極大配置は共線三石に限り、個数は `2T(k,m)`（Tは格子k×m内の共線三石数）。これらは全称証明済み。

2×3×3は安全局面6456、極大局面は3石16・5石1064・6石368。通常空盤Grundy値1、misère補助値0。通常版は8個の勝ち初手を持つ先手勝ち、misère版は後手勝ち。これらは二方式の独立した有限完全列挙で確定。

[証明と検証手順](../../experiments/coplanar-two-layer-all-widths-20261024/proof.md)。一般の2×k×mの全局面Grundy値や空盤勝敗を主張しない。


## 追加確定：両方向7以上の全安全局面

**k,m≥3** では既に4石の極大配置が存在しないことを全称証明した。さらに **k,m≥7** なら5石の極大配置も存在せず、終局は同層の共線三石または六石に限られる。全安全局面の通常Grundy値とmisère補助値を次のように全称的に決定した。

- 空盤は `(g,h)=(0,1)`（通常は後手勝ち、misèreは先手勝ち）。
- 一石は `(1,0)`。二石は、同層の共線三石に延長できる組だけ `(2,2)`、その他は `(0,1)`。
- 三石は共線なら `(0,1)`、非共線なら `(1,0)`。
- 四石は `(0,1)`、五石は `(1,0)`、六石は `(0,1)`。

したがって全安全局面で通常とmisèreの `0↔1` 交換則が成立し、2は保存される。これは7×7部分格子の直線被覆補題を使った**数学的全称証明**であり、7は一様十分条件（最小値は未確定）。既存の2×3×3の全局面有限計算とは適用範囲が異なる。[追加証明](../../experiments/coplanar-two-layer-all-widths-20261024/proof.md)・[完全列挙と標本検算](../../experiments/coplanar-two-layer-all-widths-20261024/results.md)。


**正方断面では真の閾値まで決定した。** `2×n×n` の全安全局面に上記Grundy表が成立する最小nは **5**。n=4には608個の五石極大反例がある。n=5,6はC++の方向判定とPythonの方向集合ビットマスクによる独立した有限完全列挙で五石極大0件を確認し、n≥7は上記全称証明で覆う。一般長方断面の最小閾値まで5と主張するものではない。


## 追証：長方断面の真の一様閾値は5

正方断面に限っていた結論を**任意の `k,m≥5`** に拡張した。五石安全配置からの第六石追加を妨げる七直線には四つの異なる方向があり、水平線は高々二本。短辺 `k≥5`、長辺 `m≥8` なら行ごとの被覆数だけで追加可能。長辺 `m=7` では七本が全行を覆う必要があるが、各直線の整数傾きは `-1,0,1` に限られ、四方向という条件と矛盾する。残る `5×5,5×6,6×6` は独立二方式で有限完全列挙し、向き付き安全五石数が475400、1278380、3408680、極大五石数が全て0で一致した。

これにより**全安全局面の通常・misère値の表は長方断面 `min(k,m)≥5` の全域で成立**する。`4×4` に五石極大608個があるので、`min(k,m)` のみによる一様閾値は厳密に5。無界部分は数学的証明、三つの境界盤は独立有限完全列挙。既存の「一般長方断面の閾値未確定」という記述は本追証で解消した。[証明](../../experiments/coplanar-two-layer-all-widths-20261024/proof.md)・[結果](../../experiments/coplanar-two-layer-all-widths-20261024/results.md)・[Python検証器](../../experiments/coplanar-two-layer-all-widths-20261024/rect_5x6_slope_audit.py)・[独立C++検証器](../../experiments/coplanar-two-layer-all-widths-20261024/rect_5x6_independent.cpp)。
