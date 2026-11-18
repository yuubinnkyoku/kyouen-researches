---
id: K0950
kind: proposition
status: proved
title: σ_Z値1軌跡の素数対への完全還元（HIT-ARITH・Y-FACTOR）と剰余死刑令P-KILL・PAIR-2/PAIR-3・M-SQ（K0946次課題4/5の部分解決）
relations:
  - depends_on: [K0946, K0948, K0949]
  - connects: [K0939, K0941, K0945]
artifacts:
  - research/experiments/remo-hit-prime-pair-20261118/report.md
  - research/experiments/remo-hit-prime-pair-20261118/hitpair_core.py
  - research/experiments/remo-hit-prime-pair-20261118/audit_build.py
  - research/experiments/remo-hit-prime-pair-20261118/composite_core.py
  - research/experiments/remo-hit-prime-pair-20261118/sievegen_core.py
  - research/experiments/remo-hit-prime-pair-20261118/output/hitpair_audit.json
date: 2026-11-18
tags: [remo, uniform-board, josephus, closed-form, prime, twin-prime, hardy-littlewood, machine-evidence]
---

## 主張（定理群は紙上全称証明。K0949 SIMPLE-CHARを素数判定へ崩壊させる）

K0949 SIMPLE-CHARの3条件（M素数∧k_T=M∧k_{T−1}<M∧spf(Y)≥M）を更に還元し、
値1軌跡を**線形形式の素数性と単一約数範囲判定**に完全還元する。
記法はK0946/K0949と同一（κ=K mod (M+1)・s=⌊(K−M−1)/(M+1)⌋・Y=K+1・
k₀=M(s+1)+κ−1・main regime: κ∈[0,M−2], (s,κ)≠(0,0)）。

### 補題SQ（全称）: main regimeで Y ≤ k₀²。

s≥1は M²v²−(M+1)v−M+1≥0（v=s+1≥2・M≥2）で増加、s=0はκ≥1で
Y≤2M≤M²≤k₀²。

### 補題Y-FACTOR（全称）: main regime・M素数で
(c) spf(Y)≥M ∧ (a) MYの(M,k₀]内約数なし ⟺ **[Y素数 ∨ Y=M²]**。

合成YかつM∤Yなら spf(Y)>M かつ spf(Y)≤√Y≤k₀（SQ）で(a)不成立。
M|YならY=Mq・q>M（q=MはY=M²）に対し q≤k₀（M·k₀−Y=(M²−M−1)(s+1)+(M−1)κ−(M+1)≥1、
M=2はu≥3で同値）で(a)不成立。Y素数とY=M²（κ=0・u=M−1）のみが通過。

### 定理HIT-ARITH（全称・値1判定の最終形）: main regime・M素数で
**σ_Z(M,K)=1 ⟺ [K+1素数 ∨ K+1=M²] ∧ [M(K+1)−1が[M,k₀]内に約数を持たない]**。
K0949 PARITY（κ奇）はここに包含（Y偶⟹合成⟹≠M²）。

### 補題P-KILL（全称・剰余死刑令）: M≥3素数・p素数・p|M+1 なら
**κ ≡ p−1 (mod p) ⟹ σ_Z(M,K)≠1**（p | Y=(M+1)(s+1)+κ+1 でspf(Y)≤p<M）。
p=2がK0949 PARITY。

### 系DIV-LAW-35（全称・K0946有限観察のM∈{2,3,5}側昇格）:
素数M∈{2,3,5}のmain regimeヒットは全てκ=0、すなわち**(M+1)|K**。
（dead κ集合が[0,M−2]∖{0}をちょうど覆うのはM=2,3,5に限る。M≥7は
live剰余が非空で、K0946出版の最初の非整除ヒット（M=7→K=10等）は
全てlive剰余に一致。）

### 定理K0-FAMILY（全称・κ=0族の完全判定）: M素数・u≥2:
**σ_Z(M,(M+1)u)=1 ⟺ [(M+1)u+1素数 ∨ u=M−1] ∧ ρ(M,u)**、
ρ(M,u) ⟺ M((M+1)u+1)−1が[M,Mu−1]内に約数を持たない。

### 定理M-SQ（全称）: M≥3素数: **σ_Z(M,M²−1)=1 ⟺ M²+M+1素数**
（W合成なら (M−1)spf(W) が[M,k₀]内の約数、W素数なら約数なし。
ヒットM=3,5,17,41,59,71,89,101,131,167,173…・M=7,11,13,19,23は不成立。
K0946の「M=17・K=288ヒット」の機構確定）。

### 定理PAIR-2（全称・M=2の値1軌跡の完全閉形式）:
**σ_Z(2,3u)=1 (u≥2) ⟺ 3u+1と6u+1がともに素数**。
全体軌跡（K>2）: {3} ∪ {3u : u≥2, 3u+1,6u+1素数}
（ρ節は√(6u+1)≤2u−1で6u+1素性に坍縮）。

### 定理PAIR-3（全称・M=3の値1軌跡の完全閉形式）:
**σ_Z(3,4u)=1 (u≥1) ⟺ (4u+1と6u+1がともに素数) ∨ u=2**
（MY−1=12u+2=2(6u+1)の約数構造でρ節が6u+1素性に坍縮、u=2はY=9=M²例外。
K0945のU_all 3,658要素とu≤10⁵で**集合として完全一致**）。

K0946次課題5（値1位置の分布則）はM=2,3で**双子素数型の同時素数条件**へ
完全還元され閉じ、密度の漸近はHardy–Littlewood型予想に帰着
（**予想**・未証明）:
U₂(N)~SS₂∫du/(ln3u·ln6u)（SS₂=3.96097…）・
U₃(N)~SS₃∫du/(ln4u·ln6u)（SS₃=5.28130…）。
実測/予想比は M=3: 0.9332(10⁴)→0.9848(10⁵)→**0.9967(10⁶)**、
M=2: 1.0127→0.9891→0.9864→**0.9924(333333)** と1へ収束傾向。
K0945の「冪減衰u^{−0.23}」は1/ln²u減衰のfitting産物（fitting窓で係数が
2/ln(u_eff)=0.32→0.15 と追跡する冪則ふうの見かけ）と説明（観察）。
K0946次課題4（一般MのU_M）はK0-FAMILY式+U_M掃引データ（M∈{2,3,5,7,11,13}:
1,164/1,145/1,064/541/756/327）で部分進展。一般Mの密度閉形式はOPEN。

## 機械的証拠（audit_build.py・output/hitpair_audit.json・all_ok=true）

pinned cores（K0948/K0949と同一sha）・入力ピンK0949 relay_audit.json・
K0945 deep_census.json。**cold 2回実行byte同一
（監査sha256 ac5eed8d36ebf016a339a597e74f3aac41493b5ab714d868fdbd719122762673）**:

- **ARITH-GRID**: engine σ_Z vs arith_hit: M∈[2,30]×K∈(M,1500]全43,036対
  （K0949 VOCEと同一領域）: **不一致0・ヒット656==VOCE錨**。
- **SP-REG**: 特殊K=M+1式 M∈[2,200]: 不一致0。
- **PAIR-ENGINE**: engine vs PAIR-2/PAIR-3（u≤2,000・268ヒット）: 不一致0・
  K0-FAMILY式との相互照合不一致0・M=2の奇数uヒット0。
- **K0-FAM**: engine vs K0-FAMILY式 M∈{5,7,11,13,17}×u∈[2,400]（262ヒット）:
  不一致0・arith_hit相互照合不一致0。
- **MSQ**: engine vs [M²+M+1素数] M∈[3,200]（合成M込み）: 不一致0。
- **CENSUS-REPRO**: HIT-ARITH掃引K≤2×10⁵: main regimeヒット
  M=3:2057・5:2005・7:2603・11:3003・13:3220・17:3475・19:3629・23:3739
  （**K0949 CENSPRIME表と全値一致・計23,731**）・M=2 main 2,024==PARITY錨
  （K=3特殊込み2,025・奇数ヒット{3}）。
- **DEEP3**: PAIR-3掃引u≤10⁵がK0945 U_allと**集合・バケット完全一致**
  （3,658）、u≤10⁶拡張25,860。**DEEP2**: PAIR-2掃引u≤66,666で2,024==
  PARITY錨・u≤333,333で7,750・奇数uヒット0。M=2,3のU_Mは約数走査式と
  独立AP篩で完全一致（1164==1164・1145==1145）。
- **PKILL**: 素数M∈[3,61]のdead κ集合で、K≤2×10⁵ census全ヒット・
  engine K≤1,200ともにdead剰余ヒット0。
- **SPECTRUM**: κ別分布（K≤2×10⁵）: 全8素数Mで**live κ集合が
  [0,M−2]∖dead(M)とちょうど一致**（M=7:{0,2,4}・11:{0,4,6}・
  13:{0,2,4,8,10}・17:{0,4,6,10,12}・19:7剰余・23:7剰余。
  P-KILLの逆方向・live剰余の無限性は予想P-KILL-TIGHTとして未証明）。
- 深部spot（監査外）: engineがK≈4×10⁵・10⁶点でPAIR-2/3予言に一致、
  σ_Z(173,29928)=1・σ_Z(199,39600)=0。

## 範囲と限界

- 一様盤・K0928定理RED経由の設定のみ。**11×11空盤・二石root {49,60}/{59,60}・
  S2 {59,60}・class1/2/4には一切言及しない（UNKNOWN不変）**。
- 定理群は紙上全称証明つき（K0946/K0948/K0949出版定理の組立）。
  機械検証は有限アンカーで全称性の根拠は紙上証明のみ。
- HL型密度漸近・P-KILL-TIGHT・「冪減衰=1/ln²fitting産物」は**観察・予想**
  （双子素数予想クラス・未証明）。一般M（M≥5）のU_M密度閉形式はOPEN。
- `uv run check/build`・unittestは本環境にcloneとuvがないため未実施
  （歴代remo項目と同じ扱い）。generated/とroot READMEは未編集。
