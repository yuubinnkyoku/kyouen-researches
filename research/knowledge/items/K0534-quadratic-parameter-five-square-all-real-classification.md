---
id: K0534
title: 二次形式λ版5×5を全実数で強分類し後手必勝は13個のλに限られる
kind: computation
status: computed
topics: [variants, geometry, grundy, square-outcomes, first-moves, verification]
aliases: []
relations:
- type: depends_on
  target: K0532
  note: 有限有理例外と共通禁止族への帰着で全実数パラメータを被覆
- type: verifies
  target: K0518
  note: 別C++幾何・増分再帰で既存51分類の禁止辺・全分布・全初手値を再現
artifacts:
- path: research/experiments/quadratic-lambda-five-20261024/README.md
  role: log
  note: 全実数分類・検算手法・証拠範囲と再現手順
- path: research/experiments/quadratic-lambda-five-20261024/run.py
  role: verifier
  note: 二方式コンパイルと全局面値配列のバイト単位一致検査
- path: research/experiments/quadratic-lambda-five-20261024/census.cpp
  role: solver
  note: 独立整数行列式・三点補完増分伝播による全安全局面mex
- path: research/experiments/quadratic-lambda-five-20261024/audit.cpp
  role: verifier
  note: 原禁止辺による全subset安全性DPと逆順Grundy DP
- path: research/experiments/quadratic-lambda-five-20261024/results.json
  role: data
  note: 全168分類・延べ89789920安全局面・全初手Grundy・再構成可能な禁止辺
scope: "{0,...,4}²、任意実数λ、四点のdet[x²+λy²,x,y,1]=0を禁止する通常プレイの全安全局面。"
evidence: 全12650四点組の係数を二方式で照合し、共通284辺と167例外の168族を二C++方式で全安全局面の値まで完全照合。
---

# 二次形式λ版5×5の全実数強分類

後手必勝となるパラメータの集合は厳密に

`{−4,−3,−2,−3/2,−2/3,−1/2,−1/3,−1/4,0,1/2,2/3,3/2,2}`。

λ=3または1/3なら空盤Grundy値3。
上記13個と3・1/3を除くすべての実数λでは空盤Grundy値1。
全実数には負数・0・無理数も含む。

全実数を167個の有理例外と共通禁止族に帰着し、168族の延べ89,789,920安全局面で
各局面のGrundy値を独立な二つのC++方式で完全一致させた。
全安全局面の最大Grundy値は7である。
例外外では共通284辺の同じゲームとなり、全25初手が勝ち手。
全初手の子Grundy値と禁止辺を復元できるデータを保存した。

これは5×5についての有限全数分類とK0507の全実数帰着の組合せである。
6×6以上の全λ分類や、非退化図形だけを禁止するルールは対象外。
標準λ=1の5×5の既存結果も再現した。
