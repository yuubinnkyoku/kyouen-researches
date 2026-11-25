---
id: K0532
title: 二次形式λ版は有理点盤で有限例外以外同一となり、任意二水平行では全λで同一
kind: proposition
status: proved
topics: [variants, geometry, grundy, rectangles]
aliases: []
relations:
- type: depends_on
  target: K0002
  note: 同じ合法遷移から全Grundy値と勝ち手の一致を得る
- type: depends_on
  target: K0069
  note: 二水平行の不変性を用いた数値的帰結には既存強解決を使用
artifacts:
- path: research/experiments/quadratic-lambda-20261024/proof.md
  role: proof
  note: 有限例外・転置・縮尺・二水平行不変性の全称証明
- path: research/experiments/quadratic-lambda-20261024/verify.py
  role: verifier
  note: 整数係数二方式・二行条件・転置対応の有限監査
- path: research/experiments/quadratic-lambda-20261024/results.json
  role: data
  note: 有限監査結果。全称性はproof.mdの代数的証明による
scope: det[x²+λy²,x,y,1]=0の四点禁止・通常プレイ。有限分類は任意有限有理点盤、二水平行不変性は任意有限実数点盤。
evidence: 行列式の線形性・列操作による恒等式と合法遷移の一致による数学的証明
---

# 二次形式λ版の有限分類と二行不変性

四点Qの係数をb_Q=det[x²,x,y,1]、a_Q=det[y²,x,y,1]とすると、
禁止判定はb_Q+λa_Q=0である。有理座標盤では例外集合
E={−b_Q/a_Q:a_Q≠0}は有限有理集合で、E外の全実数λは
共通禁止族{Q:a_Q=b_Q=0}を持つ。異なる区間や無理数を含め
同じゲームであり、各例外と共通族だけで全パラメータを分類できる。

λ≠0では盤の転置がλと1/λの全局面同型を与える。
点盤を(αx,βy)へ写すとパラメータはλα²/β²へ対応する。
後者は盤自体も変えるため、固定正方形盤の全正λが同じとはいえない。

任意の二水平行y∈{u,v}ではy²=(u+v)y−uvによりλ項が消え、
実数座標・不等候補集合を含め全λで全ゲームが同一になる。
標準二行盤{0,...,m−1}×{0,1}にはK0069が全実数λで適用でき、
全m・全安全局面でg≤3、m≥6の空盤は後手必勝、
m≥9ではg(S)=(6−|S|) mod2。

二鉛直列ではλ≠0のみλ=1と同じで、λ=0では全四点禁止となる。
非退化楕円・双曲線だけを禁止する別ルールや、
任意サイズの正方形盤の勝敗公式へは拡張しない。
