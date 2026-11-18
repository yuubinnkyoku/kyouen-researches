# 2026-11-18 remo-smooth-hit-census（K0958）作業ログ

目的: K0956のSPLIT/SEAMが残した「smooth-onlyヒットの集中構造」を、smooth側の
算術補題（S3・S3'・EXCLUSIVE・YSQR）とM≤2000の決定的完全センサスで確定する。

## 発見順

1. **S3の発見**: smooth候補の因数分解を眺めていて「Ω≤3なら√N以下の約数は
   すべて≤M−1」に気づく。3因子N=abcの√N以下の約数は{1,a,b,ab,c}に限る
   （ac・bcは√N超えを示唆に排除）という初等的列挙で即証明。
2. **S3'の組み立て**: S3とHIT-GAPの補窓論法（d>√NならN/d≤M−1で
   N≤k₀(M−1)<(M+1)k₀<N・核心不等式N−(M+1)k₀=2M−κ>0はt非依存）を
   接続すると、main regime・[Y ok]・smooth・Ω≤3が窓検査なしでヒットを
   保証することが分かる。レジーム仮定（k₀≥√N）も不要。
3. **EXCLUSIVEの純算術化**: K0956のSPLIT証明内の排他性議論（branch側
   P=N/d>k₀>M−1）をhit仮定・レジーム・C|dから切り離せることに気づく。
   smoothなNでN/d=p≤M−1ならN≤(M−1)²だが、main regimeでは
   N=MY−1≥M(M+2)−1>(M−1)²。2行の恒不等式。
4. **YSQR**: Y=M²状態（t=M−1,κ=0）のN=M³−1=(M−1)(M²+M+1)は、
   M²+M+1がsmoothなら必ず窓約数(M−1)pをもつのでヒットにならない。
   [Y ok]のM²側がsmoothヒットに寄与しないことを全称で排除。
5. **センサス完全性の設計**: SPLIT+EXCLUSIVEによりsmoothヒットは
   smooth-onlyゆえN≤(M−1)³（t=1は直接評価で同じ上界）。候補は
   素数Y≤(M−1)³/Mの有限集合。各p≤M−1でY≡M⁻¹ (mod p)の類を歩く
   sieve-walkで全候補のp冪割り切りが同時に走る（コストΣ1/p/候補）。
6. **CENSUS-FULL実行**: 素数5≤M≤1000（166素数・全t）でsmoothヒット
   2,609件を完全列挙（候補4,067,641・smooth 374,408・窓阻止371,799）。
   S3'違反0（阻止候補はすべてΩ≥4）・dead候補0・EXCLUSIVE重複0・SEAM違反0。
7. **CENSUS-STRIP**: 1000<M≤2000・t≤60帯で7,441件（t=60境界到達20件）。
   K0956の4,543 smooth-firstクラスはすべて帯内。
8. **K0956出版データとの全照合**: 29 SPLIT-GRID状態・97 t=1 smooth・
   firsthit 109 smooth行・1,546クラス初回ヒット再計算が0不一致。
   per-Mでcensus hit-class数≥n_smooth_first（等しいのは36/166）で
   「smoothヒットは初回ヒットとは限らない」を確定。
9. **2集団構造の発見（有限観察）**: ヒットのt分布は2集団に分かれる。
   (a) t=1（4,904件・2^k rich・Ω≥10の119件すべて）、(b) t≥40（547件すべて
   「奇素数ちょうど3個×2^{1,2}」で奇素数はM/2近傍）。中間のt=2..39は
   2,632+1,967件で薄い。max t=220@M=983（N=2·449·487²・seam bound 979の
   22.5%）。K0956の「max t=10・M≤199」観察は遠域で破れ、tはMとともに
   増えるがseam boundの4.5倍下にとどまる。

## 機械結果の要約

- CENSUS-FULL: 2,609 hit（Ω=3が28件・最頻Ω=4が1,237件・最大Ω=15）。
- CENSUS-STRIP: 7,441 hit（t≤60帯・Ω=3が50件・最頻Ω=4が3,571件・最大Ω=16）。
- 検査: S3'違反0・dead 0・EXCLUSIVE重複0（全10,050 hit）・SEAM違反0・
  engine照合 hit 288/block 101 0失敗・YSQR（62/301素数がM³−1 smooth・hit 0）。
- crosscheck: pub29完全一致・t1 smooth 97=97・firsthit 109行同t・
  1,546初回ヒット再計算0不一致・n_smooth_first不足0。
- 構造: max t=220@M=983・N≤0.225(M−1)³・per-M hit数≈M/25
  （平均1.4/5.9/14.4/28.5）・複数ヒットクラス86+366。
- 監査は決定的（2回cold実行でbyte同一）。output sha256:
  audit.json df61d25f…・hits_full.json 4d2243ea…・hits_strip.json 80d176b7…。

## 次課題

- smooth 2集団の機構: なぜt=1（2^k rich）とt≥40（奇素数3個×2^{1,2}・M/2近傍）
  に集中するか。t≥40集団の「奇素数はM/2近傍」はN=MY−1の合同構造からの
  帰結か（N≈2pq²・q≈M/2の因数分解がY素数と両立する頻度）。
- 1000<M≤2000のt>60帯の完全化（sieve-walkの窓延長・予想hit数は帯内7,441に
  対して小さいが定量したい）。
- Ω≥4のsmooth阻止候補371,799件の窓約数構造（どのp類が阻止するか）の統計。
- F型（branch型最悪クラス）との接続: K0959のFLAT-ARTIFACTと合わせ、
  t_cap予測子の設計にsmooth側の寄与上限N≤0.225(M−1)³を使う。
- 11×11レーンへの接続: EXCLUSIVE/S3'は σ_Z 判定の高速枝刈り
  （Ω≤3なら因数分解だけで確定）として使えるか別レーンで評価。
