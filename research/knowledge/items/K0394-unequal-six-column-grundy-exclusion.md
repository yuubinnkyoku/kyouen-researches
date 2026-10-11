---
id: K0394
title: 最大容量7以下の異容量6列ゲームではGrundy値6が生じない
kind: proposition
status: computed
topics:
- variants
- grundy
aliases: []
relations: []
artifacts:
- path: research/experiments/capacity-unequal-six-columns-20261010/scan_six.cpp
  role: solver
  note: 対称性同値類の有限完全mex列挙
- path: research/experiments/capacity-unequal-six-columns-20261010/verify_labeled.py
  role: verifier
  note: 最大列容量4以下のラベル付き全局面独立再計算
- path: research/experiments/capacity-unequal-six-columns-20261010/scan_six_7.log
  role: log
  note: 最大容量7の全走査結果
scope: 6列、0<=c_i<=7、1<=h<=6、r>=0、全安全局面
---

# 異容量6列の有限上界

`sum(largest h of x)<=r` を安全条件とし、各列 `x_i<=c_i` から1石ずつ増やす通常プレイについて、`w=6`、`0<=c_i<=7`、`1<=h<=6`、`r>=0` の **全安全局面で `g<=5`** が有限完全列挙によって確定した。無界容量の一般定理ではない。

`max_i c_i<=4` では `g<=3`、一方 `max_i c_i=5` で `g=5` が実現するため、6列で `g>=4` と `g>=5` を実現する最大容量の最小値はどちらも5である。容量5の証人は既知の5列証人を飽和列追加で埋め込んだもので、独立の新構成とは主張しない。

全走査は56,232個の `(c,h,r)`、127,705,374個の安全局面の対称性同値類を対象とした。最大容量4以下の2,808パラメータ・3,776,292個のラベル付き安全局面は別方式で全件照合済み。容量5〜7の独立照合は10パラメータの部分監査である。省略条件と同値類の完全性は実験READMEを参照。

`g=6` の無界容量での存在は未解決であり、有限結果を無界定理へ昇格させない。
