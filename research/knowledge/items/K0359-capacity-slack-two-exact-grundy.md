---
id: K0359
title: 任意次元容量ゲームの余裕2層は全局面二値Grundyで閉公式を持つ
kind: proposition
status: proved
topics: [variants, grundy, strategy-length]
aliases: []
relations:
- type: depends_on
  target: K0358
  note: 余裕1に移る全子のGrundy値を正確に分類する
- type: depends_on
  target: K0352
  note: 容量ゲームの安全性と偶数余剰列の二値Grundy公式を用いる
artifacts:
- path: research/experiments/capacity-slack-two-20261008/README.md
  role: proof
  note: 余裕2の全称閉公式・7場合の子値分類・mex帰納証明
- path: research/experiments/capacity-slack-two-20261008/check_slack_two.py
  role: verifier
  note: 独立mex再帰による449322局面の全パラメータ有限検査
- path: research/experiments/capacity-slack-two-20261008/check_child_types.py
  role: verifier
  note: 余裕1への全子Grundy集合の52787局面独立確認
scope: 抽象容量占有ゲームの全整数2<=h<w、m>=1、r<h*m、容量余裕sigma=2の全安全降順局面。幾何学的な平行列盤への移送にはK0352の追加条件が必要。
evidence: K0358の全称値分類とRに関する7場合のmex帰納法による無界数学的証明、別実装の有限完全列挙2種
---

# 容量余裕2は完全に二値であり、Grundy値が局所公式で決まる

安全な降順占有状態 `x_1>=...>=x_w`、`0<=x_i<=m` に対し、`sum_{i=1}^h x_i=r-2` を仮定する。以下を定義する。

```
n = w-h
b = x_h
R = n*b - sum_{i=h+1}^w x_i
c = #{i<=h : x_i=b}
delta = sum_{i=1}^{h-1} (m-x_i)
gamma = x_{h-1}-b   # c=1 のときにだけ使用
eta = 1 if (c=1 and (gamma=1 or delta=1)) else 0
```

このとき全有限パラメータ・全安全局面で厳密に

```
g(x) = (R + (n mod 2)*eta) mod 2.
```

したがって **容量余裕2の全安全局面はGrundy0または1**であり、余裕3以上の未解決予想の帰結としてではなく独立に全称証明されている。

## 全称証明

偶数 `n` では K0352 の全局面二値公式から、`g=(r+n*A(x)-|x|) mod2=R mod2` である。

奇数 `n` では `R` で帰納する。容量余裕2を保つ合法手は `b` 未満の下位列を一つ増やす手だけで、`R` を1減らし、`c,delta,gamma` は不変。容量余裕1へ移る子の Grundy 値集合を `E_p`（`p=R mod2`）とすると、K0358 から次の表を得る。

| 上位列の形 | E_p | eta |
|---|---|---|
| c>=3 | {1-p} | 0 |
| c=2 | {2+p}、高い未満杯列が存在すれば {1-p} も | 0 |
| c=1, gamma=1, delta=1 | {p} | 1 |
| c=1, gamma=1, delta>=2 | {p,2+p} | 1 |
| c=1, gamma>=2, delta=0 | {1-p} | 0 |
| c=1, gamma>=2, delta=1 | {p,3-p} | 1 |
| c=1, gamma>=2, delta>=2 | {2+p,3-p} | 0 |

`gamma=1,delta=0` は `r<h*m` に反する。各行は、最小値 `b` の列へ増やす場合と、それより高い未満杯の列へ増やす場合の二種を、K0358の境界子の型に代入すれば得られる。**完全な場合分けの導出は証明artifact**を参照。

`R=0` なら余裕2維持手はなく、各行の `mex(E_0)=eta` が基底となる。`R>0` なら余裕2維持手が必ずあり、帰納仮定によりその子の値はすべて `(R-1+eta) mod2`。表の `E_p` と合わせたmexは各行で `(R+eta) mod2` に一致する。よって帰納が閉じ、全称公式が証明される。□

## 独立検証・制限

K0358の式を使用しない合法手再帰mexで、`3<=w<=9,2<=h<w,2<=m<=8,2<=r<hm` の**449,322局面**を全件照合し、不一致0。別プログラムで奇数 `n` の余裕1子値集合を**52,787局面**で直接照合し、不一致0。これらは証明とは別の有限回帰監査である。

この命題は **余裕2のみ** の全称強解決である。余裕3以上の `g<=3`、あらゆる偶数余裕の二値性、標準正方形盤のGrundy一般則には直接拡張していない。
