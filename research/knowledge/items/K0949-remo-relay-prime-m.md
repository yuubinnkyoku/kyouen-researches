---
id: K0949
kind: proposition
status: proved
title: E状態リレー還元（RELAY-REDUCE）によるσ_Z値1軌跡の算術還元とPRIME-M・PARITYの全称証明（SIMPLE-CHAR）
relations:
  - depends_on: [K0939, K0941, K0946, K0948]
  - connects: [K0943, K0945]
artifacts:
  - research/experiments/remo-relay-prime-m-20261118/report.md
  - research/experiments/remo-relay-prime-m-20261118/audit_build.py
  - research/experiments/remo-relay-prime-m-20261118/composite_core.py
  - research/experiments/remo-relay-prime-m-20261118/sievegen_core.py
  - research/experiments/remo-relay-prime-m-20261118/output/relay_audit.json
date: 2026-11-18
tags: [remo, uniform-board, josephus, closed-form, prime, parity, machine-evidence]
---

## 主張（定理群は紙上全称証明。K0946予想PRIME-M・PARITYを解決）

K0945が「連分数様再帰」と見たσ_Z(M,K)値1判定が追跡固定点性+1段リレーに崩壊し、
値1軌跡が約数・spfの純算術に完全還元されることを確定し、K0946予想
**PRIME-M**（値1軌跡非空⟹M素数）と**PARITY**（素数Mのヒットは偶数）を
全称証明する。

### 補題RELAY-REDUCE（β≥2のE状態の値α+1判定・全称iff）

E(P;α,β)（β≥2）・k₀=α+β・**T=P(k₀+1)+β**・k_T:=Tの[2,k₀]内最大約数
（無ければ0）・k_{T−1}:=(T−1)の[2,k₀]内最大約数・P_d=⌊T/(k_T+1)⌋・
**P′=P_d+⌊P_d/k_T⌋+1** として
**σ_E(P;α,β)=α+1 ⟺ k_{T−1}<k_T ∧ k_T素数 ∧ spf(P′)≥k_T**。
証明: 追跡固定点性（E-form遷移のもとで追跡対(V=位置α・不変量T,
N₁=位置α+1・不変量T−1)は敗者がV/N₁以外のフェーズで新状態の(α′,α′+1)に
保存・gcd(T,T−1)=1でk_T≠k_{T−1}）。k_{T−1}>k_TならN₁がVより先に円サイズ
k_{T−1}で死亡し不成立。k_{T−1}<k_TならVが円サイズk_Tで死亡し、死亡時状態
E(P_d;·,β_d)（β_d=T mod (k_T+1)・Vの死亡はP_d mod k_T=α_c ⟺ k_T|T）の
遷移は一様E(P′;k_T−1,0)で**N₁はちょうど新位置0に落ちる**。以降のN₁生死は
K0948 U0-CLASSIFYで完全決定（k_T素数∧spf(P′)≥k_T）。∎

### 定理VALUE-ONE-CHAR（main regimeのσ_Z値1判定・全称iff）

K>M・κ=K mod (M+1)・s=⌊(K−M−1)/(M+1)⌋。**main regime**
（κ∈[0,M−2]・(s,κ)≠(0,0)）で k₀=M(s+1)+κ−1・Y=(M+1)(s+1)+κ+1・T=MY として
**σ_Z(M,K)=1 ⟺ k_{T−1}<k_T ∧ k_T素数 ∧ spf(P′)≥k_T**
（K0946 ONE-CHAR-GENERAL+tail E(M;κ,M(s+1))の第1フェーズbump→
E(M+1;β₁,M−κ)（β₁=M(s+1)+2κ−M−1）への値1候補の追跡固定点写像
（κ+1→β₁+1）でRELAY-REDUCEに帰着。β=M−κ≥2がmain regimeの正体）。
**特殊K=M+1**: σ_Z(M,M+1)=1 ⟺ **M素数 ∧ spf(M+2)≥M**（bump先は一様
E(M+2;M−1,0)で値1候補が位置0に落ちU0-CLASSIFY）。κ=M−1・κ=Mは
K0946 EXCL-2・EXCL-1（K0948で全称化）で除外済み。

### 補題P′-SIMPLIFY（main regimeのP′閉形式・全称）

素数k_T>Mなら k_T|Y（k_T>M≥spf(M)素因数）でY″:=Y/k_Tとして
Y″≥2・MY″≤k₀・β_d=T mod (k_T+1)≠0・**P′=M·Y″**、よって
**spf(P′)≤spf(M)<k_T**（β_d=0は(k_T+1)|MY″⟹MY″≥k_T+1が[2,k₀]内最大
約数k_T≥MY″と矛盾して不能）。k_T=Mならmain regimeで(M+1)∤Y・β_d≥1・
**P′=Y**。

### 定理HIT-KT-EQ-M・定理PRIME-M（K0946予想の全称証明）

main regimeではM|T=MYかつ2≤M≤k₀（k₀−M=Ms+κ≥1）なのでk_T≥M。
素数k_T>MならP′-SIMPLIFYでspf節が必ず失敗するので**ヒットはk_T=Mに限る**
（このときM素数）。剰余場合分け（K=M+1特殊・κ=M−1はEXCL-2・κ=Mは
EXCL-1+K0948・main regimeはHIT-KT-EQ-M）で全ケースが閉じ、
**M≥2, K>M, σ_Z(M,K)=1 ⟹ M素数**（定理PRIME-M）。
系（K0941 THM-B死後状態Z(w+1,n−t)）: **w+1合成ならσ_Z(w+1,n−t)≠1**、
すなわち死後frame位置1は合成NのV値に現れない（K0946の予想から全称定理へ）。

### 系SIMPLE-CHAR（値1軌跡の最終形・全称iff）

main regimeで **σ_Z(M,K)=1 ⟺ M素数 ∧ k_T=M ∧ k_{T−1}<M ∧ spf(Y)≥M**
（P′=Y）。全条件がM・Y・その約数のみの純算術で、K0945の「連分数様再帰」は
1段のbump+1段のリレー（V死亡→一様化→U0-CLASSIFY）で閉じる。

### 定理PARITY（K0946予想の全称証明）

**素数M≥3の値1ヒットKは全て偶数・M=2の奇数ヒットはK=3のみ**。
証明: M奇素数でM+1偶・K≡κ (mod 2)。K=M+1は偶数・κ=M−1,Mは除外済み。
main regimeでκ奇ならY=(M+1)(s+1)+κ+1=偶+偶=偶でspf(Y)=2<Mとなり
SIMPLE-CHAR不成立、ゆえκ偶・K偶。M=2: main regimeはκ=0のみでK=3(s+1)
（s≥1）。s偶≥2では(3s+4)/2が6s+8=4·((3s+4)/2)の約数かつ
(3s+4)/2≤2s+1=k₀なのでk_T>2で不成立、s=0はK=3特殊ケース（2素数∧
spf(4)=2≥2）で唯一の奇数ヒット。∎

## 機械的証拠（audit_build.py・output/relay_audit.json・all_ok=true）

pinned cores（K0948と同一sha・監査PIN照合）。cold 2回実行byte同一
（監査sha256 c92cb52f3a02d32a117441f8cbbbc3f5cc0a9a2ff1f5a63f6ca6056a90fc60b6・108秒/実行）:

- **RELAY**: RELAY-REDUCE 3節式 vs engine σ_E: グリッドP≤24・k≤69・β≥2全
  56,304状態（陽性3,183）+乱数4,000（P≤200・k≤600）: **不一致0**。
- **VOCE**: engine σ_Z vs 完全式: M≤30・K≤1500系統的43,036対（ヒット656）+
  乱数1,500（K≤2×10⁴）: **不一致0**。
- **VOCFF**: 完全式 vs 簡約式SIMPLE-CHAR: M≤40・K≤3000全116,181対: **不一致0**。
- **PSIM**: 素数k_T>M全7,378状態（P′=M·(Y/k_T)・β_d≠0・spf(P′)≤spf(M)）・
  k_T=M全10,035状態（P′=Y・(M+1)∤Y）: **違反0**。
- **ONECHAR**: 全656ヒットでσ_E(M;κ,M(s+1))=κ+1（K0946定理の直接アンカー）:
  **違反0**。
- **PRIMEM**: 合成M∈[4,16]・K≤1500全13,406対でengine値1なし: **違反0**。
- **CENSCOMP**（K≤2×10⁵・合成M∈{4,6,8,9,10,25,49}）: 素数k_T>Mの全状態
  88,662で3節全通過0・P′恒等式違反0・spf(P′)の実測上限=spf(M)毎
  （2/2/2/3/2/5/7）。
- **CENSPRIME**（K≤2×10⁵・素数M∈{3,5,7,11,13,17,19,23}）: main regime
  ヒット23,731個（M別 3:2057・5:2005・7:2603・11:3003・13:3220・17:3475・
  19:3629・23:3739）は**全てk_T=M**・k_T>Mでの全節通過0。
- **PARITY**: 素数M≥3の奇数ヒット0件・M=2の奇数ヒットは{3}のみ
  （main regimeヒット2,024個は全て偶数K=3(s+1)）。

## 範囲と限界

- 一様盤・K0928定理RED経由の設定のみ。**11×11空盤・二石root {49,60}/{59,60}・
  S2 {59,60}・class1/2/4には一切言及しない（UNKNOWN不変）**。
- 定理群は紙上全称証明つき（K0939/K0941/K0946/K0948の出版済み定理の組立）。
  機械検証範囲を超える全称主張は紙上証明に基づくもののみ。
- 一般Mの U_M={u : σ_E(M;0,M(u+1))=1} の密度・冪減衰構造（K0946次課題4）は
  本項では扱わない（SIMPLE-CHARは値1の判定を与えるが分布則はOPEN）。
- `uv run check/build`・unittestは本環境にcloneとuvがないため未実施
  （歴代remo項目と同じ扱い）。generated/とroot READMEは未編集。
