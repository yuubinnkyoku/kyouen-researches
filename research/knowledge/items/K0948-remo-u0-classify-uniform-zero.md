---
id: K0948
kind: proposition
status: proved
title: 一様E状態E(P;n,0)の零点の完全分類（U0-CLASSIFY）と系U0-NEVER・FIRST-NEVER・ZERO-SET（EXCL-1の全称定理化）
aliases: []
relations:
  - depends_on: [K0939, K0941, K0946]
  - connects: [K0937, K0945]
artifacts:
  - research/experiments/remo-u0-classify-20261118/report.md
  - research/experiments/remo-u0-classify-20261118/audit_build.py
  - research/experiments/remo-u0-classify-20261118/composite_core.py
  - research/experiments/remo-u0-classify-20261118/sievegen_core.py
  - research/experiments/remo-u0-classify-20261118/output/u0_audit.json
date: 2026-11-18
tags: [remo, uniform-board, josephus, divisor-sieve, closed-form, prime, machine-evidence]
---

## 主張（定理群は紙上全称証明。K0946の未証明帰着U0-NEVERを解決）

K0941定理CのE状態E(P;α,β)=[P]^α[P+1]^β（k=α+β人・σ_E再帰はpinned
composite_core.py）のうち一様形E(P;n,0)の監視（位置0）の生存を完全分類する。

### 補題V-TRACK（監視不変量の由来非依存性・全称）

E-form遷移（r<α→E(P+q;α−r−1,β+r)・r≥α→E(P+1+q;β+2α−r−1,r−α)）に従う
任意のE状態列で、監視者の石数不変量 **N=P(k+1)+β** は毎フェーズ保存され、
円サイズkでの死亡 ⟺ **k|N**。K0939 END-INVの帰納段は状態の由来を一切参照
しないため任意のE状態に逐語適用可能（K0941定理C「E-form自己保存」が遷移の
正当性を与える）。

### 補題WRAP（一様状態の第1フェーズ折り返し・全称）

E(P;n,0)（n≥2）の第1フェーズ（q,r=divmod(P,n)）で監視（位置0）はr=0のとき
死亡（⟺n|P⟺n|P(n+1)）。r≥1なら監視は新状態E(P+q;n−r−1,r)の**V位置
（n−r−1）**に落ち、不変量T=(P+q)n+r=P(n+1)が保存される（旧位置0は
新フレームの敗者位置r+1から数えてn−r−1=[P+1]^rブロック先頭）。

### 定理U0-CLASSIFY（零点の完全分類・全称iff）

**n≥1: σ_E(P;n,0)=0 ⟺ n+1が素数 ∧ spf(P)≥n+1**（spf(1):=∞）。
証明: WRAP+V-TRACKで監視の不変量は全程N=P(n+1)で保存され、死亡は円サイズ
k∈[2,n]がNを割り切るときかつそのときに限る（降順走査なので最大の約数kで死亡）。
(⇐) n+1素数∧spf(P)≥n+1ならk∈[2,n]はgcd(k,n+1)=1（k<n+1）なのでk|N⟹k|P
⟹spf(P)≤k≤n<n+1で矛盾（P=1ならk|Pも不成立）。(⇒) n+1合成なら
p=spf(n+1)≤(n+1)/2≤n（n+1≥4）がNを割り切り死亡。n+1素数でもspf(P)≤nなら
k=spf(P)∈[2,n]がNを割り切り死亡。∎
n=0は空円の退化形として分類の外（n=1はk∈[2,n]が空で常に生存し、式は
n+1=2素数∧spf(P)≥2と整合）。

### 系群（全称・U0-CLASSIFYの直接帰結）

- **系U0-NEVER**: M≥2, t≥2 ⟹ **σ_E(M+1;Mt−1,0)≠0**（n+1=Mt合成）。
  K0946系EXCL-1（K≡M (mod M+1), K>M ⟹ σ_Z(M,K)≠1）が帰着形から
  **全称定理**に昇格（K0946本文の帰着: tail E(M;M,M(s+1))のbump→一様
  E(M+1;M(s+2)−1,0)・値1⟺位置0生存⟺U0-CLASSIFY右辺・M(s+2)合成で不成立）。
- **系FIRST-NEVER**: P≥2, n≥P ⟹ σ_E(P;n,0)≠0（spf(P)≤P≤n<n+1）。
- **系ZERO-SET**: σ_E(P;n,0)=0となるn≥1の集合は **{p−1 : p素数≤spf(P)}**
  （P=1はspf=∞で全素数{p−1}）。K0946出版時の観察「n≡−1 (mod P−1)の零は
  0件」は n≥2 で正当化（n+1=p素数∧(P−1)|pはP−1∈{1,p}に限り、零になるのは
  (P,n)=(2,1),(3,1)のn=1のみ）。

## 機械的証拠（audit_build.py・output/u0_audit.json・all_ok=true）

pinned cores（composite_core.py sha256 3990d67ff3a89f480bd92ae784a9efa763d76264e2b8e4a2d1752507a4740f40・
sievegen_core.py sha256 a69f916c86ed02d5eeed3d5494bbb0f44f652d0d1e4714c50bbc68bef1843499・
K0937/K0941 committed版とbyte同一・監査PIN照合）。cold 2回実行byte同一
（監査sha256 d1a8316954e90cf9444cc822210a71f9f8f561dc9524f6841e7d57a8516a0356）:

- **U0**: P≤60・n∈[1,400]のengine直接値 vs 分類式: **不一致0**（零292）。
- **SIEVE**: 同全域でengine零 vs 独立約数篩判定（∃k∈[2,n]: k|P(n+1)）: **不一致0**
  （V-TRACK/WRAPの死亡合同式の別経路検証）。
- **U0N**: M,t∈[2,60]全3,481状態でσ_E(M+1;Mt−1,0)≠0: **違反0**。
- **FIRST**: P∈[2,60]・n∈[P,400]全21,830状態: **違反0**。
- **P1/ZSET**: P=1零点=n+1素数（n≤60完全一致）・P∈[2,60]全59個で
  n≤400窓内零点集合={p−1: p素数≤min(spf(P),401)}: **不一致0**。

## K0946への反映

- 系EXCL-1が全称定理化。K0946予想PRIME-M・PARITYの全称証明は後続項目K0949
  （RELAY-REDUCEの終端判定にU0-CLASSIFYを使用）。

## 範囲と限界

- 一様盤・K0928定理RED経由の設定のみ。**11×11空盤・二石root {49,60}/{59,60}・
  S2 {59,60}・class1/2/4には一切言及しない（UNKNOWN不変）**。
- 定理群は紙上全称証明つき（機械検証は有限アンカー）。機械検証範囲を超える
  全称主張は紙上証明に基づくもののみ。
- `uv run check/build`・unittestは本環境にcloneとuvがないため未実施
  （K0937/K0939/K0941/K0943/K0945/K0946と同じ扱い）。generated/とroot READMEは
  未編集。
