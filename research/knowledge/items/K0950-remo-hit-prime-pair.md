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
  - research/experiments/remo-hit-prime-pair-20261118/pkill_tight_sweep.py
  - research/experiments/remo-hit-prime-pair-20261118/pkill_tight_deep.py
  - research/experiments/remo-hit-prime-pair-20261118/kappa_density.py
  - research/experiments/remo-hit-prime-pair-20261118/pkill_class_probe.py
  - research/experiments/remo-hit-prime-pair-20261118/output/pkill_tight_tier1_slim.json
  - research/experiments/remo-hit-prime-pair-20261118/output/pkill_tight_tier2.json
  - research/experiments/remo-hit-prime-pair-20261118/output/pkill_tight_tier3.json
  - research/experiments/remo-hit-prime-pair-20261118/output/pkill_tight_tier4_slim.json
  - research/experiments/remo-hit-prime-pair-20261118/output/pkill_tight_tier5_slim.json
  - research/experiments/remo-hit-prime-pair-20261118/output/kappa_density_slim.json
  - research/experiments/remo-hit-prime-pair-20261118/output/sparse_classes_le2.json
  - research/experiments/remo-hit-prime-pair-20261118/output/pkill_probe_deep.json
  - research/experiments/remo-hit-prime-pair-20261118/firsthit_growth.py
  - research/experiments/remo-hit-prime-pair-20261118/output/firsthit_growth.json
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

### 補題P-FACTOR（全称・フォローアップ）: M素数・p素数・p|M+1・κ ≡ p−2 (mod p) なら
**クラス内の全Yで p | MY−1**（M ≡ −1 (mod p)・κ ≡ −2 ⟹
Y=(M+1)(s+1)+κ+1 ≡ κ+1 ≡ −1 (mod p) ⟹ MY−1 ≡ (−1)(−1)−1 = 0）。

### 系WINDOW-RECURSION（全称・フォローアップ）: M素数・p | MY−1 なら
**[M,k₀]内約数dの存在 ⟺ (MY−1)/p が[M/p,k₀/p]内に約数を持つ**。
d=pd′対応は全射でd′∈[M/p,k₀/p]（M | MY−1よりd=Mは除外され、
d>M ⟹ d′>M/p・d≤k₀ ⟹ d′≤k₀/p、逆方向も同型）。κ ≡ p−2 (mod p)の
クラス判定はM/pスケールの同型な約数存在問題へ再帰縮約される
（Y-FACTORの(a)節がp−2型クラスでは1段小さいMで書き直せる）。

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

## フォローアップ掃引（同日・監査外の決定的実験・report.md §9参照）

監査JSON（sha ac5eed8d…・§1–8）の後に実施した追加掃引。
**全て同梱スクリプト（pkill_tight_sweep.py等）で再生成可能な
決定的実験**であり、監査shaには含まれない。

- **P-KILL-TIGHT掃引（反例なし）**: 素数M≤200（46個）×K≤10⁷・
  M≤1000（168個）×K≤2×10⁵・M≤2000（303個）×K≤2×10⁵で
  **live κ剰余クラスの反例は0件**（全クラスがK内に初回ヒットを持つ）。
  M≤200での初回ヒット位置の最大は14,896（M=181）。ただし**初回ヒットは
  Mと共に増大傾向**で、固定K検査では不十分なクラスが出始める:
  M≤2000×K≤2×10⁵で2クラスのみ未達（(1367,κ=682)・(1741,κ=648)）だが、
  K≤10⁷拡張で**それぞれ215,458・220,140に初回ヒットが存在**。
  結論: P-KILL-TIGHTへの反例は見つかっていないが、
  「初回ヒットの遅さはMと共に増える」ため固定Kの反例探索には
  KをMの関数として取る必要がある（観察）。
- **κ密度と疎尾部（SPARSE-TAIL・有限観察）**: M≤2000・103,183 live κクラス中、
  p−2型（P-FACTOR該当）は28.6%。平均ヒット数はp−2型22.2 vs 非p−2型21.8
  （有意差なし）だが**極端な疎尾部はp−2型に濃縮**（cnt≤2の69クラス中48=69.6%・
  cnt=1の10クラス中8=80%がp−2型）。最稀クラス(991,κ=494)はK≤10⁷で
  117ヒット（通常クラスの約1/4.6）・殺し約数は[M,2M]帯に集中。
  cnt=1クラスの深部プローブ（(1231,614)=120・(1723,860)=69・(1783,772)=284ヒット・
  K≤10⁷）は全て健全（P-KILL-TIGHTと整合）。
- **engine追加照合**: M∈{29,31,37,41,43,47,53}×K≤2500で
  arith_hitとengine σ_Zが不一致0（ARITH-GRIDのM拡張）・
  M∈{419,991,997}×K∈(M,M+400]でも不一致0。
- **FIRSTHIT-GROWTH（有限観察・firsthit_growth.py）**: F(M)=live κクラスの
  初回ヒット最大値が303素数（M≤2000）全てで確定。tier3完全データでは
  F ~ 1.767·M^1.509（R²=0.899）・モデル比較はA·M^1.509(0.899) >
  A·M·lnM(0.886) > A·M·ln²M(0.871・A₂≈0.96) > A·M(0.797)。
  **M≥100でF ≤ 6.2·M·ln²M・M≥1000でF ≤ 3.03·M·ln²M**（最大比3.02が
  遅いクラス(1367,682)=215,458そのもの）。実務則: K(M)=7·M·ln²Mで
  M≤2000全素数のtight検査に十分（固定K=2×10⁵の失敗M∈{1367,1741}と整合）。
  いずれも有限観察で、大きなMでのln²M因子分離はOPEN。

## 範囲と限界

- 一様盤・K0928定理RED経由の設定のみ。**11×11空盤・二石root {49,60}/{59,60}・
  S2 {59,60}・class1/2/4には一切言及しない（UNKNOWN不変）**。
- 定理群は紙上全称証明つき（K0946/K0948/K0949出版定理の組立）。
  機械検証は有限アンカーで全称性の根拠は紙上証明のみ。
- P-FACTOR・WINDOW-RECURSIONは紙上全称証明つき（フォローアップ）。
- 尾部t≥max(M,3)の約数窓はK0952でM-smooth小因子Dと有限e枝に全称分解。
  e=1の素数対は全live κで局所許容され、HL条件付きで各live κに無限ヒットを予測する。
  ただしP-KILL-TIGHTの無条件証明は依然未解決。
  P-KILL-TIGHT自体は**依然予想**（M≤2000×K≤10⁷級で反例なし・
  初回ヒットの増大傾向はF≤6.2·M·ln²M（M≥100・有限観察）と定量化）。
  疎尾部のp−2型濃縮とFIRSTHIT-GROWTHの冪則・包絡は有限観察。
- HL型密度漸近・「冪減衰=1/ln²fitting産物」は**観察・予想**
  （双子素数予想クラス・未証明）。一般M（M≥5）のU_M密度閉形式はOPEN。
- `uv run check/build`・unittestは本環境にcloneとuvがないため未実施
  （歴代remo項目と同じ扱い）。generated/とroot READMEは未編集。
