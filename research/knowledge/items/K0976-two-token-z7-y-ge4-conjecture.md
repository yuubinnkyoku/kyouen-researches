---
id: K0976
title: 2トークン残余ゲーム z=7・y≥4 の全Grundy閉形式予想
kind: proposition
status: conjectured
topics: [grundy, residual-games]
aliases: [two-token z7 y>=4 all-Grundy formula conjecture]
relations:
- type: depends_on
  target: K0832
  note: 残余再帰、Theorem T、一般tail定理を使う
artifacts:
- path: research/experiments/vertical-fiber-two-token-z7-y-ge4-census-20261119/report.md
  role: source
  note: z=7・y>=4の値0/1/2閉形式候補と有限監査の範囲・限界
- path: research/experiments/vertical-fiber-two-token-z7-y-ge4-census-20261119/verify_z7_y_ge4.py
  role: verifier
  note: 正準多重集合再帰と順序付き再帰の二方式で候補式を照合する有限検証器
- path: research/experiments/vertical-fiber-two-token-z7-y-ge4-census-20261119/output/audit.json
  role: data
  note: 918,918状態・tail23,562点・境界2点、不一致0、二回実行byte-identical
- path: research/log/2026-11-19-vertical-fiber-two-token-z7-y-ge4-census.md
  role: log
  note: 最新main・既存未解決事項の確認、候補式抽出、有限監査、証明未了の判断記録
date: 2026-11-19
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族、z=7、全x>=y>=4、全R>=0に対するGrundy値0/1/2の閉形式候補。statusはconjecturedであり、全称命題として採用しない。
evidence: >-
  降順正準多重集合再帰と順序を保つラベル付き再帰を別々に実行。y=4..80、d=x-y=0..50、R=0..x+y+7の各459,459状態で候補式と一致。さらに各組のtail点R=S+8,S+9,S+20を各11,781点ずつ照合し、境界H(7;(3,3);7)=0も両方式で確認。合計918,918有限状態・23,562 tail点・境界2点で不一致0、二回実行byte-identical。有限範囲外の全称性は未証明。
---

## 予想

S=x+y、d=x-yとする。O[a,b]とE[a,b]はそれぞれ区間内の奇数集合・偶数集合。

値2位置:
\[
T_y(x)=\{1,3,5,7\}\cup
\begin{cases}
\{2y+5\}&d=3,\\
\{2y+7\}&d=7,\\
\{2y+7,2y+9,2y+11,2y+13,2y+15\}&d=8,\\
\{2y+7\}&d\ge9,\\
\varnothing&\text{otherwise}.
\end{cases}
\]

値1位置:
\[
P_y(x)=
\begin{cases}
E[8,2y+2]&d=0,\\
E[8,2y+8]\cup O[2y+5,2y+7]&d=1,\\
E[8,2y+4]&d=2,\\
E[8,2y+10]\cup O[2y+7,2y+9]&d=3,\\
E[8,2y+4]&d=4,\\
E[8,2y+12]\cup O[2y+7,2y+11]&d=5,\\
E[8,2y+6]&d=6,\\
E[8,2y+14]\cup O[2y+9,2y+13]&d=7,\\
E[8,2y+6]&d=8,\\
E[8,2y+6]\cup O[2y+9,\min(2y+2d-3,S+7)]&d\ge9.
\end{cases}
\]

全てのx>=y>=4、0<=R<=S+7で
\[
H(R;(x,y);7)=
\begin{cases}
2&R\in T_y(x),\\
1&R\in P_y(x),\\
0&\text{otherwise}
\end{cases}
\]
と予想する。tail R>=S+8ではK0832によりH=S mod 2。

## 根拠と限界

二方式の有限完全再帰監査は候補式を支持するが、y>80またはd>50を含む全称証明ではない。y=3ではH(7;(3,3);7)=0となり、基本ラダーの単純延長も成立しない。全称証明に必要なy=1,2,3の基底切片とA/B/C署名表は未完成である。
