---
id: K0945
kind: proposition
status: proved
title: σ_Z(3,K)のfold分解（RUN-3・FOLD）・値1位置の全称特徴付け（ONE-CHAR）・K≡2 (mod 4) 非存在（A2-NEVER）・run-bump高速算（FAST）
relations:
  - depends_on: [K0941, K0937]
  - connects: [K0943, K0928, K0939]
artifacts:
  - research/experiments/remo-sigmaz3-fold-20261118/report.md
  - research/experiments/remo-sigmaz3-fold-20261118/sievegen_core.py
  - research/experiments/remo-sigmaz3-fold-20261118/composite_core.py
  - research/experiments/remo-sigmaz3-fold-20261118/sigmaz3_core.py
  - research/experiments/remo-sigmaz3-fold-20261118/sigmaz3_verify.py
  - research/experiments/remo-sigmaz3-fold-20261118/deep_census.py
  - research/experiments/remo-sigmaz3-fold-20261118/audit_build.py
  - research/experiments/remo-sigmaz3-fold-20261118/output/sigmaz3_audit.json
  - research/experiments/remo-sigmaz3-fold-20261118/output/deep_census.json
date: 2026-11-18
tags: [remo, uniform-board, counting-recursion, josephus, fold, closed-form, machine-evidence]
---

## 主張（K0941/K0943の残課題「σ_Z(3,K)値1位置の構造」を閉じる。全定理が紙上全称証明）

K0941定理C・定理Dのσ再帰（σ_E(P;α,β)・σ_Z(M,K)・pinned composite_core.py）
の上に、σ_Z(3,K)（K=4u+a・u=⌊K/4⌋・a=K mod 4・K≥4）の完全なfold分解を確立する。

### 補題RUN-3（pot-3 runとtailの分離・全称）

σ_Z(3,K)のEゲーム入口E(3;K−4,3)（k₁=K−1人）のフェーズ列の接頭辞は
「run」s=⌊(K−4)/4⌋=u−1フェーズ: 各runフェーズはq=0・r=3<α
（k>3は常に成立）でα←α−4・β←β+3・k←k−1・pot 3不変・
fold寄与c=r+1=4定数。run終了時の状態（tail）は**E(3;a,3u)**（k=3u+a）。
foldレベルは[K−s,K]=[3u+a+1,4u+a]で各レベルc=4。

### 定理FOLD（三分法と明示式Φ_K・全称）

D=σ_tail+4u（巻き戻し無し値）とおくと σ_Z(3,K)=Φ_K(σ_tail) は三分法で
完全に決まる:

- **D≤K−1**: どのレベルでもbiteせず σ_Z(3,K)=D。
- **K≤D≤K+2**: レベルKでちょうど1回biteし σ_Z(3,K)=D−K。
- **D≥K+3**: 最初のbiteはレベルL₀=⌈(4K−D)/3⌉（<K）で値v₀=D+3L₀−4K∈[0,2]。
  以降、値vのレベルLから次のbiteはレベルm=⌈(4L−v)/3⌉・値
  v←v+4(m−1−L)+4−m∈[0,2]とO(log K)回のカスケードが続き
  （レベル比≈4/3）、最終的に σ_Z(3,K)=v+4(K−L)。

bite条件は静寂鎖v_ℓ=D+4(ℓ−K)に対するD+3ℓ≥4K、bite後の静寂鎖
v_ℓ=v+4(ℓ−L)に対する3m≥4L−vそのもの。

### 定理ONE-CHAR（値1位置の特徴付け・全称iff）

**すべてのK≥4に対し σ_Z(3,K)=1 ⟺ σ_E(3;K mod 4, 3⌊K/4⌋)=K mod 4+1。**

証明: 最終レベルKのfold v_K=1 ⟺ v_{K−1}=K−3。K≥6ではv_{K−1}>2より
レベルK−1はbiteしておらず、(i)全面静寂 D=K+1 ⟺ σ_tail=a+1、
(ii)最後のbiteがレベルℓ_m≤K−2: 4ℓ_m=3K−1+v_mが必要で
a=0: ℓ_m=3u / a=1: ℓ_m=3u+1 / a=2: 解なし / a=3: ℓ_m=3u+2だが、
foldレベルは3u+a+1以上なのでℓ_m∈{3u,3u+1,3u+2}はすべてレンジ未満で
不可能。ゆえに値1 ⟺ (i) ⟺ σ_tail=a+1。∎

K0941の値1位置観察（4,8,12,28,40,52,72,…・K≤4,000で91個）は
**{4u : σ_E(3;0,3u)=1}** に正確に特徴付けられる（監査で91↔91双方向一致・
K≤10⁵では1,146個すべてK≡0 mod 4）。

### 定理A2-NEVER（K≡2 (mod 4)は全称的に値1を取らない）

**K=4u+2≥6に対しσ_Z(3,K)≠1**（K=2は値0）。証明: ONE-CHARより
σ_tail=3を示せばよい。tail E(3;2,3u)はk=3u+2>3なので第1フェーズは
q=0・r=3≥α=2のbump: σ_tail=(4+I) mod (3u+2)・I∈[0,3u]。
σ_tail=3には4+I∈{3,3u+5}が必要だが前者<4・後者>3u+4でともに不可能。∎

K0941の「値1位置はK偶数」備考は「K≡0 (mod 4)」に強化される
（a=2は全称証明・a∈{1,3}はu≤50,000で反例ゼロの経験的事実）。

### FAST算法（run-bumpセグメント化・一般E-game）

pot P<kのE-gameはα≥P+1のrun（t=⌊α/(P+1)⌋フェーズ一括・fold寄与c=P+1
定数でレベル区間一括処理・runあたりbite数O(1)）とα≤Pのbump（1フェーズで
pot←P+1）とP≥kのendgame（個別処理）にセグメント化でき、
**σ_Z(3,K)全体がO(√K)時間・O(1)追加メモリ**（tail O(√K)+fold O(log K)・
セグメント数O(√k)は経験的観察で計算量定理ではない）。

## 機械的証拠（sigmaz3_verify.py・audit_build.py・deep_census.py）

sievegen_core.py（sha256 a69f916c…）・composite_core.py
（sha256 3990d67f…）はK0937/K0941 committed版とbyte同一のpinnedコピー。
sigmaz3_verify.pyのrun_checks（約10.6秒/回・全純算術）全合格:

- **PIN**: 両coreのsha256照合。
- **FASTEQ**: tail族（u≤800×a∈0..3）・一般E状態（P∈2..10・k≤150・全α・
  103,257状態）・σ_Z fast（M∈{2,3,5,9}・K≤100）・σ_Z3対pinned K≤1,500の
  4種が高速実装とpinnedで0不一致。
- **FOLD**: K≤4,000・3,997ゲーム: pinned σ_Z(3,K)==fold4(K, pinned tail)・0不一致。
- **ONECHAR**: 同ループで (σ_Z==1) ⟺ (tail==a+1) 双方向0不一致
  （値1は91↔91・K0941観察数と一致）。
- **A2NEVER**: K≡2 (mod 4)の値1出現0。
- **CENSUS**: u≤10,000のtail表からK≤40,000のfold4値1集合==ONE-CHAR予言集合
  （540↔540・mod4内訳{0:540,1:0,2:0,3:0}）・a∈{1,2,3}のtail==a+1出現0・
  a=0のtail∈{0,2}出現0。

audit_build.py: run_checksをin-process 1回+sigmaz3_verify.py
（内部2回実行の決定性検証つき）をcold 2回実行しstdout byte同一を確認して
output/sigmaz3_audit.jsonを書く（監査sha256
ae9d5b4bdc1c7d9109e5b26503ebbd73681a652f018b5866220793c456b98769・
cold payload sha256 0d51ea25…・all_ok=true）。

**深いセンサス（deep_census.py・2回実行byte-identical・sha256
3821c19b0828ebdcfc7bc0d830b317e23144106f506df4f1d72e6ee753c1bc1a・
U_all完全リスト3,658要素同梱）**:

- A: U={u≤10⁵ : σ_E(3;0,3u)=1}は**3,658要素**。密度バケット
  (1,1000]=90 (0.0901) / (32000,64000]=1118 (0.0349) / (64000,100000]=1137
  (0.0316) は冪的減衰（密度∝u^{−0.23}程度・ランダム1/(3u)桁より
  最低1桁以上構造的）。a=0のtail∈{0,2}はu≤10⁵で0回。
- B: a∈{1,2,3}のtail==a+1はu≤50,000で0回（a=2はA2-NEVERで全称・
  a=1,3は経験的事実）。
- C: u≤25,000表でK≤100,000: fold4値1集合==ONE-CHAR予言集合
  （1,146↔1,146・mod4{0:1146,1:0,2:0,3:0}）。

## 観察（全称主張しない）

- σ_E(3;0,3u)=1は真のアトラクタ（u≤3,000で205回・2番手の値6は15回）。
  Uの完全な特徴付け（閉形式・漸化式）は未解決。
- ONE-CHAR条件は第1フェーズbumpをほどくと a=0 ⟺ σ_E(4;3u−4,3)=3u−3・
  a=1 ⟺ σ_E(4;3u−2,2)=3u−1・a=3 ⟺ σ_Z(4,3u+2)=0 と書き直せ、
  同じfold構造がpot 4,5,…へ連分数様に再帰する。Uの冪減衰はこの深い再帰の
  反映と解釈できる（証明は今後課題）。

## 範囲と限界

- 一様盤・ゼロリセット・K0928定理RED経由の設定のみ。非一様盤・
  **11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/2/4には
  一切言及しない（UNKNOWN不変）**。
- Uの特徴付け・a∈{1,3}の反例不存在は主張しない（次課題）。
- FASTのO(√K)セグメント数は経験的観察で計算量定理ではない
  （bite回数の対数性を除く）。
- 紙上証明はK0941（定理C/D・σ再帰）・K0937（pinned core）の出版済み証明に
  依存し、機械アンカーはFASTEQ+FOLD+ONECHAR+A2NEVER+CENSUS+深いセンサス
  0不一致で裏付ける。
- `uv run check/build`・unittestは本環境にcloneとuvがないため未実施
  （K0937/K0939/K0941/K0943と同じ扱い）。generated/とroot READMEは未編集。
