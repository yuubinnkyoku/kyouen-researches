---
id: K0943
kind: proposition
status: proved
title: ladder監視状態のO(1)閉形式（STATE-CF）・死亡状態閉形式（DS-CF）・p²崩壊定理（P2）− K0941レジューム(i)完成
relations:
  - depends_on: [K0937, K0934, K0941, K0939]
  - connects: [K0929, K0931, K0933, K0942]
artifacts:
  - research/experiments/remo-deathstate-closedform-20261118/report.md
  - research/experiments/remo-deathstate-closedform-20261118/sievegen_core.py
  - research/experiments/remo-deathstate-closedform-20261118/deathstate_verify.py
  - research/experiments/remo-deathstate-closedform-20261118/audit_build.py
  - research/experiments/remo-deathstate-closedform-20261118/output/deathstate_audit.json
date: 2026-11-18
tags: [remo, uniform-board, counting-recursion, closed-form, composite, prime, ladder, machine-evidence]
---

## 主張（K0941レジューム(i)「P2OBS全称化」の完成。全定理が紙上全称証明）

### 補題H-CAP（新規・全称）

V(m)/U(m)で監視生存中のすべてのladder stretch開始状態F(w,h;n)（w≥2）は
**0≤h≤w−1**（Vはさらに**1≤h**）。素数Nのt=0エンドゲーム入口でも同じ界。
証明: 基底h=1（V）/0（U）。帰納段はLAD-GEN (c)の
h2=(h−1−r) mod (w+1)∈[0,w]が次幅w+1の界を与える。Vのh≥1は
W∤T=N（Wの素因数<spf(N)、素数NはW²<N）から。∎

**系EXC-UNREACH**: LAD-GENの唯一の監視死亡例外(h,r,t,a)=(0,0,2,w+1)は
V/Uゲームで非到達（a=w+1が必要: Vはa=h≤w−1・Uはa=h+1=w+1⟺h=wがH-CAPで排除）。

### 定理STATE-CF（新規・全称）

T=N（V）/N−1（U）とおくと、生存中の全stretch開始状態（t≥1）と素数Nの
入口状態（t=0）が一斉に

**h=(T−w) mod w・n=(T−w−h)/w**

で決まる（V: h∈[1,w−1]・U: h∈[0,w−1]）。tracker再帰・watchmapは不要で、
ladder状態列挙が(side,m,w)のO(1)算術になる。証明はINV-TRACK恒等式
T=wn+h+wとH-CAPの一意なdiv/mod分解。K0939 ENTRY-LOCのfamily範囲
h≤min(n,w)はタイトなh≤w−1に精密化される。

### 系DS-CF（全称）

合成Nの死亡stretch状態はw*=spf(N)−1でのSTATE-CF値。死亡二分法
r=h−1（V・breaking hot死・保持w+1）/r=h（U・block cold死・保持w）は
合同式 N≡h−r−1+s (mod w*+1) とレンジh−r−1∈[−w,w−2]/h−r∈[−w,w−1]
から再導出され、K0941定理Bの死後状態の全石数（盤面+pot）が閉形式から
算術検証される（V:(w+1)(n−t+1)=N・U非崩壊:E形式=N−1・U崩壊:(w+2)w=N−1）。
U曖昧ケース（w*|N−1・2候補が監視窓に両立）はH-CAPにより常にh*=0に解消
（m≤30,000で14,123例・全例h*=0・うち52例がp²崩壊）。

### 系P2（K0941 P2OBSの全称化）

**U崩壊死(t,h,r)=(1,0,0) ⟺ N=spf(N)²**・
**V死亡状態(n,t,r,h)=(p,1,0,1) ⟺ N=p²**。
証明はDS-CF閉形式と状態等式の直接計算（h*=0,n*=w*+1 ⟺ N−1=(w*+1)²−1 /
V: N=(w*+1)²）。K0941のm≤8,000観察（29↔29）はm≤30,000・p≤241の52↔52
全単射として機械確認され全称証明を得た。p²軌道のh-walk記述は不要だった。

### 系WALK-CF

ladder全状態列がO(spf(N))時間・O(1)メモリの閉形式列挙になる。
K0941定理Dのラベル合成（除去集合のJ′,bl′）も閉形式から直接計算できるので、
**合成NのV/U値計算からtrackerが完全に除去**される（残るはσ再帰O(k)のみ）。

## 機械的証拠（deathstate_verify.py・audit_build.py）

sievegen_core.pyはK0937 committed版のbyte同一コピー
（sha256 a69f916c86ed02d5eeed3d5494bbb0f44f652d0d1e4714c50bbc68bef1843499）。
6チェック全合格・決定的:

- **CFTRACK**: 両側m≤30,000・60,000ゲーム・**2,597,593 tracker step**が
  閉形式・H-CAP・窓1≤a≤n・T=wn+h+w・a=h/h+1に全一致（h=w出現0回）。
  素数入口12,111件も一致（V m=1のn=0退化形はENTRY-LOC既知例外として計上）。
- **DEATHCF**: 合成死亡47,889件: w*=spf−1・二分法・保持・死亡位相=t・
  死後石数保存が全一致。U曖昧統計14,123（52崩壊+14,071非崩壊・全h*=0）。
- **P2**: 両方向52↔52（p=3..241・m≤30,000）・件数4つ全一致・違反0。
- **SIMDEATH**: 閉形式死亡状態起点のstretch_sim 613ゲーム（全p² 52×両側を
  m≤30,000で含む）: 死亡位相・保持・exp_len・死後Z/E/崩壊holdings円・n2
  全一致・違反0。
- **ENGINE**: 新鮮play_full m≤400両側800ゲーム: ladder run開始状態6,523件が
  閉形式一致・合成525死亡のpot=w*・保持二分法一致・素数275件survivor==watch。
- **COREPIN**: core sha256照合。

audit_build.pyはrun_checksをin-process 1回+deathstate_verify.py
（内部2回実行の決定性検証つき）をcold 2回実行しbyte同一を確認して
output/deathstate_audit.jsonを書く
（監査sha256 9bc8c2f478c98ef5bbfdd08e3edd733a4a27ec31f835327d51445f1d38e48882・7,514 bytes）。

## 範囲と限界

- 一様盤・ladder regimeのみ。E-game内部遷移（K0941定理C）とσ_E/σ_Z閉形式は
  主張しない（σ_Z(3,K)値1位置4,8,12,28,40,52,72,…は次課題→K0945でONE-CHAR全称
  特徴付け・A2-NEVER・fold分解（RUN-3/FOLD）・FAST算法として出版済み）。
- 紙上証明はK0937（INV-TRACK・死亡合同式）・K0934（LAD-GEN (c)・t=1拡張）・
  K0941（定理A/B）・K0939（ENTRY-LOC）の出版済み証明に依存し、機械アンカーは
  259万step+47,889死亡+613シミュレーション+800新鮮エンジン照合0違反で裏付ける。
- 非一様盤・11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/2/4は
  **UNKNOWN不変**（本項は一切言及しない）。STATE-CFの11×11枝刈り活用は
  記録のみ（未実施）。
- `uv run check/build`・unittestは本環境にcloneとuvがないため未実施
  （K0937/K0939/K0941と同じ扱い）。generated/とroot READMEは未編集。
