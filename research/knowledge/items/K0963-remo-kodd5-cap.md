---
id: K0963
title: kodd=5 CAP定理（CK・CS・PAIR-INTERSECT・PC二分法・18設定分類・CAP-52/73/27）と予想(ii)の反証
kind: proposition
status: proved
topics: [residual-games, statistics, verification]
aliases: [COPRIME-KILL, COMPLEMENT-SMALL, PAIR-INTERSECT, K5-CAP, CAP-52, CAP-73, CAP-27]
relations:
  - type: depends_on
    target: K0961
    note: TWO-ZONE・EFFECTIVE-WINDOW・CO-FACTORを前提・PAIR-MIN系を分割補題CSへ一般化し、出版hits_full/hits_strip2を行入力に再利用
  - type: depends_on
    target: K0960
    note: 出版hits_strip2（1000<M≤2000全t・8,277行）を監査入力・掃引バリデーションアンカーに再利用
  - type: depends_on
    target: K0958
    note: 出版hits_full（M≤1000全t・2,609行）を監査入力に再利用
  - type: depends_on
    target: K0956
    note: 中核恒等式N=(M+1)k₀+2M−κとHIT-ARITHの[Y ok]クラス（素数Y∨Y=M²候補）を全称前提
  - type: depends_on
    target: K0949
    note: PARITY（[Y ok]でa=v₂(N)≥1・Y奇⟹κ偶⟹N偶）をcap証明とバンド完全性で使用
  - type: generalizes
    target: K0961
    note: K4-CAP→K5-CAP（kodd=4の3分岐からkodd=5の完全18設定分類へ）・K4交叉対二分法→PAIR-INTERSECT（r=5限定から一般rへ）
artifacts:
  - path: research/experiments/remo-kodd5-cap-20261118/report.md
    role: proof
    note: CK/CS/PAIR-INTERSECT/PC二分法・18設定表・CAP-52/73/27・K5-CAP・r≥6部分定理・掃引バンド完全性・予想(ii)反証の正本
  - path: research/experiments/remo-kodd5-cap-20261118/kodd5_core.py
    role: verifier
    note: 独立実装（依存コードなし）・regime/EW/CK/TZ/CS/PI・19キー設定表・cap_check・band_tmax・k6plus_case（sha256 35f5d50d…）
  - path: research/experiments/remo-kodd5-cap-20261118/kodd5_audit.py
    role: verifier
    note: Part 1出版10,886行監査・入力はrepo内出版兄弟dirのhits_full/hits_strip2を直接参照（sha256 6346fd06…・冷再実行byte同一）
  - path: research/experiments/remo-kodd5-cap-20261118/kodd5_sweep.py
    role: verifier
    note: Part 2掃引（チェックポイント付き・M∈(2000,10000]・バンド[4,T₅]完全列挙・sha256 1c99330c…）
  - path: research/experiments/remo-kodd5-cap-20261118/output/kodd5_audit.json
    role: data
    note: 0違反・koddヒスト出版完全一致・k5/k6設定分類（sha256 1eee533f…・冷再実行byte同一）
  - path: research/experiments/remo-kodd5-cap-20261118/output/kodd5_band_k5rows.json
    role: data
    note: kodd=5バンド406行・設定/cap/独立再検証フィールド付き（sha256 782736fd…）
  - path: research/experiments/remo-kodd5-cap-20261118/output/kodd5_band_summary.json
    role: data
    note: 掃引会計・kodd/tヒスト・min-M per t・バリデーション（sha256 aa4c9a87…）
  - path: research/log/2026-11-18-remo-kodd5-cap.md
    role: log
    note: 発見順・ルート表修正（sqrt3→cap27）の判断・機械結果の要約・次課題
date: 2026-11-18
scope: >-
  smoothヒット（素数M≥5・main regime K=(M+1)t+κ・0≤κ≤M−2・t≥2・[Y ok]クラス）のkodd=5構造。新補題CK・CS/PK・PAIR-INTERSECT、PC二分法、F=≥X̄ペア族の18設定完全分類、設定別cap（CAP-52/CAP-73/CAP-27）、掃引バンド[4,T₅(M)]の完全性、r≥6部分定理（PS/LG-PF）、予想(ii)（kodd≥5⟹t≤3）の反証。
evidence: >-
  18設定それぞれのcapは紙上全称証明（report.md T5-T8・恒等式とEW/TZ/CO-FACTORのみを使用）。機械は有限アンカー: 出版smoothヒット10,886行の独立再因数分解監査で全述語0違反、M∈(2000,10000]・926素数・26,574,669 prime-Y候補の掃引バンド完全列挙で133,726ヒット、1000<M≤2000の135素数で掃引バンドヒットが出版strip2センサス該当帯と完全一致（1,631行・不一致0）、kodd=5バンド406行の再検証0失敗、Y=M²候補は926素数すべて0件、CAP-73のt上界は全926素数でT₅以内（バンド完全性の閉包）。監査・掃引とも冷再実行byte同一（決定的）。
---

## 命題・範囲

記法はK0956/K0958/K0960/K0961と同一（M素数・main regime K=(M+1)t+κ・0≤κ≤M−2・
(t,κ)≠(1,0)・Y=K+1・k₀=Mt+κ−1・N=MY−1・窓=[M,k₀]・a=v₂(N)・σ=(M−1)/2^a・
X̄=(M+1)k₀/(M−1)・kodd=Ω(N/2^a)重複込み・中核恒等式 N=(M+1)k₀+2M−κ）。
対象はsmoothヒット（Nが(M−1)-smooth∧窓空・[Y ok]クラス・t≥2）。
a≥1は[Y ok]から回復する: Y奇（素数≥3∨Y=M²・M奇）⟹κ偶⟹N偶（パリティのみ・
K0958 S3'で[Y ok]はt≥2で自動）。

- **L1 X̄²>N（全称・t≥1）**: X̄²>N ⟺ (M+1)²k₀²>(M−1)²N。t≥2はk₀≥2M−1の展開、
  t=1・κ≥1はk₀≥Mで閉じる。
- **L2 CK（COPRIME-KILL・全称・t≥1・窓空不要）**: Nの互いに素な2約数が両方≥X̄なら
  de|N・de≥X̄²>Nで矛盾。素朴版: 指数非連続なsub-multiset積はN/2^aを割り切り、
  素性の互いに素性は不要（L3'で使用）。
- **L3 CS/PK（COMPLEMENT-SMALL・全称・t≥2・重複込み）**: N/2^aの素因数マルチセットの
  任意の分割S∪S^cで prod(S)≥X̄ なら 2^a·prod(S^c)≤M−1
  （prod(S^c)<X̄→EW→TZ。K0961 PAIR-MINの分割版・coprimality不使用で重複込みkoddで有効）。
- **L3' PAIR-INTERSECT（全称・t≥2）**: ≥X̄のペア積族Fはpairwise intersecting
  （index-disjointペア2組の積はN/2^aを割り切るsub-multiset積で≥X̄²>N/2^a）。
  K0961のK4交叉対二分法の一般r版。
- **L4 PC二分法（r=5・全称・t≥2）**: X̄>M−1（t≥2）より全約数は「≤σ（→TZ）」か
  「≥X̄」の二値。F外ペア≤σ・トリプルT≤σ ⟺ 相補ペアT^c∈F・シングルpᵢ≤σ
  （p₁≤√σ）・クアッドQᵢ≥X̄（CO-FACTOR）。
- **T5 Case A（F=∅）→ CAP-52**: 123≥X̄・123=(12)p₃≤σ√σ（12≤σ・p₃≤√σ）
  より X̄≤σ^{3/2}、すなわち **k₀²·2^{3a}(M+1)²≤(M−1)⁵**。
- **T6 Case B（45∈F）: 完全18設定分類**（report.mdの18行設定表）。
  ルートは[L]（恒等分解N=2^a·p₃·(pair)(pair)）・[U]（34,35≤σ→p₃≤σ/√X̄）の挟撃、
  [Q]（σ-トリプル×√σ素数のクアッド分解）、[27]（X̄·p₁p₂·p_c≤σ²・p₁p₂p_c≥27）の4種。
  B1/B2-14/B2-24/B3-15/B3-25→**CAP-73**（2^{4a}(M+1)³k₀³<(M−1)⁷）。
  {45,34}/{45,35}→**CAP-27**（27·k₀·2^{2a}(M+1)≤(M−1)³・X̄p₁p₂²≤σ²ルート）。
  B4-1/B4-2/B5系/B6系→**CAP-52**（クアッド=σトリプル×√σ素数）。
  B4-3は分割: σ-トリプル134/135/234/235のいずれか≤σ→CAP-52、全て≥X̄
  （例外設定）→CAP-27（125/45/14ルート）。出版監査で例外設定の実在を確認
  （M=1759・バンド掃引で369行）。
  注記: {45,34}/{45,35}の以前の√3系cap（3X̄²<σ³）は導出不能と判明し削除した
  （出版データに同設定のt≥2行はなく、監査・掃引結果は不変）。
- **T7 K5-CAP（全称・kodd=5・t≥2）**: kodd=5のsmoothヒットは設定に応じて
  CAP-52・CAP-73・CAP-27のいずれかを満たす。特に k₀≤max(K₅₂(M),K₂₇(M))
  （a=1 worst）で、**バンド T₅(M)=max(t52,t27) の外にkodd=5ヒットは存在しない**
  （修復定理: kodd=5 ⟹ t≤T₅(M)≈M/108・CAP-27線形枝が支配）。
- **T8 r≥6部分定理（kodd≥6・t≥2）**: PS（全ペア<X̄）はプレフィックス法でCAP-52。
  LG（L=p_{r−1}p_r≥X̄）で先頭側にP_j≥X̄があればCAP-52（LG-PF）。
  全プレフィックス≤σの場合は**LG-OPEN（未解決・capなし）**。
  r=6では常にLG-OPENに落ちる可能性がある（kodd≥6全称化の最大障害）。

## 現在の根拠と限界

- 上記定理は紙上全称証明（report.md正本・K0961のEW/TZ/CO-FACTORのみを前提）。
  機械は有限アンカー: 出版smoothヒット10,886行（K0958 hits_full 2,609 +
  K0960 hits_strip2 8,277・M≤2000全t）を独立再因数分解で全数検査し
  **全述語0違反**（identity/parity/smooth/window/EW/CK/TZ/CS/PI/設定/cap）。
  koddヒストはK0961出版値と完全一致（t=1: {1:2,2:424,3:1902,4:1674,5:638,6:204,
  7:46,8:12,9:2}・t≥2: {3:5424,4:552,5:5,6:1}）。
- **kodd=5・t≥2の出版5行の初の設定分類**: M=773(A)・937(B1)・1097(A)・
  1759(**B4-3例外設定・CAP-27枝の初の実在例**)・1993(B6-max)。
  kodd=6の1行 M=757(t=2・PS・CAP-52成立)。
- **掃引Part 2（M∈(2000,10000]・決定的完全列挙）**: 926素数・候補Y=素数∨Y=M²のうち
  バンドt∈[4,T₅(M)]（T₅∈[18,92]）・26,574,669 prime-Y候補・5,038,337 smooth・
  **133,726ヒット**（kodd hist {3:110,060, 4:23,260, 5:406, ≥6:0}）。
  バンド完全性: (i) a≥1・capsのa単調性、(ii) t>T₅で全κがcap違反、
  (iii) CAP-73のt上界が全926素数でT₅以内・T₅<⌈√M⌉（数値確認）。
  バリデーション: 1000<M≤2000の135素数で掃引バンドヒットと出版strip2センサス
  該当帯が**完全一致（1,631行・不一致0）**。Y=M²候補は926素数すべて0件。
- **予想(ii)（kodd≥5⟹t≤3）の反証（K0961予想の後半を解決）**: 最初の反例
  **M=2467・κ=2456・t=5・N=36,504,198=2·3²·113·131·137**
  （113·131=14,803がX̄=14,800.3の0.02%上・EWの鋭さの実証・B4-3例外設定）。
  t=4最初はM=3761。**max t=19@M=8693**（N=2·3²·409·439·449）。
  min-M per t: {4:3761,5:2467,6:3389,7:4457,8:4259,9:4733,10:6491,11:5623,
  12:8059,13:7283,14:6569,15:6967,16:7459,17:7703,18:7043,19:8693}。
  反例の91%（369/406）がB4-3例外設定・全行p₁=3・341行がp₁p₂=9
  （CAP-27の定数27=p₁p₂²の飽和構造と整合）。
- kodd=5バンド406行の独立再検証（再因数分解・窓空・EW/CK/TZ/CS/PI・設定・cap・
  Y素数）は0失敗（a∈{1:404,2:2}・設定hist B4-3:369/A:18/B6-max:14/B6-2535:3/B1:2・
  ルートhist cap27:369/cap52:35/cap73:2）。
- **kodd≥6**: バンド内0行（t∈[4,92]）+ センサスM≤2000ではt≤2。
  予想(ii)のkodd≥6部分（t≤3）はM≤10⁴まで強い支持的証拠（LG-OPEN未解決のため
  証明なし）。
- **予想(i)（kodd=4⟹t<√M）はM≤2000のまま**: バンド[4,T₅]⊂[4,√M)（926素数で
  T₅<⌈√M⌉）なので掃引はconj(i)違反帯（t≥√M）に到達しておらず、M>2000では
  OPENのまま（K0961 cap γ枝 (M−2)/36と√Mの隙間・バンド内kodd=4は23,260行0違反・
  max t=91@M=9887<√M）。
- ヒューリスティック（有限観察）: 反例帯のtスケールは3(tM²/18)^{2/3}≥tMから
  t≲M/324（t=19@M=8693・M/324=26.8と整合）。定理上界T₅≈M/108は形式的にはるか上。
- OPEN: (i) LG-OPEN r≥6のcap不在。(ii) B4-3例外設定のt分布理論（M/324スケール・
  p₁=3強制の証明）。(iii) kodd=4・conj(i)のM>2000掃引（γ枝帯のDiophantine
  scarcity・K0961 OPEN(i)継続）。(iv) κ=0 γ行のM>2000出現（K0961 OPEN(ii)継続）。
  (v) Y=M²のM>10000構造。
- branch型ヒット・F(M)には不適用（初回ヒット93.8%はbranch型・K0956不変）。
  11×11空盤に言及しない。uv check/buildは本環境にcloneとuvがなく未実施
  （歴代remo項目と同じ扱い）。generated/とroot READMEは未編集。
