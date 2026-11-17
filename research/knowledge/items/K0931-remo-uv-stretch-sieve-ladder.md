---
id: K0931
kind: proposition
status: mixed
title: U/V縮約ゲームのstretch-2構造定理・双子法則のmod 6全称決着・統一重量ラダー
relations:
  - depends_on: [K0928, K0929]
  - connects: [K0919, K0922, K0923, K0926]
artifacts:
  - research/experiments/remo-uv-stretch-ladder-20261117/report.md
  - research/experiments/remo-uv-stretch-ladder-20261117/sieve_test.py
  - research/experiments/remo-uv-stretch-ladder-20261117/theorem_verify.py
  - research/experiments/remo-uv-stretch-ladder-20261117/ladder_verify.py
  - research/experiments/remo-uv-stretch-ladder-20261117/w3_explore.py
  - research/experiments/remo-uv-stretch-ladder-20261117/audit_build.py
  - research/experiments/remo-uv-stretch-ladder-20261117/output/uv_stretch_ladder_audit.json
  - research/experiments/remo-uv-stretch-ladder-20261117/data/w3_explore.json
date: 2026-11-17
tags: [remo, uniform-board, counting-recursion, survivor, stretch, ladder, primes, machine-evidence]
---

## 主張（証明済み部分。すべてK0928のpot力学上の全称証明）

### 定理STR2-V / STR2-U（stretch-2の完全構造・全称）

K0928の縮約ゲームV(m)（m人各2石・pot 1・ptr 0）とU(m)（pot 2）の
stretch-2（potが2の連続フェーズ）を完全に決定した。

- STR2-V（m≥4）: 長さ⌈(m−1)/3⌉。block敗者はラベル4,7,10,…（≡1 mod 3）
  の冷死（保持2）。breaking敗者（保持3・hot死）はm≡1→ラベル0・
  m≡0→ラベル2・m≡2→ラベル3。終状態はm=3q+1→W3(2q)
  （circle [2,3,5,6,…] 全員3・pot 3）・m=3q→H3(2q−1)
  （末尾ラベル0がhot4）・m=3q+2→G3(2q)（末尾0,2がhot4）。
- STR2-U（m≥4）: 長さ⌈(m+1)/3⌉。block敗者はラベル2,5,8,…の冷死。
  breaking敗者はm≡0→ラベル3・m≡1→ラベル1・m≡2→ラベル0。
  終状態はm=3q+2→W3(2q+1)・m=3q+1→H3(2q)・m=3q→G3(2q−1)。

証明はblock帰納（block jのrecipient・敗者の位置算術、wrap回避条件
3j+2≤m等）とbreakingのm mod 3場合分け（report.mdに全記述）。
W3(n)=[3]∗n・H3(n)=[3]∗(n−1)+[4]・G3(n)=[3]∗(n−2)+[4,4]は
ラダー族F(3,h;n)のh=0,1,2インスタンス（6還元）。

### 系SIEVE3-V / SIEVE3-U（SIEVE予想のp=3インスタンス・全称証明）

- SIEVE3-V: V(m)でラベル0がstretch-2で死ぬ ⟺ m≡1 (mod 3)
  （⟺3|2m+1）。
- SIEVE3-U: U(m)でラベルm−1がstretch-2で死ぬ ⟺ m≡0 (mod 3)
  （⟺3|2m+3）。m≡1,2ではラベルm−1はbreaking recipientとして
  生存（保持3）。m=3は直接確認（U(3)=1≠2）。

### 定理LAW1-mod6 / LAW2-mod6（双子法則のmod 6類の全称決着）

- LAW1-mod6: C≡3 (mod 6)の全CでP(C)=1 ⟺ C素数。C=3は素数で
  P(3)=1（ピン）。C≥9は3の倍数の合成数で、m=(C−1)/2≡1 (mod 3)より
  STR2-Vのbreaking敗者がラベル0、よってV(m)≠0、K0928定理REDより
  P(C)≠1。両辺偽で同値成立。
- LAW2-mod6: C≡2 (mod 6)の全CでP(C)=C−1 ⟺ C+1素数。C=2は
  C+1=3素数でP(2)=1。C≥8はC+1≡3 (mod 6)・≥9の合成数で、
  m=(C−2)/2≡0 (mod 3)よりSIEVE3-Uでラベルm−1が死亡、
  U(m)≠m−1、P(C)≠C−1。

残クラス（LAW1: C≡1,5・LAW2: C≡0,4 mod 6）はSIEVE予想依存でOPEN。

### 定理LAD-h0（統一重量ラダーのh=0・一般w≥2で全称証明）

F(w,h;n)（先頭n−h人がw石・末尾h人がw+1 hot・pot w・ptr 0）、
n=(w+1)k+r（k≥1・0≤r≤w）のときW_w(n)=F(w,0;n)のstretch-wは
k+1フェーズで終わり、block j（j=1..k）は位置(j−1)(w+1)..j(w+1)−1を
w→w+1に配り位置j(w+1)−1（保持w・冷死）を除く。breakingは
r≥1→hot敗者kept index w−r（終状態F(w+1, w−r; wk+r−1)・pot w+1）・
r=0,k≥2→kept w（F(w+1, w; wk−1)）・r=0,k=1は崩壊で全員w+2となり
W_{w+2}(w−1)（基礎重量がw+2に跳ぶ）。6還元（STR2終状態は
W3/H3/G3=F(3,h;·)インスタンス・V(m)のphase-1はF(2,1;m−1)）により
ラダーはU/Vレベル（w=2）とweight-3レベル（w=3）を統一する。

## 予想（機械検証のみ・全称未証明）

### SIEVE予想（m≤8000で機械検証）

- V側: V(m)のラベル0はpot-(p−1)ストレッチ（p=spf(2m+1)）で
  保持pのhot死（delta=1）。2m+1が素数なら生存（V(m)=0）。
- U側: U(m)のラベルm−1はpot-(p−1)ストレッチ（p=spf(2m+3)）で
  保持p−1のcold死（delta=0）。2m+3が素数なら生存（U(m)=m−1）。

N=8000でV違反0・U違反0・ピン不一致0（K0929コミット表と完全一致）。
SIEVE3がp=3の証明済みインスタンスだった。**2026-11-18更新
（K0933）**: p=5のSIEVE5-U/Vが全称証明され、この予想の合成数側は
spf∈{3,5}で全称決着した。残るopenケースはspf≥7
（次はstretch-6・W5/F(5,h;·)族）。全称証明には死亡レベル=spf−1の
機構の一般化が必要。

### 制限付き統一ラダー（h≥1はK0934で全称証明）

F(w,h;n)のstretch-w終状態則（h′=(h−1−r) mod (w+1)・n′=wk+e・
終circle [B]^{n′−h″}+[B+1]^{h″}・pot B）は適用範囲
「h=0全r、またはh≥1でr=0またはr≥h」で4グリッド8,282検査0違反。
h≥2かつ1≤r<hはopen classだったが、**2026-11-18更新（K0934）**:
LAD-GENで全称解決した（breaking敗者は元位置n−r−1のhot・終状態は
F(w+1,h−1−r;n−t)）。

## 機械的証拠

- theorem_verify.py: m∈[4,1000]でSTR2-V/U・SIEVE3-U・6還元を
  3,988検査・0失敗。終状態期待値は定理の閉形式から生成し、
  新鮮シミュレーション・縮約ゲームの生存者→ラベル写像で
  コミットピンと照合。
- sieve_test.py: N=8000・pinsモード。死亡レベルのtop計数
  （V: pot2で2,666・pot4で1,066・pot6で608・pot10で332…すべて
  delta=1。U: 同一pot列でdelta=0）。
- ladder_verify.py: w=2 n≤1000・w=3 n≤800・w=4 n≤250・w=5 n≤150・
  h=0..wの全グリッド8,282検査0違反。
- 監査JSON（audit_build.pyが3検証器を再実行して生成・4チェック
  all_ok）は2回のcold実行でbyte同一
  （sha256 5ab2907d1800f60c6ad4d7149608e1b3be6c1ec19e19e066423ab3208cea328c）。
  入力ピンはK0928/K0929コミット表
  （pc_uv8000.json sha256 8a3b318b…・pc_p8000.json sha256 58a414bc…）。
- data/w3_explore.json: W3/H3/G3のstretch-3終状態shape（n mod 4
  類型）と位置0の死亡レベル（素数法則なし・不規則）の探索データ
  n≤300（weight-4レベルへの入力・本itemでは主張しない）。

## 範囲と限界

- 一様盤・ゼロリセット・K0859再帰（K0928定理RED経由）のみ。
  非一様盤には一切言及しない。
- 証明済み: STR2-V/U・SIEVE3-V/U・LAW1-mod6・LAW2-mod6・LAD-h0・
  制限ラダー終状態則（K0934で全称化）。機械検証のみ（無証明）:
  SIEVE予想m≤8000。
- OPEN（2026-11-18・K0934更新後）: ラダーのopen class
  （h≥2・1≤r<h）はLAD-GEN（K0934）で全wについて解決し、第一
  stretch-w法則にopenは残っていない。
  SIEVEのp=5はSIEVE5-U/V（K0933）で解決し、残りはspf≥7
  （次はstretch-6・W5族）。W4/H4/G4/T4族の第一stretch-4はS4
  （K0933）で決着し、以深はOPEN。LAW1/LAW2の残クラスはmod 30で
  spf∈{3,5}類まで決着し、spf≥7類（LAW1: C mod 30∈
  {1,7,11,13,17,19,23,29}・LAW2: {0,6,10,12,16,18,22,28}）がOPEN。
- P(C)の一般閉形式は主張しない。11×11空盤の状況は不変
  （空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
  すべてUNKNOWN）。
