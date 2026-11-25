---
id: K0360
title: 任意次元の容量余裕3は二値境界署名で全Grundyを決定でき上界3が鋭い
kind: proposition
status: proved
topics: [variants, grundy, strategy-length]
aliases: []
relations:
- type: depends_on
  target: K0359
  note: 余裕2の全称Grundy閉公式から上位着手子の二値署名を求める
- type: depends_on
  target: K0352
  note: 容量ゲームの定義・飽和列除去と平行移動のゲーム木同型を用いる
artifacts:
- path: research/experiments/capacity-slack-three-20261008/README.md
  role: proof
  note: 境界署名の定義と全称mex帰納・全次元での鋭さ構成
- path: research/experiments/capacity-slack-three-20261008/check_slack_three.py
  role: verifier
  note: 418819の容量余裕3安全降順局面について独立mexで全件一致
scope: 抽象容量占有ゲームの全整数2<=h<w、m>=1、r<h*m、容量余裕sigma=3の全安全局面。幾何学的平行列盤への移送にはK0352の幾何条件が必要。
evidence: K0359の余裕2閉公式に基づく容量余裕3の二値境界署名とRに関する全称mex帰納証明、無限族の鋭さ構成、独立有限完全mex検証
---

# 容量余裕3の完全Grundy閉公式

降順安全状態 `x=(x_1,...,x_w)`、`sum_{i<=h}x_i=r-3` と置く。`n=w-h`、`b=x_h`、`R=nb-sum_{i>h}x_i`。

上位 `h` 列のうち高さが `m` 未満の列を一つ増やした全ての（降順に正規化した）子局面 `y` の集合を `U(x)` とする。余裕3なので `U(x)` は空でなく、各 `y` の容量余裕は2である。K0359の局所指標を

```
c(y) = #{i<=h:y_i=y_h}
D(y) = sum_{i<h}(m-y_i)
eta(y) = 1 if (c(y)==1 and (y_{h-1}-y_h==1 or D(y)==1)) else 0
epsilon(y) = (n*(y_h-b)+(n mod2)*eta(y)) mod2
S(x) = {epsilon(y):y in U(x)}
```

で定義する。`S(x)` は空でない部分集合 `{0,1}` で、最初の `h` 列の占有形だけから計算できる。

**全称公式：**

```
S(x)={e}   なら g(x)=(R+e+1) mod2
S(x)={0,1} なら g(x)=2+(R mod2)
```

従って **容量余裕3のすべての局面で `g<=3`**。奇数 `n` では `g>=2` と `S(x)={0,1}` は同値である。偶数 `n` では `S(x)={0}`、かつ `g=(R+1) mod2`。

## 無界・全称証明

任意の上位着手子 `y` は容量余裕2なので K0359 より

```
g(y)=(n*y_h-sum_{i>h}y_i+(n mod2)*eta(y)) mod2
     =(R+epsilon(y)) mod2.
```

よって上位着手子のGrundy値集合は `E_R={(R+e) mod2:e in S(x)}` と完全に決定する。容量余裕3を維持する手は `b` 未満の下位列への着手のみで、必ず `R` を1減らし `S(x)` を変えない。`R=0` では維持手がなく、`S={e}` のとき `mex(E_0)=1-e`、`S={0,1}` のとき `mex(E_0)=2`。これが基底。

`R>0` では維持手があり、帰納的に各維持子のGrundyは、`S={e}` の場合 `(R+e) mod2`、`S={0,1}` の場合 `2+((R-1) mod2)` となる。前者は全上位着手子の値と同じなのでmexは `(R+e+1) mod2`。後者は上位子の値 `{0,1}` に `2+((R-1) mod2)` を加えてmexを取ると `2+(R mod2)`。よって帰納法が閉じる。□

## 鋭さと限界

任意の奇数 `n>=1` に対して `h=2,w=n+2` で、`(m,r,x)=(4,4,(1,0^{n+1}))` は `g=2`、`(5,6,(2,1,0^n))` は `g=3` となる。任意の `h>2` は先頭への `h-2` 本の満杯列の追加と `r` の増加により K0352 の同型から実現する。全占有数に一定値を足し、`m,r` を対応して増やす同型で、必要な幾何条件 `q=r+1>2w` も満たせる。従って奇数余剰列なら **あらゆる `h,n` で鋭い**。

独立mex再帰による `3<=w<=9,1<=m<=8,3<=r<hm` の容量余裕3局面 **418,819件** の全検査で不一致0。証明と検証器は [実験記録](../../experiments/capacity-slack-three-20261008/README.md) にある。

容量余裕0（K0356）、1（K0358）、2（K0359）、3（本項）まで完全分類済み。ただし **余裕4以上の全局面における `g<=3` は未証明**である。
