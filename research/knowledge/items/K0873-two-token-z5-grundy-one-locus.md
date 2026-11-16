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
- path: research/experiments/vertical-fiber-two-token-z5-y1-boundary-20261116/report.md
  role: proof
  note: z=5・y=1境界切片の全Grundy値0/1/2をR強帰納で全称証明
- path: research/experiments/vertical-fiber-two-token-z5-y1-boundary-20261116/verify_z5_y1.py
  role: verifier
  note: 正準cap再帰・順序付き再帰・A/B/C帰納選択肢署名の独立検証器
- path: research/experiments/vertical-fiber-two-token-z5-y1-boundary-20261116/output/audit.json
  role: data
  note: 21,900状態・509,490帰納署名・200散点の監査結果
- path: research/log/2026-11-16-vertical-fiber-two-token-z5-y1-boundary.md
  role: log
  note: z=5値1/2位置予想のy=1境界を証明した判断・証明・限界
scope: "κ=1残余ゲームH(R;(x,y);z)の2トークン族x≥y≥1・固定高さz=5。全x,yの値1位置式は予想。境界y=1では全x,RのGrundy値0/1/2を全称証明済み。全体予想の有限監査範囲はx≤100・0≤R≤x+y+8と固定seed散点x≤300。"
evidence: "全称証明部分はy=1を固定しR強帰納。A子は帰納仮説、B子はK0832の単一トークンz=6閉形式、C子は既証明z=4二トークン閉形式で評価し、全x・全Rを小R選択肢表と大R選択肢表で覆う。独立監査は正準cap再帰と順序付き非cap再帰をx≤200・21,900状態で照合し不一致0、候補式・帰納選択肢署名509,490点で不一致0、x≤2000の固定seed散点200件で不一致0。全yへの予想は依然として全称証明ではない。"
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


## 既証明のtail部分

K0832のtail定理により、\(R\ge S+6\) では \(H(R;(x,y);5)=S\bmod2\) が全称的に成立する。したがってこの領域に限れば、値1となる条件は \(S\) が奇数、すなわち \(d=x-y\) が奇数であることと同値である。K0873の予想のうち、このtail部分は新しい予想ではなく既証明定理の帰結であり、未証明なのは主に \(R<S+6\) の遷移帯である。


## 全称証明済み境界切片 y=1

K0832の単一トークンz=6公式と2トークンz=4全Grundy定理を用い、A/B/C手の子を評価するR強帰納によって、\(H(R;(x,1);5)\) の全Grundy値を任意の\(x\ge1,R\ge0\)で決定した。値2位置は\(x=1:\{1\}\)、\(x=2,3:\{1,3\}\)、\(x=4,5:\{1,3,5\}\)、\(x=6:\{1,3,5,7\}\)、\(x=7:\{1,3,5,7,9,11,13\}\)、\(x\ge8:\{1,3,5,7\}\)。値1位置と完全証明は実験報告を参照。有限監査は21,900状態・509,490帰納署名・200散点で不一致0。これにより本項全体のstatusはconjecturedのまま、y=1部分だけをprovedとして区別する。
