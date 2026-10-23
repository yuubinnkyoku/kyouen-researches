---
id: K0518
title: 二次形式4点禁止版の2〜4正方形全実数係数分類と3正方形二係数完全分類
kind: proposition
status: proved
topics: [variants, geometry, grundy, first-moves, verification]
aliases: []
relations:
- type: depends_on
  target: K0002
  note: 安全な追加のmex再帰と勝ち初手の規約
- type: depends_on
  target: K0504
  note: 退化を含む二次形式パラメータ版の定義
artifacts:
- path: research/experiments/quadratic-pencil-20261023/README.md
  role: proof
  note: 全実数から有限禁止族への全称帰着、完全計算の範囲と信頼境界
- path: research/experiments/quadratic-pencil-20261023/classify.py
  role: solver
  note: 3×3整数行列式と全subset mex
- path: research/experiments/quadratic-pencil-20261023/independent.py
  role: verifier
  note: 4×4置換行列式と独立合法手再帰、全安全局面照合
- path: research/experiments/quadratic-pencil-20261023/results.json
  role: data
  note: 一係数版2・3・4正方形の全51禁止族型
- path: research/experiments/quadratic-pencil-20261023/audit.json
  role: data
  note: 一係数版419950安全局面比較のreceipt
- path: research/experiments/quadratic-pencil-20261023/two_parameter.py
  role: verifier
  note: 二係数版の全直線・交点帰着、直接代入と全安全局面照合
- path: research/experiments/quadratic-pencil-20261023/two-parameter.json
  role: data
  note: 31直線175交点207型、81185安全局面比較
scope: B_nの相異なる4点にdet[x²+λy²+μxy,x,y,1]=0を禁止、退化を含む通常プレイ。μ=0ではn=2,3,4および3行5列・全実数λ、n=3では全実数λ,μ
evidence: 整数係数の一次式による全実数パラメータの有限帰着証明と全安全subsetの完全mex。別行列式・別合法手再帰による計501135安全局面比較、3行5列では追加191024安全局面比較
---

# 小盤二次形式版の全パラメータ分類

`μ=0` のとき、空盤Grundy値は2×2では常に1、3×3ではλ=0で0・他で1、
4×4ではλ=1で0・λ=−1で2・他で1。
従って4×4の後手勝ちは整数λに限らず**全実数λのうち1だけ**で成立する。
4×4、λ=−1の勝ち初手は中央2×2の4点だけ。全初手の値と全安全局面統計を保存した。

3×3で交差項μxyを加えると、31直線と175交点による207禁止族型で全実数平面を覆う。
型ごとの空盤値はg=0が31型、g=1が142型、g=2が16型、g=3が18型。
直線外は全9点が自由でg=1。単一直線型のPはλ=0、λ=1、λ−μ+1=0、λ+μ+1=0で、
いずれも他の直線との交点を除く。交点の分類は独立に保存している。

固定4点の行列式がパラメータの整数係数一次式となるため、例外点・直線と交点を列挙すれば全実数を尽くせる。
有限点パラメータの標本からの外挿ではない。有限帰着の数学的証明と、各禁止族の全局面完全計算を組み合わせた結果。
「型」は連結領域数ではなく禁止族の一致による区分。

5×5以上の一係数版や4×4以上の二係数版は対象外。通常の非退化楕円だけを禁じるゲームとも異なる。
計算はPythonで相互検査済みだが、Lean形式化・全局面証明書配布は行っていない。

## 追加：3行5列盤の全実数λ（2026-10-23）

整数格子 `0≤x≤4, 0≤y≤2` では例外係数が31個、一般型を含む32禁止族型となる。
空盤Grundy値は `g=0` が `λ∈{−3,−2,−1,0,1}`、`g=2` が `λ∈{3/2,2}`、`g=3` が `λ∈{−4,−3/2,3,5}`、その他の全実数で `g=1`。
3×3差分行列式・全subset mexと独立4×4置換行列式・上からの再帰を比較し、全32型の計191024安全局面について空盤値・局面数・勝ち初手を一致確認した。
有限帰着と全型の完全列挙により全実数を覆う。詳細と再現コードは [3×5係数分類](../../experiments/quadratic-pencil-3x5-20261023/README.md) を参照。任意の盤長への外挿ではない。
