---
id: K0388
title: 中央弦型2+1+1共円完成数と弦長集合の密度
kind: proposition
status: proved
topics:
- geometry
- statistics
aliases: []
relations: []
artifacts:
- path: research/experiments/geometry/reports/central-211-two-squares-density-20261011.md
  role: proof
  note: 全単射・素因数判定・Pell無限族・CRT篩による密度0の証明
- path: research/experiments/geometry/scripts/verify_central_211_two_squares.py
  role: verifier
  note: 独立4×4整数行列式・二平方和表現・素因数公式の有限照合
- path: research/experiments/geometry/output/central_211_two_squares_audit_20261011.json
  role: data
  note: 有限監査の実行記録
---

# 等間隔三行の中央弦型共円完成数と弦長密度

任意の正整数 `h,d` について、`(0,0),(d,0),(u,-h),(v,h)` が共円となる整数対 `(u,v)` の個数は、`a²+b²=d²-4h²` の順序・符号付き整数解数 `r₂(d²-4h²)` に等しい。

全単射は `(a,b)=(u+v-d,u-v)` であり、逆変換は `(u,v)=((d+a+b)/2,(d+a-b)/2)`。法2の合同条件は自動的に成立する。

従って `d<2h` では完成0、`d=2h` では1、`d>2h` では `d²-4h²` に現れる `3 mod 4` の素数の指数がすべて偶数であることが存在の必要十分条件。正の場合の完成数は二平方和表現数の素因数公式で与えられる。

各固定 `h` に対して完成可能な弦長 `d` は無限個存在するが、その自然密度は0である。無限性は `k²-2t²=1` のPell解から `d=2hk` を構成して証明する。密度0は `3 mod 4` 素数に対する `p²` 合同障害と中国剰余定理、および当該算術級数の素数逆数和の発散から従う。

対象は無限整数格子の**等間隔三水平行・中央行に2点**の型に限る。有限幅に収まる完成数、他の2+1+1型、ゲーム勝敗は含まない。独立行列式による144条件275,544候補の完全列挙、素因数公式3,600条件、Pell証人250条件は有限監査であり、全称性の根拠は別途記した数学的証明である。
