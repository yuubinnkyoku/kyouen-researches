---
id: K0396
title: 任意次元整数直方格子の共線q点組数と直線長分布の厳密公式
kind: proposition
status: proved
topics:
- geometry
- statistics
aliases: []
relations: []
artifacts:
- path: research/experiments/geometry/reports/d-dimensional-collinear-run-identity-20261011.md
  role: proof
  note: 任意次元の原始方向ラン長・二階差分公式とアフィン不変性の全称証明
- path: research/experiments/geometry/scripts/verify_dimensional_collinear_20261011.py
  role: verifier
  note: 点対から直線を独立構築し2〜4次元153条件を照合
- path: research/experiments/geometry/output/d-dimensional-collinear-20261011.txt
  role: data
  note: 153条件の一致と5条件の第三方式照合記録
- path: research/experiments/geometry/reports/box-collinear-all-q-jordan-20261011.md
  role: proof
  note: 全単射による全称証明とJordan関数の展開
- path: research/experiments/geometry/scripts/verify_all_q_collinear_jordan_20261011.py
  role: verifier
  note: 直線列挙1223条件とJordan独立検査4491条件
- path: research/experiments/geometry/reports/box-collinear-mobius-all-q-20261011.md
  role: proof
  note: Möbius反転による全q公式
- path: research/experiments/geometry/scripts/verify_mobius_collinear_20261011.py
  role: verifier
  note: 全q divisor-sum照合
- path: research/experiments/geometry/output/box-collinear-mobius-verification-20261011.txt
  role: data
  note: 検査結果
- path: research/experiments/geometry/reports/primitive-line-length-histogram-20261011.md
  role: proof
  note: 直線長分布と重複統計
- path: research/experiments/geometry/scripts/verify_primitive_line_histogram_20261011.py
  role: verifier
  note: 直線長独立照合
- path: research/experiments/geometry/output/primitive-line-length-histogram-20261011.txt
  role: data
  note: 監査出力
- path: research/experiments/geometry/reports/rectangular-high-q-collinear-closed-form-20261011-ja.md
  role: proof
  note: 高q箱公式の閉形式展開
- path: research/experiments/geometry/scripts/verify_rectangular_high_q_collinear_20261011.py
  role: verifier
  note: 有限条件の独立検査
- path: research/experiments/geometry/output/high_q_box_521_cases.txt
  role: data
  note: 521条件の結果
scope: 任意有限次元整数直方格子、q>=2の共線q点組数と直線長分布
evidence: 原始方向ラン長・二階差分とMöbius/Jordan反転の全称導出。
---

任意次元整数直方格子の共線q点組数・盤内直線長分布は有限和で厳密に決まる。原始方向v（最初の非零成分を正）で `A_k(v)=∏_i max(0,n_i−(k−1)|v_i|)` とすると、少なくともk点を含む直線数はA_k、ちょうどk点の直線数は `E_k=A_k−2A_{k+1}+A_{k+2}`。従って `H_q=Σ_vΣ_{k>=q} binom(k−2,q−2)A_k`。

同じ計数はMöbius/Jordanの約数和でも表せる。`N=max_i n_i`, `L_i=floor((n_i−1)/s)`, `T_i(s)=n_i(2L_i+1)−sL_i(L_i+1)`, `W_q(s)=Σ_{t|s}μ(s/t)binom(t−1,q−2)` とすれば `H_q=(1/2)Σ_{s=1}^{N−1}W_q(s)(∏_iT_i(s)−∏_in_i)`。直線長分布から重複統計も得られる。

適用範囲は全有限次元整数直方格子、q>=2。原始方向ラン長・二階差分・Möbius反転の全称証明による。共円配置やゲーム勝敗は含まない。
