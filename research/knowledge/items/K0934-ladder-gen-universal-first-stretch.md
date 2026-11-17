---
id: K0934
kind: proposition
status: proved
title: 制限ラダーF(w,h;n)第一stretch-w法則の全称決定（LAD-GEN・open class完全解決）
relations:
  - depends_on: [K0928, K0931, K0933]
  - connects: [K0929, K0930, K0932]
artifacts:
  - research/experiments/ladder-gen-20261118/report.md
  - research/experiments/ladder-gen-20261118/ladder_gen_verify.py
  - research/experiments/ladder-gen-20261118/audit_build.py
  - research/experiments/ladder-gen-20261118/output/ladder_gen_audit.json
date: 2026-11-18
tags: [remo, uniform-board, counting-recursion, ladder, stretch, open-class, machine-evidence]
---

## 主張（すべてK0928のpot力学上の全称証明）

### 定理LAD-GEN（制限ラダーF(w,h;n)の第一stretch-w完全法則・全称）

w≥2・0≤h≤w・n=(w+1)t+r（t≥1・0≤r≤w）とし、J = t（r≥h）または
t−1（r<h）とおく。このときF(w,h;n)の第一stretch-wは次の通り完全決定
される（K0931のopen class「h≥2・1≤r<h」を含む全クラス）。

- **(a) コールドblock**: 各j=1..Jのフェーズjは元位置(j−1)(w+1)..
  j(w+1)−2に初めて1石ずつ配り、元位置j(w+1)−1を保持wの冷死で除去。
- **(b) breakingフェーズ**（フェーズJ+1・敗者保持w+1でストレッチ終了）:
  r<h → ptr=n−r−w−1、配り(t−1)(w+1)..t(w+1)−2（wrapなし）・
  敗者は元位置n−r−1（hot・1度も配られていない）。r≥h・r≥1 →
  ptr=t(w+1)、配りは末尾r位置+wrap 0..w−r−1・敗者は元位置w−r
  （block-1で1度配られたcold・保持w+1）。r=h=0・t≥2 → ptr=0、
  配り0..w−1・敗者は元位置w+1（block-2で配られたcold）。崩壊ケース
  (t,r,h)=(1,0,0) → フェーズ2でq=1・全員w+2・敗者は元位置0・
  終状態は一様状態W_{w+2}(w−1)。
- **(c) 終状態（censusでなく厳密）**: 非崩壊のとき終circleは新ptrから
 ちょうど [w+1]^(n2−h2) + [w+2]^h2（正規化そのもの）で状態は
  F(w+1,h2;n2)・pot w+1。r<h → n2=n−t・h2=h−1−r。r≥h →
  n2=n−t−1・h2=h+w−r（=(h−1−r) mod (w+1)）。
- **(d) 除去集合**: 第一stretch-wの除去元位置は{ j(w+1)−1: j≤J }と
  breaking敗者。ストレッチ長はr≥hでt+1フェーズ・r<hでtフェーズ
  （崩壊は2=t+1）。
- **(e) 監視条件**: n≥2w+2・1≤a≤w+1の監視位置n−aは第一stretch-wで
  死ぬ ⟺ a=r+1。このときフェーズtで死亡し、a≥h+1なら冷死（保持w）・
  a≤hならhot最終死（保持w+1）。唯一の例外は
  (h,r,t,a)=(0,0,2,w+1): 監視n−(w+1)=w+1がr=0のbreaking敗者と
  一致し、フェーズt+1=3でhot死（保持w+1）。

### 系（すべてLAD-GENの直接の帰結）

- **LAD-h0回帰（K0931）**: h=0で r=0→F(w+1,w;wt−1)（t≥2）・
  r≥1→F(w+1,w−r;wt+r−1)・(t,r)=(1,0)→W_{w+2}(w−1)。K0931の
  LAD-h0全行を再導出。
- **open class完全解決（K0931）**: h≥2・1≤r<hは(b)(c)のケース1で
  完全決定（breaking敗者n−r−1 hot・終状態F(w+1,h−1−r;n−t)）。
  第一stretch-w法則にopen classはもう存在しない。
- **K0931制限ラダー則の全称証明化**: K0931で4グリッド8,282検査のみ
  だった「h=0全r、h≥1でr=0またはr≥h」の終状態則
  （h″=(h−1−r) mod (w+1)・n′=n−t−[r≥h]）がLAD-GENの(c)として
  全称証明された。
- **S4回帰（K0933）**: w=4の4族の死亡表（W4/F(4,1)は5|nで死亡・
  F(4,2)/F(4,3)はn≡2 (mod 5)で死亡・冷死/hot最終死の別・死亡
  block t・第一stretch長 (n−a)//5+1）が(e)とその系から導出される。
- **ラダー再帰**: 非崩壊のとき第一stretchは
  F(w,h;n)→F(w+1,(h−1−r) mod (w+1); n−t−[r≥h]) の閉形式1歩を与える
  （適用範囲h2≤w+1・n2≥w+2）。2ストレッチ合成はLG8で直接検証。

## 機械的証拠

- ladder_gen_verify.py（標準ライブラリのみ・決定的・K0928 Lemma Pの
  直接実装）: w=2..7・h=0..w・n=w+1..155の全グリッド4,949ゲームで
  LG1-LG5（長さ・68,411 block・breaking・厳密終circle・除去集合・
  監視28,470検査・例外込み）、LG6（LAD-h0回帰903）、LG7（S4回帰
  580）、LG8（2ストレッチhandoff: w≤5・n≤90・1,503ゲーム・
  stretch-2 block 8,924検査・終状態から閉形式で予測したstretch-2が
  同一シミュレーションの継続と一致）。全チェック0失敗。
- audit_build.py: 全チェックをin-process 2回実行して一致確認・
  output/ladder_gen_audit.json生成（タイムスタンプなし・sort_keys・
  決定的）。2回のcold実行でbyte同一（sha256
  52cbab9aa98095044e254b6d9355d340e68840e6fc51a809a6e4c9e95fa01d36）。
- 帰納・場合分け・censusはreport.mdの紙上証明（block帰納+breaking
  2ケース+終状態3ケース+監視条件導出+例外の一意性）。スクリプトは
  機械アンカーであり証明ではない。

## 範囲と限界

- 一様盤・ゼロリセット・K0859再帰（K0928定理RED経由）のみ。
- 定理域はw≥2・0≤h≤w・t≥1。監視条件(e)はn≥2w+2（t≥2）限定
  （t=1のwrap衝突は仮定で排除・未解析）。ラダー再帰の反復適用は
  h2≤w+1・n2≥w+2の間のみ（h2>w+1の出口はF族記法の外）。崩壊
  W_{w+2}(w−1)は一様状態レーンに属し反復しない。
- 監視位置のストレッチ間追跡（SIEVE機構）は本項の範囲外。SIEVE7
  （spf=7・stretch-6）への適用が自然な次歩: per-stretch法則は全称化
  済みなので、残るは(n mod 42)有限類の監視bookkeepingのみ。
- 次のopen target: SIEVEのp=7（stretch-5/6のW5/F(5,h;·)族）・
  LAW1/LAW2のspf≥7類。P(C)の一般閉形式は主張しない。
- 11×11空盤の状況は不変（空盤・二石root {49,60}/{59,60}・S2
  {59,60}・class 1/2/4はすべてUNKNOWN）。
