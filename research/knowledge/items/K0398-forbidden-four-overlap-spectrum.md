---
id: K0398
title: 共円・共線禁止四点組の全交差分布の厳密公式
kind: proposition
status: proved
topics:
- geometry
- statistics
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 標準禁止四点組の定義
- type: generalizes
  target: K0057
  note: 禁止四点組の総数を交差分布へ拡張
artifacts:
- path: research/experiments/geometry/reports/forbidden-four-overlap-exact-20261011.md
  role: proof
  note: 任意有限点集合の曲線束公式と11×11の厳密計数
- path: research/experiments/geometry/scripts/curve_overlap.py
  role: verifier
  note: 直線・円の整数係数による曲線束の計数
- path: research/experiments/geometry/scripts/direct_quad_overlap.cpp
  role: verifier
  note: 整数行列式による独立の完全列挙
- path: research/experiments/geometry/output/forbidden-four-overlap-census-20261011.json
  role: data
  note: 2×2〜11×11の全交差分布と曲線束スペクトル
---

# 禁止四点組の全交差分布の全称公式

任意の有限な相異なる平面点集合 P に対し、4点以上の盤点を含む直線または真円を C とし、点数を k_C とする。共線・共円の禁止四点組の異なる順序なし対で共通点が j 個のものを O_j とする。

\[
O_3=10\sum_C\binom{k_C}{5},\quad
O_2=45\sum_C\binom{k_C}{6}+\sum_{\{C,D\}:|C\cap D\cap P|=2}\binom{k_C-2}{2}\binom{k_D-2}{2}.
\]

残る O_1, O_0 は点次数と点対次数の二重計数で厳密に決まる。証明は一次資料の曲線束一意性と交差数の上界による。

11×11標準盤の有限完全計数は (O0,O1,O2,O3)=(3994540561,552180034,28906140,699880)。二独立実装で正方形n=3..11と長方形6盤を照合した。これは数学的全称公式とは別の有限完全計算であり、勝敗への直接の帰結は主張しない。

**統合注意**：このファイルはmain未反映の候補。採番衝突を確認し、必要なら再採番し、`uv run --locked python tools/knowledge/build.py` により生成物を再構築する。生成領域は手編集しない。
