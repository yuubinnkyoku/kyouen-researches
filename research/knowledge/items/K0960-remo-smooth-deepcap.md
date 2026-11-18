---
id: K0960
title: smoothヒットのDEEP-CAP定理（t < M/4）・ODDCAP/MIN3/PAIR-MINとM≤2000全t完全センサス（CENSUS-STRIP2）
kind: proposition
status: proved
topics: [residual-games, statistics, verification]
aliases: [DEEP-CAP, ODDCAP, MIN3, PAIR-MIN, K3-A, CENSUS-STRIP2]
relations:
  - type: depends_on
    target: K0958
    note: センサス手法（sieve-walk・完全性論証Sec.5）・ピン済み6 core・出版hits_full/hits_strip（M≤1000全t・M≤2000 t≤60）を再利用し、t>60帯を含むM≤2000全tで行一致検証
  - type: depends_on
    target: K0949
    note: PARITY（素数MのヒットはK偶⇒Y奇⇒N偶・a=v₂(N)≥1）をODDCAPの前提に使う
  - type: depends_on
    target: K0956
    note: 記法・HIT-ARITH（窓空⟺σ_Z=1）・SPLIT/EXCLUSIVE（ヒットN≤(M−1)³の候補有限性）
  - type: generalizes
    target: K0956
    note: SEAM t≤(M−1)(M−2)/(M+1)≈Mをsmooth側（t≥2）でt<M/4（素数M≥17）に4倍改良
artifacts:
  - path: research/experiments/remo-smooth-hit-deepcap-20261118/report.md
    role: proof
    note: ODDCAP/MIN3/DEEP-CAP/PAIR-MIN/K3-Aの全称証明とCENSUS-STRIP2完全化の正本
  - path: research/experiments/remo-smooth-hit-deepcap-20261118/census_full2000.py
    role: verifier
    note: 全tチェックポイントcensusドライバ（census_walk2・K0958 smooth_core.census_walkとM=1009,1783,1999で同値検証）
  - path: research/experiments/remo-smooth-hit-deepcap-20261118/audit_build.py
    role: verifier
    note: DEEP-CAP 6述語全数検証・engine錨・行照合・決定性監査の統合builder（resumable）
  - path: research/experiments/remo-smooth-hit-deepcap-20261118/smooth_core.py
    role: verifier
    note: K0958ピン（sha256 928c54ca…一致）
  - path: research/experiments/remo-smooth-hit-deepcap-20261118/prehit_core.py
    role: verifier
    note: K0956ピン（sha256 bf8ed817…一致）
  - path: research/experiments/remo-smooth-hit-deepcap-20261118/composite_core.py
    role: verifier
    note: K0950/K0956ピン（sha256 3990d67f…一致）
  - path: research/experiments/remo-smooth-hit-deepcap-20261118/sievegen_core.py
    role: verifier
    note: K0950/K0956ピン（sha256 a69f916c…一致）
  - path: research/experiments/remo-smooth-hit-deepcap-20261118/branch_density_core.py
    role: verifier
    note: K0954/K0956ピン（sha256 34b4ff15…一致）
  - path: research/experiments/remo-smooth-hit-deepcap-20261118/hitpair_core.py
    role: verifier
    note: K0950/K0956ピン（sha256 0237aa1b…一致）
  - path: research/experiments/remo-smooth-hit-deepcap-20261118/output/audit.json
    role: data
    note: 集計・全検査・per_M 135エントリ・ピン（sha256 4cd64fe4…）
  - path: research/experiments/remo-smooth-hit-deepcap-20261118/output/hits_strip2.json
    role: data
    note: M≤2000全t完全smoothヒット8,277行 [M,κ,t,Ω,ω,branch]・t≤60帯はK0958出版と行完全一致（sha256 784ca43c…）
  - path: research/experiments/remo-smooth-hit-deepcap-20261118/output/hits_deep_band.json
    role: data
    note: t>60帯836行・拡張field（v₂・k_odd・max_odd_prime・top_odd_pair）（sha256 1cc020b2…）
  - path: research/log/2026-11-18-remo-smooth-hit-deepcap.md
    role: log
    note: 発見順・機械結果の要約・次課題
date: 2026-11-18
---

## 命題・範囲

記法はK0956/K0958と同一（M素数・main regime K=(M+1)t+κ・t≥2・0≤κ≤M−2・
Y=K+1・k₀=Mt+κ−1・N=MY−1・窓=約数区間[M,k₀]）。対象は
「smoothヒット」= Nが(M−1)-smoothかつ窓空（HIT-ARITHでσ_Z=1・[Y ok]はYSQRで自動）。

- **ODDCAP（全称）**: a=v₂(N)≥1（K0949 PARITY）のとき、Nの各奇素因数pは
  p ≤ (M−1)/2^a。
- **MIN3（全称）**: Ω(Nの奇部分) ≥ 3。
- **DEEP-CAP（全称）**: t < max(√M, ((M−1)²+4)/(4M))。特に素数M≥17では
  **smoothヒットのt < M/4**（K0956 SEAM ≈ Mのsmooth側4倍改良）。
- **PAIR-MIN（全称）**: k₀ < min{pᵢpⱼ（重複込み組）: pᵢpⱼ ≥ M}
  （窓空性から全ペア積≥Mがk₀を超える。case Aのtop pair境界の強化で、
  実測ではtop pair境界の最大1/3まで改良する）。
- **K3-A（全称）**: kodd=3のsmoothヒットは全てcase A（top pair ≥ M）。
- **CENSUS-STRIP2（有限・決定的完全列挙）**: 素数1000<M≤2000（135素数）全tの
  smoothヒットはちょうど8,277件（候補22,653,112・smooth候補1,924,193・窓阻止
  1,915,916・t>60帯836件）。t≤60帯7,441行はK0958出版hits_strip.jsonと行完全一致
  （mismatch 0）。K0958の「t>60帯は未列挙」を解消しM≤2000を全tで完成。

## 証明の要点（report.md正本・各3〜8行）

- **ODDCAP**: 2^i p（i≤a）は約数。「2^i p ≥ M の最小i₀」が存在すれば
  2^{i₀}p ≥ M ⇒ > k₀（窓空）と 2^{i₀}p ≤ 2·(M−1) ≤ k₀（t≥2）が矛盾。
  smooth性からp<Mでi₀≥1。ゆえ全i≤aで2^i p ≤ M−1。
- **MIN3**: Ω(odd)≤2ならodd ≤ maxodd² ≤ ((M−1)/2^a)²で
  N ≤ (M−1)²/2^a ≤ (M−1)²/2 < 2M²+3M−1 ≤ N（t≥2でY≥2M+3）で矛盾。
- **DEEP-CAP case A（top pair ≥ M）**: top pair > k₀ かつ
  top pair ≤ ((M−1)/2^a)² ≤ (M−1)²/4 より t < (((M−1)/2)²+1)/M < M/4（M≥3）。
- **DEEP-CAP case B（top pair < M）**: N_odd < Mなら2^i N_odd（i≤a）が
  [M, 2M−2] ⊆ 窓に落ち矛盾するのでN_odd ≥ M。上方部分積鎖d_j=p_k···p_{k−j+1}の
  M初超えd_{j*}（j*≥3）は > k₀ かつ < M·p_{k−1} < M√M（p_{k−1}²≤top pair<M）で
  t < √M。
- **K3-A**: case BではN = 2^a·p₁·(top pair) ≤ (M−1)² < N で矛盾。
- **PAIR-MIN**: 各pᵢpⱼは約数で窓を跨げない。証明は窓空性そのもの（自明）で、
  内容はODDCAPと組み合わせたmin-pairの上界評価にある。

## 現在の根拠と限界

- ODDCAP・MIN3・DEEP-CAP・PAIR-MIN・K3-Aは紙上全称証明（report.md）。
  機械は有限アンカー: deep hit（t≥2）5,982件 = strip2 4,844 + K0958出版M≤1000の
  1,138件で6述語（oddcap/min3/case/deepcap/t<M/4/pairmin）をN独立再因数分解で
  全数検査し違反0。kodd=3 case B 0件。
- CENSUS-STRIP2は決定的有限列挙（audit_build.py）。census冷再実行で135チェック
  ポイントbyte同一、engine錨込みの冷二重実行で出力byte同一（sha256ピン）。
  engine σ_Z照合: t>60全836件+149刻み54件=890件全て1・blockedサンプル278件
  全て≠1（0失敗）。S3'違反0・dead候補0・EXCLUSIVE重複0/8,277・SEAM違反0・
  YSQR新帯（31/135 smooth・0 hit）。
- 構造観察（有限・全称主張なし）: t>60帯836件は全件kodd=3・v₂∈{1,2}で3奇素数は
  すべてM/2近傍（p₁最小149）。ODDCAP飽和2件（maxodd=(M−1)/2^aちょうど）。
  PAIR-MIN近接: t·M/min-pair中央値0.8835・最大0.9973（M=1997, t=121,
  N=2·337·719·997・k₀=241,816 vs pairmin 242,303）。max t=427@M=1789
  （N=2·881³・t/M=0.2387=M/4境界の95.5%）。case Bは5,982件中3件のみ
  （757 t=2・773 t=2・1097 t=3・いずれもkodd≥5・小素数冪構造）でt>60帯に0件。
  t=1集団3,433件（Ω最大16・Ω≥10は87件すべてt=1）。複数smoothヒット484クラス。
- これらの構造観察から、t≥40集団の機構は「窓回避の階梯が全ペア積に課す制約
  （PAIR-MIN）+ ODDCAP飽和」として算術的に説明される（K0958のOPEN「2集団の
  機構」に対する観察ベースの回答・全称定式化は次課題）。
- branch型ヒット・F(M)にはDEEP-CAP不適用（初回ヒット93.8%はbranch型・K0956不変）。
  M>2000延伸・PAIR-MIN近接分布の理論・EV増幅（K0959）の定量モデル化は次課題。
- 11×11空盤・二石rootには言及しない。uv check/buildは本環境にcloneとuvがなく
  未実施（歴代remo項目と同じ扱い）。generated/とroot READMEは未編集。
