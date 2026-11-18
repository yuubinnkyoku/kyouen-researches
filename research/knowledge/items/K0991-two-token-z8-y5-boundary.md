---
id: K0991
title: 2トークン残余ゲーム z=8・y=5境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z8 y5 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームのA/B/C再帰、Theorem T、高R tailを使用する
- type: depends_on
  target: K0987
  note: B子の評価にz=8,y=4境界切片を使用する
- type: depends_on
  target: K0981
  note: C子の評価にz=7,y=5境界切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z8-y5-boundary-20261119/report.md
  role: proof
  note: x外帰納と全xを覆うA/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z8-y5-boundary-20261119/verify_z8_y5.py
  role: verifier
  note: 順序付き・正準化直接mex再帰、K0987/K0981アンカー、署名帯・mex・tailを独立監査する検証器
- path: research/experiments/vertical-fiber-two-token-z8-y5-boundary-20261119/output/audit.json
  role: data
  note: 8,180,128検査・不一致0・二回実行byte-identical
- path: research/log/2026-11-19-vertical-fiber-two-token-z8-y5-boundary.md
  role: log
  note: 最新mainとの照合、z=8,y=5の閉形式・外帰納証明・独立監査・限界
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=8、y=5、全x>=5・全R>=0。Grundy値0/1/2を完全分類する。z=8のy=1..5境界が揃い、y>=6側の接続が開いた。
evidence: >-
  xに関する外帰納。x=5では二つのトークン減少手が同一の(x,4)子へ合流する。x>=6ではA子を帰納仮説、B子をK0987、C子をK0981で評価する。1<=R<=x+13の全域を過渡切片x=5..15と定常切片x>=16偶/x>=17奇の署名帯表で被覆し、K0832 Theorem Tのmex制約で閉じる。R>=x+14はK0832の一般tail H=(x+5) mod 2で閉じる。独立監査は8,180,128検査・不一致0・二回実行byte-identical。有限監査は証明の代わりではなく、全称性はx外帰納と署名表による。
---

## 命題・範囲

\(T_8^{(5)}(x)\) をGrundy値2の残余容量、\(P_8^{(5)}(x)\) をGrundy値1の残余容量とする。全 \(x\ge5,R\ge0\) について
\[
H(R;(x,5);8)=
\begin{cases}
2,&R\in T_8^{(5)}(x),\\
1,&R\in P_8^{(5)}(x),\\
0,&\text{otherwise}.
\end{cases}
\]
各位置集合の閉形式、A/B/C署名帯、mex表、tailの証明は対応するproof artifactに記載する。

## 現在の根拠と限界

全称性はx外帰納による。A子は同じy=5族のx-1、B子はK0987のz=8,y=4、C子はK0981のz=7,y=5に帰着する。有限監査は二つの直接再帰と署名表の独立照合であり、全称証明そのものとは区別する。

本項は抽象残余ゲームの固定切片である。z=8,y>=6、z=9,y>=5、z>=10の全Grundy分類、全高さ統一式、標準二次元盤の固定幅安定化長は未解決。z=8族のy=1..5で定常値2位置が{1,3,5,7}∪{2y+9}を5点連続で満たす観察は一般化予想の候補であり証明ではない。
