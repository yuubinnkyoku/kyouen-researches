---
id: K0356
title: 任意次元平行列容量ゲームの容量境界ではGrundy値が余剰列数と閾値の小さい方以下
kind: proposition
status: proved
topics: [variants, grundy]
aliases: []
relations:
- type: depends_on
  target: K0352
  note: 任意次元平行列盤を上位h=d−1列の容量ゲームへ縮約する
artifacts: []
scope: K0352の抽象容量ゲーム。d≥3, h=d−1, w≥d, 0≤x_i≤m, x_1≥...≥x_w, 上位h成分和が容量rに等しい全安全局面
evidence: 容量境界上の合法手軌道を直接分類し、mexの定義から得る全称数学的証明
---

# 容量境界上のGrundy上界

K0352の容量ゲームで、降順占有数を
`x_1≥...≥x_w`、`h=d−1` とし、容量境界

[
x_1+cdots+x_h=r
]

上の安全局面を考える。

同じ占有数を持つ列は交換可能である。容量境界上で占有数 `a` の列を1増やす手が合法なのは
`a<x_h` の場合に限る。`a≥x_h` なら増加後の上位h成分和が `r+1` になる。
一方 `a<x_h` なら `a+1≤x_h` なので、増加後も上位h成分和はrのままである。

従って、交換対称性で同一視した合法な子局面の個数Dは、末尾 `w−h` 成分に実際に現れる
`x_h` 未満の相異なる整数値の個数に等しい。これらの値は
`0,1,...,x_h−1` の高々 `x_h` 種であり、置かれる列も高々 `w−h` 本なので

[
Dle min(w-h,x_h).
]

mexの定義から局面のGrundy値g(x)は子局面の相異なるGrundy値の個数を超えないため、

[
oxed{g(x)le min(w-h,x_h)}.
]

さらに上位h成分はいずれも `x_h` 以上で総和rだから `hx_h≤r`。よって

[
oxed{
g(x)le
min!left(w-d+1,leftlfloorrac{r}{d-1}ightflooright).
}
]

これは有限実験ではなく全称上界である。

特に容量境界上で `g(x)≥4` が起こるためには同時に

[
w-d+1ge4,qquad x_hge4,qquad rge4(d-1)
]

が必要である。従って `w-d+1≤3` または `r<4(d-1)` の族では、容量境界上の全局面で
`g≤3` が証明される。

この命題は容量に余裕のある局面 `x_1+cdots+x_h<r` のGrundy値を制限しない。
したがって任意次元容量ゲーム全体での `g≤3` 予想は依然として未証明である。
