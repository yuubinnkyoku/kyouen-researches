---
id: K0831
title: "円の行窓二重行に対する分母補題: q | 4g（gは二重行位置差の最大公約数）・g ≤ floor((w−1)/(d−1))"
kind: proposition
status: proved
topics: [geometry, rectangles]
aliases: []
scope: "真円がw個の連続整数行にd≥2個の二重行を持つとき、二重行位置差の最大公約数gに対して、中心の2β=p/q（既約）はq|4gを満たす。さらにg≤floor((w−1)/(d−1))。旧系q|4ceil((w−1)/(d−1))は一般には偽で、厳密な円反例がある。"
evidence: "全称数学的証明: 任意の二重行対でq|4δを導き、全行位置差のgcdへBézoutで集約してq|4g。全二重行が同じ剰余類mod gにあることからg≤floor((w−1)/(d−1))。旧ceil割り切り系は中心(-2,-14/3)、円9(x+2)^2+(3y+14)^2=325、w=10,d=3,g=3,q=3で反証。K0830の7行d=5/d=4帰結は不変。"
relations:
- type: proves
  target: K0830
  note: "K0830の7行候補制限は訂正後も成立。d=5ならg=1でq|4、d=4ならg∈{1,2}でq|8。一般w,dの旧ceil割り切り主張は本項目で撤回。"
- type: depends_on
  target: K0763
  note: 接点・判別式の行ごとの構造解析の枠組み
artifacts:
- path: research/experiments/seven-row-ten-point-circle-classification-20261114/README.md
  role: proof
  note: "K0830の7行版証明の歴史的出典。旧一般w,dのceil割り切り注記は本項目の訂正報告を参照。"
- path: research/experiments/circle-row-window-gcd-correction-20261115/README.md
  role: proof
  note: "最大公約数による正しい一般w,d補題、旧系を否定する厳密円反例、K0830への影響を記録。"
- path: research/experiments/circle-row-window-gcd-correction-20261115/scripts/verify_counterexample.py
  role: verifier
  note: "円上の全整数点・q・g・旧系の失敗と7行帰結を標準ライブラリの整数演算で再検査。"
- path: research/experiments/circle-row-window-gcd-correction-20261115/output/audit.json
  role: data
  note: "反例と7行部分集合監査の機械出力。"
- path: research/log/2026-11-15-circle-row-window-denominator-correction.md
  role: log
  note: "旧系の論理的誤り、訂正方針、K0830への影響。"
---

## 補題（証明済み・全称）

真円が水平整数直線 y=c 上に2つの格子点を持つとき、その2点は中心 (α,β) に関して対称である。左右の点の差を u>0 とすると u は整数である。

二重行 y_i,y_j の左右差を u_i,u_j とすれば、
\[
u_i^2-u_j^2=4(y_j-y_i)(y_i+y_j-2\beta).
\]
まずこの式から 2β は有理数である。2β=p/q を既約表示すると、
\[
q(u_i^2-u_j^2)=4(y_j-y_i)\bigl(q(y_i+y_j)-p\bigr).
\]
gcd(q,q(y_i+y_j)-p)=1 より、全ての二重行対について
\[
q\mid4(y_j-y_i).
\]

二重行位置を Y={y_1,...,y_d} とし、
\[
g=\gcd(y_2-y_1,\ldots,y_d-y_1)
\]
と置く。上の割り切りは q|4(y_i-y_1) を全ての i について与えるので、Bézout の等式から
\[
\boxed{q\mid4g}.
\]

また全ての y_i は同じ剰余類 modulo g にある。長さ w の連続整数区間にあるその剰余類の整数は高々 floor((w-1)/g)+1 個だから、
\[
d\le\left\lfloor\frac{w-1}{g}\right\rfloor+1
\quad\Longrightarrow\quad
\boxed{g\le\left\lfloor\frac{w-1}{d-1}\right\rfloor}.
\]
従って q≤4 floor((w-1)/(d-1)) であり、より正確には q は
\[
\bigcup_{1\le h\le\lfloor(w-1)/(d-1)\rfloor}\operatorname{Div}(4h)
\]
のいずれかに属する。これは必要条件である。

## 旧ceil割り切り系の反例

円
\[
9(x+2)^2+(3y+14)^2=325
\]
の中心は (-2,-14/3) なので 2β=-28/3、q=3 である。円上の整数点はちょうど
\[
(-7,-8),(3,-8),(-8,-5),(4,-5),(-4,1),(0,1)
\]
の6点であり、二重行は Y={-8,-5,1}。

行窓 -8,...,1 は w=10、d=3 で、
\[
g=\gcd(3,9)=3,\quad
\left\lfloor\frac{9}{2}\right\rfloor=4,\quad
\left\lceil\frac{9}{2}\right\rceil=5.
\]
よって正しい q|4g は 3|12 として成立するが、旧系は 3∤20 となり破れる。

## K0830の7行帰結（変更なし）

- w=7,d=5: g≤floor(6/4)=1 より g=1、従って q|4。
- w=7,d=4: g≤floor(6/3)=2、従って q|4g。g=1,2 のいずれでも q|8。

従ってK0830の7行専用の候補制限 q∈{1,2,4}、q∈{1,2,4,8} と、その後の円分類は影響を受けない。

## 限界

- q|4g と g の上界は全称証明である。
- 分母条件は必要条件であり、指定された q,g から円が存在するとは限らない。
- K0830の有限分類範囲（弦・半径上界）を拡張する結果ではない。
