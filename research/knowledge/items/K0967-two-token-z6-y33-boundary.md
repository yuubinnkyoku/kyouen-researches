---
id: K0967
title: 2トークン残余ゲーム z=6・y=33切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z6 y33 full Grundy slice]
relations:
- type: depends_on
  target: K0832
  note: A/B/C残余再帰、Theorem T、一般tail定理を使用する
- type: depends_on
  target: K0873
  note: C子の評価にz=5の全Grundy公式を使う
- type: depends_on
  target: K0955
  note: B子とx=33境界のA子をz=6,y=32全Grundy公式で評価する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z6-y33-boundary-20261118/report.md
  role: proof
  note: z=6,y=33切片の全x,R分類、選択肢署名表、xに関する帰納証明
- path: research/experiments/vertical-fiber-two-token-z6-y33-boundary-20261118/verify_z6_y33.py
  role: verifier
  note: 順序付き・降順正準化の二方式直接再帰、y=32/z=5アンカー、全署名・mex・tailの独立監査。SHA-256 433c49a6…
- path: research/experiments/vertical-fiber-two-token-z6-y33-boundary-20261118/output/audit.json
  role: data
  note: 2,077,224署名・mex、4,584直接再帰呼び出し、5,160帰納再帰、125,952 tail検査、不一致0、二回実行byte-identical。有限監査であり全称証明とは区別する
- path: research/log/2026-11-18-vertical-fiber-two-token-z6-y33-boundary.md
  role: log
  note: 最新main・未解決事項との照合、z=6,y=33切片の証明・監査・限界
date: 2026-11-18
scope: >-
  κ=1残余ゲームH(R;(x,33);6)の2トークン族、固定高さz=6、y=33、全x≥33・全R≥0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する帰納。x=33ではA子の(32,33)が正準化後に(33,32)となりB子と一致する。x≥34ではA子をx-1の帰納仮説、B子をK0955、C子をK0873で評価する。1≤R<x+40の過渡署名表（x=33..41）と一般署名表（x≥42）で全選択肢を覆い、Theorem Tの偶奇制約とmexからT33/P33を得る。R≥x+40はK0832の一般tail定理H=(x+33) mod 2で閉じる。独立有限監査は順序付き・正準化直接再帰4,584呼び出し、A/B/C署名・mex各2,077,224件、帰納再帰5,160件、tail125,952件で不一致0、二回実行byte-identical。有限監査は証明の代わりではなく、全称性はx帰納・署名表・既証明アンカーによる。
---

## 命題

## 閉形式

\(O[a,b]\) と \(E[a,b]\) は、それぞれ区間内の奇数・偶数を表す。

\[
T_{33}(x)=\{1,3,5\}\cup
\begin{cases}
\{69\},&x=33,\\
\{71\},&x=37,\\
\{73,75,77,79\},&x=40,\\
\{73\},&x\ge41,\\
\varnothing,&\text{otherwise}.
\end{cases}
\]

\[
P_{33}(x)=
\begin{cases}
O[7,67],&x=33,\\
O[7,73]\cup E[70,72]\cup[74,\infty),&x=34,\\
O[7,69],&x=35,\\
O[7,75]\cup E[72,74]\cup[76,\infty),&x=36,\\
O[7,69],&x=37,\\
O[7,77]\cup E[72,76]\cup[78,\infty),&x=38,\\
O[7,71],&x=39,\\
O[7,71]\cup E[74,x+38]\cup[x+40,\infty),&x\ge40\text{ even},\\
O[7,71]\cup E[74,x+39],&x\ge41\text{ odd}.
\end{cases}
\]

\[
R\ge x+40\implies H(R;(x,33);6)=(x+33)\bmod2.
\]

さらに、y=26..33の8切片で個別に証明した値2位置の追加部分は共通して

\[
T_y(x)\setminus\{1,3,5\}=
\begin{cases}
\{2y+3\},&x=y,\\
\{2y+5\},&x=y+4,\\
\{2y+7,2y+9,2y+11,2y+13\},&x=y+7,\\
\{2y+7\},&x\ge y+8,\\
\varnothing,&\text{otherwise}.
\end{cases}
\]

8切片での一致は確定しているが、全 \(y\ge26\) への一般化は未証明。

全ての \(x\ge33,R\ge0\) について、Grundy値は報告書の \(T_{33}(x)\) と \(P_{33}(x)\) により0/1/2へ完全分類される。tailは

\[
R\ge x+40\implies H(R;(x,33);6)=(x+33)\bmod2.
\]

値2の追加位置は、既証明のy=26..32と合わせて8切片で同一の正規化形に一致する。ただし全yへの一般化は未証明である。

## 現在の根拠と限界

A/B/C再帰とx帰納。基底x=33ではAの(32,33)が正準化後にBの(33,32)と一致する。帰納段のBはK0955、CはK0873。過渡域x=33..41と一般域x≥42の全署名表、K0832のTheorem T、一般tail定理で全x・全Rを覆う。有限監査は順序付き・正準化直接再帰4,584呼び出し、署名・mex各2,077,224件、帰納再帰5,160件、tail125,952件で不一致0、二回実行byte-identical。有限監査は全称性の根拠ではなく、全称性はx帰納と明示署名表による。

\(z=6,y\ge34\)、\(z\ge7\)、全高さを統合する2トークン値2位置の一般式、標準二次元共円ゲームの固定幅・q点版の真の安定化長は未解決。
