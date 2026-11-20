---
id: K0936
kind: proposition
status: proved
title: SIEVE7-U/V全称証明（stretch-5/6監視追跡の合成）と双子法則のmod 210全解決
aliases: []
relations:
  - depends_on: [K0934, K0935]
  - connects: [K0931, K0933]
artifacts:
  - research/experiments/remo-sieve7-uv-20261118/report.md
  - research/experiments/remo-sieve7-uv-20261118/sieve7_verify.py
  - research/experiments/remo-sieve7-uv-20261118/audit_build.py
  - research/experiments/remo-sieve7-uv-20261118/output/sieve7_uv_audit.json
date: 2026-11-18
tags: [remo, uniform-board, counting-recursion, ladder, stretch, watched-tracking, sieve, twin-laws, machine-evidence]
---

## 主張（すべてK0928のpot力学上の全称証明）

### 定理SIEVE7-U/V（SIEVE予想のp=7インスタンス・全称証明）

U(m)（監視ラベルm−1・N=2m+3）・V(m)（監視ラベル0・N=2m+1）のmがdomain
（3∤Nかつ5∤N・V: m≡1 (mod 3) と m≡2 (mod 5) を除く・U: m≡0 (mod 3) と
m≡1 (mod 5) を除く）のとき、すべてのdomain m≥3で:

- (i) 監視はstretch-5を生存する（stretch-5死亡はdomain内で一切起こらない）。
- (ii) 監視はstretch-6で死む ⟺ 7|N かつ N>7。Vはhot最終死（breaking敗者・
  保持7）・Uは冷死（block敗者・保持6）で、死亡フェーズはn3//7
  （n3=stretch-6のcircleサイズ）。
- (iii) 7∤Nなら（N=7の退化形でゲームが監視の生存のまま終わる場合も含め）
  監視はstretch-6を生存する。

### 系SIEVE-COMPOSITE（spf∈{3,5,7}・全称）

N=2m+sが合成数でspf(N)∈{3,5,7}なら監視はstretch spf(N)−1で死み、
保持はspf(N)（V・hot）／spf(N)−1（U・cold）。（spf=3: K0931・spf=5:
K0933・spf=7: 本項。spf≤7の合成Nはm≥3で尽くされる。）

### 系LAW1/LAW2 mod 210（双子法則の全クラス解決・全称）

3|C または5|C または7|C を満たす奇数C≥3（C mod 210の57類すべて）で
P(C)=1 ⟺ C素数。3|(C+1) または5|(C+1) または7|(C+1) を満たす偶数C≥2
（C mod 210の57類すべて）でP(C)=C−1 ⟺ C+1素数。証明: RED
（P(2m+1)=1+2V(m)・P(2m+2)=3+2U(m)・K0928）で監視生存に帰着し、
類内の素数インスタンスはC∈{3,5,7}／{2,4,6}ちょうどに有限ピン
（P(3)=P(5)=P(7)=1・P(2)=1・P(4)=3・P(6)=5）、それ以外はすべて
spf≤7の合成数なのでSIEVE-COMPOSITEで監視が死みP(C)≠1・P(C)≠C−1。
spf=7の新規類はLAW1: C≡{7,49,77,91,119,133,161,203} (mod 210)の8類・
LAW2: C≡{6,48,76,90,118,132,160,202}の8類。残りのC mod 210類は
spf≥11依存でOPEN。

## 証明の構成（合成。report.md参照）

m=30j+c（domain類c・m≥60 ⟺ j≥2）と書くと:

1. STR2+S3（K0931/K0933・出版済み）: stretch-4開始状態はF(4,h4;n4)・
   監視a4で、n4=15j+c4（傾き15はS3閉形式から強制）。h4・a4・
   r4=n4 mod 5はクラス定数（domainはS4死亡剰余を除外）。
2. WATCH-MAP（K0935・w=4表）: a2・h2はクラス定数、n2=n4−t4−[r4≥h4]
   =12j+c2（傾き12強制）。
3. stretch-5判定: 死む ⟺ a2=r5+1・r5=c2 mod 6（両側クラス定数）。
   32類すべてでa2≠r5+1 → (i)。
4. WATCH-MAP反復: a3・h3はクラス定数、n3=10j+c3（傾き10強制）。
5. stretch-6判定: 死む ⟺ a3=r6+1・r6=(3j+c3) mod 7が反復全体で
   唯一のj依存分岐。gcd(3,7)=1より解はただ一つの剰余類j≡ρ (mod 7)。
   Vは全類でa3≤h3（hot・保持7）・Uは全類でa3=h3+1（cold・保持6）で
   どちらもLAD-GENにより死亡フェーズ=n3//7。
6. 合同恒等式: 7|2(30j+c)+s ⟺ 4j+2c+s≡0 (mod 7)もまたjの剰余類一つ
   で、各類で両者が一致（行ごとに1行計算・機械検証）。
7. j≥2の全領域妥当性: アフィン下界（n4≥29・n2≥19・n3≥16・
   a2≤6・a3≤7）により合成定理の domain条件がすべてのj≥2で成立。
   m≥60ではN≥121>7なので7|Nは自動的に合成数側。

3≤m<60は有限全数シミュレーション検査で網羅（domain 62対・
stretch-6死亡8件: V m=24,38,45,59・U m=23,37,44,58・N=49,77,91,119）。

## 機械的証拠（sieve7_verify.py・audit_build.py）

LAD-GEN core（ladder_gen・watch_dies・watchmap）は出版済みK0934/K0935
検証器からverbatim copy・play()はK0928 Lemma Pの位相規則（K0932/K0933
検証器と同一）・track()がその合成。m=1..700両側の新鮮シミュレーション
（1,400ゲーム）で12チェック全合格: ピン対ピンRED再構成7,998比較0不一致
・FRESHPIN 1,400一致・CANON（trackerの全ストレッチ開始状態==engine・
4,358件）・TRK（tracker死亡/生存==engine・1,282ゲーム・保持・フェーズ
まで照合）・S3REG（K0933 S3閉形式854件）・K935TBL（K0935 w=4表684件）
・SV7EDGE（有限領域62対・0失敗）・SV7（合成領域684対・死亡98・生存586・
0失敗）・CLASS（32行表・j=2..16アフィン完全一致・剰余類一意・engine
一致）・TWIN210（P表C≤8000で57+57類0違反）・SIEVEOBS（観測: 死亡potは
spf−1・保持spf/spf−1・合成なら死亡・素数なら生存・死亡potはすべて偶数
・0例外）。audit_build.pyは2回in-process実行一致・決定的
output/sieve7_uv_audit.json生成（32行表を全文埋め込み）・2回cold実行で
byte同一（file sha256
5a0fa03a4a36faf1277bc026a3e4652b2541bbef85c0f3769639e9e3aa3c8ac2）。

## 範囲と限界

- 一様盤・ゼロリセット・K0859再帰（K0928定理RED経由）のみ。非一様盤・
  11×11には一切言及しない（UNKNOWN不変）。
- SIEVE予想のspf≥11側（合成数側）と一般素数Nの生存側はOPENのまま
  （SIEVEOBSはm≤700の機械観測で定理ではない）。
- クラス表の機械検証は類あたりj=2..16・全体m≤700。m≥60の全称性は
  紙上論証（分岐パラメータのクラス定数性・傾き強制・剰余類一意性・
  アフィン下界）によるもので、機械走査によるものではない。
- 双子法則は57+57類で定理化されたが、残りのC mod 210類には一切言及
  せずP(C)の一般閉形式は主張しない。
- `uv run check/build`・unittestは本環境にcloneとuvがないため未実施
  （前項の高速レーン項目と同じ扱い）。generated/とroot READMEは未編集。
