---
id: K0385
title: 400幅以内に25二重点行を持つ円の行差最大公約数は1
kind: proposition
status: proved
topics:
- geometry
- rectangles
aliases: []
relations:
- type: depends_on
  target: K0072
  note: 二重点行の整数係数・合同式の必要条件
artifacts:
- path: research/experiments/fixed-width/reports/gcd-one-400-proof.md
  role: proof
  note: 360行起点の両端帰納法と361〜400行の合同完全排除
- path: research/experiments/fixed-width/reports/gcd-one-360-proof.md
  role: proof
  note: 360行の基底補題と合同完全排除
- path: research/experiments/fixed-width/scripts/verify_gcd_one_361_400_direct.cpp
  role: verifier
  note: 4語マスクを使った直接平方剰余列挙
- path: research/experiments/fixed-width/scripts/verify_gcd_one_361_400_inverse.cpp
  role: verifier
  note: 逆向き平方剰余構成による独立照合
---

連続する高々400本の整数水平行のうち、同じ実円が相異なる整数格子点を二つずつ持つ行が25本以上あるなら、それらの行番号差の最大公約数は1。従って円を x²+y²+Bx+Cy+D=0 と書けば B,C,D は整数。

360行以下については二独立C++検証器の合同排除、361〜400行については両端行が必須となる帰納法と二独立C++検証器の有限完全排除を組み合わせる。全40幅の検査が成功し、426合同段階の候補数が一致した。数学的必要条件の緩和を用いているため、有限探索結果を任意の円へ帰着できる。無限幅の主張でも、25行の存在や T(190)=24 の証明でもない。
