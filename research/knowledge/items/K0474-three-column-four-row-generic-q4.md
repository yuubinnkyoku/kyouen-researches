---
id: K0474
title: 不等間隔三列四行q4の一般位置は後手勝ちで全初手Grundy値4
kind: proposition
status: needs-review
topics:
- rectangles
- variants
- geometry
- grundy
- first-moves
- maximal-safe
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 四点共円・共線を禁止する完全指摘の安全手版
- type: depends_on
  target: K0434
  note: 整数行列式による禁止四点判定の正当性
artifacts:
- path: research/experiments/fixed-width/reports/three-column-four-row-generic-q4-20261017.md
  role: proof
  note: 三列円の整数等式、積の鋭い上界、有限ゲームの全称還元
- path: research/experiments/fixed-width/scripts/three_column_four_row_generic_q4_20261017.py
  role: verifier
  note: 算術判定と整数行列式の独立照合、全局面Grundy値の二重計算
- path: research/experiments/fixed-width/scripts/three_column_four_row_generic_q4_independent_20261017.cpp
  role: verifier
  note: C++17の4×4置換行列式と再帰mexによる独立監査
- path: research/experiments/fixed-width/output/three_column_four_row_generic_q4_20261017.txt
  role: data
  note: 4096パラメータと1655安全局面の検査結果
- path: research/experiments/fixed-width/output/three_column_four_row_generic_q4_independent_20261017.txt
  role: data
  note: C++17独立監査の実行出力
solution:
  board: 不等間隔3列×4行・q=4
  level: strong
  outcome: second-player-win
  classification:
  - root
  - first-moves
  - all-safe-win-loss
  - all-safe-grundy
  coverage: 指定された算術条件を満たす全正整数a,b,dの全安全局面
  conditions: d²がab(a+b)を割らない、またはab>6d²、より一般に三列円判定式288個が全て不成立
  verification:
  - mathematical-proof
  - exhaustive-enumeration
  - independent-enumeration
  certificate: 円の完全算術判定と27禁止組への還元、12ビット1655安全局面の完全mex計算
  independent_check: Pythonの整数3×3行列式とC++の整数4×4置換行列式、別方式の再帰が一致
  note: 空盤g=0、全12初手g=4、極大石数5/6/7
evidence: 2026-10-20添付統合。元資料では proved または computed と報告（個別の元statusは保存ZIPを参照）。本項目の全量化範囲に対する証明・計算の再監査は未完了。有限検証の実行範囲は統合実験のVALIDATION.mdを参照。
---


> 統合監査: 以下は取込元の主張・報告。全称証明・完全列挙の監査が未完了のため、現在の採用状態は needs-review。本文中の「証明」「一致」は元資料での報告を表す。


# 不等間隔三列四行q4の一般位置

正整数a,b,dについて盤面を `x∈{0,a,a+b}, y∈{0,d,2d,3d}` とする。三列にまたがる四点円が存在する必要十分条件は、二点を含む列の行番号u<vと他列の行番号r,tを選び、S=u+v、T_iを二点列ではuv、一点列ではj(S-j)と置いたとき

\[
 d^2\{bT_0-(a+b)T_1+aT_2\}=ab(a+b)
\]

を満たす選択があること。候補は288個。特に存在には `d²|ab(a+b)` と `ab≤6d²` が必要で、後者の定数6は `a=2,b=3,d=1` で鋭い。

三列円が存在しなければ、禁止四点組は縦列の直線3組と、二列の行番号対の和が一致する円24組、計27組のみ。この場合の抽象ゲームはパラメータに依存せず、安全局面は1655個、Grundy度数は0から順に397,514,384,324,36、極大安全配置は5石12個、6石144個、7石24個である。

\[
 g(\varnothing)=0,\qquad g(\{p\})=4\quad(\forall p\in B).
\]

全称幾何証明と有限12ビットゲームの完全再帰を組み合わせた結果である。Pythonと独立C++の全安全局面再計算が一致した。`d²∤ab(a+b)` または `ab>6d²` は適用しやすい十分条件であり、一般位置の必要条件ではない。三列円が存在する場合の勝敗はこの項目では分類しない。標準格子3×4（K0351）では空盤g=2となり、適用範囲が異なる。
