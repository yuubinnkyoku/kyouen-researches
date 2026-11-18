---
id: K0990
title: 2トークン残余ゲーム z=9・y=4境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z9 y4 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームのA/B/C再帰、Theorem T、高R tailを使用する
- type: depends_on
  target: K0989
  note: B子の評価にz=9,y=3境界切片を使用する
- type: depends_on
  target: K0987
  note: C子の評価にz=8,y=4境界切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z9-y4-boundary-20261119/report.md
  role: proof
  note: x外帰納と全xを覆うA/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z9-y4-boundary-20261119/verify_z9_y4.py
  role: verifier
  note: 順序付き・正準化直接mex再帰、K0989/K0987アンカー、署名帯・mex・tailを独立監査する検証器
- path: research/experiments/vertical-fiber-two-token-z9-y4-boundary-20261119/output/audit.json
  role: data
  note: 8,180,398検査・不一致0・二回実行byte-identical
- path: research/log/2026-11-19-vertical-fiber-two-token-z9-y4-boundary.md
  role: log
  note: 最新mainとの照合、z=9,y=4の閉形式・外帰納証明・独立監査・限界
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=9、y=4、全x>=4・全R>=0。Grundy値0/1/2を完全分類する。z=9のy=1..4境界が揃い、y>=5側の接続が開いた。
evidence: >-
  xに関する外帰納。x=4では二つのトークン減少手が同一の(x,3)子へ合流する。x>=5ではA子を帰納仮説、B子をK0989、C子をK0987で評価する。1<=R<=x+13の全域を過渡切片x=4..15と定常切片x>=16偶/x>=17奇の署名帯表で被覆し、K0832 Theorem Tのmex制約で閉じる。R>=x+14はK0832の一般tail H=(x+4) mod 2で閉じる。独立監査は8,180,398検査・不一致0・二回実行byte-identical。有限監査は証明の代わりではなく、全称性はx外帰納と署名表による。
---

## 命題・範囲

\(T_9^{(4)}(x)\) をGrundy値2の残余容量、\(P_9^{(4)}(x)\) をGrundy値1の残余容量とする。全 \(x\ge4,R\ge0\) について
\[
H(R;(x,4);9)=
\begin{cases}
2,&R\in T_9^{(4)}(x),\\
1,&R\in P_9^{(4)}(x),\\
0,&\text{otherwise}.
\end{cases}
\]
各位置集合の閉形式、A/B/C署名帯、mex表、tailの証明は対応するproof artifactに記載する。

## 現在の根拠と限界

全称性はx外帰納による。A子は同じy=4族のx-1、B子はK0989のz=9,y=3、C子はK0987のz=8,y=4に帰着する。有限監査は二つの直接再帰と署名表の独立照合であり、全称証明そのものとは区別する。

本項は抽象残余ゲームの固定切片である。z=9,y>=5、z=8のy>=5、z>=10の全Grundy分類、全高さ統一式、標準二次元盤の固定幅安定化長は未解決。z=9族のy=1..4で定常値2位置が{1,3,5,7,9}∪{z+2y}を4点連続で満たす観察は一般化予想の候補であり証明ではない。
