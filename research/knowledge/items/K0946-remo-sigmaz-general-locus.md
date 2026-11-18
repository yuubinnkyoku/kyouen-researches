---
id: K0946
kind: proposition
status: proved
title: σ_Z(M,·) 値1軌跡の一般構造（RUN-UNIV・ONE-CHAR-GENERAL・EXCL-1/2・M1-EMPTY・DEG）と素数M法則（PRIME-M・PARITY・EXCL-1はK0948/K0949で全称証明）
relations:
  - depends_on: [K0941, K0945]
  - connects: [K0937, K0943, K0948, K0949]
artifacts:
  - research/experiments/remo-sigmaz-general-locus-20261118/report.md
  - research/experiments/remo-sigmaz-general-locus-20261118/sigma_locus_core.js
  - research/experiments/remo-sigmaz-general-locus-20261118/audit_build.py
  - research/experiments/remo-sigmaz-general-locus-20261118/sievegen_core.py
  - research/experiments/remo-sigmaz-general-locus-20261118/composite_core.py
  - research/experiments/remo-sigmaz-general-locus-20261118/output/sigma_locus_audit.json
date: 2026-11-18
tags: [remo, uniform-board, josephus, closed-form, prime, machine-evidence]
---

## 主張（K0945 ONE-CHAR/RUN-3/A2-NEVERの全M一般化。定理群は紙上全称証明）

K0941定理C/Dのσ再帰（σ_E(P;α,β)・σ_Z(M,K)・pinned composite_core.py）の上で、
**σ_Z(M,K)=1 (K>M) の値1軌跡の構造を全Mに一般化**する。

### 補題RUN-UNIV（runとtailの分離・全M・全称）− RUN-3の一般化

K>MのときZ(M,K)のE入口はE(M; K−M−1, M)。α₀=K−M−1・
s=⌊α₀/(M+1)⌋・κ=α₀ mod (M+1)=K mod (M+1)とおくと、E入口の接頭辞は
**sフェーズのrun**（各フェーズq=0・r=M<α・α←α−(M+1)・β←β+M・pot M不変・
fold寄与c=M+1定数）で、run中のkの最小値はk_t+1 ≥ M+2 > Mのため
割り算レジームに入らず打ち切り不能、tailは**E(M; κ, M(s+1))**
（k_t=κ+M(s+1)）。α₀=0（K=M+1）はs=0・κ=0でtail=E(M;0,M)。

### 定理ONE-CHAR-GENERAL（値1位置の特徴付け・全称iff）− ONE-CHARの一般化

**M ≥ 2, K > M に対し σ_Z(M,K) = 1 ⟺ σ_E(M; κ, M(s+1)) = κ+1**、
κ = K mod (M+1)・s = ⌊(K−M−1)/(M+1)⌋。

証明は後方チェーン引数（NO-WRAP-RECOVERY）: runレベル[k_t+1, K−1]とZレベルKは
全fold寄与c=M+1で、前向きfold σ_ℓ=(σ_{ℓ−1}+c) mod ℓ の後方分解は
σ_{k_t}=σ_{K−1}−cs+Σ_{j∈W} j（W=wrapレベル集合）。σ_{k_t} ≤ k_t−1が常に
成り立つので、値1の場合（σ_{K−1}=K−M、σ_{K−1}−cs=κ+1）にW≠∅なら
σ_{k_t} ≥ κ+1+k_t+1 > k_t−1で矛盾、ゆえ**値1はwrapを持たない**（W=∅）で
σ_tail=κ+1。逆はsilent chain v_ℓ=κ+1+(M+1)(ℓ−k_t)がwrapしない
（v_ℓ−ℓがℓで増加しℓ=K−1で ≤ 0）ことからレベルKで値1。∎

### 系EXCL-2（κ=M−1除外・全称）− A2-NEVERの一般化

**K ≡ M−1 (mod M+1), K>M なら σ_Z(M,K) ≠ 1**。tail E(M;M−1,M(s+1))の
第1フェーズはbumpでσ_tail=(M+1+I) mod k_t（I∈[0,k_t−2]）だが、=Mには
I ≡ −1 (mod k_t)が必要でI=k_t−1しかなく範囲外。∎

### 系EXCL-1（κ=M除外・全称）とU0-NEVER（K0948で全称証明）

**K ≡ M (mod M+1), K>M なら σ_Z(M,K) ≠ 1**（t=s+2）。tail
E(M;M,M(s+1))の第1フェーズbumpでσ_tail=M+1 ⟺ 継続位置I=0、bump後状態は
均一game E(M+1; M(s+2)−1, 0)。U0-NEVER（σ_E(M+1;Mt−1,0)≠0 ∀t≥2）は
**K0948定理U0-CLASSIFYの系として全称証明**（n+1=Mt合成の即時帰結。
本項出版時点ではJS naive 1,769状態・pinned core 315状態の機械検証だった）。
参考: σ_E(P;n,0)=0の解は存在する（P≤24・n≤300で100解）。K0948系ZERO-SETに
より零点集合は{n≥1: n+1素数∧spf(P)≥n+1}={p−1: p素数≤spf(P)}と完全決定され、
n ≡ −1 (mod P−1) を満たす零は(P,n)=(2,1),(3,1)のn=1のみでn≥2では0件
（出版観察と整合）。

### 系M1-EMPTY（全称）・補題DEG（退化閉形式・全称）

- **σ_Z(1,K) ≠ 1 ∀K≥2**（値1はσ_{K−1}=K−1を要求するが σ_{K−1}≤K−2）。
- **σ_Z(M,2)=1 ⟺ M偶数**・**σ_Z(M,3)=1 ⟺ M ≡ 2 (mod 3)**・
  **σ_Z(M,M−1) ≠ 1 (M≥3)**（いずれも閉形式の直接計算・紙上証明）。

## 軌跡法則（PRIME-M・PARITYはK0949で全称証明・残りは有限観察）

- **PRIME-M（K0949で全称証明・定理昇格）**: 非退化軌跡 {K>M : σ_Z(M,K)=1}
  非空 ⟹ M素数。機構はK0949 RELAY-REDUCE+P′-SIMPLIFY（合成Mは
  spf(P′)≤spf(M)<k_Tで自動失敗）。本項出版時の機械証拠:
  M≤40完全支持（K≤10⁵: 素数{2,3,5,7,11,13,17,19,23,29,31,37}全て非空・
  合成数とM=1全て空。深部: M∈{2,3,5,7} K≤10⁶非空・M=8,9 K≤4×10⁵・
  M=15,25 K≤3×10⁵ 空）。前段階の「M+1素数⟹空」観察は一般化不能と確定
  （M=8,9,14,15はM+1合成でも空。分類変数はM自身の素性）。
- **PARITY（K0949で全称証明・定理昇格）**: 素数M≥3の非退化ヒットは全て偶数
  （M=2の奇数ヒットはK=3のみ）。機構はκ奇⟹Y偶⟹spf(Y)=2<M（K0949）。
  本項出版時の機械証拠: M≤40全素数（K≤10⁵）・M∈{3,5,7}（K≤10⁶）で違反0。
  M奇素数では偶数K ⟺ 偶数κで、EXCL-2と合わせて許容κは偶数のみになる。
- **divisibility lawの再評価（有限観察のまま）**: (M+1)|KはM∈{2,3,5}のみ
  （K≤10⁶違反0）。
  素数M≥7では偽（最初の非整除ヒット: M=7→K=10, 11→16, 13→16, 17→22,
  19→22, 23→28, 29→36, 31→36, 37→40）。
- 残差スペクトラム（κ別ヒット分布・M≤40 K≤10⁵・fast engine）を report.md に
  掲載。全ヒットがcase (i) silent（σ_tail=κ+1・cascade 0）であることを
  M∈{2,3,5,7,11,13,17,19,23}・K≤20000で確認（ONE-CHAR-GENERALの直接検証）。

## 応用（K0941 THM-B死後状態Z(w+1, n−t)への必要条件）

- **証明済み（全称）**: n−t > w+1 なら n−t ≢ w, w+1 (mod w+2)
  （EXCL-2: κ=w・EXCL-1+U0-NEVER: κ=w+1・後者はK0948で全称証明）。
- **証明済み（K0949定理PRIME-M経由・全称）**: w+1合成なら
  σ_Z(w+1, n−t) ≠ 1、すなわち死後frame位置1は合成NのV値に現れない。
- n−t ≤ w+1 は退化レジームでDEG補題族が適用される。

## 機械的証拠（audit_build.py・output/sigma_locus_audit.json・all_ok=true）

sievegen_core.py（sha256 a69f916c…）・composite_core.py（sha256 3990d67f…）
はK0937/K0941 committed版とbyte同一のpinnedコピー（監査が実行時に照合）。
audit_build.pyはcold 2回実行でbyte同一（監査sha256
edfe71c3574b06af3424ebf6327bac6283d715b14f6ff4ce002ba0d01aefa5e9・
86,040 bytes・node audit stdoutも2回実行byte同一・26秒/実行）:

- **cross（JS内3実装相互・0失敗）**: fast vs naive E-grid 87,516状態・
  Z-grid 14,388状態・literal engine（K0928 END-INVフェーズ規則の明示盤面
  第3実装）vs naive 472+4,437状態・ランダム大状態500。
- **pinned cross-language（0失敗）**: pinned Python σ_Z vs JS naiveポート
  M≤12・K≤1200全要素一致（14,388）・σ_E一致（7,722）・
  hits_small: M=1..40・K≤1200のヒット集合がpinnedと完全一致（40/40）。
- **classify（ONE-CHAR-GENERAL silent検証・0例外）**: M∈{2,3,5,7,11,13,17,19,23}
  の全ヒットでσ_tail=κ+1・cascade 0・run恒等式違反0（監査 K≤6000・
  セッション追加 K≤20000）。
- **excl1**: U0-NEVER帰着形 0違反（JS 1,769・pinned 315状態）。
- **sweep**: M=1..40・K≤10⁴の残差スペクトラムをJSON同梱。

## K0945との分工

run-bump Segmentation・no-wrap batched後方パス（FAST算法）はK0945の
出版済み算法と同一物の独立実装であり、本項は算法を再主張しない
（fastE/fastZはsweepsと相互照合専用）。本項の新規性は一般化定理群
（RUN-UNIV・ONE-CHAR-GENERAL・EXCL-2・EXCL-1帰着・M1-EMPTY・DEG）と
M横断の軌跡法則（PRIME-M・PARITY・スペクトラム）にある。

## 範囲と限界

- 一様盤・K0928定理RED経由の設定のみ。**11×11空盤・二石root
  {49,60}/{59,60}・S2 {59,60}・class1/2/4には一切言及しない（UNKNOWN不変）**。
- U0-NEVER・PRIME-M・PARITYはK0948/K0949で全称証明された（本項出版時点では
  予想）。本項自体の機械検証範囲（M≤40主にK≤10⁵・
  深部は個別記録）を超える全称主張はそれらの項目に依拠する。fast engineとpinned coreの
  直接照合はK≤1200（全M）・K≤6000（M∈{2,3,5,7}）・K≤20000（素数
  M∈{2,…,23}のclassify）で行った。
- `uv run check/build`・unittestは本環境にcloneとuvがないため未実施
  （K0937/K0939/K0941/K0943/K0945と同じ扱い）。generated/とroot READMEは
  未編集。

## 次課題

1. U0-NEVER（σ_E(M+1; Mt−1, 0) ≠ 0）の全称証明 → **完了（K0948・EXCL-1昇格）**。
2. PRIME-Mの機構 → **完了（K0949）**: 「連分数様再帰」は追跡固定点性+1段
   リレー（RELAY-REDUCE）に崩壊し、M合成の障害物はspf(P′)≤spf(M)<k_Tの
   自動失敗と確定。
3. PARITY法則の証明 → **完了（K0949）**: κ奇⟹Y偶⟹spf(Y)=2<Mで
   SIMPLE-CHARのspf節不成立。
4. 一般Mの U_M={u : σ_E(M; 0, M(u+1))=1} の冪減衰構造の比較
   （K0945 U（M=3, 3,658要素）の一般化）— 未解決。
5. K0949系SIMPLE-CHAR（値1判定の純算術化）の先の、各Mの値1位置の分布則・
   密度の閉形式 — 未解決。
