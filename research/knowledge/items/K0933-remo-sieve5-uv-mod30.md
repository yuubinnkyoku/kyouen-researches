---
id: K0933
kind: proposition
status: mixed
title: SIEVE5-U/V全称証明・双子法則のspf∈{3,5}類(mod 30)全解決・ラダーopen class初の証明済みインスタンス
relations:
  - depends_on: [K0928, K0929, K0931]
  - connects: [K0919, K0922, K0926]
artifacts:
  - research/experiments/remo-sieve5-uv-20261118/report.md
  - research/experiments/remo-sieve5-uv-20261118/sieve5_verify.py
  - research/experiments/remo-sieve5-uv-20261118/audit_build.py
  - research/experiments/remo-sieve5-uv-20261118/output/sieve5_uv_audit.json
date: 2026-11-18
tags: [remo, uniform-board, counting-recursion, survivor, stretch, sieve, primes, twin-laws, ladder, machine-evidence]
---

## 主張（証明済み部分。すべてK0928のpot力学上の全称証明）

### 定理S3-U / S3-V（STR2終状態のstretch-3完全構造・監視位置追跡つき・全称）

K0931のSTR2終状態（U: m≡1→H3(2q)監視位置n'−2・m≡2→W3(2q+1)監視n'−1。
V: m≡0→H3(2q−1)監視n'−1 hot・m≡2→G3(2q)監視n'−2 hot）から
stretch-3を8ケース全称証明した（block帰納+wrap回避条件4j≤n'+breaking
の全場合分け・監視ラベルは全ケースでbreaking recipientとして生存）。

- S3-U（m≢0 mod 3）: A-I (m=6k+1): H3(4k)→W4(3k)・監視n''−1・長さk。
  A-II (m=6k+4): H3(4k+2)→F(4,2;3k+1)・監視n''−3・長さk+1。
  B-III (m=6k+2): W3(4k+1)→F(4,2;3k)・監視n''−3・長さk+1。
  B-IV (m=6k+5): W3(4k+3)→W4(3k+2)・監視n''−1・長さk+1。
- S3-V（m≢1 mod 3）: V-A1 (m=6k+3): H3(4k+1)→F(4,3;3k)・監視n''−3・
  長さk+1。V-A2 (m=6k+6): H3(4k+3)→F(4,1;3k+2)・監視n''−1・長さk+1。
  V-B1 (m=6k+2): G3(4k)→F(4,1;3k)・監視n''−1・長さk。
  V-B2 (m=6k+5): G3(4k+2)→F(4,3;3k+1)・監視n''−3・長さk+1。

エッジ（k=0）: U m=4とV m=3,5は監視が単独生存（ストレッチ4なし・
2m+s素数と整合）、U m=5とV m=6はn''=2の1フェーズ破壊で監視生存。

### 定理S4（weight-4四族のstretch-4構造・全称）

F(4,h;n)の第一stretch-4を4族すべてのr=n mod 5で完全決定。死亡block
j*は5j*−1=監視位置を満たす唯一のjで、第一stretch-4長の閉形式は
監視位置n−1の族で(n−1)//5+1・n−3の族で(n−3)//5+1（死亡・breaking
両方を統一）。

- W4(n)（監視n−1保持4）: 5|n ⟺ block n/5で監視が冷死（ストレッチ
  継続）。r≥1はbreaking敗者=位置4−rのblock-1 recipient（hot 5）で
  監視はrecipientとして生存。LAD-h0の監視追跡版。
- F(4,1;n)（監視n−1保持5）: 5|n ⟺ block n/5で監視がhot死=第一
  stretch-4の最終フェーズ。生存類のbreaking敗者=位置4−r。
- F(4,2;n)（監視n−3保持4・hot n−2,n−1）: n≡2 (mod 5) ⟺ block
  (n−2)/5で監視が冷死。生存類のbreaking敗者位置: r=0→n−1・r=1→n−2
  （open class）・r=3→1・r=4→0、すべてhot 5。
- F(4,3;n)（監視n−3保持5・hot 3つ）: n≡2 (mod 5) ⟺ block (n−2)/5で
  監視がhot最終死（SIEVE5-Vの死亡機構）。生存類のbreaking敗者位置:
  r=0→n−1・r=1→n−2（open class）・r=3→1・r=4→0。

### 定理SIEVE5-U / SIEVE5-V（SIEVE予想のp=5インスタンス・全称証明）

- SIEVE5-U: m≥4・m≢0 (mod 3)のときU(m)のラベルm−1が最初の
  stretch-4で死ぬ ⟺ m≡1 (mod 5)（⟺5|2m+3）。m mod 30∈
  {1,11,16,26}。死亡は冷死（保持4）・blockはn''/5（h=0族）または
  (n''−2)/5（h=2族）・stretch-3以前には死なない。
- SIEVE5-V: m≥3・m≢1 (mod 3)のときV(m)のラベル0が最初のstretch-4で
  死ぬ ⟺ m≡2 (mod 5)（⟺5|2m+1）。m mod 30∈{2,12,17,27}。死亡は
  hot最終死（保持5・第一stretch-4の最終フェーズ）・block/phaseは
  n''/5または(n''−2)/5。

SIEVE3-U/V（K0931）と併せ、SIEVE予想の合成数側はspf∈{3,5}で全称決着
（U: delta=0の冷死・V: delta=1のhot死）。素数側生存（2m+sが素数
≥7）は予想のまま（機械範囲m≤8000）。

### 系LAW1-{3,5} / LAW2-{3,5}（双子法則のmod 30全解決・全称）

- LAW1-{3,5}: 3|Cまたは5|Cの奇数C≥3（C mod 30∈{3,5,9,15,21,25,27}）
  でP(C)=1 ⟺ C素数。素数側はC∈{3,5}のピン（K0919/K0929）・合成側は
  LAW1-mod6（K0931）+SIEVE5-V（5|C・3∤C類）。
- LAW2-{3,5}: 3|(C+1)または5|(C+1)の偶数C≥2（C mod 30∈
  {2,4,8,14,20,24,26}）でP(C)=C−1 ⟺ C+1素数。素数側はC∈{2,4}の
  ピン・合成側はLAW2-mod6+SIEVE5-U。

残クラス（LAW1: C mod 30∈{1,7,11,13,17,19,23,29}・LAW2:
{0,6,10,12,16,18,22,28}）はspf≥7依存でOPEN。

### ラダーの昇格（機械検証→証明済み・open class初の証明済みインスタンス）

K0931で4グリッド8,282検査のみだった制限ラダーのh≥1インスタンスの
うち、stretch-3の6インスタンス（H3両剰余×2側・G3両剰余・W3監視追跡）
とstretch-4の全r（F(4,1)・F(4,2)・F(4,3)）を証明済みに昇格。特に
**open class（h≥2・1≤r<h）の初の証明済みインスタンス**を3つ得た:
F(4,2;5t+1)（breaking敗者位置n−2・hot・phase t・終pot 5）・
F(4,3;5t+1)（同形）・F(4,3;5t+2)（hot最終死亡・SIEVE5-Vの機構）。
一般wのopen class構造はK0934（LAD-GEN）で全称解決済み。

## 予想（機械検証のみ・全称未証明）

- SIEVE予想のspf≥7: 検証器の新鮮シミュレーションでm≤700（spf≤803）
  を再確認（合成数側の死亡pot=spf−1・保持法則・素数側生存・違反0）。
  次の目標はstretch-6（spf=7）機構、すなわちW5/F(5,h;·)族の構造。
- K0931のSIEVE掃引（m≤8000）・制限ラダー（w=4はn≤250グリッド）は
  本項の証明でカバーされた範囲を含む（上方互換）。

## 機械的証拠

- sieve5_verify.py（標準ライブラリのみ・決定的・K0928 Lemma Pの直接
  実装）: m=3..700両側1,396ゲームの新鮮シミュレーション。FRESHPIN
  （生存者==コミットU/V表・0不一致）・SPF（spf法則・違反0）・SIEVE3
  回帰（違反0）・S5U/S5V（死亡⟺m≡1/2 mod 5・死亡block閉形式・U冷死/
  V hot最終死・stretch-3長・stretch-4開始状態n''/監視位置/保持
  パターン[4]^{n''−h}+[5]^h・465+465ケース・0不一致）・S4BREAK
  （生存類のbreaking構造: phase・敗者位置・保持5・723検査・0不一致）・
  REDFRESH（新鮮シミュレーションからP(C)≤1402を再構成==コミットP表・
  0不一致）。
- ピン照合: 入力はK0928/K0929コミット表（pc_uv8000.json sha256
  8a3b318b…・pc_p8000.json sha256 58a414bc…）+P(1..40)アンカー。
  REDRECON（証明済み定理REDによるピン対ピン再構成・m≤3999・7,998
  比較・0不一致）・TWIN30（コミットP表C≤8000でLAW1/LAW2の証明済み
  mod 30類の違反0・census 267/267/267/267/266/266/266×2）。
- audit_build.py: 全チェックをin-process 2回実行して結果一致を確認
  しoutput/sieve5_uv_audit.jsonを生成（タイムスタンプなし・sort_keys・
  決定的）。2回のcold実行でbyte同一（sha256
  2c1917e07254c44f69482f830b626bdc93b305d4e3d6ead733cfce7cc3fe9cf7）。

## 範囲と限界

- 一様盤・ゼロリセット・K0859再帰（K0928定理RED経由）のみ。非一様盤
  には一切言及しない。
- 証明済み: S3-U/V（8ケース）・S4（4族全r）・SIEVE5-U/V・
  LAW1-{3,5}・LAW2-{3,5}・ラダー昇格（open class 3インスタンス込み）。
- 機械検証のみ（無証明）: SIEVEのspf≥7（m≤8000・新鮮再確認m≤700）・
  素数側生存。
- OPEN: SIEVE p≥7（次はstretch-6/W5族）・W4/H4/G4/T4族の深部
  （第一stretch-4以降）・LAW1/LAW2のspf≥7類。ラダーopen classの
  一般構造（任意w）はK0934（LAD-GEN）で解決済み。P(C)の一般閉形式は主張しない。
- 11×11空盤の状況は不変（空盤・二石root {49,60}/{59,60}・S2
  {59,60}・class 1/2/4はすべてUNKNOWN）。
