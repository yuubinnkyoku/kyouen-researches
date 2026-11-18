---
id: K0993
title: 2トークン残余ゲーム z=8・y=6境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z8 y6 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームのA/B/C再帰、Theorem T、高R tailを使用する
- type: depends_on
  target: K0991
  note: B子の評価にz=8,y=5境界切片を使用する
- type: depends_on
  target: K0982
  note: C子の評価にz=7,y=6境界切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z8-y6-boundary-20261119/report.md
  role: proof
  note: x外帰納と全xを覆うA/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z8-y6-boundary-20261119/verify_z8_y6.py
  role: verifier
  note: 順序付き・正準化直接mex再帰、K0991/K0982アンカー、署名帯・mex・tailを独立監査する検証器
- path: research/experiments/vertical-fiber-two-token-z8-y6-boundary-20261119/output/audit.json
  role: data
  note: 8,185,835検査・不一致0・二回実行byte-identical
- path: research/log/2026-11-19-vertical-fiber-two-token-z8-y6-boundary.md
  role: log
  note: 最新mainとの照合、z=8,y=6の閉形式・外帰納証明・独立監査・限界
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=8、y=6、全x>=6・全R>=0。Grundy値0/1/2を完全分類する。z=8のy=1..6境界が揃い、y>=7側の接続が開いた。
evidence: >-
  xに関する外帰納。x=6では二つのトークン減少手が同一の(x,5)子へ合流する。x>=7ではA子を帰納仮説、B子をK0991、C子をK0982で評価する。1<=R<=x+14の全域を過渡切片x=6..16と定常切片x>=17奇/x>=18偶の署名帯表で被覆し、K0832 Theorem Tのmex制約で閉じる。R>=x+15はK0832の一般tail H=(x+6) mod 2で閉じる。独立監査は8,185,835検査・不一致0・二回実行byte-identical。有限監査は証明の代わりではなく、全称性はx外帰納と署名表による。
---

## 命題・範囲

\(T_8^{(6)}(x)\) をGrundy値2の残余容量、\(P_8^{(6)}(x)\) をGrundy値1の残余容量とする。全 \(x\ge6,R\ge0\) について
\[
H(R;(x,6);8)=
\begin{cases}
2,&R\in T_8^{(6)}(x),\\
1,&R\in P_8^{(6)}(x),\\
0,&\text{otherwise}.
\end{cases}
\]
各位置集合の閉形式、A/B/C署名帯、mex表、tailの証明は対応するproof artifactに記載する。

## 現在の根拠と限界

全称性はx外帰納による。A子は同じy=6族のx-1、B子はK0991のz=8,y=5、C子はK0982のz=7,y=6に帰着する。有限監査は二つの直接再帰と署名表の独立照合であり、全称証明そのものとは区別する。

本項は抽象残余ゲームの固定切片である。z=8,y>=7、z=9,y>=7、z>=10の全Grundy分類、全高さ統一式、標準二次元盤の固定幅安定化長は未解決。z=8族のy=1..6で定常値2位置が{1,3,5,7}∪{2y+9}（第5点はy=1..6で11,13,15,17,19,21の6点連続）を満たす観察、I帯の付く行がyの偶奇で交互する観察（y=4奇・y=5偶・y=6奇で2延長確認）、第5点の前倒し配置（y=6でx=8,12）は一般化予想の候補であり証明ではない。
