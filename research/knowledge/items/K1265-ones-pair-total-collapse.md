---
id: K1265
title: "{1,1}全R崩壊定理 H(R;(1,1);z)=単一トークン(2)残余 v(2,z,R) for all z,R>=0"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [ones-pair total collapse, ones-pair full-R collapse, min-token no-window row]
relations:
- type: depends_on
  target: K0832
  note: 単一トークン閉形式。本定理により{1,1}行が全Rでこの閉形式を継承(機械監査アンカーとしても使用)
- type: extends
  target: K1264
  note: 階段定理窓R<=z+min(X)を行レベルでbypass。(1,1)行では窓が消える。K1264未解決課題2「{1,1}無分離観察の全称化」の閉包
- type: related
  target: K1138
  note: ordered/canonical二直接再帰エンジンの再帰定義のprovenance源(本機経由K1138→y22機→K1264機→K1265機)
- type: related
  target: K1257
  note: K1264機の転写源(y22機struct)。本機の間接provenance
artifacts:
- path: research/experiments/ones-pair-total-collapse-20261123/report.md
  role: proof
  note: 全称証明本文(補題E・補題V1・R強帰納・z=0のmex一致3ケース)+系(closed formの全R継承・{1}^t対比・y=1特異行)+誠実記録
- path: research/experiments/ones-pair-total-collapse-20261123/verify_ones_pair_collapse.py
  role: verifier
  note: D0..D5監査・fail-closed変異電池8種・audit JSON決定性出力
- path: research/experiments/ones-pair-total-collapse-20261123/output/audit.json
  role: data
  note: 総照合67,513点・bad 0・4実行(隔離cwd・env -i別HOME込み)byte-identical
- path: research/experiments/ones-pair-total-collapse-20261123/build_verifier.py
  role: code
  note: K1264出版verifier(SHA-256 108fdd65...)からのエンジン・閉形式ブロック機械抽出機(sha256ゲート付き・手転写ゼロ)
- path: research/experiments/ones-pair-total-collapse-20261123/probe_ones.py
  role: data
  note: 宣言前探査グリッド(宣言ノートに開示済み・実験dirに収録)
- path: research/log/2026-11-23-ones-pair-total-collapse.md
  role: log
- path: research/log/2026-11-23-ones-pair-total-collapse-single-owner-note.md
  role: log
  note: 単一オーナー宣言(commit 284d82c6・publish-then-execute・宣言前探査の全開示)
scope: >-
  κ=1残余ゲーム H(R;{1,1};z) の全z>=0・全R>=0 における総和2の単一トークン残余
  v(2,z,R) への完全崩壊。他の多重集合(単一トークン・{1}^t t>=3・(x,1) x>=2等)
  の全R崩壊資格の特徴付け・窓外一般構造(R>z+min(X))・高zマージ領域は範囲外。
evidence: >-
  全称性はreport.mdの構造的強帰納: 補題V1(x=1単一トークン残余の完全特徴付け
  v(1,z,n)=0/2/1・n帰納の純構造証明)がz>=1でB子値とA子値の全n一致を与え、
  z=0では3境界ケース(n=0/1/>=2)すべてでmexが一致する。証明は閉形式を使わない。
  機械監査は独立照合: ordered/canonical二rawエンジン(K1264機から機械抽出)×
  K0832出版閉形式の3方式(プロビナンスアンカー55,242点)・補題V1掃引6,426点・
  {1,1}定理掃引2,697点・固定seed乱数深部1,500点(窓外R=z+17..z+28含む)・
  {1}^t census 1,615点(t=2零分離・t>=3の初分離はz=0,R=3で全t共通の観測)・
  witnessアンカー33点(K1264出版witness {1}^3@z=1,R=3・(2,1)@z=1,R=3照合込み)の
  総照合67,513点 bad 0。fail-closed変異電池8種すべてrc=1で捕捉({1}^3拡張6・
  補題V1 z=0反転1・n>=2パリティ破壊380・閉形式q_odd腐敗720・C手除去14・
  z=0オプション等値主張1・出版witness親値反転1・アンカー親値反転1)。
  4実行(同一cwd2+隔離cwd+env -i・PYTHONHASHSEED=random・別HOME)でaudit.json
  byte-identical。有限監査は証明そのものではない。宣言点数算術のドリフト
  3箇所(D3/D4/D5)はrun logに訂正記録(実測67,513点が正本)。
---

## 命題・範囲

全ての z>=0 と全ての R>=0 に対して H(R;(1,1);z)=v(2,z,R)。
K1264階段定理の窓 R<=z+min(X)=z+1 を (1,1) 行ではbypassして全Rで崩壊する。
y=1ファミリーで唯一の全R無分離行({1}^t構造ではアリティ2の全一対が特異)。

## 現在の根拠と限界

全称性は構造的強帰納: 補題V1(v(1,z,n)=0(n=0)/2(n=1,z>=1)/1(その他)・n帰納の
純構造証明)より z>=1 では全nで v(1,z+1,R-1)=v(1,z,R-1) が成立し B子値とA子値が
完全一致、C子はR帰納で一致。z=0ではC手不在で B子{v(1,1,n)} と A子{v(1,0,n)} は
n=1 ちょうど1点だけ異なる(2 vs 1)が、mexは全3ケース(n=0/1/>=2)で一致する。
証明は閉形式を使わない。補題V1の系として K1264補題Z のx=1版は窓外でも破れない
ことが従う(x=1の残余値は全域{0,1,2}に落ちる)。

限界: 全R崩壊する多重集合の完全特徴付けは未解決({1}^t t>=3 は z=0,R=3 で
分離・(x,1) x>=2 は境界+1で分離がK1264 C4掃引範囲で観測・{1,1,a}型は未掃引)。
窓外一般構造・y>=9境界+1希薄化・max(z+min(X),2)統合窓鋭さ(K1264課題の残3項)は
非接触。2トークン一般式・y>=23族・固定幅・q点版安定化長は範囲外。
標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は常にUNKNOWN
のまま。
