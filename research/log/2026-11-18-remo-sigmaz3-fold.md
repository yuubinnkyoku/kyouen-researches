# 2026-11-18 σ_Z(3,K)のfold分解・ONE-CHAR・A2-NEVER・FAST算法（K0945）

K0941/K0943の直接続き（K0943ログの次候補「σ_E/σ_Z閉形式探索・
σ_Z(3,K)値1位置の構造解析」を実行）。高速レーン。branchなし・main直接出版。
K0945として出版。

## 発見順

1. **着手判断**: 前回作業（closedtrack/P2OBS出版予定）は最新main確認で並走が
   K0943（STATE-CF/DS-CF/P2）として同一内容を出版済みと判明したため中止
   （数式同一: h=(T−w) mod w ≡ T mod w）。K0939 audit_build.py修復も並走が
   完了済み（fb1ab5bdc1bb）。K0941/K0943が明記した残課題
   「σ_Z(3,K)値1位置4,8,12,28,40,52,72,…の構造」が情報価値最上位。
2. **RUN-3**: E入口E(3;K−4,3)の第1フェーズ分岐はr=3<α ⟺ α≥4で、αが
   各フェーズちょうど4減るため接頭辞はs=u−1フェーズの定数fold（c=4）run。
   tailはE(3;a,3u)。foldレベル[K−s,K]=[3u+a+1,4u+a]が確定。
3. **FOLD**: 静寂鎖v_ℓ=D+4(ℓ−K)のbite条件D+3ℓ≥4Kから三分法
   （D≤K−1無bite / K≤D≤K+2レベルK単bite / D≥K+3は
   L₀=⌈(4K−D)/3⌉からbite値∈[0,2]・次レベル⌈(4L−v)/3⌉のO(log K)カスケード）。
   K≤4,000でpinned σ_Z(3,K)と0不一致。
4. **ONE-CHAR（全称iff）**: v_K=1 ⟺ v_{K−1}=K−3で、最終bite候補
   ℓ_m∈{3u,3u+1,3u+2}はfoldレンジ開始3u+a+1未満で全滅（a=2は解なし）。
   よって σ_Z(3,K)=1 ⟺ σ_tail=a+1 ⟺ σ_E(3;a,3u)=a+1。
   K0941観察91個は{4u : σ_E(3;0,3u)=1}に双方向一致。
5. **A2-NEVER（全称）**: tail E(3;2,3u)は第1フェーズbumpで
   σ_tail=(4+I) mod (3u+2)・I∈[0,3u]。σ_tail=3には4+I∈{3,3u+5}が必要で
   両方不可能。K≡2 (mod 4)は全称的に値1を取らない。
   K0941備考「K偶数」は「K≡0 (mod 4)」に強化。
6. **FAST**: E-gameのrun-bumpセグメント化+定数c fold一括（σ_E_fast）で
   σ_Z(3,K)がO(√K)時間（セグメント数は経験的O(√k)・u=10⁵のtailが1.1ms）。
   tail族・一般E状態103,257状態・σ_Z fast・σ_Z3対pinnedで0不一致。
7. **深いセンサス（deep_census.py・2回実行byte-identical）**:
   U={u≤10⁵ : σ_E(3;0,3u)=1}は3,658要素で冪減衰（∝u^{−0.23}程度）・
   a=0のtail∈{0,2}は10万まで0回・a∈{1,3}のtail==a+1は5万まで0回・
   K≤10⁵ fold値1==ONE-CHAR予言（1,146↔1,146・すべてK≡0 mod 4）。
   sha256 3821c19b0828ebdcfc7bc0d830b317e23144106f506df4f1d72e6ee753c1bc1a。
8. **検証器**: sigmaz3_verify.py（PIN/FASTEQ/FOLD/ONECHAR/A2NEVER/CENSUS・
   run_checksを2回実行し決定性assert）+ audit_build.py（in-process 1回+
   cold 2回byte同一→output/sigmaz3_audit.json・監査sha256
   ae9d5b4bdc1c7d9109e5b26503ebbd73681a652f018b5866220793c456b98769・
   約53秒・all_ok=true）。
9. **出版**: 単一コミットで実験dir 9ファイル・item・K0941/K0943 itemの
   昇格注記・README bullet（K0943 bullet直後）・本ログ。push前に最新mainを
   再取得しK0945が空きであることを確認。

## 次の候補

1. U={u : σ_E(3;0,3u)=1}の特徴付け: ONE-CHAR条件の連分数様再帰
   （a=0 ⟺ σ_E(4;3u−4,3)=3u−3 → σ_Z(4,3u−3)…）をpot 4以上へ展開し、
   値1の一般E-state版ONE-CHAR（σ_E(P;α,β)=xのfold特徴付け）を確立する。
2. σ_Z(M,K)の一般M（M=2,4,5,…）へのRUN-M/FOLD拡張（runのc=M+1・
   tail E(M;K−(M+1),M)の構造）。M=4は上記再帰の直接の母体。
3. r人対戦・d次元版への転写（一般化レーン）。

なお並走管轄の確認: K0944は並走two-token z6-y29が使用済み。K0945は
items一覧で空き（push直前に再確認）。
