# K0960: DEEP-CAP定理（smoothヒットのt < M/4）とCENSUS-STRIP2完全化 — 2026-11-18

高速レーン（remo系・σ_Z算術構造）。K0958の残課題「1000<M≤2000・t>60帯のsmoothヒット未列挙」と
構造OPEN「t≥40集団の機構」に対し、(1) 紙上全称証明3件（ODDCAP・MIN3・DEEP-CAP・系PAIR-MIN・系K3-A）、
(2) 完全センサスCENSUS-STRIP2（135素数・全t・8,277件）、(3) 全称主張の全数機械検証（5,982 deep hit・6述語0違反）
を1回の実行で確定した。記法はK0956/K0958と同一（M素数・main regime K=(M+1)t+κ・0≤κ≤M−2・
(t,κ)≠(1,0)・Y=K+1・k₀=Mt+κ−1・N=MY−1・窓=[M,k₀]・Ω重複込み）。

## 1. 命題（全称・紙上証明）

対象: 素数M≥5・main regime・t≥2・N=MY−1が(M−1)-smooth・窓空（⟺σ_Z=1、HIT-ARITH。
[Y ok]はsmoothヒットではYSQRにより自動、K0958）。

- **LEMMA ODDCAP**: a=v₂(N)≥1（K0949 PARITY: K偶⇒Y奇⇒N偶）とすると、
  Nの各奇素因数p（重複込みで各コピー）は p ≤ (M−1)/2^a を満たす。
  （2^i p (i=0..a) は約数。i₀=「2^i p ≥ M の最小i」が存在すると
  2^{i₀}p ≥ M ⇒ 2^{i₀}p > k₀、一方 2^{i₀−1}p ≤ M−1 ⇒ 2^{i₀}p ≤ 2M−2 ≤ k₀（t≥2）
  で窓内約数が生じ矛盾。ゆえ全i≤aで2^i p ≤ M−1。smooth性からp<Mでi₀≥1が保証される。）
- **LEMMA MIN3**: Ω(odd part of N) ≥ 3。Ω(odd)≤2ならodd部分≤maxodd²≤((M−1)/2^a)²で
  N ≤ (M−1)²/2^a ≤ (M−1)²/2 < 2M²+3M−1 ≤ N（t≥2でY≥2M+3）で矛盾。
- **THEOREM DEEP-CAP**: 奇素因数（重複込み昇順）p₁≤…≤p_k、top pair = p_{k−1}p_k として
  t < max(√M, ((M−1)²+4)/(4M))。特に素数M≥17では t < M/4。
  - **Case A（top pair ≥ M）**: top pairは約数で窓を跨げないので > k₀。
    ODDCAPより top pair ≤ maxodd² ≤ ((M−1)/2^a)² ≤ (M−1)²/4 ゆえ
    t < (((M−1)/2)²+1)/M < M/4（M≥3）。
  - **Case B（top pair < M）**: p_{k−1} < √M。奇部分N_odd ≥ M（N_odd < Mなら
    2^i N_odd (i≤a) が [M, 2M−2] ⊆ 窓に落ちる）。上方部分積 d_j = p_k···p_{k−j+1} の
    M初超え d_{j*}（j*≥3・d_2=top pair<M）は約数で > k₀、しかし
    d_{j*} = d_{j*−1}·p < M·p_{k−1} < M√M ゆえ t < √M。
- **COROLLARY PAIR-MIN（DEEP-CAP case Aの強化）**: 全ての組i<jについてpᵢpⱼは約数なので、
  pᵢpⱼ ≥ M なら pᵢpⱼ > k₀。よって **k₀ < min{pᵢpⱼ ≥ M}**
  （top pairだけでなく、M以上の最小ペア積がk₀の真上界）。t < (min{pᵢpⱼ ≥ M}+1)/M。
- **COROLLARY K3-A**: kodd=3のsmoothヒットは全てcase A。
  （case Bだと N = 2^a·p₁·(top pair) ≤ (M−1)² < 2M²+3M−1 ≤ N で矛盾。）

**SEAM比較（K0956のsmooth側4倍改良）**: smoothヒット（t≥2）は t < M/4 (M≥17)。
K0956 SEAM t ≤ (M−1)(M−2)/(M+1) ≈ M は M≥5 で DEEP-CAP が常に厳密に強い
（3M²−13M+8 > 0）。M=1789の実測最大t=427は境界M/4=447.25の95.5%。

## 2. CENSUS-STRIP2（決定的有限完全列挙）

- 範囲: 素数 1000 < M ≤ 2000（135素数）・全t。ymax=(M−1)³/M。K0958 CENSUS-STRIPの
  t≤60制限を除去し、同repo内のsmoothヒットセンサスをM≤2000全域で完成させる。
- 手法: `census_full2000.py`（census_walk2 = smooth_core.census_walkと同じ候補集合・
  同じsieve-walk・同じ計数。最適化は素数Y列挙のみ。M=1009, 1783, 1999で
  stats・smooth辞書・hit行が完全一致、M=1783はauditでlive再検証）+ K0958と同じ
  classify（窓DFS・branch_divisor）。完全性論証はK0958 report Sec.5と同一
  （SPLIT+EXCLUSIVE ⇒ ヒットN ≤ (M−1)³、t=1は直接N ≤ M(M+4)−1 < (M−1)³）。
- 総計: 候補22,653,112・(M−1)-smooth候補1,924,193・窓阻止1,915,916・
  **smoothヒット8,277件**（t=1: 3,433 / t∈[2,9]: 2,011 / [10,39]: 1,572 /
  [40,60]: 425 / t>60: 836）。dead候補0・S3'違反0・branch∧smooth重複0（EXCLUSIVE）・
  SEAM違反0・max t=427@M=1789・max N=1,413,991,882@M=1973（(M−1)³の0.1844）。
- **K0958出版との行完全一致**: t≤60帯7,441行は出版hits_strip.jsonとキー集合・全field
  完全一致（mismatch 0）。publish上の完全リストは出版hits_strip.json ∪ hits_deep_band.json
  （hits_strip2.jsonが単一ファイル版・行は[M,κ,t,Ω,ω,branch]でK,Y,Nは
  K=(M+1)t+κ・Y=K+1・N=MY−1で復元）。
- 決定性: census冷再実行（checkpoint破棄・133秒）で135チェックポイント全てbyte同一。
  audit全体（engine錨含む）の冷二重実行で出力3ファイルbyte同一（sha256は下記）。

## 3. 機械検証（audit_build.py・全て0違反）

- **DEEP-CAP群の全数検証**: deep hit（t≥2）5,982件 = strip2 4,844件 + K0958出版
  hits_full（M≤1000）1,138件。各件でNを独立再因数分解し、
  6述語 ok_oddcap・ok_min3・ok_case（A: k₀<top pair / B: t²<M）・
  ok_deepcap（M<17 ∨ t<M/4 ∧ ok_case）・ok_pairmin（全ペア積≥Mがk₀超え）・
  t_lt_M4 を検査。**違反0**。kodd=3 case B 0件（系K3-A機械確認）。
  v₂ヒスト: strip2 {1:4183, 2:597, 3:59, 4:5}・出版 {1:996, 2:131, 3:11}。
  koddヒスト: strip2 {3:4377, 4:464, 5:3}・出版 {3:1047, 4:88, 5:2, 6:1}。
- **engine錨**（composite_core.sigma_Z・K0948-K0950ピン）: t>60帯全836件 + t≤60帯
  149刻み54件 = 890件全てσ_Z=1（0失敗）。blockedサンプル: M∈{1423,1789,1999}の
  窓阻止smooth候補199刻み278件全てσ_Z≠1（0失敗）。
- **YSQR新帯**: M³−1が(M−1)-smoothなのは31/135素数・その0個がsquare-state hit
  （K0958 YSQRのM≤2000全素数への機械拡張）。
- **同値性**: M=1009, 1783, 1999で census_walk2 と smooth_core.census_walk
  （オリジナル）のstats・smooth辞書・行数完全一致（1783はaudit live、他2件は
  session検証・出力JSONのrows_equal/stats_equal/smooth_equalで表現）。

## 4. 構造観察（有限・全称主張なし）

- **2集団構造の確定拡張**: t=1集団3,433件（Ω最大16・Ω≥10は87件すべてt=1・2^k rich）
  と t≥40集団。**t>60帯836件は全件kodd=3・v₂∈{1,2}（833+3）**で、
  K0958の「t≥40集団547件」観察（M≤2000・t≤60の範囲）を全t・全帯域で確定。
  3つの奇素数はすべて大きい: deep bandのp₁最小値は149で、
  p₁,p₂,p₃すべてがほぼ(M−1)/2^a近傍に集中する。
- **ODDCAP飽和**: deep bandで2件が maxodd = (M−1)/2^a ちょうど
  （M=1187, t=65, N=92914798=2·157·499·593・M=1283, t=245, N=404623558=2·547·577·641。
  ODDCAPの上限が到達可能なことを実証）。
- **PAIR-MIN近接**: deep bandの t·M/min{ペア積≥M} は中央値0.8835・最大0.9973
  （M=1997, t=121, κ=180, N=2·337·719·997: k₀=241,816に対しpairmin=337·719=242,303・
  差487）。deep集団はPAIR-MIN上限に張り付く。系として「3つの奇素数がすべて
  M/2近傍でなければpairminが下がりtが押し下げられる」ことがk₀<p₁p₂・k₀<p₁p₃
  （PAIR-MIN）から直接読める。これがt≥40集団の機構の算術的説明の本体である。
- **top-by-t**: 1位 M=1789, t=427, N=2·881³（k₀=764,018 < 881²=776,161・t/M=0.2387）。
  以下 M=1777 t=392・M=1973 t=363・M=1993 t=346・M=1871 t=343・M=1811 t=340…
  （全件kodd=3・v₂=1・拡張fieldはhits_deep_band.json）。
- **case Bの稀性**: t≥2全5,982件中case Bは3件のみ
  （M=757, t=2, N=2·7⁵·47・M=773, t=2, N=2·13⁴·29・M=1097, t=3, N=2·13·19³·23）。
  いずれもkodd≥5・小素数の冪構造・t≤3で、t>60帯には1件もない。
  「case Bは本質的にt小」への全称昇格はしない（定理はt<√Mが精一杯）。
- **多重ヒット**: 484クラスが複数smoothヒット（計520余剰）をもち、smooth初回ヒット
  がクラス初回ヒットとは限らない観察（K0958）を全t帯で更新。
- per-M統計（候補数・smooth数・hit数・Ωヒスト・seam bound・max_t）はaudit.json
  per_M（135エントリ）。

## 5. 範囲・限界・次課題

- ODDCAP・MIN3・DEEP-CAP・PAIR-MIN・K3-Aは（M−1)-smoothかつ窓空（main regime・
  素数M≥5・t≥2）の全称定理。branch型ヒット・F(M)には適用されない
  （初回ヒットの93.8%はbranch型・K0956のまま）。機械検証はM≤2000のdeep hit
  5,982件（+出版M≤1000）への全数アンカーであり、証明の代替ではない。
- M>2000の延伸はsieve-walkのO(M²候補・ymax∝M²)で素直に可能（135秒/135素数の
  約2.5倍/帯）。
- OPEN（次課題）: (i) t≥40集団が「kodd=3・全素数M/2近傍」ちょうどになる条件の
  定量化（PAIR-MIN近接分布の理論）・(ii) EV増幅（K0959）の定量モデル化・
  (iii) K0959 F_t/ln²M bucket medianのM>2000延伸（F計算重い）。
- 11×11空盤・二石root・標準有限盤には言及しない。uv check/buildは本環境に
  cloneとuvがなく未実施（歴代remo項目と同じ扱い）。generated/とroot READMEは未編集。

## 6. ピン（sha256・先頭8桁）

- 依存core（K0956/K0958ピンと一致）: prehit_core bf8ed817…・composite_core 3990d67f…・
  sievegen_core a69f916c…・branch_density_core 34b4ff15…・hitpair_core 0237aa1b…・
  smooth_core 928c54ca…
- K0958出版出力: audit.json df61d25f…・hits_full.json 4d2243ea…・hits_strip.json 80d176b7…
- 本実験: census_full2000.py af8471a8…・audit_build.py a2c42c99…・
  output/audit.json 4cd64fe4…・output/hits_strip2.json 784ca43c…・
  output/hits_deep_band.json 1cc020b2…
