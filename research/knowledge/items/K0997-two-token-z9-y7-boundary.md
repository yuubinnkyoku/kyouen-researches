---
id: K0997
title: 2トークン残余ゲーム z=9・y=7境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z9 y7 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームのA/B/C再帰、Theorem T、高R tailを使用する
- type: depends_on
  target: K0994
  note: B子の評価にz=9,y=6境界切片を使用する
- type: depends_on
  target: K0995
  note: C子の評価にz=8,y=7境界切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z9-y7-boundary-20261119/report.md
  role: proof
  note: x外帰納と全xを覆うA/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z9-y7-boundary-20261119/verify_z9_y7.py
  role: verifier
  note: 順序付き・正準化直接mex再帰、K0994/K0995アンカー、署名帯・mex・tailを独立監査する検証器
- path: research/experiments/vertical-fiber-two-token-z9-y7-boundary-20261119/output/audit.json
  role: data
  note: 8,199,504検査・不一致0・二方式・二回実行byte-identical
- path: research/log/2026-11-19-vertical-fiber-two-token-z9-y7-boundary.md
  role: log
  note: 最新mainとの照合、z=9,y=7の閉形式・外帰納証明・独立監査・限界
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=9、y=7、全x>=7・全R>=0。Grundy値0/1/2を完全分類する。z=9のy=1..7境界が揃い、y>=8側の接続が開いた。
evidence: >-
  xに関する外帰納。x=7では二つのトークン減少手が同一の(x,6)子へ合流する。x>=8ではA子を帰納仮説、B子をK0994、C子をK0995で評価する。1<=R<=x+16の全域をx=7..18の過渡切片とx>=19奇/x>=20偶の定常署名帯表で被覆し、K0832 Theorem Tのmex制約で閉じる。R>=x+17はK0832の一般tail H=(x+7) mod 2で閉じる。独立監査は8,199,504検査・不一致0・二方式・二回実行byte-identical。有限監査は証明の代わりではなく、全称性はx外帰納と署名表による。
---

## 命題・範囲

\(T_9^{(7)}(x)\) をGrundy値2の残余容量、\(P_9^{(7)}(x)\) をGrundy値1の残余容量とする。全 \(x\ge7,R\ge0\) について

\[
H(R;(x,7);9)=
\begin{cases}
2,&R\in T_9^{(7)}(x),\\
1,&R\in P_9^{(7)}(x),\\
0,&\text{otherwise}.
\end{cases}
\]

値2位置は \(\{1,3,5,7,9\}\) に、x=8の19、x=12の21、x=16の23、x=17のO[23,33]、x>=18の23を加えたもの。値1位置は証明報告の表の通りである。高R tailは \(R\ge x+17\) で \(H=(x+7)\bmod2\)。

## 現在の根拠と限界

全称性はx外帰納による。x=7ではA/B子が合流し、BはK0994、CはK0995。x>=8ではAを帰納仮説、BをK0994、CをK0995で評価し、全域のA/B/C署名帯表とmexで閉じる。有限監査は二方式の直接再帰とアンカー・署名表の独立照合であり、全称証明そのものとは区別する。

本項は抽象残余ゲームの固定切片である。z=8のy>=9、z=9のy>=8、z>=10の全Grundy分類、全高さを統合する2トークン値2位置の一般式、標準二次元盤の固定幅・q点版の真の安定化長は未解決。z=9族の定常第6点z+2y（y=1..7で11,13,15,17,19,21,23の7点連続）、前倒し第6点行とI帯の行のy偶奇反転（y=6奇数行からy=7偶数行へ）は観察であり証明ではない。
