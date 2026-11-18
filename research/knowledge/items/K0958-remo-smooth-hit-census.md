---
id: K0958
title: smoothヒットの算術補題S3・S3'・EXCLUSIVE・YSQRとM≤2000完全センサス（CENSUS-FULL・CENSUS-STRIP）
kind: proposition
status: proved
topics: [residual-games, statistics, verification]
aliases: [S3, S3PRIME, EXCLUSIVE-SMOOTH, YSQR, CENSUS-FULL, CENSUS-STRIP, SIEVE-WALK]
relations:
  - type: depends_on
    target: K0950
    note: HIT-ARITH（main regime σ_Z=1 ⟺ [Y ok]∧窓空）を候補判定に使う
  - type: depends_on
    target: K0956
    note: HIT-GAP補窓論法・SPLIT/SEAM・FIRSTHIT/T1-CHANNEL出版データ・ピン済み5 core（prehit bf8ed817…・composite 3990d67f…・sievegen a69f916c…・branch_density 34b4ff15…・hitpair 0237aa1b…）を使う
  - type: generalizes
    target: K0956
    note: SPLITの排他性をhit仮定・レジーム・C|dなしの純算術恒不等式（EXCLUSIVE）へ置換え、smooth側の窓検査をΩ≤3で除去する（S3'）
  - type: connects
    target: K0952
    note: 枝形式（d≤M−1・N/d素数）とsmoothの排他がN>(M−1)²だけから従うことを純粋化する
artifacts:
  - path: research/experiments/remo-smooth-hit-census-20261118/report.md
    role: proof
    note: S3/S3'/EXCLUSIVE/YSQRの全称証明とセンサス完全性論証の正本
  - path: research/experiments/remo-smooth-hit-census-20261118/smooth_core.py
    role: verifier
    note: sieve-walk（Y≡M⁻¹ mod p類歩行・p冪割り切り）・窓DFS・候補分類の中核実装
  - path: research/experiments/remo-smooth-hit-census-20261118/audit_build.py
    role: verifier
    note: CENSUS-FULL/STRIP・crosscheck・engine錨・population統計の統合監査builder
  - path: research/experiments/remo-smooth-hit-census-20261118/prehit_core.py
    role: verifier
    note: K0956ピン（sha256 bf8ed817…一致）
  - path: research/experiments/remo-smooth-hit-census-20261118/composite_core.py
    role: verifier
    note: K0950/K0956ピン（sha256 3990d67f…一致）
  - path: research/experiments/remo-smooth-hit-census-20261118/sievegen_core.py
    role: verifier
    note: K0950/K0956ピン（sha256 a69f916c…一致）
  - path: research/experiments/remo-smooth-hit-census-20261118/branch_density_core.py
    role: verifier
    note: K0954/K0956ピン（sha256 34b4ff15…一致）
  - path: research/experiments/remo-smooth-hit-census-20261118/hitpair_core.py
    role: verifier
    note: K0950/K0956ピン（sha256 0237aa1b…一致）
  - path: research/experiments/remo-smooth-hit-census-20261118/output/audit.json
    role: data
    note: 集計・全検査・K0956照合・ピン（sha256 df61d25f…）
  - path: research/experiments/remo-smooth-hit-census-20261118/output/hits_full.json
    role: data
    note: M≤1000全2,609 hit行 [M,κ,t,K,Y,N,Ω,ω,is_branch_and_smooth]（sha256 4d2243ea…）
  - path: research/experiments/remo-smooth-hit-census-20261118/output/hits_strip.json
    role: data
    note: 1000<M≤2000・t≤60の7,441 hit行（sha256 80d176b7…）
  - path: research/log/2026-11-18-remo-smooth-hit-census.md
    role: log
    note: 発見順・機械結果の要約・次課題
date: 2026-11-18
---

## 命題・範囲

記法はK0956と同一。M素数・main regime K=(M+1)t+κ・t≥1・0≤κ≤M−2・(t,κ)≠(1,0)。
Y=K+1・k₀=Mt+κ−1・N=MY−1・C=gcd(M+1,κ+2)。「窓」は約数区間[M,k₀]。
Ω(N)は重複度込み素因数個数、(M−1)-smoothは全素因数≤M−1、
「ヒット」とはσ_Z(M,K)=1、[Y ok]とは「Y素数∨Y=M²」。

- **S3（全称）**: Nが(M−1)-smooth∧Ω(N)≤3 ⟹ Nの√N以下の約数はすべて≤M−1。
- **S3'（全称）**: main regime・[Y ok]・Nが(M−1)-smooth・Ω(N)≤3 ⟹ σ_Z(M,K)=1。
  窓検査もk₀≥√Nレジーム仮定も不要。
- **EXCLUSIVE（全称）**: Nが(M−1)-smoothなら、Nは枝約数（d≤M−1・N/d素数）を持ちえない。
  よってSPLIT二分法BRANCH/SMOOTHは全域で排他で、smoothヒットは常にsmooth-only。
  K0956のSPLIT排他性（hit前提・レジーム・C|dを使う議論）からこれら3前提を取り除いた
  純算術版である。
- **YSQR（全称）**: 素数MでY=M²となるsmoothヒットは存在しない。
  （Y=M²はt=M−1,κ=0の状態のみ。）
- **CENSUS-FULL（有限・決定的完全列挙）**: 素数5≤M≤1000（166素数・全t）の
  smoothヒットはちょうど2,609件（候補4,067,641・うち(M−1)-smooth 374,408・
  窓阻止371,799）。M=2,3はSEAM（K0956）によりsmooth不在。
- **CENSUS-STRIP（有限・決定的）**: 素数1000<M≤2000（135素数）のt≤60帯で
  7,441件（候補1,150,823・smooth 210,874・t=60境界到達20件。t>60のsmoothヒットは帯外）。

## 証明の要点

- **S3**: N=abc（a≤b≤c、各≤M−1）。√N以下の約数d∉{1,a,b}はab,ac,bc,cに限る。
  ac≤√N=√(abc)はac≤bを強制するがa≥2よりac≥2c≥2b>bで不可能。
  bc≤√Nはbc≤aを強制し矛盾。よってd∈{ab,c}で、ab≤√Nならab≤c≤M−1、
  cは素因数ゆえ≤M−1。
- **S3'**: S3より√N以下の約数は全部<M。窓約数dがd>√N側にあれば
  N/d≤√Nは約数なのでN/d≤M−1、N=d(N/d)≤k₀(M−1)。一方
  N−(M+1)k₀=2M−κ>0（κ≤M−2・t非依存・HIT-GAPの核心不等式）より
  N>(M+1)k₀>k₀(M−1)で矛盾。窓は空でHIT-ARITHが適用される。
  補窓論法は2M>κのみを使いmain regime全域で有効。
- **EXCLUSIVE**: N/d=p素数∧N smoothならp≤M−1ゆえN=dp≤(M−1)²。
  main regimeではY≥M+2（等号は除外状態(t,κ)=(1,0)のみ）なので
  N=MY−1≥M(M+2)−1=(M−1)²+4M−2>(M−1)²で矛盾。
- **YSQR**: Y=M² ⟺ (t,κ)=(M−1,0)。N=M³−1=(M−1)(M²+M+1)。
  M²+M+1が(M−1)-smoothでなければNもそうでない。smoothなら
  素因数p≤M−1をもち、d=(M−1)pはM≤2M−2≤d・d≤(M−1)²≤M²−M−1=k₀
  （M≥2）を満たす窓約数で、状態はヒットでない。
- **センサス完全性**: smoothヒットなら(i) HIT-ARITHで[Y ok]、(ii) YSQRでY素数、
  (iii) k₀≥√Nレジーム（M≥4では全t≥2）ではSPLIT+EXCLUSIVEによりヒットは
  smooth-onlyゆえN≤(M−1)³、t=1（M≥5）は直接N≤M(M+4)−1<(M−1)³。
  いずれにせよ候補は素数Y≤(M−1)³/Mかつ有効κ類の有限集合で、
  sieve-walk（各素数p≤M−1でY≡M⁻¹ (mod p)の類を歩きpの冪を割り切る。
  コスト候補あたりΣ1/p）が候補集合を同時に尽くす。逆に窓空候補はHIT-ARITHで
  ヒット。決定的で再実行はbyte同一（2回cold検証）。

## 現在の根拠と限界

- S3・S3'・EXCLUSIVE・YSQRは紙上全称証明（report.md・各3〜6行）。機械は有限アンカー。
- CENSUS-FULL/CENSUS-STRIPは決定的有限列挙（audit_build.py・2回cold実行でbyte同一）。
- 機械検査（全て0違反）: S3'違反0（smooth候補374,408+210,874のうち阻止側にΩ≤3は1件もない。
  Ω≤3のsmooth候補は全てヒット）・dead候補0（5.2M状態でP-KILL/Y素数相互作用の確認）・
  EXCLUSIVE重複0（全10,050 hit中branch∧smooth 0件）・SEAM違反0（全hitが
  t≤(M−1)(M−2)/(M+1)）・engine σ_Z照合 hit 288件/block 101件0失敗・
  YSQR機械確認（301素数中62がM³−1 (M−1)-smooth・その0個がhit）。
- K0956出版データとの照合: 29 SPLIT-GRID smooth状態はfield単位で完全一致・
  97 t=1 smoothヒット一致・firsthit_rows 109 smooth行は全てセンサス内で同t・
  1,546 liveクラスの初回ヒット独立再計算0不一致・per-Mでcensus hit-class数≥
  出版n_smooth_first（等しいのは36/166・「smoothヒットは初回ヒットとは限らない」を確定）・
  strip帯はK0956の4,543 smooth-firstクラスをすべて含む（不足0）。
- 構造観察（有限・全称主張なし）: ヒットのΩは3が28+50件のみ（S3'は鋭いが被覆率は小さい）で
  最頻値Ω=4（1,237+3,571件）・最大Ω=16。2集団構造: (a) t=1（4,904件・Ω≥10の119件は
  すべてt=1・2^kに富む因数分解、例: M=647, N=532480=2¹³·5·13）、(b) t≥40（547件すべてが
  「奇素数ちょうど3個×2^{1,2}」（v₂=1: 522件・v₂=2: 25件）で奇素数はM/2近傍に集中、
  例: M=983, t=220, N=212977762=2·449·487²がセンサス最大t）。max t=220@M=983は
  seam bound 979の22.5%で、全域でN≤0.225(M−1)³。per-M hit数の平均は
  1.4/5.9/14.4/28.5（M∈(2,100]/(100,300]/(300,600]/(600,1000]）≈M/25。
  複数smoothヒットをもつクラスは86（full）+366（strip）で、smoothヒットが
  クラスの初回ヒットであるとは限らない。
- 1000<M≤2000のt>60帯のsmoothヒットは未列挙（K0956のt_cap=7ln²(M+1)+100との
  関係はF=branch型（K0959）と矛盾しない）。smooth 2集団の機構（なぜt=1とt≥40に
  集中するか）はOPEN。
- 11×11空盤・二石root・標準有限盤には言及しない。uv check/buildは本環境にcloneとuvが
  なく未実施（歴代remo項目と同じ扱い）。generated/とroot READMEは未編集。
