---
id: K0592
title: 花弁が容量より短い任意本数のひまわり型容量ゲームでも極大配置多項式と終局長の欠番数が閉形式で求まる
kind: proposition
status: proved
topics: [maximal-safe, maximum-safe, residual-games, strategy-length, variants]
aliases: []
relations: []
artifacts:
- path: research/experiments/sunflower-short-petals-20261101/proof.md
  role: proof
  note: 任意の花弁長・異容量について極大配置の必要十分条件と終局長の単調差分を全称証明
- path: research/experiments/sunflower-short-petals-20261101/verify.py
  role: verifier
  note: 20117抽象盤・3230530部分集合を点別完全列挙して公式と独立照合
scope: 任意のr>=2、共通芯H・互いに素な花弁P_i・自由点Z、各容量p_i>=1、花弁長x_i>=0でx_i>=p_iを仮定しない有限抽象容量ゲームの極大安全集合。
evidence: 極大性の必要十分条件、石数の非増加差分、欠番数の数式による全称証明。独立点別列挙20117盤・3230530部分集合で不一致0。
---

# 短い花弁を許すひまわり型容量ゲームの終局長公式

互いに素な集合 \(H,P_1,\ldots,P_r,Z\) の点を順次選び、各 \(|S\cap(H\cup P_i)|\le p_i\) を守る。\(c=|H|\)、\(x_i=|P_i|\)、\(z=|Z|\) とし、\(p_i\ge1\)、\(x_i\ge0\)。従来のK0589の \(x_i\ge p_i\) という仮定は不要である。

\[
J=\min(c,p_1,\ldots,p_r),\qquad
j_0=\min(J,\max(0,\min_i(p_i-x_i))),
\]
\[
a_i(j)=\min(x_i,p_i-j),\qquad F(j)=z+j+\sum_i a_i(j).
\]

**極大安全集合の石数別母関数**は厳密に

\[
\boxed{P(u)=\sum_{j=j_0}^{J}
\binom cj\prod_i\binom{x_i}{a_i(j)}\,u^{F(j)}}.
\]

また \(k(j)=\#\{i:p_i-x_i\le j\}\) とすると、\(j_0\le j<J\) で \(k(j)\ge1\) かつ \(F(j)-F(j+1)=k(j)-1\)。従って

\[
\boxed{K=F(j_0),\quad s=F(J),\quad
\text{欠番数}=\sum_{j=j_0}^{J-1}\max(0,k(j)-2)}.
\]

下降幅は非減少で、隣接する実現可能な終局長の間に最大 \(r-2\) 個の欠番が生じ得る。\(r=2\) では欠番なし（K0588と整合）。\(x_i\ge p_i\) に戻せば \(k(j)=r\) となり、K0589の等差数列公式を再現する。

**新しい境界例**：\(r=3,c=2,z=0,x=(1,2,2),p=(2,2,2)\) では

\[
\boxed{P(u)=u^2+8u^4+u^5}.
\]

終局長は2・4・5石であり、3石は欠番。短い花弁を許すと、従来の公差 \(r-1\) の等差数列性は失われる。

証明は芯・花弁・自由点の追加不能性を直接分類した全称証明。独立検査では系統的19,915盤・3,059,442部分集合と固定乱数202盤・171,088部分集合を全列挙し、不一致0。**有限検証からの外挿ではない。**

**限界**：抽象容量ゲームの定理であり、任意の円・直線配置がこの形を実現するとは主張しない。11×11の残局に適用するには残余禁止条件との厳密な同値性が必要。通常版・misère版のGrundy値や11×11の勝敗は本定理だけでは決まらない。
