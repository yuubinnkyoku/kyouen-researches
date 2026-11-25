---
id: K0873
title: 2トークン残余ゲーム z=5 の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z5 Grundy classification]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義、A/B/C再帰、Theorem T、tail定理とz=4全称スライスを使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z5-full-grundy-20261117/report.md
  role: proof
  note: 固定z=5・全x,y,RのGrundy値0/1/2をR強帰納とA/A/C選択肢署名表で分類する全称証明
- path: research/experiments/vertical-fiber-two-token-z5-full-grundy-20261117/verify_z5_full.py
  role: verifier
  note: z=4公式・z=5帰納候補・y=1境界から全A/A/C選択肢署名を再構成する独立監査器
- path: research/experiments/vertical-fiber-two-token-z5-full-grundy-20261117/output/audit.json
  role: data
  note: 857,466選択肢署名・2,021,000境界式・44,793 tail検査、不一致0
- path: research/log/2026-11-17-vertical-fiber-two-token-z5-full-grundy.md
  role: log
  note: 最新main・未解決一覧との照合、z=5全分類のR強帰納証明と監査記録
- path: research/experiments/vertical-fiber-two-token-z5-y1-boundary-20261116/report.md
  role: proof
  note: y=1境界切片の全x,R全称証明
- path: research/experiments/vertical-fiber-two-token-z5-y1-boundary-20261116/verify_z5_y1.py
  role: verifier
  note: y=1境界証明の独立有限監査器
- path: research/experiments/vertical-fiber-two-token-z5-value2-locus-20261116/report.md
  role: source
  note: 定理化前の値2位置有限抽出記録
- path: research/experiments/vertical-fiber-two-token-z5-value1-locus-20261116/report.md
  role: source
  note: 定理化前の値1位置有限抽出記録
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族x≥y≥1、固定高さz=5、全R≥0。値0/1/2を全て閉形式で決定する。
evidence: >-
  y=1は先行の全称境界定理。y≥2はR強帰納。R>0ではA/A/Cの3子のみで、A子は帰納仮説またはy=1境界、C子は既証明z=4全Grundy公式で評価する。Theorem Tにより奇数親の子値は{0,1}、偶数親の親値は高々1。d=0..6の過渡域とd≥7の定常域に分けたsigma=V∩{0,1}表が全パラメータを覆い、mexから全式を得る。有限独立監査は857,466署名、2,021,000境界式、44,793 tail点で不一致0。
---

## 定理

\(S=x+y\)、\(d=x-y\) とする。偶数・奇数区間を
\[
E[a,b]=\{R\in\mathbb Z:a\le R\le b,\ R\equiv0\pmod2\},\quad
O[a,b]=\{R\in\mathbb Z:a\le R\le b,\ R\equiv1\pmod2\}
\]
とし、\(I[a,\infty)=\{R\in\mathbb Z:R\ge a\}\) とする。

値2位置 \(T_5\) は
\[
\boxed{
T_5=
\begin{cases}
\{1\},&d=0,\ y=1,\\
\{1,3\},&d=0,\ y=2,\\
\{1,3,5\},&d=0,\ y\ge3,\\
\{1,3\},&d=1,\ y=1,\\
\{1,3,5,2y+3\},&d=1,\ y\ge2,\\
\{1,3\},&d=2,\ y=1,\\
\{1,3,5\},&d=2,\ y\ge2,\\
\{1,3,5\},&d\in\{3,4\},\\
\{1,3,5,2y+5\},&d=5,\\
\{1,3,5,2y+5,2y+7,2y+9,2y+11\},&d=6,\\
\{1,3,5,2y+5\},&d\ge7.
\end{cases}}
\]

値1位置 \(P_5\) は
\[
\boxed{
P_5=
\begin{cases}
E[6,S+2],&d=0,\ y\ge3,\\
\varnothing,&d=0,\ y\le2,\\
I[4,\infty),&d=1,\ y=1,\\
E[6,S+3]\cup I[S+4,\infty),&d=1,\ y\ge2,\\
\varnothing,&d=2,\ y=1,\\
E[6,S],&d=2,\ y\ge2,\\
E[6,S+1]\cup I[S+2,\infty),&d=3,\\
E[6,S],&d=4,\\
E[6,S-1]\cup I[S+1,\infty),&d=5,\\
E[6,S-2],&d=6,\\
E[6,2y+4]\cup O[2y+7,S+4]\cup I[S+6,\infty),
 &d\ge7\text{ odd},\\
E[6,2y+4]\cup O[2y+7,S+5],
 &d\ge8\text{ even}.
\end{cases}}
\]

全ての \(x\ge y\ge1,R\ge0\) について
\[
H(R;(x,y);5)=
\begin{cases}
2,&R\in T_5,\\
1,&R\in P_5,\\
0,&\text{otherwise}.
\end{cases}
\]

## 証明と監査

完全なR強帰納、A/A/C選択肢署名表、有限監査の範囲と限界は[証明報告](../../experiments/vertical-fiber-two-token-z5-full-grundy-20261117/report.md)に記録した。y=1の境界証明は[先行報告](../../experiments/vertical-fiber-two-token-z5-y1-boundary-20261116/report.md)を参照。検証器は857,466署名・2,021,000境界式・44,793 tail点で不一致0。有限監査は証明の代わりではなく、全称性は強帰納による。

z=6,y≥34およびz≥7の全Grundy分類と全高さの統一式は未解決である。
