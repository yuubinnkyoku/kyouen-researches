---
id: K1264
title: 一般X低Rミントークン階段定理 H(R;X;z)=単一トークン(ΣX) for R<=z+min(X)
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [min-token staircase, generalx lowR min-window collapse, z+min(X) window]
relations:
- type: depends_on
  target: K0832
  note: 単一トークン閉形式・一般多重集合低R縮約R<=z+1（本定理の min(X)=被覆ケース）・tail/マージ領域
- type: related
  target: K1254
  note: FR-X/GX-Mの選択肢集合完全一致技術の低R方向対応。窓保証の相互整合
- type: related
  target: K1087
  note: z=17低R観察・witness (12,6)@R=24=z+min+1 アンカー照合元
- type: related
  target: K1259
  note: z=18低R観察・「R<=z+6全z一般証明」未解決課題の閉包・witnessアンカー
- type: related
  target: K1261
  note: z=19低R観察・witness (14,6)@R=26 アンカー照合元
- type: related
  target: K1262
  note: z=20低R観察・witness (16,6)@R=27 アンカー照合元
- type: related
  target: K1257
  note: raw engines/K0832単一トークン閉形式の転写ブロックを含む出版機体（プロビナンス）
artifacts:
- path: research/experiments/generalx-min-token-lowr-staircase-20261123/report.md
  role: proof
  note: 全称証明本文（補題E空残余・補題Z z-shift不変性・min>=2リフト・min=1基底の構造的強帰納）＋系・鋭さ・監査記録
- path: research/experiments/generalx-min-token-lowr-staircase-20261123/verify_min_token_staircase.py
  role: verifier
  note: 二直接再帰×出版閉形式の3方式照合・補題Z掃引・定理掃引（完全小＋固定seed深部）・境界census・出版witnessアンカー・8種fail-closed変異電池
- path: research/experiments/generalx-min-token-lowr-staircase-20261123/output/audit.json
  role: data
  note: 総照合2,468,581点・bad 0・4回実行（隔離cwd・env -i別HOME込み）でbyte-identical
- path: research/log/2026-11-23-generalx-min-token-lowr-staircase.md
  role: log
  note: 発見経緯（b==Aの発見とT1/T2のlemma Zへの簡約）・宣言前探査の開示・アンカー想定値訂正の正直記録
- path: research/log/2026-11-23-generalx-min-token-lowr-staircase-single-owner-note.md
  role: log
  note: 単一オーナー宣言（commit 35cbad4f・K1264仮採番・publish-then-execute）
scope: >-
  κ=1残余ゲーム H(R;X;z) の一般多重集合X（アリティ自由）・全z>=0・
  低残容量窓 0<=R<=z+min(X) における総和S=ΣXの単一トークン残余への縮約。
  窓を超える領域・高zマージ領域の一般構造は範囲外。
evidence: >-
  全称性は report.md の構造的強帰納（R強帰納・アリティ自由の選択肢集合完全一致。
  唯一の解析的成分は補題Zでそれ自体もn帰納の純構造証明）による。
  機械監査は独立照合: 二直接再帰エンジン（published K1138ブロック転写）×
  K0832出版単一トークン閉形式の3方式一致（C0 168,387点）、補題Z掃引
  （raw 64,800点＋閉形式 2,214,000点）、定理の完全小掃引（9,037点）・
  固定seed乱数深部（6,454点・境界470点）、2トークン境界census（5,400点・
  分離370点の記録）、出版z切片witnessアンカー4件＋階段鋭さwitness7件の
  総照合2,468,581点・bad 0。8種fail-closed変異電池すべてrc=1で捕捉、
  4回実行（同一cwd2＋隔離cwd1＋env -i・PYTHONHASHSEED=random・別HOME1）
  でaudit.json byte-identical。有限監査は証明そのものではない。
---

## 命題・範囲

空でない任意の有限多重集合 X、任意の z>=0、任意の 0<=R<=z+min(X) に対して
H(R;X;z)=v(ΣX,z,R)。2トークン (x,y)では窓 R<=z+y、y>=6行では
R<=z+6..z+y が全zで保証される。K0832の R<=z+1 一般縮約は
R<=z+1<=z+min(X) として被覆される（min>=2で真の拡張）。

## 現在の根拠と限界

全称性は構造的強帰納: min(X)>=2 ではA/B/C子の値集合が単一トークン側と
完全一致し（B子不在・デクリメント子の窓は z+min-1 に丁度収まる・C子は
(R-1,z-1) で予算一致）、mexが等しい。min(X)=1 ではB子値
v(S-1,z+1,R-1) が補題Z（v(x,z+1,n)=v(x,z,n), n<=z・n帰納の純構造証明）
によりA子値 v(S-1,z,R-1) に一致し、余分な選択肢が現れない。証明は
閉形式を使わない。

鋭さ: (2,1)@z=1,R=z+min+1=3 で親2 vs 単一0。行ごとの鋭さは
(2,2)@z=2,(4,3)@z=5,(4,4)@z=6,(6,5)@z=9,(6,6)@z=10 が R=z+y+1 で分離。
出版 z 切片 witness (12,6)@z=17/z=18・(14,6)@z=19・(16,6)@z=20 は
すべて R=z+min+1 ちょうどで分離しており独立傍証。

限界: 窓の外（R>z+min(X))の一般構造・行ごとの真の縮約上限の全称特徴付け
（y>=9では境界+1分離が希薄化・多くの行は窓を超えて一致し続ける）・
{1,1}の無分離観察の全称化・K0832 R<=2全z条款との統合窓
max(z+min(X),2) の鋭さは未解決。2トークン一般式・y>=23族・固定幅・
q点版安定化長は範囲外。標準11×11空盤・二石root {49,60}/{59,60}・
S2 {59,60}・class 1/2/4 は常にUNKNOWNのまま。
