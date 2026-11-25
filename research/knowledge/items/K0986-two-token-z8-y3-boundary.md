---
id: K0986
title: 2トークン残余ゲーム z=8・y=3境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z8 y3 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームのA/B/C再帰、Theorem T、高R tailを使用する
- type: depends_on
  target: K0984
  note: B子の評価にz=8,y=2境界切片を使用する
- type: depends_on
  target: K0979
  note: C子の評価にz=7,y=3境界切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z8-y3-boundary-20261119/report.md
  role: proof
  note: x外帰納と全xを覆うA/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z8-y3-boundary-20261119/verify_z8_y3.py
  role: verifier
  note: 順序付き・正準化直接mex再帰、K0984/K0979アンカー、署名帯・mex・tailを独立監査する検証器
- path: research/experiments/vertical-fiber-two-token-z8-y3-boundary-20261119/output/audit.json
  role: data
  note: 8,164,676検査・不一致0・二回実行byte-identical
- path: research/log/2026-11-19-vertical-fiber-two-token-z8-y3-boundary.md
  role: log
  note: 最新mainとの照合、z=8,y=3の閉形式・外帰納証明・独立監査・限界
date: 2026-11-19
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=8、y=3、全x>=3・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。x=3では二つのトークン減少手が同一の(x,2)子へ合流する。x>=4ではA子を帰納仮説、B子をK0984、C子をK0979で評価する。1<=R<=x+11の全域を過渡切片x=3..13と定常切片x>=14偶/x>=15奇の署名帯表で被覆し、K0832 Theorem Tのmex制約で閉じる。R>=x+12はK0832の一般tail H=(x+3) mod 2で閉じる。独立監査は8,164,676検査・不一致0・二回実行byte-identical。有限監査は証明の代わりではなく、全称性はx外帰納と署名表による。
---

## 命題・範囲

\(T_8^{(3)}(x)\) をGrundy値2の残余容量、\(P_8^{(3)}(x)\) をGrundy値1の残余容量とする。全 \(x\ge3,R\ge0\) について
\[
H(R;(x,3);8)=
\begin{cases}
2,&R\in T_8^{(3)}(x),\\
1,&R\in P_8^{(3)}(x),\\
0,&\text{otherwise}.
\end{cases}
\]
各位置集合の閉形式、A/B/C署名帯、mex表、tailの証明は対応するproof artifactに記載する。

## 現在の根拠と限界

全称性はx外帰納による。A子は同じy=3族のx-1、B子はK0984のz=8,y=2、C子はK0979のz=7,y=3に帰着する。有限監査は二つの直接再帰と署名表の独立照合であり、全称証明そのものとは区別する。

本項は抽象残余ゲームの固定切片である。z=8,y=4はK0987で全称証明済み、z=8,y>=5、z=9,y>=2、z>=10の全Grundy分類、全高さ統一式、標準二次元盤の固定幅安定化長は未解決。
