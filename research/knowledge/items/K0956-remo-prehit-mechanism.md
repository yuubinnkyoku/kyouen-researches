---
id: K0956
title: pre-tailヒット機構の全称HIT-GAP・SPLIT・SEAMとM≤2000決定的監査（HIT-GAP・SPLIT・SEAM・GAP-GRID・SPLIT-GRID）
kind: proposition
status: proved
topics: [residual-games, statistics, verification]
aliases: [HIT-GAP, SPLIT, SEAM, GAP-GRID, SPLIT-GRID, T1-CHANNEL, FIRSTHIT-M2000, BH-FROM-START-FIX]
relations:
  - type: depends_on
    target: K0950
    note: HIT-ARITH・P-KILL・tier3/FIRSTHIT-GROWTHデータ・pkill_tight_tier3ピンを使う
  - type: depends_on
    target: K0952
    note: 枝分解（Ce<M・e|Q・Q/e素数）とシームt0=max(M,3)の記法を使う
  - type: depends_on
    target: K0954
    note: from-start BHモデルの定義とfirsthit_pred 1,546行ピンを使い、t_hat発散欠陥を修正する
  - type: generalizes
    target: K0952
    note: シーム境界max(M,3)をM−3（M≥7）へ改良し枝特徴付けの成立域を拡大する
  - type: connects
    target: K0946
    note: FIRSTHIT-GROWTHの冪則をpre-tailレジームの有限観察として接続する
artifacts:
  - path: research/experiments/remo-prehit-mechanism-20261118/report.md
    role: proof
    note: 全称証明（HIT-GAP・SPLIT・SEAM）と機械結果の正本
  - path: research/experiments/remo-prehit-mechanism-20261118/prehit_core.py
    role: verifier
    note: sieve_flags・factorize・window_empty・hit_gap_pred・branch_divisor・analyze_state・scan_first_hit・修正BH（_int_range・branch_n_min・bh_expected_from_start・first_hit_tstar）の中核実装
  - path: research/experiments/remo-prehit-mechanism-20261118/audit_build.py
    role: verifier
    note: ENGINE-ANCHOR(GAP-GRID)/SPLIT-GRID/T1-CHANNEL/FIRSTHIT/FIRSTHIT-PRED(poisson_race+calibration)/RATE-PROFILE/SMOOTH-LAW統合監査
  - path: research/experiments/remo-prehit-mechanism-20261118/composite_core.py
    role: verifier
    note: K0950ピン（sha 3990d67f…一致）
  - path: research/experiments/remo-prehit-mechanism-20261118/sievegen_core.py
    role: verifier
    note: K0950ピン（sha a69f916c…一致）
  - path: research/experiments/remo-prehit-mechanism-20261118/branch_density_core.py
    role: verifier
    note: K0954ピン（sha 34b4ff15…一致）
  - path: research/experiments/remo-prehit-mechanism-20261118/hitpair_core.py
    role: verifier
    note: K0950ピン（sha 0237aa1b…一致）
  - path: research/experiments/remo-prehit-mechanism-20261118/output/audit.json
    role: data
    note: 統合監査出力（firsthit_pred.json sha 71ab1734…・pkill_tight_tier3.json sha 146cefd1…のピンを含む）
  - path: research/experiments/remo-prehit-mechanism-20261118/output/firsthit_rows.json
    role: data
    note: M≤199 live 1,546クラスの初回ヒット行（修正t*・Λ*付き）
  - path: research/log/2026-11-18-remo-prehit-mechanism.md
    role: log
    note: 発見順・smoke失敗・binningバグ修正・諸数値
date: 2026-11-18
---

## 命題・範囲

記法はK0950/K0952と同一。M素数・main regime K=(M+1)t+κ・t≥1・0≤κ≤M−2・(t,κ)≠(1,0)。
Y=K+1・k₀=Mt+κ−1・N=MY−1・C=gcd(M+1,κ+2)。「窓」は約数区間[M,k₀]。D*(N)は√N以下の
最大約数（D*(1)=1）。ヒットとはσ_Z(M,K)=1。

- **HIT-GAP（全称）**: k₀≥√Nのとき σ_Z(M,K)=1 ⟺ [Y素数∨Y=M²] ∧ D*(N)<M。
  (⟸)は核心不等式 N−(M+1)k₀=2M−κ>0（κ≤M−2・t非依存）から N>(M+1)k₀>Mk₀ を使い、
  窓約数dがあれば N/d≤√N（d≥√Nゆえ）で約数なので N/d≤D*<M、よって N=d(N/d)<Mk₀<N
  で矛盾。(⟹)は窓空＋k₀≥√Nから√N以下の約数がすべてM未満。レジーム k₀≥√N は
  f(κ)=k₀²−N のκ単調性で [M≥4,t≥2]・[M=3,t≥3]・[M=3,t=2,κ≥1]・[M=2,t≥3] で全域成立、
  不成立は(3,2,0)とt=1小κとM=2,t=2のみ。(3,2,0)（Y=9=M²・N=26・D*=2）では
  レジーム外だがHIT-GAP自体は直接確認で成立。
- **SPLIT（全称・排他的二分法）**: 同レジームの全ヒットはちょうど一方を満たす。
  (i) BRANCH: Nが約数d≤M−1・C|d・N/d素数をもつ（K0952枝形式と厳密同値。d=Ceとおくと
  恒等式CA=M(M+1)・CB=M(κ+1)−1から e|Q ⟺ t≡t_e (mod e) が自動成立し追加条件不要）。
  (ii) SMOOTH: Nは(M−1)-smooth ∧ N≤(M−1)³。排他性: N>(M−1)²と P=N/d>k₀>M−1
  （branch側）から両立不可能。証明骨子: D*<M・B₁=N/D*>k₀>M+1≥C。B₁素数なら
  gcd論法（C|N・B₁>C素数ゆえ素因数はすべてD*側）でC|D*が確定しbranch。B₁合成なら
  B₁=uvでu≤√B₁≤√N→u≤M−1（窓）。v≤√Nなら3因子D*,u,v≤M−1でsmooth・N≤(M−1)³。
  v>√Nならv≤k₀は窓矛盾→v>k₀、このとき余因子m=N/v<N/k₀<M+1でM∤Nゆえm≤M−1。
  v素数ならgcd論法でC|mがbranch、v合成ならu₂≤√v≤√N→u₂≤M−1でv₂=v/u₂について
  同様の場合分け（v₂≤√N→m,u₂,v₂の3因子smooth・v₂>k₀→再帰、vは厳密減少で終止）。
- **SEAM（全称）**: smooth側は N≥M(M+1)t+M−1 と N≤(M−1)³ から
  t≤(M−1)(M−2)/(M+1) < M−3（M≥7）・M=5はt≤2・M=3とM=2はsmooth不在。
  K0952のシーム max(M,3) を M−3 へ改良。系: M≥7でt≥M−3の全ヒットはBRANCH型
  （枝特徴付けの成立域がテール全域へ拡大）、M=3はPAIR-3と整合、M=2も全ヒットBRANCH。
- **GAP-GRID（有限）**: engine σ_Z==1 vs 生窓述語 vs HIT-GAP の3-way一致が
  30,502状態（素数M≤61×t≤50・M≤23×t∈[51,120]・全κ・dead込み・K≤7440）で不一致0。
  K0950のengine錨（K≤1500）をK≤7440へ拡大。生窓ヒット1,460+280。
- **SPLIT-GRID（有限）**: 素数M≤199・live κ・t∈[2,M−2]の24,763ヒット=24,734 branch+
  29 smooth-only。SPLIT違反0・SEAM解析境界（t≤(M−1)(M−2)/(M+1)）違反0・nonliveヒット0
  （P-KILL定理と整合）。smooth実例: M=61,κ=6,t=8: N=30682=2·23²·29・D*=58（窓[61,493]空）。
  センサス最大N=428446（M=199,κ=152,t=10）≪198³。29状態は全てaudit.json smooth_law.per_Mに記録。
- **T1-CHANNEL（有限）**: t=1ヒット532件（素数M≤199・live 741クラス）は全て
  Y(1)=M+κ+2素数を要求（Y(1)素数はliveの72%、うち209クラスは窓約数で阻止）。
  435 branch・97 smooth。
- **FIRSTHIT-M2000（有限）**: 素数M≤2000（303素数・103,185 liveクラス）・
  t_cap=7ln²(M+1)+100で全クラスヒット（n_nohit=0・初回ヒットは本物）。初回ヒット型は
  branch 96,837（93.8%）・smooth 6,348（6.1%）。F(M)（最悪初回ヒット）は全Mでbranch型。
  tier3 first/max_first_K・firsthit_pred 1,546行はK0950/K0954と0不一致。
  F-fit: M≤199の46点で F~1.767·M^1.5088（R²=0.8991）とK0950出版値1.767·M^1.509と
  完全一致。M≤2000の303点では F~2.977·M^1.3861（R²=0.9249）、M∈[200,2000]では
  指数1.280（R²=0.745）に平坦化（遠域でM^1.5より遅い成長の有限観察）。
- **BH-FROM-START-FIX（BH条件付きheuristic）**: K0954のt_hat発散（pair_integralが
  n=0近傍で発散・κ=0,e=1枝はc1=1・Simpson格子依存で非単調）の原因を特定し、定義域を
  枝ごとに修正: n_min(e)=2（e=1,t_e=0,κ=0・特殊状態K=M+1は除外）/1（t_e=0他）/0（t_e≥1）、
  各整数nはbin[n,n+1)で積分。修正モデルは単調・有限で二分探索が有効。
  pooled Spearman(t*, t_first)=0.1614（旧t_hat 0.0758）・within-M平均0.0087
  （順序はノイズ支配・K0954の否定結果を維持）。キャリブレーション: t_first≥2の
  1,014クラスで median Λ*(t_first)=0.755 ≈ ln2=0.693（Poisson競争の理論値）で
  分布レベルの較正が成立。RATE-PROFILE（M∈{7,13,23,53,101,199}のper-tセンサス）の
  BH比はM=23で0.88-1.01・M=199で1.2-1.35。

## 証明の要点

恒等式 N−(M+1)k₀=2M−κ>0 と C≤M+1<k₀ の2つが全証明を貫く。HIT-GAP(⟸)は
「√N以下の約数はD*以下」というD*の定義を2回使う（d>M側とN/d側の対称性）。
SPLITはD*の最大性からB₁=N/D*>k₀（B₁≤k₀なら窓約数）を出発点とし、
「k₀超の約数vの余因子は m=N/v<N/k₀<M+1 かつ M∤N ゆえ m≤M−1」と
「C|N・v>C素数 ⟹ C|(N/v)」のgcd論法を再帰的に適用する。再帰は大因子が
毎回2分の1以下になることで終止し、終端は必ず（大因子素数ならbranch・
第3因子が√N以下なら3因子smooth）のいずれか。SEAMはsmooth側のNの下界
（κ=0で最小 N=M(M+1)t+M−1）と上界(M−1)³の比較のみ。全証明はreport.md。

## 現在の根拠と限界

- HIT-GAP・SPLIT・SEAMは紙上全称証明（report.md）。機械グリッドは有限アンカーであり
  全称性の根拠は証明本文のみ。
- GAP-GRID/SPLIT-GRID/T1-CHANNEL/FIRSTHIT-M2000/SMOOTH-LAWは決定的有限列挙
  （audit_build.py・2回cold実行でbyte同一・out/out2照合済み）。
- BH-FROM-START-FIX・RATE-PROFILEはBH予想条件付きのheuristic。Λ* median≈ln2の
  較正は有限観察でHLの証拠ではない。within-M順序予測の否定（K0954）は維持。
- firsthit_pred.json（K0954 output・sha 71ab1734…）とpkill_tight_tier3.json
  （K0950 output・sha 146cefd1…）はshaピンで参照（実験dirへの再コピーなし・
  原本は出版実験dirに現存）。
- Fの遠域平坦化（1.386→1.280）の機構・F/(M ln²M)の真の漸近形はOPEN。
  smooth-onlyヒットの t≪解析上限 への集中（M=199でmax t=10・上限195）も未説明。
- 11×11空盤・二石root・標準有限盤には言及しない。uv check/buildは本環境にcloneとuvが
  なく未実施（歴代remo項目と同じ扱い）。generated/とroot READMEは未編集。
