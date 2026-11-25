---
id: K0880
title: 2トークン残余ゲーム z=6・y=4切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z6 y4 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義、A/B/C再帰、Theorem T、完了予算とtail定理を使用する
- type: depends_on
  target: K0873
  note: C子の評価にz=5の全Grundy公式を使用する
- type: depends_on
  target: K0879
  note: B子の評価にz=6,y=3全Grundy切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z6-y4-boundary-20261117/report.md
  role: proof
  note: 固定z=6,y=4・全x≥4,R≥0の値0/1/2をA/B/C署名表とR強帰納で分類する全称証明
- path: research/experiments/vertical-fiber-two-token-z6-y4-boundary-20261117/verify_z6_y4.py
  role: verifier
  note: 順序付き/正準化の二再帰、z=5・z=6,y=3アンカー、A/B/C署名とmexを照合する独立有限監査器
- path: research/experiments/vertical-fiber-two-token-z6-y4-boundary-20261117/output/audit.json
  role: data
  note: 4,088,723検査・不一致0・二回実行byte-identical
- path: research/log/2026-11-17-vertical-fiber-two-token-z6-y4-boundary.md
  role: log
  note: 最新main・未解決事項との照合、z=6,y=4切片の発見・証明・監査・限界
scope: >-
  κ=1残余ゲームH(R;X;z)の2トークン族X=(x,4)、全x≥4・全R≥0、固定高さz=6。Grundy値0/1/2を完全分類する。
evidence: >-
  Rに関する強帰納。x≥5ではA子が帰納仮説、B子がK0879のz=6,y=3公式、C子がK0873のz=5全公式で評価できる。x=4ではA/B手が同一子へ合流する。K0832のTheorem Tで奇数親の選択肢は{0,1}、偶数親の親値は高々1。x=4..12の過渡域とx≥13の定常域に分けたA/B/C選択肢署名表からmexを決定し、R≥x+11はtail H=(x+4) mod 2で閉じる。値2位置の追加点はK0832の3族予想のz=6,y=4特殊化（EXTのd=0,4、家族Aのd=7ラン・d≥8定常）とも完全一致する。これは当該切片の検証であり、一般予想全体の証明ではない。独立有限監査は4,088,723検査・不一致0。有限監査は証明の代わりではなく、全称性は署名表とR強帰納による。
---

## 定理

\(E[a,b]\) は区間内の偶数、\(I[a,\infty)\) はa以上の全整数とする。値2位置は
\[
T_6^{(4)}(x)=
\begin{cases}
\{1,3,5,11\},&x=4,\\
\{1,3,5\},&x\in\{5,6,7,9,10\},\\
\{1,3,5,13\},&x=8,\\
\{1,3,5,15,17,19,21\},&x=11,\\
\{1,3,5,15\},&x\ge12.
\end{cases}
\]
値1位置は
\[
P_6^{(4)}(x)=
\begin{cases}
\{7,9\},&x=4,\\
\{7,9\}\cup I[11,\infty),&x=5,\\
\{7,9,11\},&x=6,\\
\{7,9,11\}\cup I[13,\infty),&x=7,9,\\
\{7,9,11\},&x=8,\\
\{7,9,11,13\},&x=10,\\
\{7,9,11,13\}\cup E[16,20]\cup I[22,\infty),&x=11,\\
\{7,9,11,13\}\cup E[16,x+10],&x\ge12\text{ 偶数},\\
\{7,9,11,13\}\cup E[16,x+9]\cup I[x+11,\infty),&x\ge13\text{ 奇数}.
\end{cases}
\]
従って
\[
H(R;(x,4);6)=
\begin{cases}
2,&R\in T_6^{(4)}(x),\\
1,&R\in P_6^{(4)}(x),\\
0,&\text{それ以外}
\end{cases}
\]
が全 \(x\ge4,R\ge0\) で成立する。

完全なA/B/C署名表と強帰納証明は[証明報告](../../experiments/vertical-fiber-two-token-z6-y4-boundary-20261117/report.md)を参照する。独立有限監査は4,088,723検査・不一致0、二回実行byte-identical。有限監査は全称性の根拠ではなく、全称性は署名表・Theorem T・tail定理とR強帰納による。

## 限界

本項はz=6,y=4の切片のみを証明する。z=6,y≥34、z≥7の全Grundy分類、全高さを統合する3族値2位置一般式は未解決。標準二次元共円ゲームの固定幅安定化長へ直接転送しない。
