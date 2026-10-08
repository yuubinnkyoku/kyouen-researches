---
id: K0367
title: 標準整数格子円の二重点行数は幅に対して一様に劣線形
kind: proposition
status: proved
topics:
- geometry
- rectangles
- variants
aliases: []
relations:
- type: depends_on
  target: K0001
  note: q点版共円ゲームの規則
artifacts:
- path: research/experiments/fixed-width/reports/prime-modular-uniform-sublinear-density.md
  role: proof
  note: 分母gの合同条件、3 mod 4素数とCRTによる全称証明
- path: research/experiments/fixed-width/scripts/check_local_prime_double_rows.py
  role: verifier
  note: 有限体上の局所平方剰余上界の独立確認
---

# 標準整数格子円の二重点行数は一様に劣線形

連続する w 本の整数水平行で、一本の実円が相異なる2整数格子点を通る行数の最大値を T(w) とする。横座標は全整数を許す。円そのものが w ごとに異なっても

\[
\boxed{T(w)=o(w).}
\]

この証明は素数定理を用いない初等的な独立証明である。K0370は素数定理を用いてより強い定量上界を与える。

整数根を持つ複数の行の番号差の最大公約数を g とすると、円方程式の係数 C について gC は整数になる。g が大きければ二重点行は間隔 g 以上で並ぶ。g が小さければ g と互いに素な任意個の素数 p≡3 (mod 4) を用い、各法の許容剰余類が高々 (p+3)/2 個であることから CRT によって密度を任意に小さくできる。分母処理を含む詳細な全称証明は proof artifact を参照。

任意の固定 ε>0 に対し十分大きい w で q>(1+ε)w なら、標準整数格子の q 点版共円・共線ゲームは全 m≥1、全安全局面 S で

\[
g(S)=(w\min(m,q-1)-|S|)\bmod2,\qquad M_{w,q}=q-1
\]

となる。m は任意だが水平行は連続した整数行に限る。有限素数の検査は支持資料であり、無限幅についての証明は代数と中国剰余定理による。
