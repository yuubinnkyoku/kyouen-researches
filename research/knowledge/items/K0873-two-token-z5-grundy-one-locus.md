---
id: K0873
title: 2トークン残余ゲーム z=5 のGrundy値1位置候補
kind: proposition
status: conjectured
topics: [grundy, residual-games]
aliases: [two-token z5 Grundy-one locus]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義、偶奇上界、tail定理、2トークン再帰を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z5-value1-locus-20261116/report.md
  role: data
  note: z=5・2トークン族の値1位置の差d別区間候補と有限監査・証明境界
- path: research/experiments/vertical-fiber-two-token-z5-value1-locus-20261116/verify_z5_value1.py
  role: verifier
  note: 正準切り詰め再帰と順序付き再帰による値1・既存値2候補の独立有限監査
- path: research/experiments/vertical-fiber-two-token-z5-value1-locus-20261116/output/audit.json
  role: data
  note: 555,500全格子状態・200散点・二方式一致0の監査集計
- path: research/log/2026-11-16-vertical-fiber-two-token-z5-value1-locus.md
  role: log
  note: 既存z=5値2予想との重複を避けた値1位置の抽出・有限監査・次の証明課題
scope: "κ=1残余ゲームH(R;(x,y);z)の2トークン族x≥y≥1・固定高さz=5。本文の値1位置式は全x,yへの予想であり、有限監査範囲はx≤100・0≤R≤x+y+8と固定seed散点x≤300。"
evidence: "正準化・R+1切り詰め再帰と、順序付き・切り詰めなし再帰の2方式を独立実装し、x≤100の555,500状態で候補式・既存値2位置式・偶奇上界・tailを全照合。不一致0。x≤300の固定seed散点200件も別局所正準キャッシュと順序付き再帰で不一致0。有限監査であり全称証明ではない。"
---

## 命題（未証明の閉形式予想）

\(S=x+y\)、\(d=x-y\) とし、

\[
E[a,b]=\{R\in\mathbb Z:a\le R\le b,\ R\equiv0\pmod2\},\quad
O[a,b]=\{R\in\mathbb Z:a\le R\le b,\ R\equiv1\pmod2\}
\]

とする。\(I[a,\infty)=\{R\in\mathbb Z:R\ge a\}\)、空区間は空集合とする。

\[
P_5(x,y)=\{R\ge0:H(R;(x,y);5)=1\}
\]

の候補は

\[
\boxed{
P_5(x,y)=
\begin{cases}
E[6,S+2],&d=0,\ y\ge3,\\
\varnothing,&d=0,\ y\le2,\\
I[4,\infty),&d=1,\ y=1,\\
E[6,S+3]\cup I[S+4,\infty),&d=1,\ y\ge2,\\
E[6,S],&d=2,\ y\ge2,\\
\varnothing,&d=2,\ y=1,\\
E[6,S+1]\cup I[S+2,\infty),&d=3,\\
E[6,S],&d=4,\\
E[6,S-1]\cup I[S+1,\infty),&d=5,\\
E[6,S-2],&d=6,\\
E[6,2y+4]\cup O[2y+7,S+4]\cup I[S+6,\infty),
 &d\ge7\text{ odd},\\
E[6,2y+4]\cup O[2y+7,S+5],
 &d\ge8\text{ even}.
\end{cases}
}
\]

この式は有限格子に支持された予想であり、全称定理ではない。特に \(d\ge7\) の奇数・偶数帯の端点を与える一般的な選択肢表は未完成である。
